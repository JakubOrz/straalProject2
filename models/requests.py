from pydantic import BaseModel, validator, ValidationError, root_validator


class TestModel(BaseModel):
    message: str
    code: int

    @root_validator(pre=True)
    def chech_missing_fields(cls, values):
        model_fields_names = values.keys()
        missing_fields = list()
        for field in cls.__fields__.values():
            if field.name not in model_fields_names:
                missing_fields.append(field.name)

        if len(missing_fields) != 0:
            raise ValueError("Missing values: {}".format(" ".join(missing_fields)))

    @validator('message')
    def message_validate(cls, message):
        if 'hey' not in message:
            raise ValueError("You missed hey in message")
        return message

