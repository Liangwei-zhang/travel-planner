"""
Favorites module - 收藏功能
"""

import time
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from .storage import storage


SAVED_FILE = "saved.json"


async def save_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /save 命令 - 保存當前規劃"""
    args = context.args
    user_id = update.message.from_user.id
    
    # 從 context 或 args 獲取目的地
    if args:
        destination = " ".join(args)
    elif hasattr(context, 'last_destination'):
        destination = context.last_destination
    else:
        await update.message.reply_text("📝 使用方式：/save <目的地>\n範例：/save 東京")
        return
    
    saved_data = storage.load(SAVED_FILE, {"saved": []})
    
    # 建立收藏項目
    entry = {
        "id": int(time.time()),
        "user_id": user_id,
        "destination": destination,
        "saved_at": datetime.now().isoformat()
    }
    
    saved_data["saved"].append(entry)
    storage.save(SAVED_FILE, saved_data)
    
    await update.message.reply_text(f"✅ 已收藏：{destination}")


async def saved_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /saved 命令 - 查看收藏"""
    user_id = update.message.from_user.id
    
    saved_data = storage.load(SAVED_FILE, {"saved": []})
    user_saved = [s for s in saved_data["saved"] if s["user_id"] == user_id]
    
    if not user_saved:
        await update.message.reply_text("📁 你還沒有收藏任何規劃。\n使用 /save <目的地> 來收藏！")
        return
    
    # 格式化顯示
    items = []
    for i, s in enumerate(user_saved, 1):
        date = s["saved_at"][:10]
        items.append(f"{i}. {s['destination']} (儲存於 {date})")
    
    text = "📁 你的收藏：\n\n" + "\n".join(items)
    text += "\n\n使用 /remove <編號> 刪除收藏"
    
    await update.message.reply_text(text)


async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /remove 命令 - 刪除收藏"""
    args = context.args
    user_id = update.message.from_user.id
    
    if not args:
        await update.message.reply_text("📝 使用方式：/remove <編號>\n先使用 /saved 查看編號")
        return
    
    try:
        index = int(args[0]) - 1
    except ValueError:
        await update.message.reply_text("❌ 請輸入有效的編號")
        return
    
    saved_data = storage.load(SAVED_FILE, {"saved": []})
    user_saved = [s for s in saved_data["saved"] if s["user_id"] == user_id]
    
    if index < 0 or index >= len(user_saved):
        await update.message.reply_text("❌ 無效的編號，請使用 /saved 查看")
        return
    
    # 移除項目
    removed = user_saved.pop(index)
    
    # 重新建構用戶的收藏（排除已移除的）
    new_saved = [s for s in saved_data["saved"] if s["user_id"] != user_id]
    new_saved.extend(user_saved)
    saved_data["saved"] = new_saved
    storage.save(SAVED_FILE, saved_data)
    
    await update.message.reply_text(f"✅ 已移除：{removed['destination']}")