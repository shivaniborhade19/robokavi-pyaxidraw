import subprocess


def save_poem_as_svg(poem_text, filename_base):
    final_path = f"{filename_base}_final.svg"

    try:
        # Prepare vpype text block with "line" before each full line
        lines = poem_text.strip().split("\n")
        vpype_args = []
        for line in lines:
            if line.strip():
                vpype_args.extend(["line", line.strip()])

        cmd = [
            "vpype",
            "begin",
            "text",
            "-f", "futural",   # You can try others like 'timesr'
            "-s", "24",
            "-p", "800x600",
            *vpype_args,
            "end",
            "linesort",
            "write", final_path
        ]

        subprocess.run(cmd, check=True, timeout=10)
        print("✅ Final stroke SVG created:", final_path)
        return final_path

    except Exception as e:
        print("❌ SVG creation failed:", str(e))
        return None
