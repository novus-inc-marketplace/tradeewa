from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
from .security import verify_password
from datetime import datetime, timedelta
import secrets

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = models.User.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_verification_token(db: Session, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    db_token = models.VerificationToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token

def verify_user_email(db: Session, token: str):
    db_token = db.query(models.VerificationToken).filter(models.VerificationToken.token == token).first()
    if not db_token or db_token.expires_at < datetime.utcnow():
        return False
    
    user = db.query(models.User).filter(models.User.id == db_token.user_id).first()
    if user:
        user.is_verified = True
        db.delete(db_token)
        db.commit()
        db.refresh(user)
        return True
    return False
