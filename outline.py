import subprocess
import os
import time


def convert_image_to_svg_paths(
        image_path,
        output_svg_path,
        inkscape_executable=(
            "C:/Program Files/Inkscape/bin/inkscape.exe")):
    """
    Converts a bitmap image (like JPG or PNG) to an SVG with vector paths
    using Inkscape's trace bitmap functionality via subprocess.

    Args:
        image_path (str): The path to the input bitmap image
        (e.g., 'outline.jpg').
        output_svg_path (str): The desired path for the output SVG file.
        inkscape_executable (str): The path to the Inkscape executable.
                                   Ensure Inkscape 1.0 or newer is installed.
                                   Examples:
                                   - Windows:
                                   "C:/Program Files/Inkscape/bin/inkscape.exe"
                                   - macOS:
                                   "/Applications/Inkscape.app/Contents/MacOS/inkscape"
                                   - Linux:
                                   "inkscape" (
                                       if in PATH, otherwise
                                       full path like "/usr/bin/inkscape")

    Returns:
        str: The path to the generated SVG file if successful, None otherwise.
    """
    # Check if the Inkscape executable exists
    if not os.path.exists(inkscape_executable):
        print(f"""\u274C Error: Inkscape executable not found at:
              {inkscape_executable}""")
        print("""Please adjust the 'inkscape_executable' variable to your
              Inkscape installation path.""")
        return None

    # Check if the input image file exists
    if not os.path.exists(image_path):
        print(f"\u274C Error: Input image not found at: {image_path}")
        return None

    # Construct the Inkscape command for tracing a bitmap to vector paths.
    # This command directly opens the image, applies the trace bitmap action,
    # and then exports the result as a plain SVG.
    inkscape_command = [
        inkscape_executable,
        image_path,
        f"--export-filename={output_svg_path}",
        "--export-type=svg",
        # Explicitly set export type to SVG
        # Actions:
        # 1. import-type:embed; import-png-dpi-from-file;: Automatically
        # handles bitmap import dialog.
        # 2. org.inkscape.effect.bitmap.trace.path(...): Traces the bitmap,
        # creating new paths.
        # 3. selection-clear; select-by-type:image; delete;: Clears selection,
        # selects original image, and deletes it.
        # 4. select-all; export-do: Selects remaining objects (traced paths)
        # and exports.
        """--actions=import-type:embed; import-png-dpi-from-file;
        org.inkscape.effect.bitmap.trace.path(
            mode='monochrome', threshold=0.45); selection-clear;
            select-by-type:image; delete; select-all; export-do"""
    ]

    try:
        print(f"""Attempting Inkscape image tracing. Command:
              {' '.join(inkscape_command)}""")
        # Execute the Inkscape command using subprocess
        result = subprocess.run(
            inkscape_command,
            check=True,
            # Raise CalledProcessError
            # if the command returns a non-zero exit code
            timeout=120,
            # Set a timeout (in seconds) for the command to complete
            capture_output=True,
            # Capture stdout and stderr
            text=True            # Decode stdout/stderr as text
        )
        print(f"""\u2705 Inkscape command executed. Checking for output file:
              {output_svg_path}""")

        # Add a small delay to ensure the file system has time to write
        time.sleep(1)

        # --- IMPORTANT VERIFICATION STEP ---
        if os.path.exists(output_svg_path):
            print(f"""\u2705 Success: Image successfully
                  traced and exported to:
                  {output_svg_path}""")
            if result.stdout:
                print("Inkscape Output (stdout):\n", result.stdout)
            if result.stderr:
                print("Inkscape Errors (stderr):\n", result.stderr)
            return output_svg_path
        else:
            print(f"""\u274C Error: Inkscape reported success, but the file was
                  NOT found at: {output_svg_path}""")
            print("""This might indicate a permissions issue,
                  an incorrect path,""")
            print("or Inkscape saving to a different location.")
            if result.stdout:
                print("Inkscape Output (stdout):\n", result.stdout)
            if result.stderr:
                print("Inkscape Errors (stderr):\n", result.stderr)
            return None

    except subprocess.CalledProcessError as e:
        print(f"""\u274C Error: Inkscape image tracing failed
              (return code {e.returncode}).""")
        print(f"Command executed: {' '.join(e.cmd)}")
        print("Inkscape stdout:\n", e.stdout)
        print("Inkscape stderr:\n", e.stderr)
        print("""Please ensure Inkscape is installed correctly
              and the input image path is valid.""")
        return None
    except subprocess.TimeoutExpired:
        print(f"""\u274C Error: Inkscape image tracing timed out after
              120 seconds for {image_path}.""")
        return None
    except FileNotFoundError:
        print(f"""\u274C Error: Inkscape executable not found.
              Make sure the path '{inkscape_executable}' is correct.""")
        return None
    except Exception as e:
        print(f"""\u274C An unexpected error occurred during Inkscape
              image tracing: {e}""")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    # Define the path to your input image
    # (assuming it's in the same directory as this script)
    input_image_file = "outline.jpg"
    # Define the desired path for the output SVG file
    output_svg_file = "outline_traced.svg"

    # IMPORTANT: Adjust this path to your Inkscape installation
    # For Windows:
    inkscape_path = "C:/Program Files/Inkscape/bin/inkscape.exe"
    # For macOS:
    # inkscape_path = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
    # For Linux (if inkscape is in your system's PATH):
    # inkscape_path = "inkscape"
    # Or for a specific path on Linux:
    # inkscape_path = "/usr/bin/inkscape"

    print(f"Attempting to convert '{input_image_file}' to '{output_svg_file}'")
    traced_svg_path = convert_image_to_svg_paths(input_image_file,
                                                 output_svg_file,
                                                 inkscape_path)

    if traced_svg_path:
        print(f"\nConversion complete! Traced SVG saved to: {traced_svg_path}")
        print("""You can now open this SVG file in a web browser
              or an SVG editor.""")
    else:
        print("""\nImage tracing failed. Please check the error messages above
              and your Inkscape installation.""")
