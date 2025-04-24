from fastapi import FastAPI, HTTPException
import openai
from openai import OpenAI

api_key="API_Key"
app = FastAPI()

foods_list = ["Banana", "Chicken", "Beef", "Orange", "Broccoli", "Asparagus"]
workouts_list = ["Bench-Press", "Squat", "Bicep-Curl", "OverHead-Clean", "Pulldowns"]
calories_list = ["310", "1020", "2050", "500", "1560"]
users_list = ["Mary", "John", "Joseph", "Melanie", "Jackson"]

user_workouts = {
                1: ["Bench-Press", "Squat", "Bicep-Curl", ],
                2: ["OverHead-Clean", "Pulldowns", "Tricep Extensions"],
                3: ["Squat", "Calf-Extension", "Leg-Extensions"],
                4: ["Mile-Run", "Planks", "Crunches"]
}
            


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

@app.get("/workouts")
async def get_workouts():
    return {"workouts": workouts_list}

@app.post("/workouts")
async def add_workout(name: str = ""):
    workouts_list.append(name)
    return {"workouts": workouts_list}

@app.delete("/workouts")
async def delete_workout(index: int = 0):
    workouts_list.pop(index)
    return {"workouts": workouts_list}

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
            return("suggestion": response.choices[0].message.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def build_prompt(user_id):
    user_history = user_workouts[user_id]
    user_history_joined = ", ".join(user_history)
    prompt = (
        "Based on this user's previous workouts: "
        + user_history_joined +
        ", suggest one new workout they haven't done yet. "
        "Just give the name of the workout. No explanation."
    )
    return prompt
