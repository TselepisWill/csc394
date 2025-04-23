from fastapi import FastAPI

app = FastAPI()

foods_list = ["Banana", "Chicken", "Beef", "Orange", "Broccoli", "Asparagus"]
workouts_list = ["Bench-Press", "Squat", "Bicep-Curl", "OverHead-Clean", "Pulldowns"]
calories_list = ["310", "1020", "2050", "500", "1560"]
users_list = ["Mary", "John", "Joseph", "Melanie", "Jackson"]
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