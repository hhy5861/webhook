import os

# Environment variables configuration
WECOM_WEBHOOK = os.getenv("WECOM_WEBHOOK", "").strip()   # 群机器人完整 URL（含 key）
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10"))
AM_URL = os.getenv("AM_URL", "")
