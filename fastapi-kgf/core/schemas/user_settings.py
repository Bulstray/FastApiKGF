from pydantic import BaseModel, field_validator


class UserSettings(BaseModel):
    tender_notification: bool = False
    task_notification: bool = False
    message_notification: bool = False

    @field_validator(
        "tender_notification",
        "task_notification",
        "message_notification",
        mode="before",
    )
    def convert_checkbox_to_bool(cls, value: str | bool) -> bool:
        if type(value) is bool:
            return value

        if isinstance(value, str):
            return value.lower() == "on"

        return False
