import sys
import os
sys.path.append(
    os.path.dirname(__file__)
)

from fastapi import FastAPI, Depends, Response, status, UploadFile, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from api_models import (
    TokenData,
    LoginResponse,
    SuccessResponse,
    UserSigninPayload,
    UserLoginPayload,
    TaskObject,
    Status,
)
from typing import Union, List, Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from io import BytesIO
from models import User, Task
from bd_connection import Session
import os
from uuid import uuid4
import aiofiles
from celery import Celery
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from pathlib import Path
from compression import CompressionFormat

app = FastAPI(
    title="DSC entrega 1",
    description="Entrega 1 Desarrollo de Soluciones Cloud",
    version="1.0",
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "ultra_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

Path.mkdir(Path(STORAGE_DIR), exist_ok=True)

celery = Celery(
    broker=CELERY_BROKER_URL,
    backend="rpc://",
)

oauth2_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user_id(auth_credentials: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = auth_credentials.credentials
        payload = jwt.decode(token, SECRET_KEY)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user_id = token_data.user_id
    if user_id is None:
        raise credentials_exception
    return user_id


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 1


@app.post("/auth/signup", response_model=SuccessResponse)
async def sigin(sigin_payload: UserSigninPayload):
    user_entry =  User(
        user=sigin_payload.user,
        email=sigin_payload.email,
        password=pwd_context.hash(sigin_payload.password)
    )
    with Session() as session:
        session.add(user_entry)
        session.commit()
    return {"success": True}
# 2


@app.post("/auth/login", response_model=LoginResponse)
async def login(
        user_login_payload: UserLoginPayload):
    with Session() as session:
        query = session.query(User).where(
            (User.user==user_login_payload.user_or_email) |
            (User.email==user_login_payload.user_or_email),
            )
        try:
            user = query.one()
        except:
            raise HTTPException(status_code=404, detail="Wrong user or password")
    
    if not pwd_context.verify(user_login_payload.password, user.password):
        raise HTTPException(status_code=404, detail="Wrong user or password")

    token = create_access_token({
        "user_id": user.id,
    })
    return {
        "valid": True,
        "token": token,
    }


def generate_file_name(extension, user_id):

    file_name = "{}_{}{}".format(
            uuid4().hex,
            user_id,
            extension)
    return file_name

async def save_file(file, path):
    async with aiofiles.open(path, "wb") as new_file:
        await new_file.write(await file.read())

@app.post("/tasks", response_model=SuccessResponse)
async def create_task(
    file: UploadFile,
    target_file_ext: str = Body(),
    user_id = Depends(get_current_user_id)
    ):

    if file.filename.endswith(CompressionFormat.ZIP.value):
        original_file_ext = CompressionFormat.ZIP.value
    elif file.filename.endswith(CompressionFormat.TAR_GZ.value):
        original_file_ext = CompressionFormat.TAR_GZ.value
    elif file.filename.endswith(CompressionFormat.TAR_BZ2.value):
        original_file_ext = CompressionFormat.TAR_BZ2.value
        
    original_stored_file_name = generate_file_name(
        original_file_ext,
        user_id)

    target_stored_file_name = generate_file_name(
        target_file_ext,
        user_id)


    await save_file(
        file, 
        os.path.join( STORAGE_DIR, original_stored_file_name)
    )

    task_entry = Task(
        user_id=user_id,
        original_file_name=file.filename,
        original_file_ext=original_file_ext,
        original_stored_file_name=original_stored_file_name,
        target_file_ext=target_file_ext,
        target_stored_file_name=target_stored_file_name
    )
    with Session() as session:
        session.add(task_entry)
        session.commit()
        id_task = task_entry.id

    celery.send_task(
        "v1.tasks.process_task",
        args=[id_task],
    )
    return {"success": True, "message": "Tarea creada con éxito"}


# 3
@app.get("/tasks", response_model=List[TaskObject])
async def list_tasks(
    max: Optional[int]=None,
    order: Optional[int]=None,
    user_id = Depends(get_current_user_id)
    ):

    with Session() as session:
        query = session.query(Task).where(Task.user_id==user_id)
        if order == 0:
            query = query.order_by(Task.id)
        elif order == 1:
            query = query.order_by(-Task.id)

        if max:
            query = query.limit(max)
        task_list = query.all()

    return [
        {
            "task_id": task.id,
            "original_file_name": task.original_file_name,
            "original_file_ext": task.original_file_ext,
            "original_stored_file_name": task.original_stored_file_name,
            "target_file_ext": task.target_file_ext,
            "target_stored_file_name": task.target_stored_file_name,
            "uploaded_at": task.uploaded_at,
            "status": task.status,
        } for task in task_list]





@app.get("/tasks/{id_task}", response_model=TaskObject)
async def list_tasks(
    id_task: int,
    user_id = Depends(get_current_user_id)
    ):

    with Session() as session:
        task = session.query(Task).get(id_task)

    if not task or (task.user_id != user_id):
        raise HTTPException(status_code=404, detail="Task not found")

    return {
            "task_id": task.id,
            "original_file_name": task.original_file_name,
            "original_file_ext": task.original_file_ext,
            "original_stored_file_name": task.original_stored_file_name,
            "target_file_ext": task.target_file_ext,
            "target_stored_file_name": task.target_stored_file_name,
            "uploaded_at": task.uploaded_at,
            "status": task.status,
        }


@app.delete("/tasks/{id_task}", response_model=SuccessResponse)
async def list_tasks(
    id_task: int,
    user_id = Depends(get_current_user_id)
    ):

    with Session() as session:
        affected_ids = session.query(Task).filter(
            Task.id==id_task,
            Task.user_id==user_id,
            Task.status==Status.PROCESSED.value).delete(
            synchronize_session="fetch"
        )
        if affected_ids != 1:
            raise HTTPException(status_code=404, detail="Task not found")
        session.commit()

    return {"success": True, "message": "Task deleted"}

@app.get("/files/{filename}", response_class=FileResponse)
async def list_tasks(
    filename: str,
    user_id = Depends(get_current_user_id)
    ):

    file_base_name = filename.split(".")[0]
    file_user_id = int(file_base_name.split("_")[-1])

    if file_user_id != user_id:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
    path=os.path.join(
        STORAGE_DIR,
        filename
    ),
    filename=filename,
    )
