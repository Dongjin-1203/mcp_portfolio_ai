import anthropic

from app.config import Config
from app.mcp.tools.github_tools import (
    list_repositories,
    get_repository_info, 
    get_readme_content
)

from app.mcp.tools.notion_tools import (
    create_portfolio_page_from_markdown,
    find_portfolio_page_by_title,
    delete_portfolio_page_by_id,
    delete_portfolio_page
) 

config = Config()

# Anthropic 클라이언트 초기화
client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

# MCP 도구 스키마 정의
mcp_tools_schema = [
    {
        "name": "list_repositories",
        "description": "사용자의 GitHub 레포지토리 목록을 가져옵니다",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_repository_info",
        "description": "특정 레포지토리의 상세 정보를 가져옵니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "레포지토리 이름 (예: username/repo)"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_readme_content",
        "description": "README.md 내용을 가져옵니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "레포지토리 이름"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "create_portfolio_page_from_markdown",
        "description": "마크다운을 Notion 포트폴리오 페이지로 생성합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "페이지 제목"
                },
                "markdown_content": {
                    "type": "string",
                    "description": "마크다운 텍스트"
                }
            },
            "required": ["title", "markdown_content"]
        }
    },
    {
        "name": "find_portfolio_page_by_title",
        "description": "부모 페이지의 자식 페이지에서 제목으로 찾습니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "페이지 제목"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "delete_portfolio_page_by_id",
        "description": "페이지 ID로 포트폴리오 페이지를 삭제합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "string",
                    "description": "페이지 ID"
                }
            },
            "required": ["page_id"]
        }
    },
    {
        "name": "delete_portfolio_page",
        "description": "제목으로 포트폴리오 페이지를 찾아 삭제합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "페이지 제목"
                }
            },
            "required": ["title"]
        }
    }    
]

# Tool 실행 매핑
tool_functions = {
    "list_repositories": list_repositories,
    "get_repository_info": get_repository_info,
    "get_readme_content": get_readme_content,
    "create_portfolio_page_from_markdown": create_portfolio_page_from_markdown,
    "find_portfolio_page_by_title": find_portfolio_page_by_title,
    "delete_portfolio_page_by_id": delete_portfolio_page_by_id,
    "delete_portfolio_page": delete_portfolio_page
}

# 핵심 로직 함수
def call_claude_with_tools(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    
    for iteration in range(10):
        # 1. Claude 호출 (업데이트된 messages 사용)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=mcp_tools_schema,
            messages=messages  # ✅ 여기!
        )
        
        # 2. Tool 사용 여부 확인
        if response.stop_reason == "tool_use":
            # Assistant 응답 추가 (먼저!)
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Tool 실행 및 결과 수집
            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_func = tool_functions[content.name]
                    result = tool_func(**content.input)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": str(result)
                    })
            
            # Tool Result 추가
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            # 루프 계속 (다음 iteration에서 재호출)
            
        else:
            # 3. 최종 답변
            return {
                "response": response.content[0].text,
                "success": True
            }
    
    # 4. 최대 반복 초과
    return {
        "error": "최대 반복 횟수 초과",
        "success": False
    }