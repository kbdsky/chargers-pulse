# ☁️ 24시간 PC 없이 스마트폰 단독 실행: 무료 클라우드 배포 가이드

PC를 켜둘 필요 없이, **스마트폰 단독으로 24시간 365일 언제든 최신 뉴스를 긁어오고 실행**할 수 있도록 **100% 무료 클라우드(Render.com)** 에 배포하는 방법입니다.

---

## 🚀 배포 순서 (초간단 3단계)

### 1단계: GitHub에 코드 올리기
1. [GitHub.com](https://github.com)에 로그인 후 새 Repository(저장소)를 생성합니다 (예: `chargers-pulse`).
2. 현재 프로젝트 폴더의 코드를 해당 GitHub 저장소에 Push(업로드)합니다.

---

### 2단계: Render.com에서 1클릭 무료 배포 (비용: 0원)
1. [Render.com](https://render.com)에 접속하여 무료 회원가입(GitHub 계정으로 1초 로그인)을 합니다.
2. 대시보드 우측 상단 **[New +]** 버튼을 누르고 **[Web Service]** 를 선택합니다.
3. 1단계에서 생성한 GitHub 저장소(`chargers-pulse`)를 선택하고 **[Connect]** 를 누릅니다.
4. 아래 설정값을 확인하고 **[Create Web Service]** 를 클릭합니다:
   - **Name**: `chargers-pulse` (원하는 이름)
   - **Region**: `Singapore` 또는 `Ohio`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn newspulse.mobile.server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free ($0/month)**
5. 약 1~2분 후 배포가 완료되면 상단에 **영구 전용 HTTPS 주소**가 발급됩니다:
   - 예: `https://chargers-pulse.onrender.com`

---

### 3단계: 스마트폰에서 영구 앱으로 설치
1. 스마트폰(Android) 브라우저를 열고 위에서 발급된 주소(`https://chargers-pulse.onrender.com`)로 접속합니다.
2. 화면 상단의 **[설치]** 버튼 또는 브라우저 메뉴의 **[홈 화면에 앱 추가]** 를 누릅니다.
3. **완료!** 🎉 
   - 이제 **내 컴퓨터가 꺼져 있거나 외출 중이어도**, 스마트폰 바탕화면의 앱 아이콘을 터치하면 24시간 언제든 최신 LA Chargers 뉴스를 실시간으로 긁어와 브리핑해 줍니다.
