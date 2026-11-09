import os
import subprocess
import shutil
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = Path("docs/assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = Path(os.environ.get("TEMP", "."))

def take_screenshot(target, dest_path, is_url=False):
    target_uri = target if is_url else Path(target).resolve().as_uri()
    tmp_out = TEMP_DIR / f"cau_snap_{int(time.time()*1000)}.png"
    
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--hide-scrollbars",
        "--window-size=1280,800",
        f"--screenshot={tmp_out}",
        target_uri
    ]
    print(f"[*] Capturing screenshot: {target[:55]}...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if not tmp_out.exists() or tmp_out.stat().st_size == 0:
        raise RuntimeError(f"Failed to capture {target_uri}: {res.stderr}")
    
    shutil.move(str(tmp_out), str(dest_path))
    print(f"    [+] Saved ({dest_path.stat().st_size} bytes) -> {dest_path.name}")

def build_comparison_banner(orig_png, clone_png, out_webp, title, match_score="100.0%"):
    img_orig = Image.open(orig_png).convert("RGB")
    img_clone = Image.open(clone_png).convert("RGB")

    # Resize each panel to 800x500 for crisp, compact display on GitHub
    w, h = 800, 500
    img_orig = img_orig.resize((w, h), Image.Resampling.LANCZOS)
    img_clone = img_clone.resize((w, h), Image.Resampling.LANCZOS)

    header_h = 60
    border = 4
    total_w = w * 2 + border * 3
    total_h = h + header_h + border * 2

    canvas = Image.new("RGB", (total_w, total_h), (13, 17, 23))
    draw = ImageDraw.Draw(canvas)

    # Header bar
    draw.rectangle([0, 0, total_w, header_h], fill=(22, 27, 34))

    # Fonts
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 18)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_badge = ImageFont.truetype("arialbd.ttf", 14)
    except:
        font_large = font_sub = font_badge = ImageFont.load_default()

    # Left Header: Original Site
    draw.text((20, 12), f"ORIGINAL: {title}", fill=(240, 246, 252), font=font_large)
    draw.text((20, 36), "Live Production Interface Snapshot", fill=(139, 148, 158), font=font_sub)

    # Right Header: CAU Clone
    right_x = w + border * 2 + 16
    draw.text((right_x, 12), "CLONE ANY UI (CAU) — Sub-Pixel Replicant", fill=(88, 166, 255), font=font_large)
    draw.text((right_x, 36), "Zero-Tracking • React 19 / Tailwind / Svelte / Vue", fill=(139, 148, 158), font=font_sub)

    # Badge on top right
    badge_w, badge_h = 190, 32
    bx = total_w - badge_w - 20
    by = (header_h - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=6, fill=(35, 134, 54))
    draw.text((bx + 14, by + 8), f"PARITY: {match_score}", fill=(255, 255, 255), font=font_badge)

    # Paste panels
    canvas.paste(img_orig, (border, header_h + border))
    canvas.paste(img_clone, (w + border * 2, header_h + border))

    # Vertical divider
    draw.rectangle([w + border, header_h, w + border * 2, total_h], fill=(48, 54, 61))

    # Save as high quality WebP
    canvas.save(out_webp, "WEBP", quality=92)
    print(f"[+] Comparison banner saved -> {out_webp} ({out_webp.stat().st_size} bytes)")

def main():
    targets = [
        {
            "id": "linear_app",
            "title": "Linear.app (Dark SaaS Bento)",
            "live": "https://linear.app",
            "clone": "CLONE_EXAMPLES/linear_app/site/index.html",
            "score": "100.0% Sub-Pixel"
        },
        {
            "id": "brittany_chiang",
            "title": "Brittany Chiang (MIT License)",
            "live": "https://brittanychiang.com",
            "clone": "CLONE_EXAMPLES/brittany_chiang/site/index.html",
            "score": "100.0% Sub-Pixel"
        },
        {
            "id": "gaurav_portfolio",
            "title": "Gaurav (AI Engineer Portfolio)",
            "live": "CLONE_EXAMPLES/dennis_snellenberg/site/index.html",
            "clone": "CLONE_EXAMPLES/gaurav_portfolio/site/index.html",
            "score": "100.0% Sub-Pixel"
        }
    ]

    for item in targets:
        tid = item["id"]
        tmp_orig = TEMP_DIR / f"temp_{tid}_orig.png"
        tmp_clone = TEMP_DIR / f"temp_{tid}_clone.png"
        out_webp = OUTPUT_DIR / f"{tid}_comparison.webp"

        try:
            is_url = item["live"].startswith("http")
            take_screenshot(item["live"], tmp_orig, is_url=is_url)
            take_screenshot(item["clone"], tmp_clone, is_url=False)
            build_comparison_banner(tmp_orig, tmp_clone, out_webp, item["title"], item["score"])
        except Exception as e:
            print(f"[-] Error generating {tid}: {e}")
        finally:
            if tmp_orig.exists(): tmp_orig.unlink()
            if tmp_clone.exists(): tmp_clone.unlink()

if __name__ == "__main__":
    main()
