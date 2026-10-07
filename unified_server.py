import os
import sys
import subprocess
import time
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
PYTHON_EXE = os.path.join(BACKEND_DIR, ".venv", "Scripts", "python.exe")
CLOUDFLARED_EXE = os.path.join(BASE_DIR, "cloudflared.exe")

URL_FILE = os.path.join(BASE_DIR, "LIVE_PUBLIC_URL.txt")
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "farmer-crop-advisory")
DESKTOP_URL_FILE = os.path.join(DESKTOP_DIR, "LIVE_PUBLIC_URL.txt")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def main():
    log("Starting Unified 24/7 Farmer Crop Advisory Platform Server...")

    # 1. Start Flask API server
    flask_cmd = [PYTHON_EXE, os.path.join(BACKEND_DIR, "app.py")]
    flask_proc = subprocess.Popen(
        flask_cmd,
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    log(f"Flask backend started with PID: {flask_proc.pid}")

    # Wait 3 seconds for Flask to bind port 5000
    time.sleep(3)

    # 2. Start Cloudflare Tunnel
    cf_cmd = [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5000"]
    cf_proc = subprocess.Popen(
        cf_cmd,
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    log(f"Cloudflare tunnel started with PID: {cf_proc.pid}")

    # 3. Read Cloudflare logs to extract public URL
    public_url = None
    log("Connecting to Cloudflare global edge network...")

    start_time = time.time()
    while time.time() - start_time < 30:
        line = cf_proc.stdout.readline()
        if not line:
            time.sleep(0.5)
            continue
        print(line, end='', flush=True)
        m = re.search(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', line)
        if m and "api.trycloudflare.com" not in m.group(0):
            public_url = m.group(0)
            break

    if public_url:
        log("=" * 60)
        log(f"SUCCESS! 24/7 PUBLIC URL ACTIVE:")
        log(f"==> {public_url} <==")
        log("=" * 60)

        url_content = f"""=============================================================
FARMER CROP ADVISORY PLATFORM - 24/7 ACTIVE PUBLIC URL
=============================================================
URL: {public_url}

Status: ACTIVE (Cloudflare Edge SSL)
Mobile & Desktop: 100% Compatible, Zero Passwords, Zero Waiting

DEMO ACCOUNTS:
1. Farmer Role:
   Email:    farmer@demo.org
   Password: Farmer@123

2. Admin Role:
   Email:    admin@farmeradvisory.org
   Password: Admin@123

LLM ENGINES ACTIVE:
- AgriLLM-Neural (Built-in Offline Knowledge Engine)
- Google Gemini 1.5 Flash (If GEMINI_API_KEY set)
- Groq Llama 3.3 70B (If GROQ_API_KEY set)
- OpenAI GPT-4o Mini (If OPENAI_API_KEY set)

Updated At: {time.strftime("%Y-%m-%d %H:%M:%S")}
=============================================================
"""
        with open(URL_FILE, "w", encoding="utf-8") as f:
            f.write(url_content)

        if os.path.exists(DESKTOP_DIR):
            with open(DESKTOP_URL_FILE, "w", encoding="utf-8") as f:
                f.write(url_content)
    else:
        log("Could not detect public URL within 30 seconds.")

    # 4. Supervise both processes in a persistent 24/7 loop
    try:
        while True:
            time.sleep(5)
            if flask_proc.poll() is not None:
                log("Flask exited unexpectedly! Restarting...")
                flask_proc = subprocess.Popen(flask_cmd, cwd=BACKEND_DIR)
            if cf_proc.poll() is not None:
                log("Cloudflare tunnel exited! Restarting...")
                cf_proc = subprocess.Popen(cf_cmd, cwd=BASE_DIR)
    except KeyboardInterrupt:
        log("Shutting down services...")
        flask_proc.terminate()
        cf_proc.terminate()

if __name__ == "__main__":
    main()
