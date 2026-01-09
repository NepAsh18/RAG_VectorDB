import redis
import json
from app.core.config import settings

class ChatMemory:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    # --- Existing Message History logic ---
    def get_history(self, session_id: str):
        data = self.redis.get(f"history:{session_id}")
        return json.loads(data) if data else []

    def save_history(self, session_id: str, messages: list):
        self.redis.setex(f"history:{session_id}", 3600, json.dumps(messages))

    # --- NEW: Booking State logic (Slot Filling) ---
    def get_booking_state(self, session_id: str) -> dict:
        data = self.redis.get(f"state:{session_id}")
        return json.loads(data) if data else {}

    def update_booking_state(self, session_id: str, new_data: dict):
        # 1. Get current saved slots
        current_state = self.get_booking_state(session_id)
        # 2. Merge with new info (e.g., add email to existing name)
        # We only update fields that are NOT null in the new_data
        for key, value in new_data.items():
            if value is not None:
                current_state[key] = value
        # 3. Save back to Redis
        self.redis.setex(f"state:{session_id}", 3600, json.dumps(current_state))