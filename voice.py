import pyttsx3

engine = pyttsx3.init()
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
print("Available voices:", len(voices))

engine.say("Your dental clinic timings are Monday to Saturday, twelve PM to nine PM.")
engine.runAndWait()

print("Speech test completed.")