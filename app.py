import json
from pathlib import Path
import pyttsx3
import speech_recognition as sr
from appointment import save_appointment

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
def speak(text):
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-c",
         "import pyttsx3; import sys; "
         "e=pyttsx3.init(); "
         "e.say(sys.argv[1]); e.runAndWait()",
         str(text)],
        check=False
    )
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Please speak clearly.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1.2
        recognizer.energy_threshold = 300

        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=10
            )

            print("Recognizing your speech...")
            text = recognizer.recognize_google(audio, language="en-IN")
            print("You said:", text)
            return text

        except sr.WaitTimeoutError:
            print("I could not hear you. Please try again.")
            return ""

        except sr.UnknownValueError:
            print("Sorry, I could not understand. Please speak again.")
            return ""

        except sr.RequestError:
            print("Speech recognition connection problem. Check your internet.")
            return ""

def get_user_response():
    print("\nChoose how to respond:")
    print("1. Speak")
    print("2. Type")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        return listen()
    elif choice == "2":
        return input("You: ").strip()
    else:
        print("Invalid choice. Please try again.")
        return get_user_response()
# Load dental clinic information
BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR.parent / "knowledge_base.json"

with open(json_path, "r", encoding="utf-8") as file:
    clinic = json.load(file)

print("Clinic information loaded successfully!")
welcome_message = f"Welcome to {clinic['clinic_name']}. How may I help you?"
print(welcome_message)
speak(welcome_message)
def book_appointment():
    print("\nAgent: Certainly! I can record your appointment request.")

    speak("May I know your name?")
    name = get_user_response()

    speak("What is your phone number?")
    phone = get_user_response()

    speak("What treatment do you need?")
    service = get_user_response()

    speak("Which day would you prefer?")
    date = get_user_response()

    speak("What time would you prefer?")
    time = get_user_response()

    print("\nAgent: Please confirm your appointment request.")
    print("Name:", name)
    print("Phone:", phone)
    print("Treatment:", service)
    print("Preferred day:", date)
    print("Preferred time:", time)

    speak("Would you like to confirm these details? Please say yes or no.")
    confirmation = get_user_response()

    print("Recognized confirmation:", repr(confirmation))

    confirmation = confirmation.lower().strip()
    if confirmation.startswith("yes") or confirmation == "yeah":
        save_appointment(name, phone, service, date, time)
        print("Agent: Your appointment request has been saved.")
        print("Agent: Clinic staff must confirm the actual appointment.")
        speak("Your appointment request has been saved.")
    else:
        print("Agent: No problem. Your request has not been saved.")
        speak("No problem. Your request has not been saved.")
def answer_question(question):
    question = question.lower()

    if "samay" in question or "timing kya hai" in question or "time kya hai" in question:
      return clinic["timings"]

    elif "pata" in question or "address kya hai" in question:
      return clinic["address"]

    elif "fees kitni" in question or "kitna paisa" in question or "kharcha" in question:
      return clinic["consultation_fee"]

    elif "appointment book" in question or "appointment chahiye" in question:
      return "Appointment book karne ke liye please type: book appointment."

    if "timing" in question or "hours" in question:
      return clinic["timings"]
    elif "address" in question or "location" in question:
      return clinic["address"]
    elif "emergency" in question:
      return "Please contact our clinic staff to confirm emergency availability."
    elif "service" in question or "treatment" in question:
      return ",".join(clinic["services"])
    elif "fee" in question or "cost" in question:
      return clinic["consultation_fee"]
    elif "sunday" in question:
      return "Please contact our clinic staff to confirm Sunday opening hours."

    elif "appointment" in question:
      return "You can ask me to book an appointment. I will record your preferred date and time."

    elif "teeth whitening" in question:
      return "Yes, teeth whitening is one of the services listed by our clinic."

    elif "root canal" in question:
      return "Our clinic lists root canal treatment among its services."
    
    else:
     return (
        "I don't have that information. "
        "Please contact our clinic staff for further assistance."
    )
print(f"Welcome to {clinic['clinic_name']}!")
print("Ask a question, or type 'exit' to stop.")

while True:
    print("\n--- BIJAY DENTAL CLINIC AI AGENT ---")
    print("1. Speak")
    print("2. Type")
    print("3. Exit")

    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        user_question = listen()

    elif choice == "2":
        user_question = input("You: ").strip()

    elif choice == "3":
        speak("Thank you for contacting Bijay Dental Clinic. Goodbye!")
        break

    else:
        print("Please choose 1, 2, or 3.")
        continue

    if not user_question:
        print("No question received. Please try again.")
        continue

    if "appointment" in user_question.lower() or "book" in user_question.lower():
        book_appointment()
    else:
        response = answer_question(user_question)
        print("Agent:", response)
        speak(response)