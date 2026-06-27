import httpx
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
            self.active_users[user_id]["history"].append(prompt)
            # This is where the external APIs will be connected later
            return {
                "user_id": user_id,
                "friday_response": f"Processed '{prompt}' securely.",
                "status": "success"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

engine = FridayEngine()

