import os
import re
import sys

print("[*] Starting fast targeted security audit...")
sys.stdout.flush()

SECRET_PATTERNS = [
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'), 'GitHub PAT'),
    (re.compile(r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}'), 'Fine-grained GitHub PAT'),
    (re.compile(r'sk-[a-zA-Z0-9]{20,}'), 'OpenAI/Anthropic Key'),
    (re.compile(r'AKIA[0-9A-Z]{16}'), 'AWS Key'),
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'), 'Private RSA/SSH Key'),
    (re.compile(r'(?i)(?:password|passwd|secret_key|private_key)\s*[:=]\s*["\']([^"\']{8,})["\']'), 'Hardcoded password/key'),
]

# High priority dirs
TARGET_DIRS = ['.github', 'scripts', 'studio', 'tests', 'templates', 'examples']
TARGET_FILES = ['clone_any_ui.py', 'run_studio.py', 'bookmarklet.js', 'install.sh', 'install.bat', 'README.md', 'SKILL.md', 'pyproject.toml']

findings = []
scanned = 0

for tf in TARGET_FILES:
    if os.path.exists(tf):
        scanned += 1
        with open(tf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for rx, name in SECRET_PATTERNS:
                for m in rx.finditer(content):
                    findings.append((tf, name, m.group(0)[:60]))

for td in TARGET_DIRS:
    if not os.path.exists(td):
        continue
    for root, dirs, files in os.walk(td):
        for f in files:
            if f.endswith(('.png', '.jpg', '.webp', '.mp4', '.woff2', '.woff', '.ttf', '.svg', '.bin')):
                continue
            fp = os.path.join(root, f)
            if os.path.getsize(fp) > 1024 * 1024: # skip >1MB
                continue
            scanned += 1
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                    for rx, name in SECRET_PATTERNS:
                        for m in rx.finditer(content):
                            findings.append((fp, name, m.group(0)[:60]))
            except Exception:
                pass

print(f"[+] Total files checked: {scanned}")
print(f"[+] Secrets found: {len(findings)}")
for fp, name, snippet in findings:
    print(f"    [{name}] {fp} -> {snippet}")
sys.stdout.flush()
