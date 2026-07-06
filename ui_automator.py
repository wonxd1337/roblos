import re
from adb_utils import dump_ui, tap, input_text, press_keycode

def find_element_by_text(text, class_name=None):
    """
    Cari elemen UI yang mengandung teks tertentu.
    Return (x, y) center koordinat atau None jika tidak ditemukan.
    """
    xml = dump_ui()
    pattern = r'<node.*?(?:text|content-desc)="([^"]*{}[^"]*?)".*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'.format(re.escape(text))
    match = re.search(pattern, xml, re.IGNORECASE | re.DOTALL)
    if match:
        x1, y1, x2, y2 = map(int, match.groups()[1:])
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return (center_x, center_y)
    return None

def find_edit_text():
    """Cari EditText pertama di UI, return koordinat center."""
    xml = dump_ui()
    pattern = r'<node.*?class="android\.widget\.EditText".*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'
    match = re.search(pattern, xml, re.DOTALL)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return (center_x, center_y)
    return None

def find_button_by_text(text):
    """Cari tombol dengan teks tertentu, return koordinat center."""
    return find_element_by_text(text, class_name="android.widget.Button")