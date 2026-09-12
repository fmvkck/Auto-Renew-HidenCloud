import os, time, sys
from chromix import launch

USER = os.environ.get("HC_USER", "5JSH5vIiAG")
PASS = os.environ.get("HC_PASS", "DYEJMoW9JHvbHoeZ")

b = launch(headless=False, args=["--disable-gpu", "--disable-dev-shm-usage"])
page = b.new_page()
try:
    print("[1] goto login...", flush=True)
    page.goto("https://dash.hidencloud.com/auth/login", timeout=60000)
    # 等盾：最多 150s
    form_ok = False
    for i in range(25):
        try: t = page.title()
        except Exception: time.sleep(4); continue
        low = t.lower()
        if "moment" in low or "verification" in low or "checking" in low or not t:
            print(f"  [{i}] challenge page: {t!r}", flush=True)
            time.sleep(6)
            try: page.reload(timeout=30000)
            except Exception: pass
            continue
        try:
            page.wait_for_selector('input[name="username"]', timeout=5000)
            form_ok = True
            break
        except Exception:
            time.sleep(4)
    print(f"[2] form: {'APPEARED' if form_ok else 'NOT FOUND'} title={page.title()!r}", flush=True)
    page.screenshot(path="/tmp/01_login_page.png")
    if not form_ok:
        print("RESULT: CHALLENGE_STUCK", flush=True)
        sys.exit(0)
    # 尝试登录
    page.fill('input[name="username"]', USER)
    page.fill('input[name="password"]', PASS)
    page.click('button[type="submit"]')
    ok = False
    for i in range(90):
        time.sleep(2)
        if "/auth/login" not in page.url:
            ok = True; break
    print(f"[3] login: {'SUCCESS' if ok else 'REJECTED'} url={page.url}", flush=True)
    page.screenshot(path="/tmp/02_after_login.png")
    if ok:
        page.goto("https://dash.hidencloud.com/client", timeout=60000)
        time.sleep(6)
        body = page.inner_text("body")
        for line in body.split("\n"):
            if any(k in line.lower() for k in ["231021", "expire", "renew", "due"]):
                print(">>", line.strip()[:120], flush=True)
        page.screenshot(path="/tmp/03_client.png")
        print("RESULT: LOGIN_OK", flush=True)
    else:
        print("RESULT: LOGIN_REJECTED", flush=True)
except Exception as e:
    print(f"[!] {str(e)[:200]}", flush=True)
    try: page.screenshot(path="/tmp/99_error.png")
    except Exception: pass
finally:
    b.close()
