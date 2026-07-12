import os
import base64
from sarvamai import SarvamAI
from sarvamai.core.api_error import ApiError

from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get("API_KEY")
if not apikey:
    raise ValueError("API Key not found Please check your .env file.")

client = SarvamAI(api_subscription_key=apikey)

def textToSpeech(text, output_filename="output.wav"):

    print(f"\nGenerating audio")

    try:
        response = client.text_to_speech.convert(
            text=text,
            target_language_code="ta-IN",
            #without this target language the programe gives error
            model="bulbul:v3",
            speaker="shubh"
        )

        audioBytes = base64.b64decode(response.audios[0])

        with open(output_filename, "wb") as f:
            f.write(audioBytes)

        print(f"Audio saved to demo_audio.wav.\n")

    except ApiError as e:
        print(f"API Error during Text to Speech: {e.status_code} - {e.body}")

def speechToText(audio_filename):
    print(f"\nGenerating text from '{audio_filename}'")

    try:
        response = client.speech_to_text.transcribe(
            file=open(audio_filename, "rb"),
            model="saaras:v3",
            mode="transcribe"
        )

        print("Complete")
        print(f"Text Output:\n{response.transcript}\n")

    

    except ApiError as e:
         print(f"API Error: {e.status_code} - {e.body}")
    except FileNotFoundError:
         print(f"Could not find the audio file '{audio_filename}'")
    except Exception as e:
         print(f"An unknown error occurred: {e}")

def aiChatbot(text):
    response = client.chat.completions(
    model="sarvam-105b",
    
    messages=[
        {"role": "user", "content": userQuestion}
    ]
)
    print(response.choices[0].message.content)

    
    
    


if __name__ == "__main__":
    while True:
        print("\nSpeech & Text Converter using Sarvam AI")
        print("Press 1 for Text to Speech")
        print("Press 2 for Speech to Text")
        print("Press 3 for using AI Chatbot")
        print("Press 4 for Exit")

        choice = input("Enter your choice 1, 2, 3 or 4: ").strip()

        if choice == '1':
            user_text = input("\nEnter the text you want to convert: ")
            if user_text.strip():

                textToSpeech(user_text, "demo_audio.wav")
            else:
                print("No text entered going back to menu.")

        elif choice == '2':
            file_path = input("\nEnter the audio filename you want to convert to text (Example: 'audio_filename.mp3'): ").strip()

            if not file_path:
                file_path = "audio_filename.mp3"

            speechToText(file_path)

        elif choice == '3':
            userQuestion = input("\nAsk me anything: ").strip()
            aiChatbot(userQuestion)


        elif choice == '4':
            print("Exiting program")
            break

        else:
            print("Invalid choice Please enter 1, 2, 3 or 4.")




