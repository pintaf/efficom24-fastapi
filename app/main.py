from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = [
    {   
        "id": 1,
        "name": "John",
        "age": 28
    },
    {
        "id": 2,
        "name": "Jane",
        "age": 32
    },
    {
        "id": 3,
        "name": "Doe",
        "age": 45
    },
    {
        "id": 4,
        "name": "Smith",
        "age": 22
    }
]

class RootReturnObj(BaseModel):
    Hello: str

@app.get("/")
async def helloWorld() -> RootReturnObj:
    return {"Hello": "World"}


@app.get("/say-hello-john")
async def helloJohn():
    return "Hello John!"


class User(BaseModel):
    id: int
    name: str
    age: int


@app.get("/users")
async def getUsers() -> list[User]:
    """
    Endpoint to return all users
    """
    return users

@app.get("/users/{user_id}", responses={404: {"model": str}})
async def getUser(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

