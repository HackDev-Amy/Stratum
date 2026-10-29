import logging, os, requests
logger = logging.getLogger(__name__)

def send_notification(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": message},
                timeout=5,
            )
        except Exception as e:
            logger.warning(f"Telegram notify failed: {e}")
    else:
        logger.info(f"[NOTIFY] {message}")