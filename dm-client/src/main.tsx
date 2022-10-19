import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './routes/App'
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Navigate
} from "react-router-dom";
import ErrorPage from './routes/ErrorPage';
import DiagnosticsPage from './routes/DiagnosticsPage';
import OverviewPage from './routes/OverviewPage';

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
        path: "",
        element: <Navigate to="/overview" replace />
      }
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
