import subprocess


def save_poem_as_svg(poem_text, filename_base):
    svg_path = f"{filename_base}.svg"
    vector_path = f"{filename_base}_vector.svg"
    final_path = f"{filename_base}_final.svg"

    # Step 1: Write base text SVG
    lines = [
        line.strip() for line in poem_text.strip().split("\n") if line.strip()]
    svg = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <g font-family="sans-serif" font-size="32" text-anchor="middle"
  fill="#000">
'''
    for i, line in enumerate(lines):
        y = 200 + i * 50
        svg += f'    <text x="400" y="{y}">{line}</text>\n'
    svg += "  </g>\n</svg>"

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("\u2705 Base SVG written:", svg_path)

    # Step 2: Convert to vector path with Inkscape 1.2
    try:
        subprocess.run([
            "C:/Program Files/Inkscape/bin/inkscape.exe", svg_path,
            "--export-type=svg",
            f"--export-filename={vector_path}",
            "--export-text-to-path"
        ], check=True, timeout=30)

        print("\u2705 Vector SVG exported via Inkscape:", vector_path)
    except Exception as e:
        print("\u274C Inkscape path conversion failed:", e)
        return None

    # Step 3: Optional - optimize with vpype
    # (can be skipped if pen paths already clean)
    try:
        subprocess.run([
            "vpype", "read", vector_path, "linesort", "write", final_path
        ], check=True, timeout=10)
        print("\u2705 Final optimized SVG:", final_path)
        return final_path
    except Exception as e:
        print(
            "\u274C Vpype optimization failed, using vector SVG as fallback:",
            e)
        return vector_path
