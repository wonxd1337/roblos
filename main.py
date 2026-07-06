import time
from config import PACKAGES_FILE, SCRIPT_FILE, PLACE_ID, DELAY_BETWEEN_INSTANCES, MONITOR_INTERVAL, CHANNEL_ID
from delta_control import full_process
from monitor import monitor_loop

def main():
    try:
        with open("token.txt", "r") as f:
            token = f.read().strip()
            if not token:
                raise FileNotFoundError
    except:
        token = input("Masukkan token Discord: ").strip()

    with open(PACKAGES_FILE, 'r') as f:
        packages = [line.strip() for line in f if line.strip()]
    if not packages:
        print("[Main] Tidak ada package di packages.txt")
        return

    try:
        with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"[Main] File {SCRIPT_FILE} tidak ditemukan")
        return

    print(f"[Main] Memulai startup untuk {len(packages)} instance")
    for i, pkg in enumerate(packages):
        print(f"\n[Main] === Instance {i+1}/{len(packages)}: {pkg} ===")
        success = full_process(pkg, script_content, PLACE_ID, token, CHANNEL_ID)
        if not success:
            print(f"[Main] Gagal memproses {pkg}, lanjut ke berikutnya...")
        else:
            print(f"[Main] {pkg} berhasil diproses.")
        time.sleep(DELAY_BETWEEN_INSTANCES)

    print("\n[Main] Startup selesai, memulai monitoring...")
    monitor_loop(packages, script_content, PLACE_ID, token, CHANNEL_ID, MONITOR_INTERVAL)

if __name__ == "__main__":
    main()
