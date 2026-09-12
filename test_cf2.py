import time, sys
from chromix import launch

b = launch(headless=False, args=["--disable-gpu", "--disable-dev-shm-usage"])
page = b.new_page()
try:
    page.goto("https://dash.hidencloud.com/auth/login", timeout=60000)
    form_ok = False
    for i in range(30):
        time.sleep(4)
        try:
            t = page.title()
            has_form = 'name="username"' in page.content()
        except Exception as e:
            print(f"  [{i}] exc: {str(e)[:60]}", flush=True)
            continue
        print(f"  [{i}] title={t!r} form={has_form}", flush=True)
        if has_form:
            form_ok = True
            break
    print(f"RESULT: {'FORM_APPEARED' if form_ok else 'STUCK'}", flush=True)
except Exception as e:
    print(f"[!] {str(e)[:200]}", flush=True)
finally:
    b.close()
