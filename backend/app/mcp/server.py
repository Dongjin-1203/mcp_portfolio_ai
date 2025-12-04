from mcp.server.fastmcp import FastMCP

# MCP 서버 인스턴스 생성 (FastAPI 내부에서 사용)
mcp = FastMCP("Portfolio MCP Server")

# Constants
NWS_API_BASE = "https://api.portfolio.gov"
USER_AGENT = "manage-portfolio-app/1.0"