import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: No API Key found in .env file!")
else:
    genai.configure(api_key=api_key)
    print(f"Checking models for Key: {api_key[:5]}...")
    
    try:
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ AVAILABLE: {m.name}")
                found_any = True
        
        if not found_any:
            print("❌ No models found. Your API Key might be invalid or has no access.")
            
    except Exception as e:
        print(f"❌ Error connecting to Google: {e}")
        