from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

# -------------- Дані, спільні для А і С  --------------------
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$wXQX36VoV9NhLUVRS9gDPuliZGbKTg/p3mxjXEnSO6smBwKa4Nwje",  # for pass = '123456'
    }
}

# -------------- Моделі Pydantic--------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    hashed_password: str


# -------------- Виключно для хешування паролів --------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# -------------- Юзер менеджер --------------------

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# -------------- Створення токену --------------------

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Створює зашифрований токен, використовуючі
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----------------- Кінцева точка, яка видає токени ---------------------------

app = FastAPI()

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=15)  # видихнеться за 15 хвилин
    )
    return Token(access_token=access_token, token_type="bearer")



# -------------- Безпекова залежність --------------------

from fastapi.security import OAuth2PasswordBearer

# Це каже FastAPI, що токен треба брати з заголовка
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Розшифровує токен, використовуючі SECRET_KEY, ALGORITHM.
    За даними з токену знаходить користувача в БД і повертає його.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/add/{a}/{b}")
async def add( a: int, b: int, user: User = Depends(get_current_user) ) -> int:
    return a + b

# from fastapi import FastAPI, Security, HTTPException, status
# from fastapi.security.api_key import APIKeyHeader


# # 1️⃣ Оголошуємо схему безпеки (з'явиться в OpenAPI)
# api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# # 2️⃣ Безпекова залежність з цією схемою
# async def get_api_key(api_key: str = Security(api_key_header)):
#     if api_key != "secret123":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or missing API key"
#         )
#     return {"role": "admin", "name": "Alice"}

# # 3️⃣ Захищена точка (Swagger тепер покаже замок 🔒)
# @app.get("/protected")
# async def protected_route(user_info: dict = Security(get_api_key)):
#     return {"message": f"Welcome, {user_info['name']}!"}

