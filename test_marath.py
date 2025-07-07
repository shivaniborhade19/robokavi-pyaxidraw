import os
import subprocess


def save_marathi_svg():
    poem_text = [
        "सूर्य उगवतो रोज सकाळी",
        "पाखरं करतात किलबिलाट",
        "मनात उमटते एक नवी सुरावट"
    ]
    filename_base = "marathi_test"
    base_dir = os.getcwd()

    svg_path = os.path.join(base_dir, f"{filename_base}.svg")
    vector_path = os.path.join(base_dir, f"{filename_base}_vector.svg")
    final_path = os.path.join(base_dir, f"{filename_base}_final.svg")
    # Create SVG with Unicode Devanagari text
    svg_content = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"
viewBox="0 0 800 600">
  <g font-family="Mukta" font-size="32px" text-anchor="middle"
  fill="#000">
'''

    line_spacing = 50
    start_y = 200

    for i, line in enumerate(poem_text):
        y = start_y + i * line_spacing
        svg_content += f'    <text x="400" y="{y}">{line}</text>\n'

    svg_content += '  </g>\n</svg>'

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print("✅ Base Marathi SVG saved:", svg_path)

    # Convert to stroked path using Inkscape (just like GUI)
    try:
        subprocess.run([
            r"C:\Program Files\Inkscape\bin\inkscape.com",
            svg_path,
            '--export-type=svg',
            f'--export-filename={vector_path}',
            '--export-text-to-path'  # ✅ critical for Devanagari
        ], check=True, timeout=60)
        print("✅ Vector (outlined) SVG saved:", vector_path)
    except Exception as e:
        print("❌ Inkscape failed:", e)
    try:
        subprocess.run([
            "vpype", "read", vector_path,
            "splitall", "linemerge", "reloop", "linesort",
            "write", final_path
        ], check=True, timeout=15)
        print("✅ Final cleaned SVG for plotting:", final_path)
    except Exception as e:
        print("❌ Vpype failed:", e)
        return


if __name__ == '__main__':
    save_marathi_svg()
