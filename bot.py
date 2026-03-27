#!/usr/bin/env python3
"""
Travel Planner (旅遊規劃師) - Telegram Bot
為 Yvonne 提供全面的旅遊規劃資訊
"""

import os
import re
import asyncio
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8585851488:AAFT7326kF79zgT-yVK6EEbxvic-MLTr1pg")

# 預設目的地數據庫
DESTINATION_DB = {
    "東京": {
        "country": "日本",
        "currency": "日幣 (JPY)",
        "budget_daily": {
            "budget": "NT$3,000-4,000",
            "mid": "NT$4,000-6,000",
            "luxury": "NT$6,000+"
        },
        "best_season": "3-5月 (春季)、9-11月 (秋季)",
        "attractions": [
            "淺草寺 - 東京最古老的佛教寺廟",
            "東京晴空塔 - 俯瞰全市景色",
            "新宿御苑 - 皇家公園",
            "築地市場 - 海鮮美食天堂",
            "秋葉原 - 動漫與電器聖地",
            "澀谷十字路口 - 世界最繁忙交叉口",
            "明治神宮 - 都市中的森林神社",
            "東京迪士尼樂園 - 夢幻王國"
        ],
        "food": [
            "壽司 - 築地市場新鮮壽司",
            "拉麵 - 一蘭拉麵、豚骨拉麵",
            "天婦羅 - 炸蝦、炸蔬菜",
            "燒肉 - 敘敘苑、烤肉",
            "便當 - 鐵路便當",
            "抹茶甜點 - 抹茶冰淇淋、蛋糕"
        ],
        "transport": [
            "地鐵 - JR線、都營地下鐵",
            "計程車 - 較昂貴但方便",
            "巴士 - 觀光循環巴士"
        ],
        "accommodation": [
            "新宿 - 交通樞紐，購物方便",
            "澀谷 - 年輕時尚區",
            "淺草 - 傳統文化區",
            "上野 - 博物館與公園區"
        ],
        "customs": [
            "進室內需脫鞋",
            "自動販賣機前不可飲食",
            "排隊秩序很重要",
            "電車上避免講電話"
        ],
        "safety": "東京是非常安全的城市，但仍需注意扒竊"
    },
    "巴黎": {
        "country": "法國",
        "currency":歐元 (EUR)",
        "budget_daily": {
            "budget": "NT$4,000-6,000",
            "mid": "NT$6,000-10,000",
            "luxury": "NT$10,000+"
        },
        "best_season": "4-6月、9-11月",
        "attractions": [
            "艾菲爾鐵塔 - 巴黎地標",
            "羅浮宮 - 世界最大博物館",
            "聖母院 - 哥德式建築經典",
            "香榭麗舍大道 - 購物天堂",
            "蒙馬特高地 - 藝術家廣場",
            "凡爾賽宮 - 奢華宮殿",
            "奧塞博物館 - 印象派收藏"
        ],
        "food": [
            "法式可麗餅 - 經典街頭美食",
            "馬卡龍 - Ladurée甜點",
            "法式洋蔥湯 - 傳統湯品",
            "紅酒燉牛肉 - 經典法菜",
            "可頌麵包 - 早餐必備",
            "法式蝸牛 - 特色料理"
        ],
        "transport": [
            "地鐵 - 涵蓋全市",
            "RER - 郊區交通",
            "計程車 - Uber普及"
        ],
        "accommodation": [
            "香榭麗舍 - 高檔購物區",
            "瑪黑區 - 藝術時尚區",
            "蒙帕納斯 - 藝術家區",
            "拉丁區 - 學生區，經濟實惠"
        ],
        "customs": [
            "見面需行貼面禮",
            "進入餐廳需打招呼",
            "小費通常是消費的10%",
            "下午1-3点是午餐時間"
        ],
        "safety": "小心扒手，尤其在觀光區"
    },
    "台北": {
        "country": "台灣",
        "currency": "新台幣 (TWD)",
        "budget_daily": {
            "budget": "NT$2,000-3,000",
            "mid": "NT$3,000-5,000",
            "luxury": "NT$5,000+"
        },
        "best_season": "3-5月、10-12月",
        "attractions": [
            "台北101 - 世界最高綠建築",
            "故宮博物院 - 中華文化寶藏",
            "士林夜市 - 最大的夜市",
            "龍山寺 - 傳統廟宇",
            "陽明山國家公園 - 溫泉與自然",
            "淡水老街 - 河岸風光",
            "信義商圈 - 購物與夜景"
        ],
        "food": [
            "珍珠奶茶 - 台灣發源地",
            "蚵仔煎 - 夜市經典",
            "牛肉麵 - 紅燒、清燉",
            "小籠包 - 鼎泰豐",
            "滷肉飯 - 國民美食",
            "挫冰 - 水果冰品"
        ],
        "transport": [
            "捷運 - 便捷的軌道交通",
            "UBike - YouBike租借",
            "計程車 - 隨處可見"
        ],
        "accommodation": [
            "信義區 - 最繁華商圈",
            "中山區 - 購物與美食",
            "大安區 - 文青區",
            "西門町 - 年輕潮流區"
        ],
        "customs": [
            "乘捷運需排队",
            "博愛座讓給有需要的人",
            "餐廳收取10%服務費",
            "很多場所禁止吸菸"
        ],
        "safety": "台北非常安全，適合獨旅"
    }
}

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

🎯 試試輸入：「東京」、「巴黎」或「台北」

或者輸入任何你想去的城市！
"""
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """幫助命令"""
    help_text = """📚 使用說明

只需輸入你想去的城市名稱，我就會為你生成完整的旅遊規劃！

範例：
• "東京"
• "巴黎"
• "台北"
• "紐約"
• "倫敦"

我會盡力為你搜尋最新的旅遊資訊。"""
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶訊息"""
    destination = update.message.text.strip()
    
    # 顯示規劃中的訊息
    planning_msg = await update.message.reply_text(f"🔍 正在為你規劃 {destination} 的行程...")
    
    try:
        # 先檢查資料庫
        if destination in DESTINATION_DB:
            plan = generate_plan_from_db(destination, DESTINATION_DB[destination])
        else:
            # 網路搜索獲取資訊
            plan = await search_and_generate_plan(destination)
        
        await planning_msg.edit_text(plan, parse_mode='Markdown')
    except Exception as e:
        await planning_msg.edit_text(f"❌ 抱歉，無法處理這個目的地: {destination}\n請稍後再試或嘗試其他城市。")

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

async def search_and_generate_plan(destination: str) -> str:
    """搜索並生成規劃"""
    from web_search import search_destination_info
    
    try:
        # 獲取城市資訊
        info = await search_destination_info(destination)
        return info
    except Exception as e:
        # 如果搜索失敗，使用通用格式
        return f"""🎯 **{destination}** 旅遊規劃

抱歉，目前無法獲取 {destination} 的詳細資訊。

💡 建議：
• 請嘗試其他熱門城市如「東京」、「巴黎」、「台北」
• 或者稍後再試

❓ 輸入 /help 查看更多使用說明"""

async def search_destination_info(destination: str) -> str:
    """搜索目的地資訊（預留介面）"""
    # 這裡可以接入真實的網路搜索 API
    # 目前返回通用模板
    return f"""🎯 **{destination}** 旅遊規劃

🌍 歡迎來到 {destination}！

📍 【热门景点】
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
💡 想知道更詳細的資訊嗎？嘗試輸入特定城市名稱！"""

def main():
    """啟動 Bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 註冊命令處理器
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # 註冊訊息處理器
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🌍 旅遊規劃師 Bot 啟動中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
