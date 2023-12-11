from pydantic import BaseModel

# user type
class IUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    role: str
    password: str
    birthdate: str


# login input 
class ILoginInput(BaseModel):
    username: str
    password: str





    