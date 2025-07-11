import os
import subprocess
import time # For a small delay to ensure file system operations complete

def create_rectangle_with_title_svg(output_filename="robo_kavi_box_vectorized.svg",
                                    width_mm=150, height_mm=100, # Increased default size
                                    stroke_width_mm=0.5, stroke_color="#000000",
                                    title_text="RoboKavi",
                                    title_font_size_mm=1, # Adjusted default font size
                                    title_offset_from_top_mm=15, # Adjusted default offset
                                    footer_text="made in jalihal", # New parameter for footer text
                                    footer_font_size_mm=0.9, # Smaller font size for footer
                                    footer_offset_from_bottom_mm=20, # Offset from bottom border
                                    font_family="Arial, sans-serif", # Common font for both texts
                                    inkscape_executable="/home/shree/Downloads/Inkscape-b0a8486-x86_64.AppImage"): # Inkscape path
    """
    Generates a clean SVG file containing a rectangle with title and footer text.
    It uses Inkscape via subprocess to convert all text to vector paths,
    making it ideal for plotters that require vectorized text.

    Args:
        output_filename (str): The name of the SVG file to create.
                               It will be saved in the same directory as this script.
        width_mm (float): The width of the rectangle in millimeters.
        height_mm (float): The height of the rectangle in millimeters.
        stroke_width_mm (float): The thickness of the rectangle's outline in millimeters.
        stroke_color (str): The color of the rectangle's outline (e.g., "#000000" for black).
        title_text (str): The text to be placed as a title at the top.
        title_font_size_mm (float): The font size for the title text in millimeters.
        title_offset_from_top_mm (float): The vertical distance from the top edge of the
                                         rectangle to the baseline of the title text.
        footer_text (str): The text to be placed as a footer at the bottom.
        footer_font_size_mm (float): The font size for the footer text in millimeters.
        footer_offset_from_bottom_mm (float): The vertical distance from the bottom edge of the
                                              rectangle to the baseline of the footer text.
        font_family (str): The font family for both text elements.
                           Ensure this font is installed on the system where Inkscape runs.
        inkscape_executable (str): The path to the Inkscape executable.
                                   Ensure Inkscape 1.0 or newer is installed for --actions.

    Returns:
        str: The full path to the generated SVG file if successful, None otherwise.
    """
    # Check if the Inkscape executable exists
    if not os.path.exists(inkscape_executable):
        print(f"""\u274C Error: Inkscape executable not found at:
              {inkscape_executable}""")
        print("""Please adjust the 'inkscape_executable' variable to your
              Inkscape installation path.""")
        return None

    # Calculate viewBox dimensions. Using 1 unit = 1mm for simplicity.
    rect_x = stroke_width_mm / 2
    rect_y = stroke_width_mm / 2
    rect_width = width_mm - stroke_width_mm
    rect_height = height_mm - stroke_width_mm

    # Calculate title text position
    title_text_x = width_mm / 2 # Center horizontally
    title_text_y = title_offset_from_top_mm # Vertical position (baseline)

    # Calculate footer text position
    footer_text_x = width_mm / 2 # Center horizontally
    # Y position is total height minus offset from bottom
    footer_text_y = height_mm - footer_offset_from_bottom_mm

    # --- Step 1: Create a temporary SVG with rectangle and SVG <text> elements ---
    temp_svg_filename = "temp_" + output_filename
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_svg_path = os.path.join(script_dir, temp_svg_filename)
    final_output_path = os.path.join(script_dir, output_filename)

    temp_svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="{width_mm}mm"
   height="{height_mm}mm"
   viewBox="0 0 {width_mm} {height_mm}"
   version="1.1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs2" />
  <g
     id="layer1">
    <rect
       style="fill:none;stroke:{stroke_color};stroke-width:{stroke_width_mm};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       id="rect1"
       width="{rect_width}"
       height="{rect_height}"
       x="{rect_x}"
       y="{rect_y}" />
    <text
       style="font-family:{font_family};font-size:{title_font_size_mm}mm;text-anchor:middle;fill:{stroke_color};stroke:none;"
       id="text_title"
       x="{title_text_x}"
       y="{title_text_y}">{title_text}</text>
    <text
       style="font-family:{font_family};font-size:{footer_font_size_mm}mm;text-anchor:middle;fill:{stroke_color};stroke:none;"
       id="text_footer"
       x="{footer_text_x}"
       y="{footer_text_y}">{footer_text}</text>
  </g>
