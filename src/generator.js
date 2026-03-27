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
    
    // 住宿處理（支援新舊格式）
    let accommodationStr;
    if (typeof data.accommodation === 'object' && !Array.isArray(data.accommodation)) {
      const budget = data.accommodation.budget.map(a => `  • ${a}`).join('\n');
      const mid = data.accommodation.mid.map(a => `  • ${a}`).join('\n');
      const luxury = data.accommodation.luxury.map(a => `  • ${a}`).join('\n');
      accommodationStr = `💰 經濟型：\n${budget}\n🏠 中檔：\n${mid}\n🌟 豪華：\n${luxury}`;
    } else {
      accommodationStr = data.accommodation.map(a => `  • ${a}`).join('\n');
    }
    
    const customs = data.customs.map(c => `  • ${c}`).join('\n');
    
    // 每日行程
    let itineraryText = '';
    if (data.itinerary) {
      for (const [day, activities] of Object.entries(data.itinerary)) {
        const dayName = day.replace('day', 'Day ');
        itineraryText += `\n${dayName}: ${activities.join(' → ')}`;
      }
    }
    
    // 機場交通
    const airportText = data.airport_transport || '請查詢當地交通官網';
    
    // 穿搭建議
    const clothingText = data.clothing || '建議穿著舒適，視季節而定';
    
    // 緊急聯絡
    let emergencyText = '';
    if (data.emergency) {
      const em = data.emergency;
      emergencyText = `🚨 緊急電話：
  • 報警：${em.police || 'N/A'}
  • 救護車：${em.ambulance || 'N/A'}
  • 旅遊警察：${em.tourist_police || em.tourist_service || em.tourist_hotline || 'N/A'}
  • 駐外單位：${em.embassy || 'N/A'}`;
    }
    
    // 預算細項
    let budgetText = '';
    if (data.budget_breakdown) {
      const bb = data.budget_breakdown;
      budgetText = `📊 預算細項（每日）：
  • 住宿：${bb.accommodation || 'N/A'}
  • 餐飲：${bb.food || 'N/A'}
  • 交通：${bb.transport || 'N/A'}
  • 娛樂：${bb.entertainment || 'N/A'}`;
    }
    
    return `🎯 *${destination}* 旅遊規劃

📍 【景點推薦】
${attractions}

🍜 【當地美食】
${food}

📅 【每日行程】${itineraryText}

💰 【預算估算】(每日)
  • 經濟型：${data.budget_daily.budget}
  • 中檔：${data.budget_daily.mid}
  • 豪華：${data.budget_daily.luxury}

${budgetText}

🚗 【交通指南】
${transport}

✈️ 【機場交通】
${airportText}

🏨 【住宿推薦】
${accommodationStr}

🌤️ 【最佳旅遊季節】
  ${data.best_season}

👕 【穿搭建議】
${clothingText}

⚠️ 【當地習俗與安全】
${customs}

${emergencyText}

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

📅 【每日行程】
  Day 1: 市中心探索
  Day 2: 博物館參觀
  Day 3: 當地市場體驗

💰 【預算估算】(每日)
  • 經濟型：NT$2,000-3,000
  • 中檔：NT$3,000-5,000
  • 豪華：NT$5,000+

📊 【預算細項】（每日）
  • 住宿：NT$800-2,000
  • 餐飲：NT$500-1,200
  • 交通：NT$150-400
  • 娛樂：NT$300-800

🚗 【交通指南】
  • 機場交通
  • 公共交通
  • 計程車/共乘

✈️ 【機場交通】
  請查詢當地交通官網

🏨 【住宿推薦】
  • 市中心飯店
  • 經濟型住宿
  • 特色民宿

🌤️ 【最佳旅遊季節】
  請查詢當地天氣

👕 【穿搭建議】
  建議穿著舒適，視季節攜帶適當衣物

⚠️ 【實用提示】
  • 提前預訂機票與住宿
  • 兌換當地貨幣
  • 注意保管隨身物品

🚨 【緊急電話】
  • 當地報警：請查詢
  • 救護車：請查詢
  • 駐外單位：請查詢

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
• 預算估算（含細項分類）
• 交通指南（含機場交通）
• 住宿推薦（各價位）
• 穿搭建議
• 緊急聯絡資訊

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