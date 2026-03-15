# Deal Hunter Pro X - Telegram Bot Helper
# Uses the Telegram Bot API directly via requests (no python-telegram-bot dependency needed).

import requests


TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"


def send_alert(token: str, chat_id: str, message: str) -> dict:
    """
    Send a message to a Telegram chat or channel.

    Args:
        token: Telegram Bot API token (from BotFather)
        chat_id: Target chat ID or channel username (e.g. "@mychannel" or "-1001234567890")
        message: Message text (supports basic Markdown)

    Returns:
        dict with keys: success (bool), status_code (int), response (dict or str)
    """
    if not token or not chat_id or not message:
        return {
            "success": False,
            "status_code": 400,
            "response": "Missing required parameters: token, chat_id, or message.",
        }

    url = TELEGRAM_API_BASE.format(token=token, method="sendMessage")
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        return {
            "success": resp.status_code == 200 and data.get("ok", False),
            "status_code": resp.status_code,
            "response": data,
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 408,
            "response": "Request timed out. Check your internet connection.",
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "status_code": 503,
            "response": "Connection error. Check your internet connection.",
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "response": str(e),
        }


def test_connection(token: str) -> dict:
    """
    Test a bot token by calling getMe.

    Args:
        token: Telegram Bot API token

    Returns:
        dict with keys: success (bool), bot_name (str), username (str), error (str)
    """
    if not token:
        return {"success": False, "bot_name": None, "username": None, "error": "No token provided."}

    url = TELEGRAM_API_BASE.format(token=token, method="getMe")
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("ok"):
            result = data.get("result", {})
            return {
                "success": True,
                "bot_name": result.get("first_name"),
                "username": result.get("username"),
                "error": None,
            }
        else:
            return {
                "success": False,
                "bot_name": None,
                "username": None,
                "error": data.get("description", "Unknown error from Telegram API"),
            }
    except Exception as e:
        return {"success": False, "bot_name": None, "username": None, "error": str(e)}


def format_deal_alert(deal: dict) -> str:
    """
    Format a deal dict into a Telegram-friendly alert message.

    Args:
        deal: deal dictionary (from sample_data.py format)

    Returns:
        Formatted string ready to send via Telegram
    """
    saving = deal.get("original_price", 0) - deal.get("price", 0)
    saving_str = f"R{saving:,.0f}" if saving > 0 else "N/A"

    risk_emoji = {
        "low": "GREEN circle",
        "caution": "YELLOW circle",
        "elevated": "ORANGE circle",
        "high": "RED circle",
    }.get(deal.get("risk_level", "low"), "circle")

    message = (
        f"*DEAL HUNTER PRO X ALERT*\n\n"
        f"*{deal.get('title', 'Unknown')}*\n"
        f"Price: *R{deal.get('price', 0):,.0f}*\n"
        f"Saving: {saving_str}\n"
        f"Location: {deal.get('location', 'N/A')}\n"
        f"Platform: {deal.get('platform', 'N/A')}\n"
        f"Value Score: {deal.get('value_score', 0)}/100\n"
        f"Safety: {risk_emoji} {deal.get('risk_level', 'N/A').title()}\n"
        f"Scout: {deal.get('scout_source', 'N/A')}\n"
        f"Posted: {deal.get('posted_ago', 'N/A')}\n"
    )
    return message
