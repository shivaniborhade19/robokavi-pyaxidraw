import os
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from poem_genrator import generate_poem
from svg_creator import save_poem_as_svg
from tes2 import plot_svg  # Assuming plot_svg function is defined in tes2.py

app = Flask(__name__, template_folder='templates')
CORS(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generate-poem', methods=['POST'])
def generate():
    data = request.get_json()
    name = data.get("name", "").strip()
    subject = data.get("subject", "").strip()
    language = data.get("language", "mr")

    if not name or not subject:
        return jsonify({"error": "Name and subject required."}), 400

    try:
        # 1. Generate poem
        poem = generate_poem(name, subject, language)
        filename_base = f"{name}_{subject}".replace(" ", "_")

        # 2. Generate and optimize SVG
        final_path = save_poem_as_svg(poem, filename_base)

        if not final_path:
            raise ValueError("SVG generation failed or returned None.")

        time.sleep(1)  # ensure file system is ready

        # 3. Plot Robo_Box.svg first
        template_path = os.path.join(os.path.dirname(__file__),
                                     "outline_traced.svg")
        if os.path.exists(template_path):
            plot_svg(template_path)
        else:
            print("⚠️ Robo_Box.svg not found at:", template_path)

        # 4. Plot final SVG
        plot_svg(final_path)

        return jsonify({
            "success": True,
            "message": "Poem written successfully!",
            "svg_filename": os.path.basename(final_path),
            "svg_path": final_path
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "error": f"SVG generation or plotting failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=False)
