from fastapi import FastAPI, Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field , computed_field
from typing import Annotated, Literal,Optional

app = FastAPI()

class Patients(BaseModel):
    id:Annotated[str,Field(..., description='Id of the patient',example='P001')]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City patietn belongs to')]
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient')]
    weight:Annotated[float,Field(...,gt=0, description='Weight of the patient')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:

        if self.bmi>18.5:
            return 'Underweight'
        elif self.bmi >25:
            return 'Normal'
        elif self.bmi >30:
            return 'Normal'
        else:
            return 'Obese'

        
class Patient_update(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[str],Field(default=None,gt=0)]
    weight:Annotated[Optional[str],Field(default=None,gt=0)]



def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open ('patient.json','w')as f:
        json.dump(data,f)

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

@app.post('/create')
def create_patients(patient:Patients):
    #load data
    data=load_data()
    #check if the data already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exist')
    
    #if new patient add it into database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'Patient is created sucessfully'})


@app.put('/edit/{patient_id}')
def edit_patient(patient_id:str,patient_update:Patient_update):
    #load data
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,content='This Patient id is not available')
    
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    for key , value in updated_patient_info.items():
        existing_patient_info[key]=value
    
    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patients(**existing_patient_info)
    #pyd object to dictionary
    existing_patient_info=patient_pydantic_object.model_dump(exclude='id')

    data[patient_id]=existing_patient_info

    save_data(data)

    return JSONResponse (status_code=201,content='Your patient Updates are done')

@app.delete('/delete/{patient_id}')
def delete_pateint(patient_id:str):
    data=load_data()

    if patient_id not in data:
        raise HTTPException (status_code=404, detail='This patient id is not in data')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content="you have sucessfully deleted")