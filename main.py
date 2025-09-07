import argparse
import pdfkit
import base64
import sys
import traceback
import os
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

options = {
    "enable-local-file-access": None
}

BASE_PATH = os.getenv("BASE_PATH", "")

def rewrite_html_paths(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("/userdata/"):
            img["src"] = f"file://{BASE_PATH}{src}"

    return str(soup)


@app.route('/', methods=['POST'])
def create_pdf():
    try:
        title = request.form.get('title')
        html_content = request.form.get('html')

        if not title or not html_content:
            return jsonify({"success": False, "message": "Missing required parameters"}), 400

        html_content = rewrite_html_paths(html_content)
        pdf_output = pdfkit.from_string(html_content, False,options=options)

        if pdf_output:
            pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')
            return jsonify({"success": True, "pdf": pdf_base64})
        else:
            return jsonify({"success": False, "message": "Failed to generate PDF"}), 500

    except ModuleNotFoundError as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"success": False, "message": f"ModuleNotFoundError: {str(e)}"}), 500
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


def safe_run_app(host, port):
    """Chạy Flask app, không để crash toàn bộ app."""
    while True:
        try:
            print(f"Starting Flask app on {host}:{port}...", file=sys.stderr)
            app.run(host=host, port=port)
        except Exception as e:
            # In lỗi ra stderr nhưng không tắt chương trình
            print(f"[ERROR] Flask app crashed: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print("Restarting Flask app...", file=sys.stderr)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Flask app to generate PDF")
        parser.add_argument('host', type=str, help="Host IP address")
        parser.add_argument('port', type=int, help="Port number")
        args = parser.parse_args()

        safe_run_app(args.host, args.port)

    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
