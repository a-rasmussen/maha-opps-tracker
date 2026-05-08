#!/usr/bin/env python3
"""
push_to_github.py — Push files to a GitHub repo via the Contents API.

Modeled after the SAM Target States project's push_to_github.py.
Resolves the GitHub MCP write-tool reliability issue (returns "Bad credentials"
or "Resource not accessible by personal access token" depending on variant).

Usage:
    python3 push_to_github.py \
        --owner a-rasmussen --repo maha-opps-tracker \
        --source-dir "/path/to/MAHA Opps Tracker/MAHA Mortality Tracker" \
        --repo-prefix mortality-tracker \
        --files Project_Instructions.md Research_Protocol.md \
        --message "Initial mortality tracker scaffolding"

PAT lookup order (first existing wins):
    1. --pat-file argument
    2. <source-dir>/.gh_pat
    3. <source-dir>/../.gh_pat   (parent of source-dir)
    4. /sessions/.../mnt/MAHA Opps Tracker/.gh_pat   (sandbox)
    5. /Users/jwe973/Documents/Claude/Projects/MAHA Opps Tracker/.gh_pat
    6. ~/.gh_pat

PAT requirements (fine-grained):
    Resource owner: matches --owner
    Repository access: --repo (or all)
    Permissions:
      Contents: Read and write   (REQUIRED — expand the section to find)
      Metadata: Read-only (auto)
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def find_pat(pat_file_arg, source_dir):
    """Find a GitHub PAT, trying provided arg then default locations."""
    candidates = []
    if pat_file_arg:
        candidates.append(Path(pat_file_arg))
    sd = Path(source_dir).resolve()
    candidates.append(sd / ".gh_pat")
    candidates.append(sd.parent / ".gh_pat")
    # Hardcoded fallbacks for common locations
    candidates.append(Path("/sessions/youthful-modest-hypatia/mnt/MAHA Opps Tracker/.gh_pat"))
    candidates.append(Path("/Users/jwe973/Documents/Claude/Projects/MAHA Opps Tracker/.gh_pat"))
    candidates.append(Path.home() / ".gh_pat")

    seen = set()
    for candidate in candidates:
        c = candidate.resolve() if candidate.exists() else candidate
        if c in seen:
            continue
        seen.add(c)
        if candidate.is_file():
            pat = candidate.read_text().strip()
            if pat:
                return pat, candidate

    tried = "\n  ".join(str(c) for c in candidates)
    raise SystemExit(f"ERROR: No PAT found. Tried:\n  {tried}")


def github_request(method, url, token, body=None):
    """Make a GitHub API request."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "claude-maha-push",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8")
            return resp.status, json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8") if e.fp else ""
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, ValueError):
            data = {"raw": payload}
        return e.code, data


def get_existing_sha(owner, repo, path, branch, token):
    """Return the SHA of an existing file, or None if not present."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    status, data = github_request("GET", url, token)
    if status == 200:
        return data.get("sha")
    if status == 404:
        return None
    raise RuntimeError(
        f"Failed to GET {path}: HTTP {status}: {data.get('message', data)}"
    )


def push_file(owner, repo, repo_path, content_bytes, message, branch, token):
    """Push a single file. Creates or updates as needed."""
    sha = get_existing_sha(owner, repo, repo_path, branch, token)

    body = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode("ascii"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{repo_path}"
    status, data = github_request("PUT", url, token, body)

    if status in (200, 201):
        commit_sha = data.get("commit", {}).get("sha", "")[:7]
        action = "Updated" if sha else "Created"
        return True, f"  [OK] {action:7s} {repo_path} ({commit_sha})"

    msg = data.get("message", str(data))
    return False, f"  [FAIL] {repo_path}: HTTP {status}: {msg}"


def main():
    parser = argparse.ArgumentParser(
        description="Push files to GitHub via Contents API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--owner", required=True, help="Repo owner (user or org)")
    parser.add_argument("--repo", required=True, help="Repo name")
    parser.add_argument("--branch", default="main", help="Branch (default: main)")
    parser.add_argument("--pat-file", help="Override PAT file path")
    parser.add_argument("--source-dir", required=True,
                        help="Local directory containing files to push")
    parser.add_argument("--repo-prefix", default="",
                        help="Subdirectory prefix in the repo (e.g., 'mortality-tracker')")
    parser.add_argument("--files", nargs="+", required=True,
                        help="Files to push (paths relative to --source-dir)")
    parser.add_argument("--message", required=True, help="Commit message")
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.is_dir():
        raise SystemExit(f"ERROR: source-dir not found: {source_dir}")

    token, pat_path = find_pat(args.pat_file, args.source_dir)
    print(f"PAT loaded from: {pat_path}")
    print(f"Repo: {args.owner}/{args.repo} (branch: {args.branch})")
    if args.repo_prefix:
        print(f"Prefix: {args.repo_prefix.strip('/')}/")
    print(f"Message: {args.message}")
    print()

    successes = 0
    failures = 0

    for file_arg in args.files:
        local_path = source_dir / file_arg
        if not local_path.is_file():
            print(f"  [FAIL] File not found: {local_path}")
            failures += 1
            continue

        repo_path = file_arg
        if args.repo_prefix:
            repo_path = f"{args.repo_prefix.strip('/')}/{file_arg}"

        content = local_path.read_bytes()
        ok, msg = push_file(
            args.owner, args.repo, repo_path, content,
            args.message, args.branch, token,
        )
        print(msg)
        if ok:
            successes += 1
        else:
            failures += 1

    print()
    print(f"Result: {successes} pushed, {failures} failed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
