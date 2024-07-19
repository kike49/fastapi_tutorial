from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])

# Create an user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    # Create the user in the database with the input from user
    created_user = models.User(**new_user.model_dump())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

# Get user from id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.id == id).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user_found