from flask import Flask, render_template_string, request
from pathlib import Path
import json

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base.json"

with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
    clinic = json.load(file)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bijay Dental Clinic | AI Assistant</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #e0f7fa, #eef4ff);
            color: #243447;
            min-height: 100vh;
            padding: 40px 15px;
        }

        .box {
            background: white;
            max-width: 700px;
            margin: 30px auto;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 35px rgba(0, 70, 100, 0.12);
            text-align: center;
        }

        .icon {
            font-size: 55px;
            margin-bottom: 10px;
        }

        h1 {
            color: #087e8b;
            margin-bottom: 10px;
            font-size: 32px;
        }

        h3 {
            color: #34495e;
            margin-top: 10px;
        }

        .description {
            color: #64748b;
            line-height: 1.6;
            margin-bottom: 25px;
        }

        form {
            display: flex;
            gap: 10px;
            margin-top: 25px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 15px;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #087e8b;
        }

        button {
            padding: 15px 25px;
            background: #087e8b;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #066570;
        }

        .answer {
            margin-top: 25px;
            padding: 20px;
            background: #e8f8f5;
            border-left: 5px solid #087e8b;
            border-radius: 10px;
            text-align: left;
            line-height: 1.7;
            overflow-wrap: anywhere;
        }

        .footer {
            margin-top: 25px;
            color: #64748b;
            font-size: 13px;
        }

        @media (max-width: 500px) {
            .box {
                padding: 22px;
            }

            h1 {
                font-size: 25px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <div class="box">
        <div class="icon">🦷</div>

        <h1>BIJAY DENTAL CLINIC</h1>
        <h3>AI Dental Assistant</h3>

        <p class="description">
            Welcome! Ask our AI assistant about clinic timings,
            location, consultation fees, and dental treatments.
        </p>

        <form method="POST">
            <input
                type="text"
                name="question"
                placeholder="Type your question here..."
                required
            >
            <button type="submit">Ask Now</button>
        </form>
<h2>📅 Book an Appointment</h2>

<form method="POST">
    <input type="hidden" name="booking" value="yes">

    <input type="text" name="patient_name"
           placeholder="Your full name" required>

    <input type="tel" name="phone"
           placeholder="Your phone number" required>

    <input type="date" name="appointment_date" required>

    <input type="time" name="appointment_time" required>

    <input type="text" name="reason"
           placeholder="Reason for visit" required>

    <button type="submit">Request Appointment</button>
</form>
        {% if answer %}
    <div class="answer">
        <strong>AI Dental Assistant:</strong>
        <p id="answerText">{{ answer }}</p>
        <button type="button" onclick="speakAnswer()">
            🔊 Speak Again
        </button>
    </div>
{% endif %}

        <div class="footer">
            Your dental care matters to us.
            <br>
            For emergencies, contact the clinic directly.
        </div>
    </div>
    <script>
function speakAnswer() {
    const answer = document.getElementById("answerText");

    if (!answer) return;

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(answer.innerText);
    speech.lang = "en-IN";
    speech.rate = 1;

    window.speechSynthesis.speak(speech);
}

window.addEventListener("load", function() {
    if (document.getElementById("answerText")) {
        speakAnswer();
    }
});
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":

        # Handle appointment requests
        if request.form.get("booking") == "yes":
            name = request.form.get("patient_name", "")
            date = request.form.get("appointment_date", "")
            time = request.form.get("appointment_time", "")

            answer = (
                f"Thank you, {name}. Your appointment request "
                f"for {date} at {time} has been received. "
                "Please wait for confirmation from the clinic."
            )

        # Handle questions from the Ask Now form
        else:
            question = request.form.get("question", "").strip().lower()

            if not question:
                answer = "Please type a question."

            elif any(word in question for word in [
                "fee", "price", "cost", "charge",
                "consultation", "500", "rupee", "rupees"
            ]):
                answer = (
                    f"Our consultation fee is "
                    f"{clinic.get('consultation_fee', '500 INR')}."
                )

            elif any(word in question for word in [
                "timing", "time", "open", "hours", "close"
            ]):
                answer = str(
                    clinic.get(
                        "timings",
                        "Please contact the clinic for timings."
                    )
                )

            elif any(word in question for word in [
                "address", "location", "where", "direction"
            ]):
                answer = str(
                    clinic.get(
                        "address",
                        "Please contact the clinic for its address."
                    )
                )

            elif any(word in question for word in [
                "emergency", "urgent", "pain", "swelling"
            ]):
                answer = (
                    "For a dental emergency, please contact the clinic "
                    "directly. If you have difficulty breathing, severe "
                    "swelling, or uncontrolled bleeding, seek urgent "
                    "medical care."
                )

            elif any(word in question for word in [
                "service", "treatment", "cleaning", "root canal",
                "braces", "whitening", "filling", "crown", "gum"
            ]):
                services = clinic.get("services", [])
                answer = (
                    ", ".join(services)
                    if isinstance(services, list)
                    else str(services)
                )

            elif "appointment" in question or "book" in question:
                answer = (
                    "Please complete the appointment form below "
                    "to request an appointment."
                )

            else:
                answer = (
                    "Sorry, I don't have that information yet. "
                    "Please contact the clinic staff."
                )

    return render_template_string(HTML_PAGE, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
