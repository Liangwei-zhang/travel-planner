/**
 * 目的地匹配引擎
 * 負責從 JSON 資料庫中查找匹配的目的地
 */

const fs = require('fs');
const path = require('path');

class DestinationMatcher {
  /**
   * @param {string} dataPath - 資料庫檔案路徑
   */
  constructor(dataPath) {
    this.dataPath = dataPath;
    this.destinations = null;
  }

  /**
   * 載入資料庫
   */
  load() {
    const absolutePath = path.resolve(this.dataPath);
    const data = fs.readFileSync(absolutePath, 'utf8');
    this.destinations = JSON.parse(data);
    return this;
  }

  /**
   * 精確匹配
   * @param {string} query - 查詢關鍵字
   * @returns {object|null} 匹配的目的地資料或 null
   */
  exactMatch(query) {
    if (!this.destinations) this.load();
    return this.destinations[query] || null;
  }

  /**
   * 模糊匹配 - 檢查查詢字串是否包含目的地名稱
   * @param {string} query - 查詢關鍵字
   * @returns {object|null} 匹配的目的地資料或 null
   */
  fuzzyMatch(query) {
    if (!this.destinations) this.load();
    
    const keys = Object.keys(this.destinations);
    const lowerQuery = query.toLowerCase();
    
    // 檢查 query 是否包含某個目的地名稱
    for (const dest of keys) {
      if (query.includes(dest)) {
        return { name: dest, data: this.destinations[dest] };
      }
    }
    
    // 檢查目的地名稱是否包含 query
    for (const dest of keys) {
      if (dest.includes(query)) {
        return { name: dest, data: this.destinations[dest] };
      }
    }
    
    // 忽略大小寫匹配
    for (const dest of keys) {
      if (dest.toLowerCase() === lowerQuery) {
        return { name: dest, data: this.destinations[dest] };
      }
    }
    
    return null;
  }

  /**
   * 智能匹配 - 優先精確匹配，失敗則 fuzzy
   * @param {string} query - 查詢關鍵字
   * @returns {object|null} { name, data } 或 null
   */
  match(query) {
    // 優先精確匹配
    const exact = this.exactMatch(query);
    if (exact) {
      return { name: query, data: exact };
    }
    
    // 嘗試模糊匹配
    return this.fuzzyMatch(query);
  }

  /**
   * 取得所有目的地名稱列表
   * @returns {string[]} 目的地名稱陣列
   */
  listDestinations() {
    if (!this.destinations) this.load();
    return Object.keys(this.destinations);
  }

  /**
   * 檢查目的地是否存在
   * @param {string} query - 查詢關鍵字
   * @returns {boolean}
   */
  hasDestination(query) {
    return this.match(query) !== null;
  }
}

module.exports = DestinationMatcher;