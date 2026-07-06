import subprocess
import time
import re

def run(cmd):
    """Jalankan perintah langsung di Termux."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"[Error] {e}")
        return ""

def tap(x, y):
    run(f"input tap {x} {y}")

def input_text(text):
    text = text.replace(" ", "%s").replace("&", "\\&")
    run(f"input text '{text}'")

def press_keycode(keycode):
    run(f"input keyevent {keycode}")

def get_clipboard():
    out = run("service call clipboard 1")
    match = re.search(r"'(.*?)'", out)
    if match:
        return match.group(1)
    return ""

def set_clipboard(text):
    text_escaped = text.replace("'", "\\'")
    run(f"service call clipboard 2 i32 0 s16 '{text_escaped}'")

def is_app_running(pkg):
    out = run(f"ps | grep {pkg}")
    return pkg in out

def start_app(pkg):
    """Buka aplikasi dengan am start -p (paling reliable)."""
    # METODE 1: am start -p (paling simpel dan berhasil)
    cmd = f"am start -p {pkg}"
    out = run(cmd)
    print(f"[Start] {cmd} -> {out[:150]}")
    if "Starting" in out or "Activity" in out or out:
        return out
    
    # METODE 2: am start dengan activity splash
    activity = f"{pkg}/com.roblox.client.startup.ActivitySplash"
    cmd = f"am start -n {activity}"
    out = run(cmd)
    print(f"[Start] {cmd} -> {out[:150]}")
    if "Starting" in out or "Activity" in out:
        return out
    
    # METODE 3: Intent fallback
    cmd = f"am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER {pkg}"
    out = run(cmd)
    print(f"[Start] Fallback: {cmd} -> {out[:150]}")
    return out

def dump_ui():
    run("uiautomator dump /sdcard/ui.xml")
    out = run("cat /sdcard/ui.xml")
    return out

def wait_for_app(pkg, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_app_running(pkg):
            return True
        time.sleep(1)
    return False
