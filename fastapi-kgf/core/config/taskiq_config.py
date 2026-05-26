from pydantic import BaseModel, AmqpDsn


class TaskiqConfig(BaseModel):
    url: AmqpDsn = "amqp://guest:guest@localhost:5672//"
