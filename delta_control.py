import time
from adb_utils import start_app, tap, input_text, press_keycode, get_clipboard, set_clipboard, is_app_running, run, wait_for_app, dump_ui
from ui_automator import find_element_by_text, find_edit_text, find_button_by_text, wait_for_element
from key_fetcher import get_key_from_shortlink

def wait_for_delta(pkg, timeout=30):
    print(f"[Delta] Menunggu Delta muncul untuk {pkg} (timeout {timeout}s)...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        coords = find_button_by_text("Receive Key") or find_button_by_text("Get Key")
        if coords:
            print(f"[Delta] Delta muncul!")
            return True
        time.sleep(2)
    print(f"[Delta] Timeout menunggu Delta untuk {pkg}")
    return False

def get_shortlink_from_delta(pkg):
    coords = find_button_by_text("Receive Key") or find_button_by_text("Get Key")
    if not coords:
        print("[Delta] Tombol Receive Key/Get Key tidak ditemukan.")
        return None
    tap(*coords)
    time.sleep(2)
    shortlink = get_clipboard()
    if shortlink and shortlink.startswith("http"):
        print(f"[Delta] Shortlink: {shortlink[:60]}...")
        return shortlink
    return None

def input_key_and_continue(pkg, key):
    edit_coords = find_edit_text()
    if not edit_coords:
        print("[Delta] Kolom input key tidak ditemukan.")
        return False
    tap(*edit_coords)
    time.sleep(0.5)
    input_text(key)
    time.sleep(0.5)
    cont_coords = find_button_by_text("Continue")
    if cont_coords:
        tap(*cont_coords)
        print("[Delta] Key dimasukkan dan Continue ditekan.")
        return True
    print("[Delta] Tombol Continue tidak ditemukan.")
    return False

def execute_script(pkg, script_content):
    script_tab = find_element_by_text("Script") or find_element_by_text("Executor")
    if script_tab:
        tap(*script_tab)
        time.sleep(1)
    edit_coords = find_edit_text()
    if not edit_coords:
        paste_coords = find_element_by_text("Paste")
        if paste_coords:
            tap(*paste_coords)
            time.sleep(0.5)
    set_clipboard(script_content)
    if edit_coords:
        tap(*edit_coords)
        time.sleep(0.5)
        press_keycode(279)  # KEYCODE_PASTE
        time.sleep(1)
    execute_btn = find_button_by_text("Execute") or find_button_by_text("Run")
    if execute_btn:
        tap(*execute_btn)
        print("[Delta] Script dieksekusi.")
        return True
    print("[Delta] Tombol Execute tidak ditemukan.")
    return False

def full_process(pkg, script_content, place_id, token, channel_id):
    print(f"\n[Delta] === Memproses {pkg} ===")

    # 1. Buka clone (pakai am start -p)
    print(f"[Delta] Membuka {pkg}...")
    start_app(pkg)
    time.sleep(3)
    
    # Tunggu aplikasi terbuka
    if not wait_for_app(pkg, timeout=10):
        print(f"[Delta] {pkg} tidak terbuka dalam 10 detik, lanjutkan...")

    # 2. Join ke game (deep link)
    print(f"[Delta] Join ke game dengan place ID: {place_id}")
    run(f"am start -a android.intent.action.VIEW -d 'roblox://placeId={place_id}' {pkg}")
    time.sleep(5)

    # 3. Tunggu Delta muncul
    if not wait_for_delta(pkg, timeout=30):
        print(f"[Delta] Delta tidak muncul untuk {pkg}, skip...")
        return False

    # 4. Dapatkan shortlink
    shortlink = get_shortlink_from_delta(pkg)
    if not shortlink:
        print(f"[Delta] Gagal dapat shortlink untuk {pkg}")
        return False

    # 5. Dapatkan key via Discord
    key = get_key_from_shortlink(shortlink, token, channel_id)
    if not key:
        print(f"[Delta] Gagal dapat key untuk {pkg}")
        return False
    print(f"[Delta] Key: {key[:20]}...")

    # 6. Input key dan Continue
    if not input_key_and_continue(pkg, key):
        print(f"[Delta] Gagal input key untuk {pkg}")
        return False
    time.sleep(2)

    # 7. Execute script
    if not execute_script(pkg, script_content):
        print(f"[Delta] Gagal execute script untuk {pkg}")
        return False

    print(f"[Delta] {pkg} selesai diproses.")
    return True
