import time
from adb_utils import start_app, tap, input_text, press_keycode, get_clipboard, set_clipboard, is_app_running, adb
from ui_automator import find_element_by_text, find_edit_text, find_button_by_text
from key_fetcher import get_key_from_shortlink

def get_shortlink_from_delta(pkg):
    """
    Buka Delta, cari tombol "Receive Key", klik, ambil shortlink dari clipboard.
    """
    start_app(pkg)
    time.sleep(3)
    # Cari tombol "Receive Key"
    coords = find_button_by_text("Receive Key")
    if coords:
        tap(*coords)
        time.sleep(2)
        # Ambil shortlink dari clipboard
        shortlink = get_clipboard()
        if shortlink and shortlink.startswith("http"):
            return shortlink
    return None

def input_key_and_continue(pkg, key):
    """
    Cari kolom input key, masukkan key, lalu klik Continue.
    """
    # Cari EditText
    edit_coords = find_edit_text()
    if edit_coords:
        tap(*edit_coords)
        time.sleep(0.5)
        input_text(key)
        time.sleep(0.5)
        # Cari tombol Continue
        cont_coords = find_button_by_text("Continue")
        if cont_coords:
            tap(*cont_coords)
            return True
    return False

def execute_script(pkg, script_content):
    """
    Paste script ke area script, lalu klik Execute.
    """
    # Cari tab "Script" atau "Executor"
    script_tab = find_element_by_text("Script") or find_element_by_text("Executor")
    if script_tab:
        tap(*script_tab)
        time.sleep(1)
    # Cari EditText untuk script
    edit_coords = find_edit_text()
    if not edit_coords:
        # Jika tidak ada, coba tap area teks
        paste_coords = find_element_by_text("Paste")
        if paste_coords:
            tap(*paste_coords)
            time.sleep(0.5)
    # Tempelkan script ke clipboard
    set_clipboard(script_content)
    if edit_coords:
        tap(*edit_coords)
        time.sleep(0.5)
        press_keycode(279)   # KEYCODE_PASTE
        time.sleep(1)
    # Cari tombol Execute
    execute_btn = find_button_by_text("Execute") or find_button_by_text("Run")
    if execute_btn:
        tap(*execute_btn)
        return True
    return False

def full_process(pkg, script_content, place_id, token, channel_id):
    """
    Satu siklus penuh: buka Delta, dapatkan key, input key, execute script, join game.
    """
    # 1. Buka Delta
    start_app(pkg)
    time.sleep(3)
    # 2. Dapatkan shortlink
    shortlink = get_shortlink_from_delta(pkg)
    if not shortlink:
        print(f"[Delta] Gagal dapat shortlink untuk {pkg}")
        return False
    print(f"[Delta] Shortlink: {shortlink[:60]}...")
    # 3. Dapatkan key via Discord
    key = get_key_from_shortlink(shortlink, token, channel_id)
    if not key:
        print(f"[Delta] Gagal dapat key untuk {pkg}")
        return False
    print(f"[Delta] Key untuk {pkg}: {key[:20]}...")
    # 4. Input key dan Continue
    if not input_key_and_continue(pkg, key):
        print(f"[Delta] Gagal input key untuk {pkg}")
        return False
    time.sleep(2)
    # 5. Execute script
    if not execute_script(pkg, script_content):
        print(f"[Delta] Gagal execute script untuk {pkg}")
        return False
    # 6. Join game (deep link)
    time.sleep(1)
    adb(f"am start -a android.intent.action.VIEW -d 'roblox://placeId={place_id}' {pkg}")
    return True