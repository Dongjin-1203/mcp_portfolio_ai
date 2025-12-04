from app.mcp import mcp
from app.mcp.tools.github_tools import (
    list_repositories,
    get_repository_info,
    get_readme_content
)

# 테스트 1: MCP 서버 확인
print("MCP 서버 이름:", mcp.name)

# 테스트 2: 레포 목록
print("\n=== 레포 목록 ===")
repos = list_repositories()
print(f"총 {len(repos)}개 레포")
if repos:
    print(repos)

# 테스트 3: 특정 레포 정보
print("\n=== 레포 정보 ===")
info = get_repository_info("<실제 깃허브 repo 이름 입력>")
print(info)

# 테스트 4: README
print("\n=== README ===")
readme = get_readme_content("<실제 깃허브 repo 이름 입력>")
print(readme[:200] if readme else "README 없음")
