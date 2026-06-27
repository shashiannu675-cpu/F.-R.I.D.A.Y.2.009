import google.generativeai as genai
from fastapi import HTTPException
from config import settings

class FridayEngine:
    def __init__(self):
        self.active_users = {}

    def register_user(self, user_id: str):
        if user_id not in self.active_users:
            self.active_users[user_id] = {"history": [], "status": "active"}
        return {"message": f"Friday is ready for: {user_id}"}

    async def process_request(self, user_id: str, prompt: str) -> dict:
        if user_id not in self.active_users:
            self.register_user(user_id)
            
        if not settings.PRIMARY_AI_API_KEY:
            raise HTTPException(status_code=500, detail="PRIMARY_AI_API_KEY is missing in Render.")

        try:
            # 1. Connect to Gemini using your secret key from Render
            genai.configure(api_key=settings.PRIMARY_AI_API_KEY)
            
            # 2. Load the Gemini model (using gemini-1.5-flash for fast responses)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 3. Send the prompt and get the answer
            ai_response = model.generate_content(prompt)
            answer = ai_response.text

            # 4. Save to user history
            self.active_users[user_id]["history"].append({"user": prompt, "friday": answer})
            
            return {
                "user_id": user_id,
                "friday_response": answer,
                "status": "success"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

engine = FridayEngine()
