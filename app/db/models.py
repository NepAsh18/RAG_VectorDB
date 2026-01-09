from sqlalchemy import Column, Integer, String, Date, Time, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
   
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True) 
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    
    __table_args__ = (
        UniqueConstraint('date', 'time', name='_date_time_uc'),
    )