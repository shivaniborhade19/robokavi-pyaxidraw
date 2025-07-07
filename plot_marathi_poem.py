import os
import subprocess
from pyaxidraw import axidraw

# === CONFIGURATION ===
INKSCAPE_PATH = r"C:\Program Files\Inkscape\bin\inkscape.com"
SVG_OUTPUT_BASE_DIR = r"C:\Users\hp\Downloads\AxiDraw_API(3)\AxiDraw_API_396"
FILENAME_BASE = "marathi_poem_test"

# === MARATHI TEXT (3 lines) ===
poem_text = """
सूर्य उगवतो रोज नवा,
प्रकाश देतो जीवनाला,
हीच जीवनाची नवी कथा।
"""


def save_and_convert_svg(poem_text, filename_base, save_dir=None):
    if save_dir is None:
        save_dir = SVG_OUTPUT_BASE_DIR

    os.makedirs(save_dir, exist_ok=True)

    # Paths
    svg_path = os.path.join(save_dir, f"{filename_base}.svg")
    svg_vector_path = os.path.join(save_dir, f"{filename_base}_vector.svg")
    # Layout settings
    svg_width, svg_height = 800, 600
    font_size, line_spacing = 28, 50
    font_family = "HersheySans 1"  # You can change this if needed
    lines = poem_text.strip().splitlines()
    total_height = (len(lines) - 1) * line_spacing
    start_y = (svg_height // 2) - (total_height // 2)

    # SVG with text
    svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}"
height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <g fill="none" stroke="#000" stroke-width="1">
'''

    for i, line in enumerate(lines):
        y = start_y + i * line_spacing
        svg_content += f'''    <text x="{svg_width//2}" y="{y}"
        font-family="{font_family}" font-size="{font_size}px"
        text-anchor="middle">{line}</text>\n'''

    svg_content += '  </g>\n</svg>'

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("✅ SVG saved:", svg_path)

    # Inkscape: Convert text to path
    try:
        subprocess.run([
            INKSCAPE_PATH,
            svg_path,
            '--export-type=svg',
            f'--export-filename={svg_vector_path}',
            '--actions=select-all;object-to-path;export-do;quit'
        ], check=True, timeout=20)
        print("✅ Text converted to path:", svg_vector_path)
        return svg_vector_path  # ✅ Return the path here!
    except Exception as e:
        print("❌ Inkscape conversion failed:", e)
        return None


def plot_with_axidraw(svg_vector_path):
    ad = axidraw.AxiDraw()
    if not ad.connect():
        print("❌ AxiDraw not connected.")
        return

    ad.options.pen_pos_down = 30      # adjust as needed
    ad.options.pen_pos_up = 70        # adjust as needed
    ad.options.speed_pendown = 25     # plotting speed
    ad.options.speed_penup = 75       # pen-up travel speed
    ad.options.accel = 15
    ad.options.model = 2              # most recent models
    ad.options.units = 1              # SVG units (mm)

    ad.plot_setup(svg_vector_path)
    ad.plot_run()
    print("✅ Done plotting.")
    ad.disconnect()


# === RUN THE PIPELINE ===
svg_result = save_and_convert_svg(poem_text, FILENAME_BASE,
                                  SVG_OUTPUT_BASE_DIR)
if svg_result:
    plot_with_axidraw(svg_result)
# At the very end of the function
else:
    print("❌ Plotting skipped due to SVG error.")
