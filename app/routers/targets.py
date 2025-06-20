from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, deps

router = APIRouter(
    prefix="/targets",
    tags=["Targets"],
)

@router.patch("/{target_id}", response_model=schemas.Target)
def update_mission_target(target_id: int, target: schemas.TargetUpdate, db: Session = Depends(deps.get_db)):
    db_target = crud.get_target(db, target_id=target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    
    db_mission = db_target.mission
    if db_mission.complete:
        raise HTTPException(status_code=400, detail="Cannot update target notes, the mission is already complete.")
    if db_target.complete:
        raise HTTPException(status_code=400, detail="Cannot update target notes, the target is already marked as complete.")
        
    return crud.update_target(db=db, target_id=target_id, target_update=target)