# GitHub 셋업 가이드 (상업용)

## 계정
- 상업용 Gmail(moducompanyofficial@gmail.com)로 **새 GitHub 계정** 생성.
- 사용자명: 개인 이름 대신 **브랜드형**(제품/스튜디오명). 예: `acme-labs`.
- 제품군이 커지면 나중에 **Organization**으로 승격(레포 이전 무료).

## 로컬 git 설정 (이 폴더에서)
```bash
git init
git config user.name "Modu Company"
git config user.email "moducompanyofficial@gmail.com"   # 또는 GitHub noreply 주소(이메일 비공개)
git add .
git commit -m "feat: content repurposer (free) + MCP server"
git branch -M main
git remote add origin https://github.com/<브랜드사용자명>/content-repurposer.git
git push -u origin main
```

## 공개 범위 (중요)
- ✅ 공개: 이 폴더(무료 도구 `repurpose.py`, `mcp_server.py`, README, LICENSE, 예시)
- ❌ 비공개: 유료 버전 `repurpose_pro.py`는 **올리지 말 것**(별도 private 레포 또는 Gumroad만).

## 발견성(스타·리드)
- 리포 About에 한 줄 + 토픽 태그: `ai`, `content-marketing`, `mcp`, `automation`.
- README 상단에 데모 GIF/스크린샷, 하단에 PRO(Gumroad) CTA.
- README의 `[GUMROAD_LINK]`, `Modu Company` 치환.
