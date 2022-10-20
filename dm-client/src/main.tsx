import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './routes/App'
import {
  createBrowserRouter,
  RouterProvider,
  Navigate
} from "react-router-dom";
import ErrorPage from './routes/ErrorPage';
import DiagnosticsPage from './routes/DiagnosticsPage';
import OverviewPage from './routes/OverviewPage';
import { Provider } from 'react-redux'
import { setupStore } from './store';
import { increment } from './reducer/messageSlice';
import SettingsPage from './routes/SettingsPage';
import { WS_ADDRESS } from './utils';

const store = setupStore()
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "overview",
        element: <OverviewPage />,
      },
      {
        path: "diagnostics",
        element: <DiagnosticsPage />,
      },
      {
        path: "settings",
        element: <SettingsPage />,
      },
      {
        path: "",
        element: <Navigate to="/overview" replace />
      }
    ],
  },
]);
const socket = new WebSocket(WS_ADDRESS);
// Connection opened
socket.addEventListener('open', (event) => {
  console.log("websocket open");
  socket.send("Activate client")
});

// Listen for messages
socket.addEventListener('message', (event) => {
  console.log(event.data)
  if(event.data == "GET_DATA") {
    store.dispatch(increment())
  }
});


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
)
