"""
Weather module - 天氣 API 整合
"""

import os
import json
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
from .storage import storage


# 嘗試載入天氣 API 金鑰（可選）
WEATHER_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY") or os.environ.get("WEATHER_API_KEY")

# 城市對應表 (目的地 -> 天氣城市代碼)
CITY_CODE_MAP = {
    "東京": {"name": "Tokyo", "country": "JP"},
    "巴黎": {"name": "Paris", "country": "FR"},
    "台北": {"name": "Taipei", "country": "TW"},
    "紐約": {"name": "New York", "country": "US"},
    "倫敦": {"name": "London", "country": "GB"},
    "首爾": {"name": "Seoul", "country": "KR"},
    "大阪": {"name": "Osaka", "country": "JP"},
    "香港": {"name": "Hong Kong", "country": "HK"},
    "新加坡": {"name": "Singapore", "country": "SG"},
    "曼谷": {"name": "Bangkok", "country": "TH"},
}

WEATHER_CACHE_FILE = "weather_cache.json"


def get_weather_sync(city: str) -> str:
    """同步取得天氣資訊（供非同步環境使用）"""
    # 嘗試匹配城市
    city_info = None
    for key in CITY_CODE_MAP:
        if key in city or city in key:
            city_info = CITY_CODE_MAP[key]
            break
    
    if not city_info:
        return f"🌤️ {city} 的天氣資訊需要 API 金鑰"
    
    # 如果有 API 金鑰，嘗試取得真實資料
    if WEATHER_API_KEY:
        try:
            import urllib.request
            import urllib.parse
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_info['name']},{city_info['country']}&appid={WEATHER_API_KEY}&units=metric"
            
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                
                # 快取結果
                cache_weather(city, data)
                
                return f"🌤️ {city} 天氣：{description}\n🌡️ 溫度：{temp}°C\n💧 濕度：{humidity}%"
        except Exception:
            pass  # 回退到快取或預設
    
    # 回退到快取或預設訊息
    cached = get_cached_weather(city_info["name"])
    if cached:
        temp = cached["main"]["temp"]
        description = cached["weather"][0]["description"]
        return f"🌤️ {city} 天氣（快取）：{description}\n🌡️ 溫度：{temp}°C"
    
    return f"🌤️ {city} 天氣資訊：請設定 OPENWEATHERMAP_API_KEY 以取得即時天氣"


def cache_weather(city: str, data: dict) -> None:
    """快取天氣資料"""
    cache = storage.load(WEATHER_CACHE_FILE, {"cache": {}})
    cache["cache"][city] = {
        "data": data,
        "timestamp": __import__("time").time()
    }
    storage.save(WEATHER_CACHE_FILE, cache)


def get_cached_weather(city: str) -> dict | None:
    """取得快取的天氣資料"""
    cache = storage.load(WEATHER_CACHE_FILE, {"cache": {}})
    entry = cache["cache"].get(city)
    if entry:
        import time
        # 快取有效期 1 小時
        if time.time() - entry["timestamp"] < 3600:
            return entry["data"]
    return None


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /weather 命令"""
    args = context.args
    
    if not args:
        help_text = """🌤️ 使用方式：
/weather <城市>

範例：
/weather 東京
/weather 巴黎"""
        await update.message.reply_text(help_text)
        return
    
    destination = " ".join(args)
    
    # 取得天氣資訊
    weather_text = get_weather_sync(destination)
    await update.message.reply_text(weather_text)


# 非同步版本（如果需要）
async def weather_command_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /weather 命令（非同步版本）"""
    args = context.args
    
    if not args:
        await update.message.reply_text("📝 使用方式：/weather <城市>")
        return
    
    destination = " ".join(args)
    weather_text = get_weather_sync(destination)
    await update.message.reply_text(weather_text)