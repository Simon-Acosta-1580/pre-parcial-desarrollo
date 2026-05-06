from fastapi import FastAPI, HTTPException
from models import EstudianteBase, EstudianteId, EstudianteUpload
from estudianteOperations import createEstudiante
from sqlmodel import Session
from sqlmodel.orm import session
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)

@app.get("/saludo")
def saludo():
    return {"saludo": "Hola"}

@app.post("/estudiante", response_model=EstudianteId)
async def create_estudiante(estudiante: EstudianteBase, session: SessionDep):
    return createEstudiante(estudiante, session)



