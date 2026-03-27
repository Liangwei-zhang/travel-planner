"""
Feedback module - 用戶反饋機制
"""

import time
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from .storage import storage


FEEDBACK_FILE = "feedback.json"


async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /feedback 命令"""
    args = context.args
    
    if not args:
        help_text = """📝 使用方式：
/feedback 你的建議或意見

範例：
/feedback 希望增加更多亞洲城市！
/feedback 天氣資訊很有用，謝謝！"""
        await update.message.reply_text(help_text)
        return
    
    feedback_text = " ".join(args)
    user = update.message.from_user
    
    feedback_entry = {
        "id": int(time.time()),
        "user_id": user.id,
        "username": user.username or "",
        "full_name": user.full_name,
        "feedback": feedback_text,
        "timestamp": datetime.now().isoformat()
    }
    
    # 載入現有反饋
    feedback_data = storage.load(FEEDBACK_FILE, {"feedbacks": []})
    feedback_data["feedbacks"].append(feedback_entry)
    storage.save(FEEDBACK_FILE, feedback_data)
    
    await update.message.reply_text("✅ 感謝你的反饋！我們會認真考慮你的建議。")