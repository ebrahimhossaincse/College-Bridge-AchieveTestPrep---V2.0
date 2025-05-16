from datetime import datetime
from pathlib import Path
from config.base_config import BaseConfig

def take_screenshot(page, name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path(BaseConfig.SCREENSHOT_DIR)
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / f"{name}_{timestamp}.png"
    page.screenshot(path=file_path)
    return file_path

def highlight_element(page, selector, color="yellow", duration=0.5):
    # Use JS to set element style temporarily
    page.eval_on_selector(
        selector,
        f"""(el) => {{
            const original = el.style.border;
            el.style.border = "2px solid {color}";
            setTimeout(() => el.style.border = original, {int(duration*1000)});
        }}"""
    )