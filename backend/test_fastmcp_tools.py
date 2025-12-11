from app.mcp import mcp

print("=== MCP 서버 정보 ===")
print(f"서버 이름: {mcp.name}")
print()

# FastMCP 내부 구조 확인
print("=== FastMCP 속성 확인 ===")
print(f"사용 가능한 속성: {dir(mcp)}")
print()

# Tools 정보 가져오기 (여러 방법 시도)
print("=== Tools 정보 ===")

# 방법 1
if hasattr(mcp, '_tools'):
    print("mcp._tools 존재:")
    print(mcp._tools)
    print()

# 방법 2
if hasattr(mcp, 'list_tools'):
    print("mcp.list_tools() 존재:")
    tools = mcp.list_tools()
    print(tools)
    print()

# 방법 3
if hasattr(mcp, 'get_tools'):
    print("mcp.get_tools() 존재:")
    tools = mcp.get_tools()
    print(tools)
    print()

# 방법 4 - FastMCP 서버 스키마
if hasattr(mcp, 'to_json') or hasattr(mcp, 'schema'):
    print("스키마 확인:")
    try:
        print(mcp.schema())
    except:
        try:
            print(mcp.to_json())
        except:
            print("스키마 메서드 없음")