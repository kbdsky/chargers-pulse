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
    from github import Github, GithubException, Auth

    auth = Auth.Token(token)
    g = Github(auth=auth)
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

    def _sync_file(repo_obj, branch: str, file_path_rel: str, file_bytes: bytes, commit_msg: str):
        """Helper to create or update file without sha conflicts, skipping identical files."""
        try:
            contents = repo_obj.get_contents(file_path_rel, ref=branch)
            # Skip if identical content
            if contents.decoded_content == file_bytes:
                return True
            try:
                repo_obj.update_file(contents.path, commit_msg, file_bytes, contents.sha, branch=branch)
                return True
            except GithubException as ge_up:
                if ge_up.status in (409, 422):
                    # Refetch freshest SHA and retry once
                    fresh = repo_obj.get_contents(file_path_rel, ref=branch)
                    if fresh.decoded_content != file_bytes:
                        repo_obj.update_file(fresh.path, commit_msg, file_bytes, fresh.sha, branch=branch)
                    return True
                raise ge_up
        except GithubException as ge:
            if ge.status == 404:
                repo_obj.create_file(file_path_rel, commit_msg, file_bytes, branch=branch)
                return True
            else:
                # Retry getting content in case of race condition
                try:
                    fresh = repo_obj.get_contents(file_path_rel, ref=branch)
                    if fresh.decoded_content != file_bytes:
                        repo_obj.update_file(fresh.path, commit_msg, file_bytes, fresh.sha, branch=branch)
                    return True
                except Exception:
                    raise ge
        return False

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

                if _sync_file(repo, "main", rel_path, content, f"⚡ Auto-sync {rel_path}"):
                    files_uploaded += 1
            except Exception as ex:
                logger.warning(f"Failed to upload {rel_path}: {ex}")

    print(f"🎉 총 {files_uploaded}개 파일의 GitHub (main 브랜치) 동기화가 완료되었습니다!", flush=True)

    # 2. Sync gh-pages branch for GitHub Pages PWA hosting
    print("🚀 GitHub Pages (gh-pages 브랜치) 웹 앱 배포 중...", flush=True)
    try:
        # Check if gh-pages branch exists
        try:
            repo.get_branch("gh-pages")
        except GithubException:
            # Create gh-pages branch from main
            main_branch = repo.get_branch("main")
            repo.create_git_ref(ref="refs/heads/gh-pages", sha=main_branch.commit.sha)

        gh_pages_files = {
            "index.html": root_dir / "newspulse" / "mobile" / "static" / "index.html",
            "manifest.json": root_dir / "newspulse" / "mobile" / "static" / "manifest.json",
            "service-worker.js": root_dir / "newspulse" / "mobile" / "static" / "service-worker.js",
            "latest_mobile_data.json": root_dir / "reports" / "latest_mobile_data.json",
        }

        # Also add icon files
        icons_dir = root_dir / "newspulse" / "mobile" / "static" / "icons"
        if icons_dir.exists():
            for icon_file in icons_dir.glob("*"):
                if icon_file.is_file():
                    gh_pages_files[f"icons/{icon_file.name}"] = icon_file

        gh_synced = 0
        for target_path, src_path in gh_pages_files.items():
            if src_path.exists():
                with open(src_path, "rb") as f:
                    content = f.read()
                try:
                    if _sync_file(repo, "gh-pages", target_path, content, f"⚡ Deploy {target_path}"):
                        gh_synced += 1
                except Exception as ex:
                    logger.warning(f"Failed to sync {target_path} to gh-pages: {ex}")

        print(f"✨ GitHub Pages (gh-pages) 배포 완료! ({gh_synced}개 파일 동기화)", flush=True)
        print(f"📱 실시간 모바일 PWA 웹사이트: https://{user.login.lower()}.github.io/{repo_name}/", flush=True)
    except Exception as e:
        logger.warning(f"gh-pages deployment note: {e}")

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
