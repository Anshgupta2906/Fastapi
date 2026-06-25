from fastapi import FastAPI, Path,HTTPException
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

#path and parameter to access any particyular patient
@app.get("/patientid/{patient_id}")
def view_patient(patient_id:str = Path(...,description="enter the patient id of the patient",example='P001')):
    data= load_data()
    for patient_id in data:
        return data[patient_id]
    #instead of returning error we will raise an exception 404
    raise HTTPException(status_code='404',detail='Patient not found')