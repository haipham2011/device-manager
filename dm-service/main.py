from typing import Any, List
from models.message import Message
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from modules.device_management import DeviceConf
from models.device import Device
from modules.database import MessageDb
from logging.config import dictConfig
import logging
from config import LogConfig

import logging

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

API_VERSION = 1
API_PREFIX = f"api/dm/v{API_VERSION}"

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device_config = DeviceConf("./public/device_conf.json")
messageDb = MessageDb('127.0.0.1', 9042, {
                      'username': 'cassandra', 'password': 'cassandra'})

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: Any, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    logger.info("Init database")
    messageDb.initialize_db()


@app.get(f"/{API_PREFIX}/overview")
async def get_overview():
    return device_config.get_system_overview()


@app.get(f"/{API_PREFIX}/devices")
async def get_devices():
    return device_config.get_devices()


@app.get(f"/{API_PREFIX}/" + "devices/{item_id}")
async def get_device(item_id: int):
    return device_config.get_device_with_id(item_id)


@app.get(f"/{API_PREFIX}/" + "messages")
async def get_messages():
    messages = messageDb.query_message()
    return {"messages" : messages[0:20]}


@app.post(f"/{API_PREFIX}/" + "messages")
async def insert_message(message: Message):
    messageDb.insert_message(message)

    await manager.broadcast("GET_DATA")
    return {"status": "success"}


@app.post(f"/{API_PREFIX}/" + "devices")
async def upsert_device(device: Device):
    return device_config.upsert_device(device)


@app.delete(f"/{API_PREFIX}/" + "devices/{item_id}")
def delete_device(item_id: int):
    return device_config.delete_device(item_id)


@app.post(f"/{API_PREFIX}/" + "uploadConfig")
async def create_upload_file(file: UploadFile):
    return device_config.import_devices(file.file.read().decode('utf-8').splitlines())


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutdown database")
    messageDb.shutdown_db()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")