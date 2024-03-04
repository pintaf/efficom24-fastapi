from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = [
    {   
        "id": 1,
        "email": "a@b.c",
        "name": "John",
        "age": 28
    },
    {
        "id": 2,
        "email": "b@c.d",
        "name": "Jane",
        "age": 32,
    },
    {
        "id": 3,
        "email": "c@d.e",
        "name": "Doe",
        "age": 45
    },
    {
        "id": 4,
        "email": "d@e.f",
        "name": "Smith"
    }
]

class CreateUser(BaseModel):
    name: str
    age: int
    email: str

class User(CreateUser):
    id: int

class RootReturnObj(BaseModel):
    Hello: str

@app.get("/")
async def helloWorld() -> RootReturnObj:
    return {"Hello": "World"}


@app.get("/say-hello-john")
async def helloJohn():
    return "Hello John!"


@app.get("/users")
async def getUsers(minimum_age: int | None = None) -> list[User]:
    """
    Endpoint to return all users
    """
    if minimum_age:
        return [user for user in users if user["age"] >= minimum_age]
    return users

@app.get("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getUser(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.post("/users", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createUser(user: CreateUser) -> User:
    max_id = 0
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if existing_user["id"] > max_id:
            max_id = existing_user["id"]

    # we made the checks before for the email, so we can be sure that the email is unique
    # we raise errors in that case and this piece of code won't be executed
    user = user.dict()
    user['id'] = max_id + 1
    users.append(user)
    return user

@app.delete("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteUser(user_id: int) -> None:
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.put("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def updateUser(user_id: int, updated_user: CreateUser) -> None:
    user_index = None
    for index, user in enumerate(users):
        if user["email"] == updated_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if user["id"] == user_id:
            user_index = index
    
    if user_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    updated_user = updated_user.dict()
    updated_user["id"] = user_id
    users[user_index]= updated_user

