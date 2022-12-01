from typing import Type, Union, Optional

from pydantic import validator, ValidationError
from pydantic import BaseModel as PDBaseModel


class HttpError(Exception):
    
    def __init__(self, status_code: int, message: Union[str, dict, list]):
        self.status_code = status_code
        self.message = message


class CreateUserSchema(PDBaseModel):
    name: str
    rating: Optional[int]
    
    @validator('name')
    def check_name(cls, value: str):
        if len(value) > 50:
            raise ValueError('name must be less than 50')
        return value
    
    @validator('rating')
    def check_rating(cls, value: int):
        if value > 100 or value < 0:
            raise ValueError('rating must be in range 0 to 100')
        return value


class PatchUserSchema(PDBaseModel):
    name: Optional[str]
    rating: Optional[int]
    
    @validator('name')
    def check_name(cls, value: str):
        if len(value) > 50:
            raise ValueError('name must be less than 50')
        return value
    
    @validator('rating')
    def check_rating(cls, value: int):
        if value > 100 or value < 0:
            raise ValueError('rating must be in range 0 to 100')
        return value


class CreateAdvSchema(PDBaseModel):
    title: str
    description: str
    owner_id: int
    
    @validator('title')
    def check_title(cls, value: str):
        if len(value) > 50:
            raise ValueError('title must be less than 50')
        return value

    @validator('description')
    def check_description(cls, value: str):
        if len(value) < 10:
            raise ValueError('description must be more than 10')
        return value


class PatchAdvSchema(PDBaseModel):
    title: Optional[str]
    description: Optional[str]
    
    @validator('title')
    def check_title(cls, value: str):
        if len(value) > 50:
            raise ValueError('title must be less than 50')
        return value
    
    @validator('description')
    def check_description(cls, value: str):
        if len(value) < 10:
            raise ValueError('description must be more than 10')
        return value


def validate(data_to_validate: dict,
             validation_class: Union[
                 Type[CreateUserSchema],
                 Type[PatchUserSchema],
                 Type[CreateAdvSchema],
                 Type[PatchAdvSchema]
                 ]
             ):
    try:
        return validation_class(**data_to_validate).dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())
    