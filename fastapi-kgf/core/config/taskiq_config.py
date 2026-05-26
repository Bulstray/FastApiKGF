from pydantic import AmqpDsn, BaseModel


class TaskiqConfig(BaseModel):
    url: AmqpDsn = "amqp://guest:guest@localhost:5672//"
