#!/usr/bin/env python3
"""
Game Builder Skill — Visual QA Tool
Captures game screenshots and analyzes them with AI vision for bugs.
Supports: Puppeteer (web games), Godot headless (native games)
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# ═══════════════════════════════════════════════════
# Screenshot Capture
# ═══════════════════════════════════════════════════

def capture_web(url: str, output_dir: str, count: int = 3, delay: float = 2.0) -> list:
    """Capture screenshots of a web game using Puppeteer."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Check if puppeteer is available
    check = subprocess.run(["npx", "--yes", "puppeteer", "--version"],
                          capture_output=True, text=True)

    screenshots = []
    js_script = f"""
const puppeteer = require('puppeteer');
(async () => {{
    const browser = await puppeteer.launch({{
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }});
    const page = await browser.newPage();
    await page.setViewport({{ width: 1280, height: 720 }});
    await page.goto('{url}', {{ waitUntil: 'networkidle2', timeout: 30000 }});

    // Wait for game to load
    await new Promise(r => setTimeout(r, {int(delay * 1000)}));

    // Take multiple screenshots
    for (let i = 0; i < {count}; i++) {{
        const path = '{output_dir}/screenshot_' + String(i+1).padStart(2, '0') + '.png';
        await page.screenshot({{ path, fullPage: false }});
        console.log('Captured: ' + path);
        await new Promise(r => setTimeout(r, {int(delay * 1000)}));
    }}

    await browser.close();
}})();
"""
    script_path = Path(output_dir) / "_capture.js"
    with open(script_path, "w") as f:
        f.write(js_script)

    try:
        result = subprocess.run(
            ["node", str(script_path)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if "Captured:" in line:
                    path = line.split("Captured:")[-1].strip()
                    screenshots.append(path)
                    print(f"📸 {path}")
        else:
            print(f"❌ Puppeteer error: {result.stderr[:500]}")

    except subprocess.TimeoutExpired:
        print("❌ Screenshot capture timed out")
    except FileNotFoundError:
        print("❌ Node.js not found. Install: nvm install --lts")
    finally:
        script_path.unlink(missing_ok=True)

    return screenshots


def capture_file(html_path: str, output_dir: str) -> list:
    """Capture screenshot of a local HTML file."""
    import http.server
    import threading

    # Start a simple HTTP server
    port = 8765
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(("", port), handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    try:
        return capture_web(f"http://localhost:{port}/{html_path}", output_dir)
    finally:
        server.shutdown()


# ═══════════════════════════════════════════════════
# AI Vision Analysis
# ═══════════════════════════════════════════════════

def analyze_screenshot(image_path: str) -> dict:
    """Analyze a game screenshot with Gemini Flash Vision."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set for visual QA")
        return {"error": "No API key", "issues": []}

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Determine mime type
    ext = Path(image_path).suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
    mime_type = mime_map.get(ext, "image/png")

    # Use Gemini Flash for vision analysis (free tier available)
    model = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    prompt = """You are a game QA tester analyzing a screenshot of a game.
Identify ALL visual issues. For each issue, provide:
1. severity: "critical" / "major" / "minor"
2. category: "texture" / "ui" / "physics" / "layout" / "rendering" / "text"
3. description: What's wrong
4. location: Where on screen (top-left, center, etc.)
5. suggestion: How to fix it

Also note what looks GOOD about the game visually.

Respond in JSON format:
{
  "issues": [
    {"severity": "...", "category": "...", "description": "...", "location": "...", "suggestion": "..."}
  ],
  "positives": ["..."],
  "overall_score": 1-10,
  "summary": "Brief overall assessment"
}

If the game looks fine with no issues, return empty issues array and high score."""

    payload = json.dumps({
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": mime_type, "data": image_data}},
                {"text": prompt}
            ]
        }],
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())

        # Extract text response
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "text" in part:
                    text = part["text"]
                    # Try to parse JSON from response
                    try:
                        # Clean markdown code blocks if present
                        if "```json" in text:
                            text = text.split("```json")[1].split("```")[0]
                        elif "```" in text:
                            text = text.split("```")[1].split("```")[0]
                        result = json.loads(text.strip())
                        return result
                    except json.JSONDecodeError:
                        return {
                            "issues": [],
                            "positives": [],
                            "overall_score": 5,
                            "summary": text[:500],
                            "raw_response": True
                        }

        return {"error": "No response from vision model", "issues": []}

    except urllib.error.HTTPError as e:
        print(f"❌ Vision API error: {e.code}")
        return {"error": f"API error {e.code}", "issues": []}
    except Exception as e:
        print(f"❌ Vision error: {e}")
        return {"error": str(e), "issues": []}


def run_qa_loop(url_or_path: str, output_dir: str, max_rounds: int = 3) -> dict:
    """Run the full visual QA loop: capture → analyze → report."""
    print(f"\n🔍 Starting Visual QA Loop (max {max_rounds} rounds)")
    print(f"   Target: {url_or_path}")
    print(f"   Output: {output_dir}\n")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    all_results = []

    for round_num in range(1, max_rounds + 1):
        print(f"═══ Round {round_num}/{max_rounds} ═══")

        # Capture
        round_dir = f"{output_dir}/round_{round_num}"
        if url_or_path.startswith("http"):
            screenshots = capture_web(url_or_path, round_dir, count=2)
        else:
            screenshots = capture_file(url_or_path, round_dir)

        if not screenshots:
            print("❌ No screenshots captured, skipping round")
            continue

        # Analyze each screenshot
        round_issues = []
        for ss in screenshots:
            print(f"\n🔎 Analyzing: {ss}")
            result = analyze_screenshot(ss)
            issues = result.get("issues", [])
            score = result.get("overall_score", 0)

            if issues:
                for issue in issues:
                    sev = issue.get("severity", "unknown")
                    desc = issue.get("description", "?")
                    print(f"   {'🔴' if sev == 'critical' else '🟡' if sev == 'major' else '🟢'} [{sev}] {desc}")
                round_issues.extend(issues)
            else:
                print(f"   ✅ No issues found (score: {score}/10)")

            all_results.append({
                "round": round_num,
                "screenshot": ss,
                "result": result
            })

        # Check if we can stop early
        critical_issues = [i for i in round_issues if i.get("severity") == "critical"]
        if not critical_issues and not round_issues:
            print(f"\n✅ Visual QA passed in round {round_num}!")
            break

        if round_num < max_rounds:
            # Generate fix report for Claude Code to act on
            fix_report = {
                "round": round_num,
                "issues": round_issues,
                "fix_instructions": [
                    f"Fix: {i['description']} at {i.get('location', 'unknown')} — {i.get('suggestion', '')}"
                    for i in round_issues
                ]
            }
            report_path = f"{round_dir}/fix_report.json"
            with open(report_path, "w") as f:
                json.dump(fix_report, f, indent=2, ensure_ascii=False)
            print(f"\n📋 Fix report: {report_path}")
            print(f"   Claude Code should fix these issues and re-run QA")

    # Save full report
    report_path = f"{output_dir}/qa_report.json"
    with open(report_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\n📊 Full QA report: {report_path}")

    return {"rounds": len(all_results), "report": report_path}


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Game Visual QA Tool")
    sub = parser.add_subparsers(dest="command")

    # capture
    cap_p = sub.add_parser("capture", help="Capture screenshots")
    cap_p.add_argument("--url", help="Game URL (web)")
    cap_p.add_argument("--file", help="Local HTML file")
    cap_p.add_argument("--output", default="screenshots/", help="Output directory")
    cap_p.add_argument("--count", type=int, default=3)
    cap_p.add_argument("--delay", type=float, default=2.0)

    # analyze
    ana_p = sub.add_parser("analyze", help="Analyze a screenshot")
    ana_p.add_argument("--image", required=True, help="Screenshot path")

    # qa (full loop)
    qa_p = sub.add_parser("qa", help="Run full QA loop")
    qa_p.add_argument("--url", help="Game URL")
    qa_p.add_argument("--file", help="Local HTML file")
    qa_p.add_argument("--output", default="qa_results/")
    qa_p.add_argument("--rounds", type=int, default=3)

    args = parser.parse_args()

    if args.command == "capture":
        target = args.url or f"file://{os.path.abspath(args.file)}"
        if args.url:
            capture_web(args.url, args.output, args.count, args.delay)
        elif args.file:
            capture_file(args.file, args.output)

    elif args.command == "analyze":
        result = analyze_screenshot(args.image)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "qa":
        target = args.url or args.file
        if not target:
            print("❌ Specify --url or --file")
            return
        run_qa_loop(target, args.output, args.rounds)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
