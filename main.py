from fastapi import FastAPI, Depends, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from api_models import (
    TokenData,
    LoginResponse,
    SuccessResponse,
    UserSigninPayload,
    UserLoginPayload,
    TaskObject,
    ConvertFilePayload,
)
from typing import Union, List, Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from io import BytesIO

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id = 1  # payload.get("user_id")
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
    return {"success": True}

# 2


@app.post("/auth/login", response_model=LoginResponse)
async def login(
        user_login_payload: UserLoginPayload):
    token = create_access_token({
        "user_id": 1,
    })
    return {
        "valid": True,
        "token": token,
    }

# 3


@app.get("/tasks", response_model=List[TaskObject])
async def list_tasks(max: Optional[int]=None, order: Optional[int]=None):
    return [
        {
            "task_id": 1,
            "original_file_name": "file_user_1",
            "original_file_ext": "zip",
            "target_file_ext": "7z",
            "finished": False,
        },
        {
            "task_id": 2,
            "original_file_name": "file_2_user_1",
            "original_file_ext": "uncompressed",
            "target_file_ext": "mp3",
            "finished": False,
        }
    ]


@app.post("/tasks", response_model=SuccessResponse)
async def create_task(convert_file_payload: ConvertFilePayload):
    return {"success": True, "message": "Usuario creado exitosamente"}


@app.get("/tasks/{id_task}", response_model=TaskObject)
async def list_tasks(id_task: int):
    return {
        "task_id": 1,
        "original_file_name": "file_user_1",
        "original_file_ext": "zip",
        "target_file_ext": "7z",
        "finished": False,
    }

@app.delete("/tasks/{id_task}", response_model=TaskObject)
async def list_tasks(id_task: int):
    return Response(status_code=HTTP_200_OK)

@app.get("/files/{filename}", response_class=StreamingResponse)
async def list_tasks(filename: str):
    
    file = BytesIO()
    file.write(b"mockup file")
    file.seek(0)
    return StreamingResponse(
        file, 
        media_type="text/csv",
        headers={
            'Content-Disposition': 'attachment; filename="{}"'.format(
                filename
            )
            }
        )