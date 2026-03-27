"""
Share module - 分享功能
"""

import urllib.parse
from telegram import Update
from telegram.ext import ContextTypes
from .storage import storage
from .preferences import get_user_prefs


async def share_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /share 命令 - 生成分享訊息"""
    args = context.args
    user_id = update.message.from_user.id
    
    if not args:
        help_text = """📝 使用方式：
/share <目的地>

範例：
/share 東京

會生成分享格式你可以複製分享給朋友！"""
        await update.message.reply_text(help_text)
        return
    
    destination = " ".join(args)
    
    # 取得用戶偏好
    prefs = get_user_prefs(user_id)
    
    # 生成分享訊息
    share_text = f"""🌍 旅遊規劃分享

📍 目的地：{destination}
📅 天數：{prefs['days']} 天
💰 預算：{prefs['budget']}
🏷️ 興趣：{', '.join(prefs['tags'])}

透過 /travel-planner Bot 規劃"""
    
    await update.message.reply_text(share_text)


async def sharelink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /sharelink 命令 - 生成簡化分享連結"""
    args = context.args
    
    if not args:
        await update.message.reply_text("📝 使用方式：/sharelink <目的地>")
        return
    
    destination = " ".join(args)
    # 這裡可以使用短網址服務，未來可擴展
    encoded = urllib.parse.quote(destination)
    share_url = f"https://t.me/your_bot?start={encoded}"
    
    await update.message.reply_text(
        f"🔗 分享連結：\n{share_url}\n\n"
        f"（請將 your_bot 替換為你的 Bot username）"
    )