#!/usr/bin/env python3
"""
Travel Planner (旅遊規劃師) - Telegram Bot
為 Yvonne 提供全面的旅遊規劃資訊
"""

import os
import json
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration - 從環境變數讀取
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")

if not BOT_TOKEN:
    print("❌ 錯誤：請設定 TELEGRAM_BOT_TOKEN 環境變數")
    print("   請建立 .env 檔案或設定環境變數")
    exit(1)

# 載入目的地資料庫
DATA_PATH = Path(__file__).parent.parent / "data" / "destinations.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    DESTINATION_DB = json.load(f)

# 匯入模組
from modules.storage import storage
from modules.feedback import feedback_command
from modules.preferences import prefs_command, get_user_prefs
from modules.favorites import save_command, saved_command, remove_command
from modules.share import share_command, sharelink_command
from modules.weather import weather_command, get_weather_sync


# 儲存最後規劃的目的地（供收藏使用）
user_context = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎命令"""
    welcome_text = """🌍 歡迎使用旅遊規劃師！

我是你的私人旅遊助理，可以幫你規劃行程。

📝 使用方式：
輸入你想去的城市名稱，我會為你提供：

• 景點推薦
• 當地美食
• 行程規劃
• 預算估算
• 交通指南
• 住宿建議
• 天氣與提示
• 當地習俗與安全

🎯 試試輸入：「東京」、「巴黎」或「台北」"""
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """幫助命令"""
    help_text = """📚 旅遊規劃師 - 指令列表

🗺️ 主要指令：
/start - 開始使用
/help - 顯示幫助
/weather <城市> - 查看天氣

⚙️ 個人化設定：
/prefs - 查看/設定偏好
  /prefs days <天數> - 設定行程天數 (1-14)
  /prefs budget <經濟|中檔|豪華> - 設定預算
  /prefs tags <標籤> ... - 設定興趣標籤

📁 收藏功能：
/save <目的地> - 收藏規劃
/saved - 查看收藏
/remove <編號> - 刪除收藏

📤 分享功能：
/share <目的地> - 生成分享訊息
/sharelink <目的地> - 生成分享連結

💬 反饋：
/feedback <建議> - 提交反饋

---
直接輸入城市名稱即可獲得規劃！"""
    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶訊息"""
    # 檢查是否為 owner
    if OWNER_ID and str(update.message.from_user.id) != OWNER_ID:
        return  # 忽略非 owner 的訊息
    
    destination = update.message.text.strip()
    user_id = update.message.from_user.id
    
    # 顯示規劃中的訊息
    planning_msg = await update.message.reply_text(f"🔍 正在為你規劃 {destination} 的行程...")
    
    try:
        # 先檢查資料庫
        plan = generate_plan(destination)
        
        # 加入天氣資訊（可選）
        try:
            weather_info = get_weather_sync(destination)
            if "需要 API 金鑰" not in weather_info:
                plan += f"\n\n{weather_info}"
        except:
            pass
        
        await planning_msg.edit_text(plan, parse_mode='Markdown')
        
        # 儲存最後目的地供收藏使用
        user_context[user_id] = destination
        
    except Exception as e:
        await planning_msg.edit_text(f"❌ 抱歉，無法處理這個目的地: {destination}\n請稍後再試或嘗試其他城市。")


def generate_plan(destination: str) -> str:
    """生成旅遊規劃"""
    # 嘗試精確匹配
    if destination in DESTINATION_DB:
        return generate_plan_from_db(destination, DESTINATION_DB[destination])
    
    # 嘗試模糊匹配
    for dest_name in DESTINATION_DB:
        if dest_name in destination or destination in dest_name:
            return generate_plan_from_db(dest_name, DESTINATION_DB[dest_name])
    
    # 找不到時使用通用格式
    return generate_generic(destination)


