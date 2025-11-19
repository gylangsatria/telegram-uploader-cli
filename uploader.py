import os
import time
import asyncio
from dotenv import load_dotenv
from tqdm import tqdm
import requests
from requests.adapters import HTTPAdapter, Retry
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from telethon import TelegramClient

# Load environment
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
group_target = int(os.getenv("GROUP_TARGET"))
upload_mode = os.getenv("UPLOAD_MODE", "telethon").lower()

# Init Telethon client
client = TelegramClient('bot', api_id=api_id, api_hash=api_hash)

async def start_client():
    await client.start(bot_token=bot_token)

# Session dengan retry untuk Bot API
session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# Baca daftar file yang sudah diupload dari log
def load_uploaded_files(log_path="upload.log"):
    uploaded = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as log:
            for line in log:
                path = line.split("|")[0].strip()
                uploaded.add(path)
    return uploaded

# Upload via Bot API dengan progress bar
def upload_bot_api(full_path):
    try:
        size_bytes = os.path.getsize(full_path)
        with open(full_path, 'rb') as f:
            encoder = MultipartEncoder(
                fields={'chat_id': str(group_target),
                        'document': (os.path.basename(full_path), f)}
            )
            with tqdm(total=size_bytes, unit='B', unit_scale=True, desc=os.path.basename(full_path)) as pbar:
                def callback(monitor):
                    pbar.update(monitor.bytes_read - pbar.n)

                monitor = MultipartEncoderMonitor(encoder, callback)
                response = session.post(
                    f"https://api.telegram.org/bot{bot_token}/sendDocument",
                    data=monitor,
                    headers={'Content-Type': monitor.content_type},
                    timeout=300
                )
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)

# Upload via Telethon dengan progress bar
async def upload_telethon(full_path, semaphore):
    async with semaphore:
        try:
            size_bytes = os.path.getsize(full_path)
            with tqdm(total=size_bytes, unit='B', unit_scale=True, desc=os.path.basename(full_path)) as pbar:
                def progress_callback(sent, total):
                    pbar.update(sent - pbar.n)

                await client.send_file(
                    group_target,
                    full_path,
                    part_size_kb=8192,   # 8 MB chunk untuk percepat file kecil
                    use_cache=False,
                    progress_callback=progress_callback
                )
            end = time.time()
            print(f"Uploaded: {os.path.basename(full_path)}")
            with open("upload.log", "a") as log:
                log.write(f"{full_path} | {size_bytes/1024/1024:.2f} MB | Telethon\n")
            return True
        except Exception as e:
            print(f"Failed: {os.path.basename(full_path)} — {e}")
            with open("error.log", "a") as err:
                err.write(f"{full_path} — {e}\n")
            return False

# Hybrid uploader dengan verifikasi, progress bar folder, dan paralel upload
async def upload_folder(folder_path, concurrency=10):
    print(f"Starting upload from: {folder_path} (mode={upload_mode})")
    
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in sorted(files):  # urutkan alfabet
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    uploaded_files = load_uploaded_files()
    semaphore = asyncio.Semaphore(concurrency)

    tasks = []
    for full_path in all_files:
        if full_path in uploaded_files:
            print(f"Skipped (already uploaded): {os.path.basename(full_path)}")
            continue

        size_bytes = os.path.getsize(full_path)
        size_mb = size_bytes / (1024 * 1024)

        if upload_mode == "hybrid" and size_mb <= 50:
            loop = asyncio.get_event_loop()
            tasks.append(loop.run_in_executor(None, upload_bot_api, full_path))
        else:
            tasks.append(upload_telethon(full_path, semaphore))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("Upload selesai, total:", len(results))

# Main runner
async def main():
    await start_client()
    await upload_folder("/media", concurrency=10)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

