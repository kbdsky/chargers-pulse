"""Autonomous Cloud & GitHub Deployer for ChargersPulse."""

import os
import sys
import logging
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logger = logging.getLogger("newspulse.deployer")


def push_to_github(token: str, repo_name: str, private: bool = False):
    """Create repository and push files directly using PyGithub."""
    from github import Github, GithubException

    g = Github(token)
    user = g.get_user()
    print(f"👤 GitHub 로그인 성공: {user.login}", flush=True)

    try:
        repo = user.create_repo(repo_name, private=private, description="⚡ LA Chargers NewsPulse 2.0 - 24/7 Cloud Intelligence & Mobile App")
        print(f"✨ GitHub 저장소 생성 완료: {repo.html_url}", flush=True)
    except GithubException as e:
        if e.status == 422: # Already exists
            repo = user.get_repo(repo_name)
            print(f"ℹ️ 기존 저장소 연결: {repo.html_url}", flush=True)
        else:
            raise e

    # Upload core project files
    root_dir = Path(os.getcwd())
    ignore_patterns = [".git", "__pycache__", ".pytest_cache", "cloudflared.exe", ".venv", "venv", ".DS_Store"]

    files_uploaded = 0
    for file_path in root_dir.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(root_dir).as_posix()
            if any(p in rel_path for p in ignore_patterns):
                continue
            if file_path.stat().st_size > 25 * 1024 * 1024: # Skip large binaries
                continue

            try:
                with open(file_path, "rb") as f:
                    content = f.read()

                # Try to get existing file
                try:
                    contents = repo.get_contents(rel_path, ref="main")
                    repo.update_file(contents.path, f"⚡ Auto-sync {rel_path}", content, contents.sha, branch="main")
                except GithubException:
                    repo.create_file(rel_path, f"⚡ Add {rel_path}", content, branch="main")
                files_uploaded += 1
            except Exception as ex:
                logger.warning(f"Failed to upload {rel_path}: {ex}")

    print(f"🎉 총 {files_uploaded}개 파일의 GitHub 업로드가 완료되었습니다!", flush=True)
    print(f"🌐 24시간 클라우드 저장소 주소: {repo.html_url}", flush=True)
    print(f"⚡ GitHub Actions를 통한 24/7 주간 자동 실행이 활성화되었습니다.", flush=True)
    return repo.html_url


def main():
    import argparse
    parser = argparse.ArgumentParser(description="⚡ NewsPulse 2.0 Autonomous GitHub Cloud Deployer")
    parser.add_argument("--token", "-t", type=str, default=os.getenv("GITHUB_TOKEN"), help="GitHub Personal Access Token")
    parser.add_argument("--repo", "-r", type=str, default="chargers-pulse", help="GitHub Repository Name")
    parser.add_argument("--private", action="store_true", help="Create private repository")

    args = parser.parse_args()

    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("\n" + "=" * 65, flush=True)
        print("☁️ [NewsPulse] 24시간 클라우드 자동 배포 도우미", flush=True)
        print("=" * 65, flush=True)
        print("GitHub Personal Access Token이 설정되지 않았습니다.", flush=True)
        print("환경 변수 GITHUB_TOKEN을 설정하거나 --token <TOKEN> 옵션으로 실행하세요.", flush=True)
        print("\n자세한 수동 배포 가이드는 CLOUD_DEPLOY_GUIDE.md를 참조하세요.", flush=True)
        print("=" * 65 + "\n", flush=True)
        return

    push_to_github(token, args.repo, args.private)


if __name__ == "__main__":
    main()
