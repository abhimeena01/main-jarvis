import requests
import pyttsx3
import json

# Load API key from config.json
with open("engine\\config.json", "r") as config_file:
    config = json.load(config_file)
    api_key = config["GEMINI_API_KEY"]

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

def chatBot(query):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": query
                        }
                    ]
                }
            ]
        }
        
        # Send the POST request to the Gemini API
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Parse and print the full response JSON to analyze its structure
        response_data = response.json()
        print("Full response data:", response_data)  # Print the full response
        
        # Attempt to retrieve the response text, with adjusted parsing if needed
        response_text = response_data.get('contents', [{}])[0].get('parts', [{}])[0].get('text', 'No response text available')
        
        # Print and speak the response
        print(response_text)
        speak(response_data)

        return response_text
    except Exception as e:
        print(f"Error occurred: {e}")
        speak("Sorry, I couldn't fetch the response from the chatbot.")
        return ""

# Example usage
chatBot("tell me about rohit sharma")
