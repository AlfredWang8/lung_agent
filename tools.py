import os
import requests
from langchain.tools import tool
from typing import Optional

class SerpAPITool:
    """SerpAPI搜索工具类"""
    
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, num_results: int = 5) -> Optional[dict]:
        """
        使用SerpAPI执行搜索
        
        Args:
            query: 搜索查询
            num_results: 返回结果数量
            
        Returns:
            搜索结果字典或None
        """
        if not self.api_key:
            raise ValueError("SERP_API_KEY环境变量未设置")
        
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": num_results
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"SerpAPI搜索失败: {e}")
            return None

@tool
def serpapi_search_tool(query: str) -> str:
    """
    使用SerpAPI搜索最新医学信息、临床指南和研究进展。
    特别适用于查找肺结节诊断、治疗指南和最新研究。
    
    Args:
        query: 搜索查询，例如"肺结节诊断指南 2024"
        
    Returns:
        格式化的搜索结果字符串
    """
    serpapi = SerpAPITool()
    result = serpapi.search(query)
    
    if not result:
        return "搜索失败，请检查网络连接或API密钥"
    
    # 解析搜索结果
    output = []
    
    # 添加基本信息
    if "search_information" in result:
        search_info = result["search_information"]
        output.append(f"📊 搜索结果统计:")
        output.append(f"   搜索查询: {search_info.get('query_displayed', query)}")
        output.append(f"   总结果数: {search_info.get('total_results', '未知')}")
        output.append(f"   搜索耗时: {search_info.get('time_taken_displayed', '未知')}")
        output.append("")
    
    # 添加有机搜索结果
    if "organic_results" in result:
        organic_results = result["organic_results"][:5]  # 取前5个结果
        output.append("🔍 相关搜索结果:")
        
        for i, item in enumerate(organic_results, 1):
            title = item.get("title", "无标题")
            link = item.get("link", "无链接")
            snippet = item.get("snippet", "无摘要")
            
            output.append(f"{i}. {title}")
            output.append(f"   链接: {link}")
            output.append(f"   摘要: {snippet}")
            output.append("")
    
    # 添加知识图谱信息（如果有）
    if "knowledge_graph" in result:
        kg = result["knowledge_graph"]
        output.append("📚 知识图谱信息:")
        
        if "title" in kg:
            output.append(f"   主题: {kg.get('title')}")
        if "description" in kg:
            output.append(f"   描述: {kg.get('description')}")
        if "type" in kg:
            output.append(f"   类型: {kg.get('type')}")
        
        output.append("")
    
    # 添加相关搜索建议
    if "related_searches" in result:
        related = result["related_searches"][:3]  # 取前3个相关搜索
        output.append("💡 相关搜索建议:")
        for i, rel in enumerate(related, 1):
            output.append(f"   {i}. {rel.get('query', '')}")
    
    return "\n".join(output)

# 导出工具
__all__ = ["serpapi_search_tool"]