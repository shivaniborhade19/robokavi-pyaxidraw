import subprocess
import os


def save_poem_as_svg(poem_text, filename_base, font_family="Lohit Devanagari"):
    """
    Generates an SVG from Marathi text, converts text to paths using Inkscape,
    and optionally optimizes for AxiDraw using vpype.

    Args:
        poem_text (str): The Marathi poem text.
        filename_base (str): Base name for the output SVG files.
        font_family (str): The font family to use for the Marathi text.
                           Ensure this font is installed on the system where
                           Inkscape runs.
                           "Lohit Devanagari", "Noto Sans Devanagari",
                           or "Mangal" are common.
    Returns:
        str: The path to the final optimized SVG, or the vector
        SVG if vpype fails,
             or None if Inkscape conversion fails.
    """
    svg_path = f"{filename_base}.svg"
    vector_path = f"{filename_base}_vector.svg"

    # Define the Inkscape executable path (adjust if necessary for your system)
    inkscape_executable = "C:/Program Files/Inkscape/bin/inkscape.exe"
    if not os.path.exists(inkscape_executable):
        print(
            f"\u274C Inkscape executable not found at: {inkscape_executable}")
        print("""Please adjust the 'inkscape_executable'
              variable to your Inkscape installation path.""")
        return None

    # Step 1: Write base text SVG
    lines = [
        line.strip() for line in poem_text.strip().split("\n") if line.strip()]
    # Calculate height based on number of lines
    line_height = 50
    start_y = 100
    # Starting y position for the first line
    svg_height = start_y + len(lines) * line_height + 50
    # Add some padding

    svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="800" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <g font-family="{font_family}" font-size="32" text-anchor="middle"
  fill="#000">
'''
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        svg += f'    <text x="400" y="{y}">{line}</text>\n'
    svg += "  </g>\n</svg>"

    try:
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"\u2705 Base SVG written: {svg_path}")
    except IOError as e:
        print(f"\u274C Failed to write base SVG: {e}")
        return None

    # Step 2: Convert to vector path with Inkscape 1.2 using --actions
    inkscape_command = [
        inkscape_executable,
        svg_path,
        f"--export-filename={vector_path}",
        "--actions=select-all;object-to-path;export-do"
        # Select all objects and convert to path, then export
    ]
    try:
        print(f"Attempting Inkscape conversion: {' '.join(inkscape_command)}")
        result = subprocess.run(
            inkscape_command,
            check=True,
            timeout=60,
            # Increased timeout to 60 seconds
            capture_output=True,
            # Capture output for better error messages
            text=True
        )
        print("\u2705 Vector SVG exported via Inkscape:", vector_path)
        if result.stdout:
            print("Inkscape Output (stdout):\n", result.stdout)
        if result.stderr:
            print("Inkscape Errors (stderr):\n", result.stderr)
        return vector_path
    except subprocess.CalledProcessError as e:
        print(f"""\u274C Inkscape path
              conversion failed (return code {e.returncode}):""")
        print(f"Command: {' '.join(e.cmd)}")
        print("Inkscape stdout:\n", e.stdout)
        print("Inkscape stderr:\n", e.stderr)
        print("""Ensure the specified font is installed and Inkscape path is
              correct.""")
        return None
    except subprocess.TimeoutExpired:
        print("\u274C Inkscape path conversion timed out after 60 seconds.")
        return None
    except FileNotFoundError:
        print(f"""\u274C Inkscape executable not found.
              Make sure '{inkscape_executable}' is correct.""")
        return None
    except Exception as e:
        print(
            f"""\u274C An unexpected error occurred during Inkscape
            conversion: {e}""")
        return None
