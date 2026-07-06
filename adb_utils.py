import subprocess
import time
import re

def adb(cmd):
    """Jalankan perintah ADB shell dan kembalikan output sebagai string."""
    try:
        result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"[ADB Error] {e}")
        return ""

def tap(x, y):
    """Tap pada koordinat x, y."""
    adb(f"input tap {x} {y}")

def input_text(text):
    """Ketik teks (menggunakan input text)."""
    # Escape karakter khusus
    text = text.replace(" ", "%s").replace("&", "\\&")
    adb(f"input text '{text}'")

def press_keycode(keycode):
    """Tekan keycode (misal 66 = Enter, 279 = Paste)."""
    adb(f"input keyevent {keycode}")

def get_clipboard():
    """Ambil teks dari clipboard Android."""
    out = adb("service call clipboard 1")
    # Parse output untuk mengambil teks (format: Parcel(..., ...))
    match = re.search(r"'(.*?)'", out)
    if match:
        return match.group(1)
    return ""

def set_clipboard(text):
    """Set clipboard Android."""
    text_escaped = text.replace("'", "\\'")
    adb(f"service call clipboard 2 i32 0 s16 '{text_escaped}'")

def is_app_running(pkg):
    """Cek apakah proses dengan package name sedang berjalan."""
    out = adb(f"ps | grep {pkg}")
    return pkg in out

def start_app(pkg, activity=".MainActivity"):
    """Buka aplikasi."""
    adb(f"am start -n {pkg}/{activity}")

def dump_ui():
    """Dump UI ke file /sdcard/ui.xml dan kembalikan isinya."""
    adb("uiautomator dump /sdcard/ui.xml")
    try:
        with open("/sdcard/ui.xml", "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        # Jika file tidak ada, coba pull
        subprocess.run("adb pull /sdcard/ui.xml /tmp/ui.xml", shell=True)
        with open("/tmp/ui.xml", "r", encoding="utf-8", errors="ignore") as f:
            return f.read()