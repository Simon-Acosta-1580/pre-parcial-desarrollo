from fastapi import FastAPI, HTTPException
from models import EstudianteBase, EstudianteId, EstudianteUpload
from estudianteOperations import createEstudiante, get_active_students, get_inactive_students, find_one_student, update_one_student, delete_student, reactivate_estudiante
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

@app.get("/estudiantes", response_model=list[EstudianteId])
async def show_estudiantes(session: SessionDep):
    estudiante_activos = get_active_students(session)
    if not estudiante_activos:
        raise HTTPException(status_code=404, detail="No estudiantes activos")
    return estudiante_activos

@app.get("/estudiantesInactivos", response_model=list[EstudianteId])
async def show_estudiantesInactivos(session: SessionDep):
    estudiante_inactivos = get_inactive_students(session)
    if not estudiante_inactivos:
        raise HTTPException(status_code=404, detail="No estudiantes inactivos")
    return estudiante_inactivos

@app.get("/estudiante/{id}", response_model=EstudianteId)
async def show_one_estudiante(id: int, session: SessionDep):
    estudiante = find_one_student(id, session)
    if not (estudiante):
        raise HTTPException(status_code=404, detail=f"{id} Estudiante not found")
    return estudiante

@app.patch("/estudiante/{id}", response_model=EstudianteId, response_model_exclude={"id", "activo"})
async def update_estudiante(id: int, estudiante: EstudianteUpload, session: SessionDep):
    update = update_one_student(id, estudiante, session)
    if not (update):
        raise HTTPException(status_code=404, detail=f"{id} Estudiante not found")
    return update


@app.delete("/estudiante/{id}", response_model=EstudianteId)
async def delete_estudiante(id: int, session: SessionDep):
    estudiante_eliminado = delete_student(id, session)

    if not estudiante_eliminado:
        raise HTTPException(status_code=404, detail=f"Estudiante {id} no encontrado")

    return estudiante_eliminado


@app.patch("/estudiante/rehabilitar/{id}", response_model=EstudianteId)
def rehabilitar_estudiante(id: int, session: SessionDep):
    estudiante = reactivate_estudiante(id, session)

    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return estudiante

