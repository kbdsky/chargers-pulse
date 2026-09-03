# 📱 ChargersPulse Android App 프로젝트

이 폴더는 Android Studio에서 직접 열어 `.apk` 파일로 빌드할 수 있는 안드로이드 앱 소스코드입니다.

---

## 🚀 Android Studio로 APK 빌드하는 방법

1. **Android Studio 실행**:
   - `File > Open`을 누르고 `c:\Users\master\Documents\antigravity\cool-rutherford\android_project` 폴더를 선택합니다.
2. **서버 주소 설정**:
   - `app/src/main/java/com/chargerspulse/app/MainActivity.kt` 파일을 엽니다.
   - `defaultServerUrl` 변수에 본인 PC의 IP 주소(예: `http://192.168.0.x:8000`) 또는 배포된 도메인을 입력합니다.
3. **APK 빌드**:
   - 상단 메뉴에서 `Build > Build Bundle(s) / APK(s) > Build APK(s)` 클릭.
   - 빌드가 완료되면 생성된 `app-debug.apk` 파일을 스마트폰으로 복사하여 설치합니다.

---

## ⚡ 더 간편한 추천 방식: PWA 앱 (설치 불필요)
Android Studio 빌드 과정 없이, PC에서 `python -m newspulse.mobile_launcher`를 실행하고 스마트폰 카메라로 QR 코드를 스캔한 뒤 **[홈 화면에 앱 추가]** 만 누르면 1초 만에 스마트폰 앱으로 즉시 설치됩니다!
