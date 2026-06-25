from fastapi import FastAPI, Path,HTTPException,Query
import json
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()

class Patients(BaseModel):
    id:Annotated[str,Field(..., description='Id of the patient',example='P001')]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City patietn belongs to')]
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient')]
    weight:Annotated[float,Field(...,gt=0, description='Weight of the patient')]




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

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='sort the patients on the basis of height weight and BMI'), order:str=Query('asc', description='sort in ascending or descending order')):

    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code='400',detail=f'invalid field select form {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code='400',detail= 'invalid order select from asc and desc')
    
    data=load_data

    sort_order= True if order=='desc' else False


    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=sort_order)

    return sorted_data


