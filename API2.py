from fastapi import FastAPI, HTTPException
import openai
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware


api_key="api-key"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # allow your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

foods_list = ["Banana", "Chicken", "Beef", "Orange", "Broccoli", "Asparagus"]


calories_list = ["310", "1020", "2050", "500", "1560"]
users_list = ["Mary", "John", "Joseph", "Melanie", "Jackson"]

#

#Foods

@app.get("/foods")
async def get_foods():
    return {"foods": foods_list}

@app.post("/foods")
async def add_food(name: str = ""):
    foods_list.append(name)
    return {"foods": foods_list}

@app.delete("/foods")
async def delete_food(index: int = 0):
    foods_list.pop(index)
    return {"foods": foods_list}

#Workouts

# ---------- Pydantic Models ----------
from pydantic import BaseModel

class Workouts(BaseModel):
    id: int
    workout_name: str
    muscle_group: str

    class Config:
        orm_mode = True

# ---------- SQLite Setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./workouts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":
False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------- SQLAlchemy Model ----------
class WorkoutDB(Base):
        __tablename__ = "workouts"
        id = Column(Integer, primary_key=True, index=True)
        workout_name = Column(String, index=True)
        muscle_group = Column(String)

## create tables if they don't exist
Base.metadata.create_all(bind=engine)

# ---------- Routes ----------
@app.get("/workouts")
def read_workouts():
    with SessionLocal() as session:
        workouts = session.query(WorkoutDB).all()
        return [
    {
        "id": w.id,
        "workout_name": w.workout_name,
        "muscle_group": w.muscle_group
    }
    for w in workouts
]


    
@app.post("/workouts", response_model=Workouts)
def create_workout(workout: Workouts):
    with SessionLocal() as session:
        db_workout = WorkoutDB(**workout.dict())
        session.add(db_workout)
        session.commit()
        session.refresh(db_workout)
    return db_workout

@app.delete("/workouts", response_model=Workouts)
def delete_workout(workout_id: int):
    with SessionLocal() as session:
        workout = session.query(WorkoutDB).filter(WorkoutDB.id == workout_id).first()
        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")
        session.delete(workout)
        session.commit()
        return workout



workouts_list = [
Workouts(id=1, workout_name="Bench", muscle_group="Chest"),
]

#Calories

@app.get("/calories")
async def get_calories():
    return {"calories": calories_list}

@app.post("/calories")
async def add_calories(name: str = ""):
    calories_list.append(name)
    return {"calories": calories_list}

@app.delete("/calories")
async def delete_calories(index: int = 0):
    calories_list.pop(index)
    return {"calories": calories_list}

#Users

@app.get("/users")
async def get_users():
    return {"users": users_list}

@app.post("/users")
async def add_user(name: str = ""):
    users_list.append(name)
    return {"users": users_list}

@app.delete("/users")
async def delete_user(index: int = 0):
    users_list.pop(index)
    return {"users": users_list}




@app.get("/user_workouts")
async def get_user_workouts(index: int = 0):
    if index <= 0 :
        all_workouts = []
        for workout_list in user_workouts.values():
            all_workouts.extend(workout_list)
        return {"workouts": all_workouts}
    elif index <= len(user_workouts):
        return {"workouts": user_workouts[index]}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/suggestions")
async def get_strings(index: int =0):
    if index <= 0 or index > len(user_workouts):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        try:
            prompt = build_prompt(index)
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]

            )
            return{"suggestion": response.choices[0].message.content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def build_prompt(user_id):
    workout_list = user_workouts[user_id]
    workouts_joined = ", ".join(workout_list)
    prompt = """Based on this user's previous workouts, suggest one new workout they haven't done yet.
            Just give the name of the workout. No explanation.
            """ + workouts_joined
    
    print(prompt)
    return prompt