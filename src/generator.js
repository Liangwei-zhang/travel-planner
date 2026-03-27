/**
 * 旅遊規劃生成器
 * 負責將目的地資料轉換為格式化的旅遊規劃訊息
 */

class PlanGenerator {
  /**
   * 從資料庫格式的目的地資料生成旅遊規劃
   * @param {string} destination - 目的地名稱
   * @param {object} data - 目的地資料
   * @returns {string} 格式化的旅遊規劃訊息
   */
  generateFromDB(destination, data) {
    const attractions = data.attractions.map(a => `  • ${a}`).join('\n');
    const food = data.food.map(f => `  • ${f}`).join('\n');
    const transport = data.transport.map(t => `  • ${t}`).join('\n');
    const accommodation = data.accommodation.map(a => `  • ${a}`).join('\n');
    const customs = data.customs.map(c => `  • ${c}`).join('\n');

    return `🎯 *${destination}* 旅遊規劃

📍 【景點推薦】
${attractions}

🍜 【當地美食】
${food}

💰 【預算估算】(每日)
  • 經濟型：${data.budget_daily.budget}
  • 中檔：${data.budget_daily.mid}
  • 豪華：${data.budget_daily.luxury}

🚗 【交通指南】
${transport}

🏨 【住宿推薦】
${accommodation}

🌤️ 【最佳旅遊季節】
  ${data.best_season}

⚠️ 【當地習俗與安全】
${customs}

💵 當地貨幣：${data.currency}

---
💡 資料僅供參考，實際費用可能有所不同。`;
  }

  /**
   * 生成通用規劃（當找不到資料時）
   * @param {string} destination - 目的地名稱
   * @returns {string} 通用旅遊規劃訊息
   */
  generateGeneric(destination) {
    return `🎯 *${destination}* 旅遊規劃

🌍 歡迎來到 ${destination}！

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
💡 想知道更詳細的資訊嗎？嘗試輸入「東京」、「巴黎」、「台北」等熱門城市！`;
  }

  /**
   * 生成歡迎訊息
   * @returns {string} 歡迎訊息
   */
  generateWelcome() {
    return `🌍 歡迎使用旅遊規劃師！

我是你的私人旅遊助理，可以幫你規劃行程。

📝 使用方式：
直接輸入你想去的城市名稱，我會為你提供：

• 景點推薦
• 當地美食
• 行程規劃
• 預算估算
• 交通指南
• 住宿建議
• 天氣與提示
• 當地習俗與安全

🎯 試試輸入：「東京」、「巴黎」或「台北」`;
  }

  /**
   * 生成錯誤訊息
   * @param {string} destination - 目的地名稱
   * @returns {string} 錯誤訊息
   */
  generateError(destination) {
    return `❌ 抱歉，無法處理這個目的地: ${destination}
請稍後再試或嘗試其他城市。`;
  }

  /**
   * 生成規劃中訊息
   * @param {string} destination - 目的地名稱
   * @returns {string} 規劃中訊息
   */
  generatePlanning(destination) {
    return `🔍 正在為你規劃 ${destination} 的行程...`;
  }
}

module.exports = PlanGenerator;