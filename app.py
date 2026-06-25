from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import uuid

# Load environment variables
load_dotenv()

# Flask App
app = Flask(__name__)

# Upload Folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Gemini Client
client = genai.Client(api_key=API_KEY)


# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("home.html")


# ==========================
# Analyze Food Combination
# ==========================
@app.route("/check", methods=["POST"])
def check():

    try:

        food1 = request.form.get("food1", "").strip()
        food2 = request.form.get("food2", "").strip()
        language = request.form.get("language", "English")

        image_name = None

        # Validation
        if not food1 or not food2:
            return render_template(
                "result.html",
                result="Please enter both food items.",
                image_name=None,
                food1=food1,
                food2=food2
            )

        # Image Upload
        uploaded_file = request.files.get("food_image")

        if uploaded_file and uploaded_file.filename:

            ext = os.path.splitext(
                secure_filename(uploaded_file.filename)
            )[1]

            unique_filename = (
                str(uuid.uuid4()) + ext
            )

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                unique_filename
            )

            uploaded_file.save(filepath)

            image_name = unique_filename

        # Gemini Prompt
        prompt = f"""
You are FoodSafeAI.

Respond in {language}.

The user ate:

Food 1: {food1}
Food 2: {food2}

Analyze BOTH foods together.

Return exactly in this format:

SAFETY_SCORE:
(score out of 100)

SAFETY_STATUS:
(Safe / Unsafe / Use With Caution)

POSSIBLE_EFFECTS:
(List effects)

SYMPTOMS:
(List symptoms)

SCIENTIFIC_EVIDENCE:
(Scientific explanation)

TRADITIONAL_BELIEFS:
(Traditional beliefs)

ADVICE:
(Practical advice)

DOCTOR_WARNING:
(When to see a doctor)

FINAL_RECOMMENDATION:
(Final conclusion)

IMPORTANT:
Analyze the combination of both foods.
Do not analyze them separately.
"""

        # Gemini Request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text

        return render_template(
            "result.html",
            result=result,
            image_name=image_name,
            food1=food1,
            food2=food2
        )

    except Exception as e:

        print("ERROR:", e)

        return render_template(
            "result.html",
            result=f"Error: {str(e)}",
            image_name=None,
            food1="",
            food2=""
        )


# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )