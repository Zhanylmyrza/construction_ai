import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def get_project_tasks(project_name: str, location: str):
    async with httpx.AsyncClient() as client:
        prompt = f"List construction tasks for {project_name} in {location}. Return only the task names, one per line."
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GEMINI_API_KEY}"
        }
        
        try:
            response = await client.post(
                GEMINI_URL,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                response_data = response.json()
                
                if "candidates" in response_data:
                    text_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    task_lines = [line.strip() for line in text_response.split('\n') 
                                 if line.strip() and not line.strip().startswith('#')]
                    
                    tasks = [{"name": task, "status": "pending"} for task in task_lines]
                    return tasks
                else:
                    raise ValueError("No candidates found in Gemini API response")
            else:
                raise ValueError(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception in Gemini API call: {str(e)}")
            return get_default_tasks()

def get_default_tasks():
    return [
        {"name": "Find suitable location", "status": "pending"},
        {"name": "Obtain permits", "status": "pending"},
        {"name": "Hire contractors", "status": "pending"},
        {"name": "Purchase materials", "status": "pending"},
        {"name": "Begin construction", "status": "pending"}
    ]
