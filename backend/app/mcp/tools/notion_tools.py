from app.mcp.server import mcp
from notion_client import Client
import os
import logging

from app.config import Config

config = Config()

logger = logging.getLogger(__name__)

def _get_notion_client() -> Client:
    """Notion 클라이언트를 안전하게 가져옵니다"""
    token = config.NOTION_TOKEN
    if not token:
        raise ValueError("NOTION_TOKEN이 설정되지 않았습니다")
    return Client(auth=token)

def _markdown_to_notion_blocks(markdown: str) -> list:
    """마크다운을 Notion 블록으로 변환합니다 (간단 버전)"""
    blocks = []
    
    for line in markdown.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # 헤더 변환
        if line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        else:
            # 일반 텍스트
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
    
    return blocks

@mcp.tool()
def create_portfolio_page_from_markdown(title: str, markdown_content: str) -> dict:
    """마크다운을 Notion 포트폴리오 페이지로 생성합니다
    
    Returns:
        {"url": "페이지 URL", "id": "페이지 ID"}
    """
    try:
        notion = _get_notion_client()
        parent_page_id = os.getenv("NOTION_PORTFOLIO_PAGE_ID")
        
        if not parent_page_id:
            raise ValueError("NOTION_PORTFOLIO_PAGE_ID가 설정되지 않았습니다")
        
        blocks = _markdown_to_notion_blocks(markdown_content)
        
        response = notion.pages.create(
            parent={"page_id": parent_page_id},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            children=blocks[:100]
        )
        
        logger.info(f"페이지 생성 성공: {title}")
        return {
            "url": response['url'],
            "id": response['id'],  # ID 추가!
            "title": title
        }
        
    except Exception as e:
        logger.error(f"페이지 생성 실패 ({title}): {e}")
        return {"error": str(e)}

@mcp.tool()
def find_portfolio_page_by_title(title: str) -> dict:
    """부모 페이지의 자식 페이지에서 제목으로 찾습니다"""
    try:
        notion = _get_notion_client()
        parent_page_id = config.NOTION_PORTFOLIO_PAGE_ID
        
        # 부모 페이지의 자식 블록 가져오기
        children = notion.blocks.children.list(block_id=parent_page_id)
        
        for block in children['results']:
            if block['type'] == 'child_page':
                # 자식 페이지 정보 가져오기
                page = notion.pages.retrieve(page_id=block['id'])
                
                # 제목 비교
                page_title = ""
                if 'title' in page['properties']:
                    title_list = page['properties']['title']['title']
                    if title_list:
                        page_title = title_list[0]['plain_text']
                
                if page_title == title:
                    return {
                        "id": page['id'],
                        "url": page['url'],
                        "title": page_title
                    }
        
        return {"error": f"'{title}' 페이지를 찾을 수 없습니다"}
        
    except Exception as e:
        logger.error(f"페이지 검색 실패: {e}")
        return {"error": str(e)}

@mcp.tool()
def delete_portfolio_page_by_id(page_id: str) -> str:
    """페이지 ID로 포트폴리오 페이지를 삭제합니다"""
    try:
        notion = _get_notion_client()
        
        # 페이지 삭제 (archived)
        notion.pages.update(
            page_id=page_id,
            archived=True
        )
        
        logger.info(f"페이지 삭제 성공: {page_id}")
        return f"페이지가 삭제되었습니다"
        
    except Exception as e:
        logger.error(f"페이지 삭제 실패 ({page_id}): {e}")
        return f"페이지 삭제 실패: {str(e)}"
    
@mcp.tool()
def delete_portfolio_page(title: str) -> str:
    """제목으로 포트폴리오 페이지를 찾아 삭제합니다"""
    try:
        # 1단계: 제목으로 페이지 찾기
        page_info = find_portfolio_page_by_title(title)
        
        if "error" in page_info:
            return page_info["error"]
        
        # 2단계: 찾은 ID로 삭제
        return delete_portfolio_page_by_id(page_info['id'])
        
    except Exception as e:
        logger.error(f"페이지 삭제 실패 ({title}): {e}")
        return f"페이지 삭제 실패: {str(e)}"