from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

# --- Target Schemas ---
class TargetBase(BaseModel):
    name: str
    country: str

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    complete: Optional[bool] = None

class Target(TargetBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    notes: Optional[str] = None
    complete: bool
    mission_id: int

# --- Mission Schemas ---
class MissionBase(BaseModel):
    complete: bool = False

class MissionCreate(MissionBase):
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)

class MissionUpdate(BaseModel):
    complete: Optional[bool] = None
    cat_id: Optional[int] = None

class Mission(MissionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    cat_id: Optional[int] = None
    targets: List[Target] = []

# --- Cat Schemas ---
class CatBase(BaseModel):
    name: str
    breed: str

class CatCreate(CatBase):
    years_of_experience: int
    salary: float

class CatUpdate(BaseModel):
    salary: Optional[float] = None

class Cat(CatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    years_of_experience: int
    salary: float
    mission: Optional[Mission] = None