</svg>'''
    # Note: For the temporary SVG, we set fill to stroke_color and stroke to none for text.
    # This is because Inkscape's object-to-path works on the fill of the text.
    # We will convert it back to fill:none;stroke:color; after vectorization.


    try:
        with open(temp_svg_path, "w", encoding="utf-8") as f:
            f.write(temp_svg_content)
        print(f"\u2705 Temporary SVG with text elements created: {temp_svg_path}")
    except IOError as e:
        print(f"\u274C Error writing temporary SVG file: {e}")
        return None

    # --- Step 2: Use Inkscape to convert text to path and save final SVG ---
    # The stroke width for text paths is typically half of the main border for a finer line.
    text_stroke_width = stroke_width_mm / 2

    inkscape_command = [
        inkscape_executable,
        temp_svg_path,
        f"--export-filename={final_output_path}",
        "--export-type=svg",
        # Actions:
        # 1. select-by-id:text_title; object-to-path; selection-set-style:fill:none;stroke:{stroke_color};stroke-width:{text_stroke_width};: Vectorize and style title text.
        # 2. select-by-id:text_footer; object-to-path; selection-set-style:fill:none;stroke:{stroke_color};stroke-width:{text_stroke_width};: Vectorize and style footer text.
        # 3. select-all; export-do: Select all objects (rectangle and new text paths) and export.
        "--actions=select-by-id:text_title; object-to-path; selection-set-style:fill:none;stroke:{stroke_color};stroke-width:{text_stroke_width};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1; select-by-id:text_footer; object-to-path; selection-set-style:fill:none;stroke:{stroke_color};stroke-width:{text_stroke_width};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1; select-all; export-do"
    ]

    try:
        print(f"""Attempting Inkscape text vectorization. Command:
              {' '.join(inkscape_command)}""")
        result = subprocess.run(
            inkscape_command,
            check=True,
            timeout=120,
            capture_output=True,
            text=True
        )
        print(f"\u2705 Inkscape command executed. Checking for final output file: {final_output_path}")

        time.sleep(1) # Small delay for file system write

        if os.path.exists(final_output_path):
            print(f"""\u2705 Success: SVG with vectorized text generated:
                  {final_output_path}""")
            if result.stdout:
                print("Inkscape Output (stdout):\n", result.stdout)
            if result.stderr:
                print("Inkscape Errors (stderr):\n", result.stderr)
            return final_output_path
        else:
            print(f"""\u274C Error: Inkscape reported success, but the final file was
                  NOT found at: {final_output_path}""")
            if result.stdout:
                print("Inkscape Output (stdout):\n", result.stdout)
            if result.stderr:
                print("Inkscape Errors (stderr):\n", result.stderr)
            return None

    except subprocess.CalledProcessError as e:
        print(f"""\u274C Error: Inkscape text vectorization failed
              (return code {e.returncode}).""")
        print(f"Command executed: {' '.join(e.cmd)}")
        print("Inkscape stdout:\n", e.stdout)
        print("Inkscape stderr:\n", e.stderr)
        print("Ensure Inkscape 1.0+ is installed and the font is available to Inkscape.")
        return None
    except subprocess.TimeoutExpired:
        print(f"""\u274C Error: Inkscape text vectorization timed out after
              120 seconds.""")
        return None
    except FileNotFoundError:
        print(f"""\u274C Error: Inkscape executable not found.
              Make sure the path '{inkscape_executable}' is correct.""")
        return None
    except Exception as e:
        print(f"""\u274C An unexpected error occurred during Inkscape
              vectorization: {e}""")
        return None
    finally:
        # --- Step 3: Clean up temporary SVG file ---
        if os.path.exists(temp_svg_path):
            try:
                os.remove(temp_svg_path)
                print(f"\u2705 Cleaned up temporary file: {temp_svg_path}")
            except OSError as e:
                print(f"\u274C Error deleting temporary file {temp_svg_path}: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # Define desired dimensions and output file
    output_file_name = "robo_kavi_box_with_footer_vectorized.svg" # Changed output filename for clarity
    box_width_mm = 200  # Increased to 200 mm wide
    box_height_mm = 150 # Increased to 150 mm tall
    line_thickness_mm = 0.5 # 0.5 mm thick line for the border

    # Title text specific settings
    title_text_content = "RoboKavi"
    title_font_size_mm = 2# Smaller font size for title
    title_offset_from_top_mm = 15 # More offset from top

    # Footer text specific settings
    footer_text_content = "made in jalihal"
    footer_font_size_mm = 2 # Smaller than title
    footer_offset_from_bottom_mm = 10 # Offset from bottom

    # IMPORTANT: Adjust this path to your Inkscape installation
    # For Windows:
    # inkscape_path = "C:/Program Files/Inkscape/bin/inkscape.exe"
    # For Linux (using AppImage path from your previous input):
    inkscape_path = "/home/shree/Downloads/Inkscape-b0a8486-x86_64.AppImage"
    # For macOS:
    # inkscape_path = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
    # For Linux (if inkscape is in your system's PATH):
    # inkscape_path = "inkscape"


    print(f"Generating a {box_width_mm}mm x {box_height_mm}mm rectangle with '{title_text_content}' and '{footer_text_content}'...")
    generated_svg_path = create_rectangle_with_title_svg(
        output_filename=output_file_name,
        width_mm=box_width_mm,
        height_mm=box_height_mm,
        stroke_width_mm=line_thickness_mm,
        title_text=title_text_content,
        title_font_size_mm=title_font_size_mm,
        title_offset_from_top_mm=title_offset_from_top_mm,
        footer_text=footer_text_content,
        footer_font_size_mm=footer_font_size_mm,
        footer_offset_from_bottom_mm=footer_offset_from_bottom_mm,
        inkscape_executable=inkscape_path # Pass the Inkscape executable path
    )

    if generated_svg_path:
        print(f"\nSVG created successfully at: {generated_svg_path}")
        print("You can now use this file with your AxiDraw plotter.")
        print("Remember to adjust pen height settings in your AxiDraw software/script for proper pen up/down.")
    else:
        print("\nFailed to generate SVG.")
