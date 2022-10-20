# Documentation


## Overview
The purpose of this project is to build device management system. Basically, users could config the device and save to JSON file in the server. Beside, the server is also able to collect message data from a mock PLC OPCUA server of devices by OPCUA communication.


## Features
1. As a user, he/she could see the information of device system in overview page
2. As a user, he/she could see the realtime message table in diagnostics page
3. As a user, he/she could upload a device config file in CSV and the system will change all the device information


## Requirement
1. Python > 3.6
2. virtualenv > 20
3. Docker
4. Node > 16


## Getting started

### Without Docker

1. Start database server by running
```
docker-compose up -d cassandra
```

2. Start OPCUA server and client by running
```
pip install -r requirements.txt
cd plc-opc-ua-server
./run.sh
```

3. Start web server 
```
cd dm-service
uvicorn main:app --reload
```

4. Create env file for client
```
cd dm-client
touch .env

# Copy these config to .env file
VITE_BACKEND_HOST=127.0.0.1
VITE_BACKEND_PORT=8000
VITE_API_VERSION=v1
VITE_SOCKET_ID=1234
```
4. Start web app 
```
cd dm-client
pnpm install
pnpm run dev
```

### With docker

1. Build dm-client by this command
```
cd dm-client
pnpm run build
```

2. Start data feed from OPCUA
```
cd plc-opcua-server
./run.sh
```

3. Start Web UI, service and database
```
docker-compose up -d
```

## How to use the app
<img src="images/Instruction.gif"/>

## Architecture

### Backend side
The message is streamed from OPC UA server to a Python client whenever a new update happened in OPC UA sever. This client will insert the message to message database by Restful communication to web service (FastAPI). The web service will trigger a message to web client (React) by websocket and the client will fetch newest messages from database.

### Frontend side
User can get all information of the machine by make Restful requests to web service. The web service will read the JSON file and return the values to client.

<img src="images/Architecture.png"/>


