from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from sqlmodel.orm import session

from models import EstudianteBase, EstudianteId, EstudianteUpload


def createEstudiante(estudiante: EstudianteBase, session: Session):
    new_estudiante = EstudianteId.model_validate(estudiante)
    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)

    return new_estudiante

def getAllEstudiantes(session: Session):
    return session.query(EstudianteBase).all()

def get_active_students(session: Session):
    statement = select(EstudianteId).where(EstudianteId.activo == True)
    results = session.exec(statement).all()
    return results

def get_inactive_students(session: Session):
    statement = select(EstudianteId).where(EstudianteId.activo == False)
    results = session.exec(statement).all()
    return results

def find_one_student(id: int, session: Session):
    try:
        return session.get_one(EstudianteId, id)
    except NoResultFound:
        return None

def update_one_student(id: int, new_estudiante: EstudianteUpload, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    try:
        update_data = new_estudiante.model_dump(exclude_unset=True)

        estudiante_db.sqlmodel_update(update_data)

        session.add(estudiante_db)
        session.commit()
        session.refresh(estudiante_db)
        return estudiante_db

    except Exception as e:
        return None


def delete_student(id: int, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    estudiante_db.activo = False

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)

    return estudiante_db


def reactivate_estudiante(id: int, session: Session):
    estudiante_db = session.get(EstudianteId, id)

    if not estudiante_db:
        return None

    estudiante_db.activo = True

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)

    return estudiante_db