def generate_plan_from_db(destination: str, data: dict) -> str:
    """從本地資料庫生成規劃"""
    attractions = "\n".join([f"  • {a}" for a in data["attractions"]])
    food = "\n".join([f"  • {f}" for f in data["food"]])
    transport = "\n".join([f"  • {t}" for t in data["transport"]])
    
    # 住宿處理（支援新舊格式）
    if isinstance(data.get("accommodation"), dict):
        acc_budget = "\n".join([f"  • {a}" for a in data["accommodation"].get("budget", [])])
        acc_mid = "\n".join([f"  • {a}" for a in data["accommodation"].get("mid", [])])
        acc_luxury = "\n".join([f"  • {a}" for a in data["accommodation"].get("luxury", [])])
        accommodation_str = f"""💰 經濟型：
{acc_budget}
🏠 中檔：
{acc_mid}
🌟 豪華：
{acc_luxury}"""
    else:
        accommodation_str = "\n".join([f"  • {a}" for a in data["accommodation"]])
    
    customs = "\n".join([f"  • {c}" for c in data["customs"]])
    
    # 每日行程
    itinerary_text = ""
    if "itinerary" in data:
        for day, activities in data["itinerary"].items():
            day_name = day.replace("day", "Day ")
            itinerary_text += f"\n{day_name}: {' → '.join(activities)}"
    
    # 機場交通
    airport_text = data.get("airport_transport", "請查詢當地交通官網")
    
    # 穿搭建議
    clothing_text = data.get("clothing", "建議穿著舒適，視季節而定")
    
    # 緊急聯絡
    emergency_text = ""
    if "emergency" in data:
        em = data["emergency"]
        emergency_text = f"""🚨 緊急電話：
  • 報警：{em.get('police', 'N/A')}
  • 救護車：{em.get('ambulance', 'N/A')}
  • 旅遊警察：{em.get('tourist_police', em.get('tourist_service', em.get('tourist_hotline', 'N/A')))}
  • 駐外單位：{em.get('embassy', 'N/A')}"""
    
    # 預算細項
    budget_text = ""
    if "budget_breakdown" in data:
        bb = data["budget_breakdown"]
        budget_text = f"""📊 預算細項（每日）：
  • 住宿：{bb.get('accommodation', 'N/A')}
  • 餐飲：{bb.get('food', 'N/A')}
  • 交通：{bb.get('transport', 'N/A')}
  • 娛樂：{bb.get('entertainment', 'N/A')}"""
    
    plan = f"""🎯 **{destination}** 旅遊規劃

📍 【景點推薦】
{attractions}

🍜 【當地美食】
{food}

📅 【每日行程】{itinerary_text}

💰 【預算估算】(每日)
  • 經濟型：{data['budget_daily']['budget']}
  • 中檔：{data['budget_daily']['mid']}
  • 豪華：{data['budget_daily']['luxury']}

{budget_text}

🚗 【交通指南】
{transport}

✈️ 【機場交通】
{airport_text}

🏨 【住宿推薦】
{accommodation_str}

🌤️ 【最佳旅遊季節】
  {data['best_season']}

👕 【穿搭建議】
{clothing_text}

⚠️ 【當地習俗與安全】
{customs}

{emergency_text}

💵 當地貨幣：{data['currency']}

---
💡 資料僅供參考，實際費用可能有所不同。"""
    return plan


def generate_generic(destination: str) -> str:
    """生成通用規劃"""
    return f"""🎯 **{destination}** 旅遊規劃

🌍 歡迎來到 {destination}！

📍 【熱門景點】
  • 市中心廣場
  • 國家博物館
  • 歷史古蹟
  • 當地市場

🍜 【當地美食】
  • 特色料理 1
  • 特色料理 2
  • 街頭小吃

💰 【預算估算】(每日)
  • 經濟型：NT$2,000-3,000
  • 中檔：NT$3,000-5,000
  • 豪華：NT$5,000+

🚗 【交通指南】
  • 機場交通
  • 公共交通
  • 計程車/共乘

🏨 【住宿推薦】
  • 市中心飯店
  • 經濟型住宿
  • 特色民宿

⚠️ 【實用提示】
  • 提前預訂機票與住宿
  • 兌換當地貨幣
  • 注意保管隨身物品

---
💡 想知道更詳細的資訊嗎？嘗試輸入「東京」、「巴黎」、「台北」等熱門城市！"""


# 包裝收藏命令以傳遞 context
async def save_with_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args
    
    if not args:
        # 嘗試使用最後規劃的目的地
        if user_id in user_context:
            context.args = [user_context[user_id]]
        else:
            await update.message.reply_text("📝 使用方式：/save <目的地>\n範例：/save 東京")
            return
    
    await save_command(update, context)


def main():
    """啟動 Bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 註冊命令處理器
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("feedback", feedback_command))
    app.add_handler(CommandHandler("prefs", prefs_command))
    app.add_handler(CommandHandler("save", save_with_context))
    app.add_handler(CommandHandler("saved", saved_command))
    app.add_handler(CommandHandler("remove", remove_command))
    app.add_handler(CommandHandler("share", share_command))
    app.add_handler(CommandHandler("sharelink", sharelink_command))
    app.add_handler(CommandHandler("weather", weather_command))
    
    # 註冊訊息處理器
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🌍 旅遊規劃師 Bot 啟動中...")
    print("📚 可用指令：/help")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()