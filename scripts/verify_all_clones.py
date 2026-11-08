#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Universal Test & Verification Runner.

Audits all reference clones in CLONE_EXAMPLES/ across:
1. File & directory structure
2. Asset integrity (images, fonts, stylesheets, scripts)
3. JavaScript / Data syntax verification (node --check & json.loads)
4. Sub-Pixel Micro-Fidelity Audit (10-point 0.5px precision checks)
5. Multi-framework output validation (React, Vue, Svelte, HTML)

Usage:
  python scripts/verify_all_clones.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
CLONES_DIR = ROOT_DIR / "CLONE_EXAMPLES"


def check_clone(name: str, path: Path) -> dict:
    result = {
        "name": name,
        "path": str(path),
        "html_count": len(list(path.rglob("*.html"))),
        "has_site": (path / "site").exists(),
        "has_tokens": (path / "tokens" / "tokens.json").exists(),
        "has_react": (path / "components" / "react").exists(),
        "has_vue": (path / "components" / "vue").exists(),
        "has_svelte": (path / "components" / "svelte").exists(),
        "has_html": (path / "components" / "html").exists(),
        "self_heal_pass": False,
        "subpixel_score": "0%",
        "subpixel_pass": False,
    }

    # Run self-heal
    res_heal = subprocess.run(
        [sys.executable, str(ROOT_DIR / "scripts" / "self_heal_and_verify.py"), "--target-dir", str(path)],
        capture_output=True,
        text=True,
    )
    if res_heal.returncode == 0 and "Syntax: PASS" in res_heal.stdout:
        result["self_heal_pass"] = True

    # Run subpixel audit
    res_audit = subprocess.run(
        [sys.executable, str(ROOT_DIR / "scripts" / "audit_subpixel_fidelity.py"), "--target", str(path)],
        capture_output=True,
        text=True,
    )
    for line in res_audit.stdout.splitlines():
        if "Score:" in line:
            result["subpixel_score"] = line.split("Score:")[-1].strip().split()[0]
            if "100" in result["subpixel_score"]:
                result["subpixel_pass"] = True

    return result


def main() -> None:
    print("\n" + "=" * 78)
    print("🔬 CLONE ANY UI (CAU) — MASTER REPOSITORY FIDELITY BENCHMARK")
    print(f"📁 Target Directory: {CLONES_DIR}")
    print("=" * 78)

    if not CLONES_DIR.exists():
        print("[-] CLONE_EXAMPLES directory not found.")
        sys.exit(1)

    projects = sorted([d for d in CLONES_DIR.iterdir() if d.is_dir()])
    results = []

    for p in projects:
        print(f"  ▶ Benchmarking [{p.name}]...", end="", flush=True)
        r = check_clone(p.name, p)
        results.append(r)
        print(" DONE")

    print("\n" + "-" * 78)
    print(f"{'PROJECT':<22} | {'PAGES':<6} | {'FRAMEWORKS':<12} | {'SELF-HEAL':<10} | {'SUB-PIXEL':<10}")
    print("-" * 78)

    all_passed = True
    for r in results:
        fmwks = []
        if r["has_react"]: fmwks.append("React")
        if r["has_vue"]: fmwks.append("Vue")
        if r["has_svelte"]: fmwks.append("Svelte")
        if r["has_html"]: fmwks.append("HTML")
        fmwk_str = f"{len(fmwks)}/4" if fmwks else "None"

        heal_str = "✓ PASS" if r["self_heal_pass"] else "✗ FAIL"
        subpixel_str = f"✓ {r['subpixel_score']}" if r["subpixel_pass"] else f"✗ {r['subpixel_score']}"

        if not r["self_heal_pass"] or not r["subpixel_pass"]:
            all_passed = False

        print(f"{r['name']:<22} | {r['html_count']:<6} | {fmwk_str:<12} | {heal_str:<10} | {subpixel_str:<10}")

    print("-" * 78)
    if all_passed:
        print("🎉 ALL REFERENCE CLONES ACHIEVED 100% PASSING STATUS!\n")
    else:
        print("⚠️ SOME CHECKS REQUIRE ATTENTION. Inspect above output.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
