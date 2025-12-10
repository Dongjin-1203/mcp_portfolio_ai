from app.config import Config

config = Config()

config.NOTION_TOKEN = "your_token"
config.NOTION_PORTFOLIO_PAGE_ID = "your_page_id"

from app.mcp.tools.notion_tools import (
    create_portfolio_page_from_markdown,
    find_portfolio_page_by_title,
    delete_portfolio_page_by_id
)

# 테스트 마크다운
markdown = """
# RFPilot 프로젝트

## 개요
RAG 기반 챗봇

## 기술 스택
- Python
- LangChain
"""

# 1. 페이지 생성
print("=== 페이지 생성 ===")
result = create_portfolio_page_from_markdown("RFPilot 테스트", markdown)
print(result)



# 2. 페이지 검색
print("\n=== 페이지 검색 ===")
page = find_portfolio_page_by_title("RFPilot 테스트")
print(page)

# 3. 페이지 삭제
if "id" in result:
    page_id = result['id']
    
    # 2. 페이지 삭제 (ID 사용)
    print("\n=== 페이지 삭제 ===")
    delete_result = delete_portfolio_page_by_id(page_id)
    print(delete_result)