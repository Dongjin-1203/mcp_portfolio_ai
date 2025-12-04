from app.mcp.server import mcp
from github import Github
import logging

from app.config import Config

# 토큰 인증
config = Config()

def _get_github_client() -> Github:
    """GitHub 클라이언트를 안전하게 가져옵니다"""
    token = config.GITHUB_TOKEN
    if not token:
        raise ValueError("GITHUB_TOKEN이 설정되지 않았습니다")
    return Github(token)

# Tool 1: 레포 목록
@mcp.tool()
def list_repositories() -> list:
    """사용자의 GitHub 레포지토리 목록을 가져옵니다"""
    try:
        g = _get_github_client()
        repos = []
        for repo in g.get_user().get_repos():
            repos.append({
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description or "설명 없음",
                "url": repo.html_url,
                "language": repo.language or "Unknown"
            })
        return repos
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"레포 목록 조회 실패: {e}")
        return []

# Tool 2: 레포 상세 정보
@mcp.tool()
def get_repository_info(repo_name: str) -> dict:
    """특정 레포지토리의 상세 정보를 가져옵니다
    
    Args:
        repo_name: 레포지토리 이름 (예: "username/repo")
    
    Returns:
        레포 정보 딕셔너리
    """
    try:
        g = _get_github_client()
        repo_dict = g.get_repo(repo_name)
        return {
            "name": repo_dict.name,
            "full_name": repo_dict.full_name,
            "description": repo_dict.description,
            "url": repo_dict.html_url,
            "stars": repo_dict.stargazers_count,
            "forks": repo_dict.forks_count,
            "language": repo_dict.language,
        }
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"레포 정보 조회 실패: {e}")
        return {
            "error": str(e),
            "repo_name": repo_name
        }

# Tool 3: README 가져오기
@mcp.tool()
def get_readme_content(repo_name: str) -> str:
    """README.md 내용을 가져옵니다
    
    Args:
        repo_name: 레포지토리 이름
        
    Returns:
        README Markdown 텍스트
    """
    g = _get_github_client()
    # GitHub Repository README 가져오기
    try:
        repository = g.get_repo(repo_name)
        # PyGithub의 get_contents 메서드를 사용하여 README.md 파일을 가져옵니다.
        contents = repository.get_contents("README.md")
        
        # content 속성은 base64 인코딩된 문자열입니다.
        decoded_content = contents.decoded_content.decode('utf-8')
        return decoded_content

        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"README 가져오기 실패: {e}")
        return None