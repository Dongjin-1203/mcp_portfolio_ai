from fastapi import FastAPI
from app.mcp.server import mcp  # MCP 서버 인스턴스 가져오기

app = FastAPI()

@app.post("/api/portfolio/create")
async def create_portfolio():
    # 여기서 Claude API 호출하면서 MCP tools 사용
    pass