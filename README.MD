
# Telegram Uploader (Docker Ready)

A smart uploader that sends files to a Telegram group using either a hybrid approach (Bot API + Telethon) or Telethon only, depending on configuration. Perfect for batch uploads, speed tracking, and detailed logging.

With Docker, users only need to install Docker and Docker Compose—no manual Python setup required.

---

## Features

- **Configurable upload mode**:
  - **hybrid**: Bot API for small files (≤50 MB), Telethon for larger files.
  - **telethon**: All files sent via Telethon (more stable, chunked upload).

- **Interactive progress bar** with `tqdm`.

- **Detailed logging**:
  - `upload.log` for successful uploads.
  - `error.log` for failed attempts.

- **Speed stats**: duration and estimated kbps per file.

- **Concurrency limit**: upload multiple files in parallel with controlled limits.


---

## Setup

### 1. Install Docker & Docker Compose

```bash
docker --version
docker compose version
```

### 2. Clone the repository

```bash
git clone https://github.com/your-username/telegram-hybrid-uploader.git
cd telegram-hybrid-uploader
```
### 3. Configure docker-compose.yml

Example configuration with volume mapping

```yaml
version: '3.8'
services:
  telegram-uploader:
    build: .
    image: telegram_uploader:latest
    container_name: telegram-uploader
    env_file:
      - .env
    volumes:
      - "/media/your-local-folder:/media:ro"
    develop:
      watch:
        - path: .
          action: sync
          target: /app
        - path: requirements.txt
          action: rebuild

```

### 4. Create or Edit a `.env` file

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
GROUP_TARGET=your_group_id
UPLOAD_MODE=hybrid   # bisa "hybrid" atau "telethon"
```
- **UPLOAD_MODE=hybrid**: Bot API for files ≤50 MB, Telethon for files >50 MB.

- **UPLOAD_MODE=telethon**: All files uploaded via Telethon

### 5. Run with Docker compose

```bash
docker compose up --build
```

---

## Usage

Docker will automatically:

- **Build the image** with Python and dependencies.
- **Mount the `/media` folder** as configured.
- **Run the uploader** with the mode specified in `.env`.
---

## Log Format

### upload.log

```
/media/file1.pdf | 12.34 MB | 3.21s | 312.45 kbps | Bot API
/media/file2.zip | 120.00 MB | 25.00s | 4096.00 kbps | Telethon
```

### error.log

```
/media/file3.mp4 — Connection aborted
```

---

## Upload Logic

| Mode     | File Size | Upload Method | Library   |
|----------|-----------|---------------|-----------|
| Hybrid   | ≤ 50 MB   | Bot API       | requests  |
| Hybrid   | > 50 MB   | Telethon      | Telethon  |
| Telethon | All files | Telethon      | Telethon  |

## Notes

- Ensure your bot is added to the target group with permission to send files.
- Files larger than 2 GB may fail depending on Telegram limits and your connection.
- For maximum throughput, use `UPLOAD_MODE=telethon` with larger chunk sizes and concurrency.


---

## License

MIT License © 2025 Gylang
```

Let me know if you want this styled with badges, GitHub Actions, or modularized into multiple scripts. I can also help you refactor it into CLI mode or add argparse support.
