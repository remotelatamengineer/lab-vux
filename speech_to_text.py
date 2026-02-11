import speech_recognition as sr
import os

def speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Increase the pause threshold (time in seconds that counts as the end of a phrase)
    # Default is 0.8; making it larger allows for longer pauses between words.
    recognizer.pause_threshold = 2.0

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Speak now!")
        
        try:
            # Listen for the user's input
            # timeout: maximum seconds to wait for speech to start
            # phrase_time_limit: maximum seconds for the phrase once it starts
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=60)
            print("Processing speech...")
            
            # Recognize speech using Google Web Speech API with Brazilian Portuguese language
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"I heard: {text}")
            
            # Save the text to a file
            output_file = "prompt.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"Success! Text saved to '{output_file}'")
            
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    speech_to_text()
