const { VITE_BACKEND_HOST, VITE_BACKEND_PORT, VITE_API_VERSION, VITE_SOCKET_ID } = import.meta.env
export const API_URL = `http://${VITE_BACKEND_HOST}:${VITE_BACKEND_PORT}/api/dm/${VITE_API_VERSION}/`
export const WS_ADDRESS = `ws://${VITE_BACKEND_HOST}:${VITE_BACKEND_PORT}/ws/${VITE_SOCKET_ID}`

