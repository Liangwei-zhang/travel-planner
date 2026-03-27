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
OWNER_ID = os.environ.get("OWNER_ID", "6390423676")

if not BOT_TOKEN:
    print("❌ 錯誤：請設定 TELEGRAM_BOT_TOKEN 環境變數")
    print("   請建立 .env 檔案或設定環境變數")
    exit(1)

# 載入目的地資料庫
DATA_PATH = Path(__file__).parent / "data" / "destinations.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    DESTINATION_DB = json.load(f)


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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶訊息"""
    destination = update.message.text.strip()
    
    # 顯示規劃中的訊息
    planning_msg = await update.message.reply_text(f"🔍 正在為你規劃 {destination} 的行程...")
    
    try:
        # 先檢查資料庫
        plan = generate_plan(destination)
        await planning_msg.edit_text(plan, parse_mode='Markdown')
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
    accommodation = "\n".join([f"  • {a}" for a in data["accommodation"]])
    customs = "\n".join([f"  • {c}" for c in data["customs"]])
    
    plan = f"""🎯 **{destination}** 旅遊規劃

📍 【景點推薦】
{attractions}

🍜 【當地美食】
{food}

💰 【預算估算】(每日)
  • 經濟型：{data['budget_daily']['budget']}
  • 中檔：{data['budget_daily']['mid']}
  • 豪華：{data['budget_daily']['luxury']}

🚗 【交通指南】
{transport}

🏨 【住宿推薦】
{accommodation}

🌤️ 【最佳旅遊季節】
  {data['best_season']}

⚠️ 【當地習俗與安全】
{customs}

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


def main():
    """啟動 Bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 註冊命令處理器
    app.add_handler(CommandHandler("start", start_command))
    
    # 註冊訊息處理器
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🌍 旅遊規劃師 Bot 啟動中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()