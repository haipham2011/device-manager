from pydantic import BaseModel

class Message(BaseModel):
    id: int
    message_type: str
    start_time: str
    status_code: int
    machine_id: int