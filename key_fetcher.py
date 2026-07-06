#!/usr/bin/env python3
"""
Key Fetcher via Discord REST API
"""

import requests
import time
import re

DISCORD_API = "https://discord.com/api/v9"

def get_key_via_discord(token, channel_id, shortlink, timeout=60):
    """
    Kirim command ke Discord via REST API, lalu polling balasan.
    Mengembalikan key atau None.
    """
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # Kirim pesan
    url = f"{DISCORD_API}/channels/{channel_id}/messages"
    payload = {"content": f"/bypass url: {shortlink}"}

    try:
        print("[*] Mengirim command ke Discord...")
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"[!] Gagal kirim pesan: {resp.status_code}")
            print(resp.text[:200])
            return None
        print("[✓] Pesan terkirim, menunggu balasan...")
    except Exception as e:
        print(f"[!] Error kirim: {e}")
        return None

    # Polling untuk membaca balasan
    start_time = time.time()
    last_message_id = None

    while time.time() - start_time < timeout:
        try:
            # Ambil 10 pesan terakhir di channel
            resp = requests.get(f"{url}?limit=10", headers=headers, timeout=5)
            if resp.status_code != 200:
                print(f"[!] Gagal membaca pesan: {resp.status_code}")
                time.sleep(2)
                continue

            messages = resp.json()
            for msg in messages:
                content = msg['content']
                # Cari key dengan pola FREE_
                match = re.search(r'(FREE_[a-fA-F0-9]{32,})', content)
                if match:
                    key = match.group(1)
                    print("[✓] Key ditemukan!")
                    return key
                # Jika pesan error dari bot
                if "error" in content.lower() or "failed" in content.lower():
                    print(f"[!] Bot merespon error: {content[:100]}")
                    return None
        except Exception as e:
            print(f"[!] Error polling: {e}")

        time.sleep(2)

    print("[!] Timeout menunggu balasan.")
    return None

def get_key_from_shortlink(shortlink, token=None, channel_id=None):
    """
    Fungsi utama: dapatkan key dari shortlink.
    Jika token dan channel_id disediakan, pakai Discord.
    """
    if token and channel_id:
        return get_key_via_discord(token, channel_id, shortlink)
    else:
        print("[!] Token atau channel_id tidak disediakan.")
        return None