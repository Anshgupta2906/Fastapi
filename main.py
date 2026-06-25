from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)
    
    return data

@app.get("/")
def hello():
    return{"message":"Hospital data center"}

@app.get("/about")
def about():
    return{'message':'we can see patients details here'}

@app.get("/view")
def view():
    data=load_data()
    return data