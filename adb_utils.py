import subprocess
import time
import re

def adb(cmd):
    try:
        result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"[ADB Error] {e}")
        return ""

def tap(x, y):
    adb(f"input tap {x} {y}")

def input_text(text):
    text = text.replace(" ", "%s").replace("&", "\\&")
    adb(f"input text '{text}'")

def press_keycode(keycode):
    adb(f"input keyevent {keycode}")

def get_clipboard():
    out = adb("service call clipboard 1")
    match = re.search(r"'(.*?)'", out)
    if match:
        return match.group(1)
    return ""

def set_clipboard(text):
    text_escaped = text.replace("'", "\\'")
    adb(f"service call clipboard 2 i32 0 s16 '{text_escaped}'")

def is_app_running(pkg):
    out = adb(f"ps | grep {pkg}")
    return pkg in out

def start_app(pkg, activity=".MainActivity"):
    cmd = f"am start -n {pkg}/{activity}"
    out = adb(cmd)
    print(f"[ADB] {cmd} -> {out[:150]}")
    return out

def dump_ui():
    adb("uiautomator dump /sdcard/ui.xml")
    out = adb("cat /sdcard/ui.xml")
    return out
