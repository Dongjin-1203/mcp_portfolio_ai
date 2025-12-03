# MCP 개발자 포트폴리오 자동 관리 AI
---

## 프로젝트 디렉토리 구조

```
portfolio-ai/
├── backend/                      # FastAPI 백엔드 + MCP 서버
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── config.py            # 환경 변수, 설정
│   │   ├── dependencies.py      # 의존성 주입
│   │   │
│   │   ├── api/                 # API 라우터
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 인증 (GitHub, Notion OAuth)
│   │   │   ├── portfolio.py     # 포트폴리오 생성 API
│   │   │   ├── chat.py          # 채팅/수정 요청 API
│   │   │   └── webhooks.py      # GitHub/Notion 웹훅
│   │   │
│   │   ├── mcp/                 # MCP 서버 구현
│   │   │   ├── __init__.py
│   │   │   ├── server.py        # MCP 서버 메인
│   │   │   ├── tools/           # MCP Tools
│   │   │   │   ├── github_tools.py
│   │   │   │   ├── notion_tools.py
│   │   │   │   └── template_tools.py
│   │   │   └── prompts/         # MCP Prompts
│   │   │       └── portfolio_prompts.py
│   │   │
│   │   ├── services/            # 비즈니스 로직
│   │   │   ├── github_service.py
│   │   │   ├── notion_service.py
│   │   │   ├── claude_service.py
│   │   │   └── portfolio_service.py
│   │   │
│   │   ├── models/              # Pydantic 모델
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   └── chat.py
│   │   │
│   │   ├── db/                  # 데이터베이스
│   │   │   ├── database.py      # SQLAlchemy 설정
│   │   │   ├── models.py        # DB 모델
│   │   │   └── crud.py          # CRUD 작업
│   │   │
│   │   └── utils/               # 유틸리티
│   │       ├── auth.py          # JWT, 암호화
│   │       ├── markdown_parser.py
│   │       └── cache.py         # Redis 캐싱
│   │
│   ├── tests/                   # 테스트 코드
│   │   ├── test_api/
│   │   ├── test_mcp/
│   │   └── test_services/
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                     # Next.js 웹 프론트엔드
│   ├── src/
│   │   ├── app/                 # Next.js 14 App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx         # 홈페이지
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx     # 대시보드
│   │   │   ├── create/
│   │   │   │   └── page.tsx     # 포트폴리오 생성
│   │   │   └── api/             # API 라우트
│   │   │       └── auth/[...nextauth]/route.ts
│   │   │
│   │   ├── components/          # React 컴포넌트
│   │   │   ├── ui/              # shadcn/ui 컴포넌트
│   │   │   ├── auth/
│   │   │   │   └── LoginButton.tsx
│   │   │   ├── portfolio/
│   │   │   │   ├── RepoSelector.tsx
│   │   │   │   ├── DraftEditor.tsx
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   └── NotionPreview.tsx
│   │   │   └── layout/
│   │   │       ├── Header.tsx
│   │   │       └── Sidebar.tsx
│   │   │
│   │   ├── lib/                 # 유틸리티
│   │   │   ├── api.ts           # API 클라이언트
│   │   │   ├── auth.ts          # NextAuth 설정
│   │   │   └── utils.ts
│   │   │
│   │   ├── hooks/               # Custom Hooks
│   │   │   ├── usePortfolio.ts
│   │   │   ├── useChat.ts
│   │   │   └── useWebSocket.ts
│   │   │
│   │   ├── store/               # 상태 관리 (Zustand)
│   │   │   ├── portfolioStore.ts
│   │   │   └── userStore.ts
│   │   │
│   │   └── types/               # TypeScript 타입
│   │       ├── portfolio.ts
│   │       └── api.ts
│   │
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── shared/                       # 공유 코드
│   ├── types/                   # 공통 타입 정의
│   │   └── index.ts
│   └── constants/
│       └── index.ts
│
├── docs/                         # 문서
│   ├── API.md
│   ├── SETUP.md
│   └── ARCHITECTURE.md
│
├── .github/
│   └── workflows/               # CI/CD
│       ├── backend-deploy.yml
│       └── frontend-deploy.yml
│
├── docker-compose.yml           # 로컬 개발 환경
├── .gitignore
└── README.md
```