import argparse
import pdfkit
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def create_pdf():
    try:
        title = request.form.get('title')
        html_content = request.form.get('html')

        if not title or not html_content:
            return jsonify({"success": False, "message": "Missing required parameters"}), 400

        pdf_output = pdfkit.from_string(html_content, False)

        if pdf_output:
            pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')
            return jsonify({"success": True, "pdf": pdf_base64})
        else:
            return jsonify({"success": False, "message": "Failed to generate PDF"}), 500
    except ModuleNotFoundError as e:
        return jsonify({"success": False, "message": f"ModuleNotFoundError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask app to generate PDF")
    parser.add_argument('host', type=str, help="Host IP address")
    parser.add_argument('port', type=int, help="Port number")


    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
