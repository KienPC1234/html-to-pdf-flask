### Flask Application to Generate PDF from HTML

This application uses Flask and PDFKit to convert HTML to PDF and returns it as a base64 string. You can run this app in two ways: directly via Flask or using uWSGI for production environments.

---

### 1. Install Dependencies

Before running the app, ensure that the necessary dependencies are installed:

1. **Install Python** (if not already installed):
   ```bash
   sudo apt install python3 python3-pip
   ```

2. **Install Python libraries**:
   ```bash
   pip install flask pdfkit
   ```

3. **Install wkhtmltopdf**:
   This app uses `wkhtmltopdf` to convert HTML to PDF. Install `wkhtmltopdf` according to your operating system:

   - **Linux (Debian/Ubuntu)**:
     ```bash
     sudo apt-get install wkhtmltopdf
     ```

   - **Fedora / RHEL / CentOS**:
     ```bash
     sudo yum install wkhtmltopdf
     ```

   - **Windows**:
     Download the installer from the [wkhtmltopdf downloads page](https://wkhtmltopdf.org/downloads.html) and add the folder containing the `wkhtmltopdf` binary to your PATH.

   - **Mac**:
     Install via Homebrew:
     ```bash
     brew install wkhtmltopdf
     ```

---

### 2. Running the Flask App

#### Option 1: Run Directly with Flask

1. Start the application with the desired `host` and `port` arguments:

   ```bash
   python main.py --host 0.0.0.0 --port 8888
   ```

   **Note**: You can change the `host` and `port` values as needed.

2. The app will be running and accessible at `http://0.0.0.0:8888`.

#### Option 2: Run with uWSGI

1. **Install uWSGI**:
   ```bash
   pip install uwsgi
   ```

2. Create the `uwsgi.ini` configuration file with the following content:

   ```ini
   [uwsgi]
   module = wsgi:app

   http = 127.0.0.1:8888
   processes = 4
   threads = 2
   logto = /var/log/uwsgi/myapp.log
   chdir = /path/to/your/application
   virtualenv = /path/to/your/virtualenv
   ```

3. **Run uWSGI**:
   ```bash
   uwsgi --ini uwsgi.ini
   ```

---

### 3. Using the API

- **POST Request** to the `/` endpoint with the following parameters:
  - **`title`**: The title of the PDF.
  - **`html`**: The HTML content to be converted to a PDF.

  **Example cURL**:
  ```bash
  curl -d "title=Hello&html=Hello, World" -X POST -H "Content-Type: application/x-www-form-urlencoded" http://localhost:8888
  ```

  **Response**:
  ```json
  {
      "success": true,
      "pdf": "base64 encoded pdf content"
  }
  ```

  **Error Handling**: If an error occurs during the PDF generation or if the required parameters are missing, the response will include a `"success": false` status with a message describing the issue.

  **Example error response**:
  ```json
  {
      "success": false,
      "message": "Missing required parameters"
  }
  ```

---

### 4. Project Structure

Your project should have the following structure:

```
/your-application
    ├── main.py           # Flask app
    ├── wsgi.py           # Entry point for uWSGI
    ├── requirements.txt  # Required libraries
    └── uwsgi.ini         # uWSGI configuration file
```

---

### 5. Troubleshooting

- **ModuleNotFoundError**: Ensure that all Python libraries are installed correctly.
- **PDFKit errors**: Ensure that `wkhtmltopdf` is installed and accessible by your Flask application.

---

Thank you for using our app!