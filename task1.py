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
            model="bulbul:v3",
            speaker="shubh"
        )

        audioBytes = base64.b64decode(response.audios[0])

        with open(output_filename, "wb") as f:
            f.write(audioBytes)

        print(f"Audio saved to {output_filename}.\n")

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
        output = response.transcript
        print(f"Text Output:\n{output} ")
        return output

    except ApiError as e:
        print(f"API Error: {e.status_code} - {e.body}")
        return None
    except FileNotFoundError:
        print(f"Could not find the audio file '{audio_filename}'")
        return None
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return None




def aiChatbot(text):
    
    response = client.chat.completions(
        model="sarvam-105b",
        messages=[
            {"role": "user", "content": text} 
        ]
    )
    print("\nAI Chatbot Response:")
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
                file_path = "demo_audio.wav" 
            
            speechToText(file_path)

        elif choice == '3':
            print("Press 1 for giving text input")
            print("Press 2 for giving voice input")
            inp = input("Press 1 or 2: ").strip()
            
            if inp == '1':
                userQuestion = input("\nAsk me anything: ").strip()
                if userQuestion:
                    aiChatbot(userQuestion)
                else:
                    print("You didn't ask anything.")
                    
            elif inp == '2':
                file_path = input("\nEnter the question audio filename (Example: 'sampleQuestion1.mp3'): ").strip()
                
                
                if not file_path:
                    file_path = "sampleQuestion1.mp3"
                    
                example = speechToText(file_path)
                
                
                if example:
                    print(f"\nThe Question you asked:\n{example}")
                    
                    aiChatbot(example) 
                else:
                    print("Transcription failed or audio was empty.")
                    
            else:
                print("Invalid Choice")
                print("Exiting chatbot menu")

        elif choice == '4':
            print("Exiting program")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")