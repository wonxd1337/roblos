import time
from adb_utils import is_app_running, start_app
from delta_control import full_process

def monitor_loop(packages, script_content, place_id, token, channel_id, interval=10):
    """
    Loop monitoring: cek setiap package, jika mati -> restart.
    """
    while True:
        for pkg in packages:
            if not is_app_running(pkg):
                print(f"[Monitor] {pkg} mati, restart...")
                full_process(pkg, script_content, place_id, token, channel_id)
        time.sleep(interval)