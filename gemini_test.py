import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from the .env file
load_dotenv()

# Initialize the client (it will automatically look for GEMINI_API_KEY)
client = genai.Client()

# Your remaining code...
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, Gemini!",
)
print(response.text)
