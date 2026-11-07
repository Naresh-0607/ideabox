from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Idea, User
from schemas import IdeaCreate, IdeaResponse, IdeaStatus, IdeaUpdate, TokenResponse, UserCreate, UserResponse
from security import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api")
Db = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Db):
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with that email already exists")
    return user


@router.post("/auth/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Db):
    user = db.scalar(select(User).where(User.email == form_data.username.lower()))
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/auth/me", response_model=UserResponse)
def me(user: CurrentUser):
    return user


def owned_idea(db: Session, user: User, idea_id: int) -> Idea:
    idea = db.scalar(select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id))
    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.get("/ideas", response_model=list[IdeaResponse])
def list_ideas(
    user: CurrentUser,
    db: Db,
    search: str | None = Query(default=None, max_length=200),
    status_filter: IdeaStatus | None = Query(default=None, alias="status"),
    tag: str | None = Query(default=None, max_length=40),
):
    query = select(Idea).where(Idea.user_id == user.id).order_by(Idea.updated_at.desc(), Idea.id.desc())
    if search:
        query = query.where(Idea.title.ilike(f"%{search}%"))
    if status_filter:
        query = query.where(Idea.status == status_filter.value)
    if tag:
        query = query.where(Idea.tags.contains([tag.strip()]))
    return list(db.scalars(query))


@router.post("/ideas", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def create_idea(payload: IdeaCreate, user: CurrentUser, db: Db):
    idea = Idea(user_id=user.id, **payload.model_dump())
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea


@router.get("/ideas/{idea_id}", response_model=IdeaResponse)
def get_idea(idea_id: int, user: CurrentUser, db: Db):
    return owned_idea(db, user, idea_id)


@router.put("/ideas/{idea_id}", response_model=IdeaResponse)
def update_idea(idea_id: int, payload: IdeaUpdate, user: CurrentUser, db: Db):
    idea = owned_idea(db, user, idea_id)
    for key, value in payload.model_dump().items():
        setattr(idea, key, value)
    db.commit()
    db.refresh(idea)
    return idea


@router.delete("/ideas/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(idea_id: int, user: CurrentUser, db: Db):
    idea = owned_idea(db, user, idea_id)
    db.delete(idea)
    db.commit()
