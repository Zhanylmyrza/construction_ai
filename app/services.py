import httpx
import os


from google import genai

client = genai.Client(api_key="AIzaSyCI90BtC5yv9lCCRkhhqZkM4yXihoNG8cM")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)


GEMINI_API_KEY = "AIzaSyCI90BtC5yv91CCRkhhqZkM4yXihoNG8cM"

# Correct Gemini API URL
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
            
            response_data = response.json()
            
            # Process the Gemini response to extract tasks
            if response.status_code == 200 and "candidates" in response_data:
                text_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Extract tasks from the text response (simplified)
                task_lines = [line.strip() for line in text_response.split('\n') 
                             if line.strip() and not line.strip().startswith('#')]
                
                # Convert to required format
                tasks = [{"name": task, "status": "pending"} for task in task_lines]
                return tasks
            else:
                print(f"API Error: {response.text}")
                # Return a default list of tasks if the API fails
                return [
                    {"name": "Find suitable location", "status": "pending"},
                    {"name": "Obtain permits", "status": "pending"},
                    {"name": "Hire contractors", "status": "pending"},
                    {"name": "Purchase materials", "status": "pending"},
                    {"name": "Begin construction", "status": "pending"}
                ]
                
        except Exception as e:
            print(f"Exception in Gemini API call: {str(e)}")
            # Return a default list of tasks if there's an exception
            return [
                {"name": "Find suitable location", "status": "pending"},
                {"name": "Obtain permits", "status": "pending"},
                {"name": "Hire contractors", "status": "pending"},
                {"name": "Purchase materials", "status": "pending"},
                {"name": "Begin construction", "status": "pending"}
            ]