from email.policy import default
from sqlmodel import SQLModel, Field
class EstudianteBase(SQLModel):
    nombre: str
    apellido: str
    activo: bool

class EstudianteId(EstudianteBase, table=True):
    id: int = Field(default = None, primary_key=True, gt=0)

class EstudianteUpload(EstudianteBase):
    id: int = Field(default = None, exclude=True)
    nombre: str
    apellido: str
    activo: bool = Field(default = False, exclude=True)