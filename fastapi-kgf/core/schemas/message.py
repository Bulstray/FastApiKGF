from pydantic import BaseModel, ConfigDict, model_validator


class Message(BaseModel):
    task_id: int
    initials: str = None
    text: str
    author: str
    created_at: str

    @model_validator(mode="after")
    def generate_initials(self):
        if not self.initials and self.author:
            words = self.author.strip().split()
            self.initials = "".join(word[0].upper() for word in words if word)
        return self

    model_config = ConfigDict(extra="ignore")
