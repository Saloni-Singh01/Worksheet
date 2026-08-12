# Flask application for resume portal
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

import os
import subprocess

from database import get_connection


app = Flask(__name__)


# -----------------------------
# Folder Configuration
# -----------------------------

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create folders if they don't exist

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


# Allowed Word extensions

ALLOWED_EXTENSIONS = {
    "doc",
    "docx"
}


# Store currently uploaded file

uploaded_file = None


# -----------------------------
# Check File Extension
# -----------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# -----------------------------
# Home Page
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# Submit Registration
# -----------------------------

@app.route("/submit", methods=["POST"])
def submit_registration():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")


    if not name or not email or not phone:

        return jsonify({
            "success": False,
            "message": "Please fill all registration details."
        })


    try:

        connection = get_connection()

        cursor = connection.cursor()


        query = """
        INSERT INTO registrations
        (name, email, phone)
        VALUES (%s, %s, %s)
        """


        values = (
            name,
            email,
            phone
        )


        cursor.execute(
            query,
            values
        )


        connection.commit()


        cursor.close()
        connection.close()


        return jsonify({

            "success": True,

            "message":
            "Registration submitted successfully."

        })


    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "message":
            "Database error occurred."

        })


# -----------------------------
# Upload Resume
# -----------------------------

@app.route("/upload", methods=["POST"])
def upload_resume():

    global uploaded_file


    if "resume" not in request.files:

        return jsonify({

            "success": False,

            "message":
            "Please select a Word file."

        })


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({

            "success": False,

            "message":
            "No file selected."

        })


    # Check extension

    if not allowed_file(file.filename):

        return jsonify({

            "success": False,

            "message":
            "Only Word files (.doc and .docx) are allowed."

        })


    # Secure filename

    filename = secure_filename(
        file.filename
    )


    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    # Save file

    file.save(filepath)


    uploaded_file = filepath


    # Update database with filename

    try:

        connection = get_connection()

        cursor = connection.cursor()


        query = """
        UPDATE registrations
        SET resume_filename = %s
        WHERE id = (
            SELECT id
            FROM (
                SELECT id
                FROM registrations
                ORDER BY id DESC
                LIMIT 1
            ) AS latest
        )
        """


        cursor.execute(
            query,
            (filename,)
        )


        connection.commit()


        cursor.close()
        connection.close()


    except Exception as e:

        print(e)


    return jsonify({

        "success": True,

        "message":
        "Resume uploaded successfully.",

        "filename":
        filename

    })


# -----------------------------
# Convert Word → PDF
# -----------------------------

@app.route("/download-resume")
def download_resume():

    global uploaded_file


    if not uploaded_file:

        return "No resume uploaded.", 404


    if not os.path.exists(uploaded_file):

        return "Resume file not found.", 404


    try:

        # LibreOffice conversion

        subprocess.run(

            [
                "soffice",

                "--headless",

                "--convert-to",
                "pdf",

                "--outdir",
                CONVERTED_FOLDER,

                uploaded_file
            ],

            check=True

        )


    except Exception as e:

        print(e)

        return (
            "PDF conversion failed. "
            "Make sure LibreOffice is installed."
        ), 500


    # Get original filename

    original_name = os.path.basename(
        uploaded_file
    )


    # Remove .doc / .docx

    pdf_name = os.path.splitext(
        original_name
    )[0] + ".pdf"


    pdf_path = os.path.join(
        CONVERTED_FOLDER,
        pdf_name
    )


    if not os.path.exists(pdf_path):

        return "PDF file was not created.", 500


    # Download PDF

    return send_file(

        pdf_path,

        as_attachment=True,

        download_name=pdf_name,

        mimetype="application/pdf"

    )


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )