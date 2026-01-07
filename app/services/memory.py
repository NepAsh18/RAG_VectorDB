import redis
import json
from app.core.config import settings

class ChatMemory:
    def __init__(self):
     self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)


    def get(self, session_id:str):
       data = self.redis.get(session_id)
       return json.loads(data) if data else []

    def save(self, session_id:str, messages:list):
       self.redis.setex(session_id, 3600, json.dumps(messages)) 