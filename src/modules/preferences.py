"""
Preferences module - 用戶偏好自訂
"""

from telegram import Update
from telegram.ext import ContextTypes
from .storage import storage


PREFS_FILE = "preferences.json"

VALID_DAYS = list(range(1, 15))  # 1-14 days
VALID_BUDGETS = ["經濟", "中檔", "豪華"]
VALID_TAGS = ["美食", "景點", "購物", "文化"]


def get_user_prefs(user_id: int) -> dict:
    """取得用戶偏好"""
    prefs_data = storage.load(PREFS_FILE, {"preferences": {}})
    return prefs_data["preferences"].get(str(user_id), {
        "days": 3,
        "budget": "中檔",
        "tags": ["景點", "美食"]
    })


def save_user_prefs(user_id: int, prefs: dict) -> None:
    """儲存用戶偏好"""
    prefs_data = storage.load(PREFS_FILE, {"preferences": {}})
    prefs_data["preferences"][str(user_id)] = prefs
    storage.save(PREFS_FILE, prefs_data)


async def prefs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /prefs 命令"""
    args = context.args
    user_id = update.message.from_user.id
    
    if not args:
        # 顯示當前偏好
        prefs = get_user_prefs(user_id)
        current_text = f"""⚙️ 你的當前偏好：

📅 行程天數：{prefs['days']} 天
💰 預算等級：{prefs['budget']}
🏷️ 興趣標籤：{', '.join(prefs['tags'])}

修改方式：
/prefs days <天數> - 設定天數 (1-14)
/prefs budget <經濟|中檔|豪華> - 設定預算
/preprefs tags <標籤1> <標籤2> ... - 設定興趣標籤

範例：
/prefs days 7
/prefs budget 豪華
/prefs tags 美食 購物"""
        await update.message.reply_text(current_text)
        return
    
    command = args[0].lower()
    
    if command == "days":
        try:
            days = int(args[1])
            if days not in VALID_DAYS:
                await update.message.reply_text(f"❌ 天數需在 1-14 之間")
                return
            prefs = get_user_prefs(user_id)
            prefs["days"] = days
            save_user_prefs(user_id, prefs)
            await update.message.reply_text(f"✅ 已設定行程天數為 {days} 天")
        except (IndexError, ValueError):
            await update.message.reply_text("❌ 請輸入有效的天數 (1-14)")
    
    elif command == "budget":
        if len(args) < 2:
            await update.message.reply_text("❌ 請指定預算等級：經濟、中檔、豪華")
            return
        budget = args[1]
        if budget not in VALID_BUDGETS:
            await update.message.reply_text(f"❌ 預算需為：{', '.join(VALID_BUDGETS)}")
            return
        prefs = get_user_prefs(user_id)
        prefs["budget"] = budget
        save_user_prefs(user_id, prefs)
        await update.message.reply_text(f"✅ 已設定預算為 {budget}")
    
    elif command == "tags":
        tags = args[1:]
        if not tags:
            await update.message.reply_text("❌ 請指定至少一個標籤")
            return
        valid_tags = [t for t in tags if t in VALID_TAGS]
        if not valid_tags:
            await update.message.reply_text(f"❌ 有效標籤：{', '.join(VALID_TAGS)}")
            return
        prefs = get_user_prefs(user_id)
        prefs["tags"] = valid_tags
        save_user_prefs(user_id, prefs)
        await update.message.reply_text(f"✅ 已設定興趣標籤：{', '.join(valid_tags)}")
    
    else:
        await update.message.reply_text("❌ 未知指令，請使用 /prefs 查看說明")