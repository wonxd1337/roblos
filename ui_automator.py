import re
import time
from adb_utils import dump_ui, tap, input_text, press_keycode

def find_element_by_text(text, class_name=None):
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
    return find_element_by_text(text, class_name="android.widget.Button")

def wait_for_element(text, timeout=30, interval=2):
    start_time = time.time()
    while time.time() - start_time < timeout:
        coords = find_element_by_text(text)
        if coords:
            return coords
        time.sleep(interval)
    return None
