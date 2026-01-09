from app.db.postgres import SessionLocal
from app.db.models import InterviewBooking
from app.services.memory import ChatMemory
from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional

class BookingState(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None

class BookingService:
    def __init__(self):
        self.memory = ChatMemory()

    def process_booking(self, extracted_data: dict, session_id: str):
        """
        Merges new data with Redis memory and decides whether to save to Postgres.
        """
       
        current_state_dict = self.memory.get_booking_state(session_id)

        
        for key, value in extracted_data.items():
            if value is not None:
                current_state_dict[key] = value

       
        state = BookingState(**current_state_dict)

        
        required = ["name", "email", "date", "time"]
        missing = [f for f in required if getattr(state, f) is None]

        if missing:
           
            return f"I've noted that. To complete the booking, I still need your: {', '.join(missing)}."

        
        try:
            self.save(state.model_dump())
            
            self.memory.redis.delete(f"state:{session_id}")
            return f"Perfect {state.name}! Your interview is booked for {state.date} at {state.time}."
        except Exception as e:
            return f"I encountered an error while saving your booking: {str(e)}"

    def save(self, data: dict):
        with SessionLocal() as db:
            booking = InterviewBooking(**data)
            db.add(booking)
            db.commit()