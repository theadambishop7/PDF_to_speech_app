from flask import Flask, url_for, render_template, redirect, request, flash, get_flashed_messages
from werkzeug.utils import secure_filename
from gtts import gTTS
import os
import PyPDF2

app = Flask(__name__)
app.secret_key = 'jkqhwiuh1j34nri1j243u8orih1biwledbqwe'
path_to_save = "/static/speech-files/speech.mp3"


def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:  # iterate through each page
            text += page.extract_text()
    return text


def execute(text_to_read):
    tts = gTTS(text=text_to_read, lang='en')  # Create a gTTS object
    tts.save("static/speech-files/speech.mp3")  # Save the speech audio into a file


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if 'file' not in request.files:
        flash('No file part')
        return redirect("/")
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect("/")
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.getcwd(), filename)
        file.save(file_path)  # Save the file temporarily
        text = extract_text_from_pdf(file_path)
        os.remove(file_path)  # Remove the file after reading
        execute(text)
        flash('mp3_ready')
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
