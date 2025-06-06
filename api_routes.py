from fastapi import FastAPI, HTTPException, Depends, Request
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime


# SQL database configuration setup
DATABASE_URL = "sqlite:///./reminders.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #connects to SQL-lite
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)     #Creates a session
Base = declarative_base()       #a base class which table will inherit.

class Reminder(Base):  #Reminder table inheriting Base class properties.
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    message = Column(String)

Base.metadata.create_all(bind=engine) 

# FASTAPI app instance
app = FastAPI()

#creating db session and safely provide it to endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#function to parse string date input to python data syntax
def parse_date(date: str):
    try :
        return datetime.strptime(date,"%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400,  detail="Invalid date format. Use YYYY-MM-DD.")
    
#function to parse string time input to python time syntax
def parse_time(time: str):
    try: 
        return datetime.strptime(time,"%H:%M:%S").time()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM:SS.")



#route to get all reminders details .
@app.get("/reminders")
def read_reminders(db: Session = Depends(get_db)):
    reminders = db.query(Reminder).all()
    return [
        {"id": r.id, "date": str(r.date), "time": str(r.time), "message": r.message}
        for r in reminders
    ]


#route to add new reminder to the table.
@app.post("/reminders")
async def create_reminder(request: Request, db : Session = Depends(get_db)):
    
    data = await request.json()
    date = parse_date(data.get("date"))
    time = parse_time(data.get("time"))
    message = data.get("message")
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required.") 
    
    reminder = Reminder(date = date , time = time, message = message)

    db.add(reminder)  
    db.commit()
    db.refresh(reminder)

    return {
        "id": reminder.id,
        "date": str(reminder.date),
        "time": str(reminder.time),
        "message": reminder.message
    }

#route to modify any reminder in table using id.
@app.put("/reminders")
async def update_reminders(request : Request , db: Session = Depends(get_db)):
    data = await request.json()
    reminder = db.query(Reminder).filter(Reminder.id == data.get("id")).first()

    if not reminder:
        raise HTTPException(status_code=404, detail="record not found!")
    if "date" in data:
        reminder.date = parse_date(data.get("date"))
    if "time" in data:
        reminder.time = parse_time(data.get("time"))
    if "message" in data:
        reminder.message = data.get("message")

    db.commit()
    db.refresh(reminder)
    
    return {
        "id": reminder.id,
        "date": str(reminder.date),
        "time": str(reminder.time),
        "message": reminder.message
    }

# route to delete any reminder in table using id.
@app.delete("/reminders")
async def delete_reminder(request:Request,db : Session = Depends(get_db)):
    data = await request.json()
    reminder = db.query(Reminder).filter(Reminder.id == data.get("id")).first()

    if not reminder:
        raise HTTPException(status_code=404 , detail="Record not found")
    
    db.delete(reminder)
    db.commit()
    return {
        "result" : "record deleted."
    }