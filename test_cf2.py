import time, sys
from chromix import launch

b = launch(headless=False, args=["--disable-gpu", "--disable-dev-shm-usage"])
page = b.new_page()
try:
    page.goto("https://dash.hidencloud.com/auth/login", timeout=60000)
    for i in range(12):
        try:
            t = page.title()
            html = page.content()[:500]
        except Exception as e:
            print(f"  [{i}] exc: {str(e)[:80]}", flush=True)
            time.sleep(5)
            continue
        has_form = 'name="username"' in page.content()
        print(f"  [{i}] title={t!r} form={has_form}", flush=True)
        print(f"       body[:300]: {html[:300]!r}", flush=True)
        if has_form:
            print("RESULT: FORM_APPEARED", flush=True)
            sys.exit(0)
        time.sleep(6)
        try: page.reload(timeout=30000)
        except Exception: pass
    print("RESULT: STUCK", flush=True)
except Exception as e:
    print(f"[!] {str(e)[:200]}", flush=True)
finally:
    b.close()
