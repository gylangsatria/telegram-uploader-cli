
# Telegram Hybrid Uploader

A smart uploader that sends files to a Telegram group using a hybrid approach: **Bot API** for small files (≤50MB) and **Telethon** for larger ones. Ideal for batch uploads, speed tracking, and detailed logging.

---

## Features

- **Hybrid logic**: Automatically selects the best upload method based on file size.
- **Interactive progress bar**: Uses `tqdm` for real-time feedback.
- **Detailed logging**:
  - `upload.log` for successful uploads.
  - `error.log` for failed attempts.
- **Speed stats**: Displays duration and estimated kbps per file.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-hybrid-uploader.git
cd telegram-hybrid-uploader
```

### 2. Create a `.env` file

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
GROUP_TARGET=your_group_id
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
telethon
python-dotenv
tqdm
requests
```

---

## Usage

Edit the folder path at the bottom of the script:

```python
upload_folder("/media")
```

Then run:

```bash
python uploader.py
```

Or if you use Docker, just simply run this docker container

```bash
docker compose up --build
```

---

## Log Format

### upload.log

```
/media/file1.pdf | 12.34 MB | 3.21s | 312.45 kbps | Bot API
```

### error.log

```
/media/file2.zip — [Errno 13] Permission denied
```

---

## Upload Logic

| File Size     | Upload Method | Library     |
|---------------|----------------|-------------|
| ≤ 50 MB       | Bot API        | `requests`  |
| > 50 MB       | Telethon       | `Telethon`  |

---

## Notes

- Make sure your bot is added to the target group and has permission to send files.
- Files larger than 2GB may fail depending on Telegram limits and your connection.
- Upload speed may vary based on file size, network stability, and Telegram server response.

---

## Next Steps

Want to extend this project with:

- ✅ Extension-based filtering
- ✅ Multi-group routing
- ✅ CDN fallback logic
- ✅ Upload queue and retry mechanism

Just open an issue or start a discussion!

---

## License

MIT License © 2025 Gylang
```

Let me know if you want this styled with badges, GitHub Actions, or modularized into multiple scripts. I can also help you refactor it into CLI mode or add argparse support.
