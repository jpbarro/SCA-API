from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, deps

router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)

@router.post("/", response_model=schemas.Mission, status_code=status.HTTP_201_CREATED)
def create_new_mission(mission: schemas.MissionCreate, db: Session = Depends(deps.get_db)):
    return crud.create_mission(db=db, mission=mission)

@router.get("/", response_model=List[schemas.Mission])
def read_all_missions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    missions = crud.get_missions(db, skip=skip, limit=limit)
    return missions

@router.get("/{mission_id}", response_model=schemas.Mission)
def read_single_mission(mission_id: int, db: Session = Depends(deps.get_db)):
    db_mission = crud.get_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission

@router.patch("/{mission_id}/assign", response_model=schemas.Mission)
def assign_cat_to_mission_endpoint(mission_id: int, cat_id: int, db: Session = Depends(deps.get_db)):
    db_mission = crud.get_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    db_cat = crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    if db_cat.mission is not None:
        raise HTTPException(status_code=400, detail=f"Cat {cat_id} is already on mission {db_cat.mission.id}")
    
    return crud.assign_cat_to_mission(db=db, mission_id=mission_id, cat_id=cat_id)

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_mission(mission_id: int, db: Session = Depends(deps.get_db)):
    db_mission = crud.get_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    if db_mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete a mission that is assigned to a cat")
    crud.delete_mission(db=db, mission_id=mission_id)
    return