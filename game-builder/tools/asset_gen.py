#!/usr/bin/env python3
"""
Game Builder Skill — AI Asset Generation Tool
Supports: Gemini (Nano Banana), Imagen 4, Grok Imagine, GPT Image
Usage: python3 asset_gen.py <command> [options]
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════

BUDGET_FILE = ".asset_budget.json"

PROVIDERS = {
    "gemini": {
        "model": "gemini-3.1-flash-image-preview",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "env_key": "GOOGLE_API_KEY",
        "costs": {"512": 5, "1K": 7, "2K": 10, "4K": 15},  # cents
    },
    "imagen": {
        "model": "imagen-4.0-fast-generate-001",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/{model}:predict",
        "env_key": "GOOGLE_API_KEY",
        "costs": {"fast": 2, "standard": 4, "ultra": 6},  # cents
    },
    "grok": {
        "model": "grok-imagine-image",
        "endpoint": "https://api.x.ai/v1/images/generations",
        "env_key": "XAI_API_KEY",
        "costs": {"default": 2},  # cents
    },
    "openai": {
        "model": "gpt-image-1",
        "endpoint": "https://api.openai.com/v1/images/generations",
        "env_key": "OPENAI_API_KEY",
        "costs": {"low": 1, "medium": 4, "high": 17},  # cents
    },
}

# ═══════════════════════════════════════════════════
# Budget Management
# ═══════════════════════════════════════════════════

def load_budget() -> dict:
    if Path(BUDGET_FILE).exists():
        with open(BUDGET_FILE) as f:
            return json.load(f)
    return {"budget_cents": 500, "spent_cents": 0, "history": []}

def save_budget(data: dict):
    with open(BUDGET_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_budget(cost_cents: int) -> bool:
    data = load_budget()
    remaining = data["budget_cents"] - data["spent_cents"]
    if cost_cents > remaining:
        print(f"❌ Budget insufficient: need {cost_cents}c, have {remaining}c")
        return False
    return True

def record_spend(cost_cents: int, description: str):
    data = load_budget()
    data["spent_cents"] += cost_cents
    data["history"].append({"cost": cost_cents, "desc": description})
    save_budget(data)
    remaining = data["budget_cents"] - data["spent_cents"]
    print(f"💰 Spent: {cost_cents}c | Total: {data['spent_cents']}c / {data['budget_cents']}c | Remaining: {remaining}c")

# ═══════════════════════════════════════════════════
# Image Generation — Gemini (Nano Banana)
# ═══════════════════════════════════════════════════

def generate_gemini(prompt: str, output: str, size: str = "1K", aspect_ratio: str = "1:1") -> bool:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return False

    model = PROVIDERS["gemini"]["model"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    # Build size instruction
    size_map = {"512": "512x512", "1K": "1024x1024", "2K": "2048x2048", "4K": "4096x4096"}
    ar_instruction = f"Aspect ratio: {aspect_ratio}. " if aspect_ratio != "1:1" else ""
    size_instruction = f"Image size: {size_map.get(size, '1024x1024')}. "

    full_prompt = f"{size_instruction}{ar_instruction}Generate this image: {prompt}"

    payload = json.dumps({
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())

        # Extract image from response
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    Path(output).parent.mkdir(parents=True, exist_ok=True)
                    with open(output, "wb") as f:
                        f.write(img_data)

                    cost = PROVIDERS["gemini"]["costs"].get(size, 7)
                    record_spend(cost, f"gemini:{size} {Path(output).name}")
                    print(f"✅ Gemini image saved: {output}")
                    return True

        print("❌ No image in Gemini response")
        return False

    except urllib.error.HTTPError as e:
        print(f"❌ Gemini API error: {e.code} {e.reason}")
        try:
            err_body = e.read().decode()
            print(f"   {err_body[:300]}")
        except:
            pass
        return False
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False

# ═══════════════════════════════════════════════════
# Image Generation — Imagen 4
# ═══════════════════════════════════════════════════

def generate_imagen(prompt: str, output: str, quality: str = "fast") -> bool:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return False

    model_map = {
        "fast": "imagen-4.0-fast-generate-001",
        "standard": "imagen-4.0-generate-001",
        "ultra": "imagen-4.0-ultra-generate-001",
    }
    model = model_map.get(quality, "imagen-4.0-fast-generate-001")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={api_key}"

    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1},
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())

        predictions = data.get("predictions", [])
        if predictions and "bytesBase64Encoded" in predictions[0]:
            img_data = base64.b64decode(predictions[0]["bytesBase64Encoded"])
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "wb") as f:
                f.write(img_data)

            cost = PROVIDERS["imagen"]["costs"].get(quality, 2)
            record_spend(cost, f"imagen:{quality} {Path(output).name}")
            print(f"✅ Imagen image saved: {output}")
            return True

        print("❌ No image in Imagen response")
        return False

    except urllib.error.HTTPError as e:
        print(f"❌ Imagen API error: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Imagen error: {e}")
        return False

# ═══════════════════════════════════════════════════
# Image Generation — Grok Imagine
# ═══════════════════════════════════════════════════

def generate_grok(prompt: str, output: str) -> bool:
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("❌ XAI_API_KEY not set")
        return False

    url = "https://api.x.ai/v1/images/generations"
    payload = json.dumps({
        "model": "grok-imagine-image",
        "prompt": prompt,
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())

        if data.get("data") and data["data"][0].get("url"):
            img_url = data["data"][0]["url"]
            # Download the image
            img_req = urllib.request.Request(img_url)
            with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                img_data = img_resp.read()

            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "wb") as f:
                f.write(img_data)

            record_spend(2, f"grok {Path(output).name}")
            print(f"✅ Grok image saved: {output}")
            return True

        print("❌ No image URL in Grok response")
        return False

    except urllib.error.HTTPError as e:
        print(f"❌ Grok API error: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Grok error: {e}")
        return False

# ═══════════════════════════════════════════════════
# Image Generation — OpenAI GPT Image
# ═══════════════════════════════════════════════════

def generate_openai(prompt: str, output: str, quality: str = "low") -> bool:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return False

    url = "https://api.openai.com/v1/images/generations"
    payload = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "quality": quality,
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())

        if data.get("data") and data["data"][0].get("b64_json"):
            img_data = base64.b64decode(data["data"][0]["b64_json"])
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "wb") as f:
                f.write(img_data)

            cost_map = {"low": 1, "medium": 4, "high": 17}
            record_spend(cost_map.get(quality, 4), f"openai:{quality} {Path(output).name}")
            print(f"✅ OpenAI image saved: {output}")
            return True

        print("❌ No image in OpenAI response")
        return False

    except urllib.error.HTTPError as e:
        print(f"❌ OpenAI API error: {e.code} {e.reason}")
        return False
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return False

# ═══════════════════════════════════════════════════
# Unified Generate with Fallback
# ═══════════════════════════════════════════════════

def generate_image(prompt: str, output: str, provider: str = "auto",
                   size: str = "1K", aspect_ratio: str = "1:1",
                   quality: str = "fast") -> bool:
    """Generate an image with automatic provider fallback."""

    if provider == "auto":
        # Try providers in cost-efficiency order
        providers_to_try = []
        if os.environ.get("GOOGLE_API_KEY"):
            providers_to_try.extend(["imagen", "gemini"])
        if os.environ.get("XAI_API_KEY"):
            providers_to_try.append("grok")
        if os.environ.get("OPENAI_API_KEY"):
            providers_to_try.append("openai")

        if not providers_to_try:
            print("❌ No API keys found. Set GOOGLE_API_KEY, XAI_API_KEY, or OPENAI_API_KEY")
            return False

        for p in providers_to_try:
            print(f"🎨 Trying {p}...")
            if p == "gemini" and generate_gemini(prompt, output, size, aspect_ratio):
                return True
            elif p == "imagen" and generate_imagen(prompt, output, quality):
                return True
            elif p == "grok" and generate_grok(prompt, output):
                return True
            elif p == "openai" and generate_openai(prompt, output, quality):
                return True
            print(f"   {p} failed, trying next...")

        print("❌ All providers failed")
        return False

    # Specific provider
    if provider == "gemini":
        return generate_gemini(prompt, output, size, aspect_ratio)
    elif provider == "imagen":
        return generate_imagen(prompt, output, quality)
    elif provider == "grok":
        return generate_grok(prompt, output)
    elif provider == "openai":
        return generate_openai(prompt, output, quality)
    else:
        print(f"❌ Unknown provider: {provider}")
        return False

# ═══════════════════════════════════════════════════
# Spritesheet Generation
# ═══════════════════════════════════════════════════

def generate_spritesheet(prompt: str, output: str, bg: str = "#00FF00",
                         provider: str = "auto") -> bool:
    """Generate a 4x4 spritesheet (16 frames)."""
    sheet_prompt = (
        f"Create a 4x4 grid spritesheet with exactly 16 cells. "
        f"Each cell shows one frame of: {prompt}. "
        f"Background color: {bg}. "
        f"All cells same size, evenly spaced, clear grid lines between cells. "
        f"Game asset, clean pixel art style, consistent character across all frames."
    )
    return generate_image(sheet_prompt, output, provider=provider, size="1K")

# ═══════════════════════════════════════════════════
# Spritesheet Slicing
# ═══════════════════════════════════════════════════

def slice_spritesheet(input_path: str, output_dir: str, frames: int = 16,
                      cols: int = 4, remove_bg: bool = True,
                      names: Optional[str] = None) -> bool:
    """Slice a spritesheet into individual frames."""
    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow...")
        os.system(f"{sys.executable} -m pip install Pillow --break-system-packages -q")
        from PIL import Image

    img = Image.open(input_path)
    w, h = img.size
    rows = (frames + cols - 1) // cols
    cell_w = w // cols
    cell_h = h // rows

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    name_list = names.split(",") if names else [f"{i+1:02d}" for i in range(frames)]

    for i in range(min(frames, len(name_list))):
        row = i // cols
        col = i % cols
        x = col * cell_w
        y = row * cell_h
        cell = img.crop((x, y, x + cell_w, y + cell_h))

        if remove_bg:
            cell = cell.convert("RGBA")
            # Simple chroma key: remove corners' color
            pixels = cell.load()
            bg_color = pixels[0, 0][:3]
            threshold = 40
            for py in range(cell.height):
                for px in range(cell.width):
                    r, g, b, a = pixels[px, py]
                    if (abs(r - bg_color[0]) < threshold and
                        abs(g - bg_color[1]) < threshold and
                        abs(b - bg_color[2]) < threshold):
                        pixels[px, py] = (r, g, b, 0)

        out_path = Path(output_dir) / f"{name_list[i].strip()}.png"
        cell.save(out_path)

    print(f"✅ Sliced {frames} frames to {output_dir}")
    return True

# ═══════════════════════════════════════════════════
# Background Removal
# ═══════════════════════════════════════════════════

def remove_background(input_path: str, output_path: str) -> bool:
    """Remove background from an image using rembg or simple chroma key."""
    try:
        import rembg
        from PIL import Image
        img = Image.open(input_path)
        result = rembg.remove(img)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        result.save(output_path)
        print(f"✅ Background removed (rembg): {output_path}")
        return True
    except ImportError:
        # Fallback: simple chroma key
        try:
            from PIL import Image
        except ImportError:
            os.system(f"{sys.executable} -m pip install Pillow --break-system-packages -q")
            from PIL import Image

        img = Image.open(input_path).convert("RGBA")
        pixels = img.load()
        # Auto-detect background from corners
        corners = [pixels[0, 0], pixels[img.width-1, 0],
                   pixels[0, img.height-1], pixels[img.width-1, img.height-1]]
        bg = corners[0][:3]
        threshold = 40
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                if (abs(r - bg[0]) < threshold and
                    abs(g - bg[1]) < threshold and
                    abs(b - bg[2]) < threshold):
                    pixels[x, y] = (r, g, b, 0)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print(f"✅ Background removed (chroma key): {output_path}")
        return True

# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Game Asset Generator")
    sub = parser.add_subparsers(dest="command", help="Command")

    # image
    img_p = sub.add_parser("image", help="Generate a single image")
    img_p.add_argument("--prompt", required=True, help="Image description")
    img_p.add_argument("--provider", default="auto", choices=["auto", "gemini", "imagen", "grok", "openai"])
    img_p.add_argument("--size", default="1K", choices=["512", "1K", "2K", "4K"])
    img_p.add_argument("--aspect-ratio", default="1:1")
    img_p.add_argument("--quality", default="fast", choices=["fast", "standard", "ultra", "low", "medium", "high"])
    img_p.add_argument("-o", "--output", required=True, help="Output file path")

    # spritesheet
    ss_p = sub.add_parser("spritesheet", help="Generate a 4x4 spritesheet")
    ss_p.add_argument("--prompt", required=True, help="Animation/collection description")
    ss_p.add_argument("--provider", default="auto")
    ss_p.add_argument("--bg", default="#00FF00", help="Background color hex")
    ss_p.add_argument("-o", "--output", required=True)

    # slice
    sl_p = sub.add_parser("slice", help="Slice spritesheet into frames")
    sl_p.add_argument("--input", required=True)
    sl_p.add_argument("--output", required=True, help="Output directory")
    sl_p.add_argument("--frames", type=int, default=16)
    sl_p.add_argument("--cols", type=int, default=4)
    sl_p.add_argument("--remove-bg", action="store_true")
    sl_p.add_argument("--names", default=None, help="Comma-separated frame names")

    # remove-bg
    rb_p = sub.add_parser("remove-bg", help="Remove image background")
    rb_p.add_argument("--input", required=True)
    rb_p.add_argument("--output", required=True)

    # set-budget
    sb_p = sub.add_parser("set-budget", help="Set budget in cents")
    sb_p.add_argument("amount", type=int, help="Budget in cents")

    # budget
    sub.add_parser("budget", help="Show current budget")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(args.prompt, args.output, args.provider, args.size,
                       args.aspect_ratio, args.quality)
    elif args.command == "spritesheet":
        generate_spritesheet(args.prompt, args.output, args.bg, args.provider)
    elif args.command == "slice":
        slice_spritesheet(args.input, args.output, args.frames, args.cols,
                          args.remove_bg, args.names)
    elif args.command == "remove-bg":
        remove_background(args.input, args.output)
    elif args.command == "set-budget":
        data = load_budget()
        data["budget_cents"] = args.amount
        save_budget(data)
        print(f"✅ Budget set to {args.amount}c (${args.amount/100:.2f})")
    elif args.command == "budget":
        data = load_budget()
        remaining = data["budget_cents"] - data["spent_cents"]
        print(f"💰 Budget: {data['spent_cents']}c / {data['budget_cents']}c | Remaining: {remaining}c (${remaining/100:.2f})")
        if data["history"]:
            print(f"   Last 5 items:")
            for item in data["history"][-5:]:
                print(f"     {item['cost']}c — {item['desc']}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
