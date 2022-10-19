import "./App.css"
import SideBar from '../components/SideBar'
import { Outlet } from "react-router-dom";

function App() {

  return (
    <>
      <SideBar />
      <Outlet />
    </>
  )
}

export default App
