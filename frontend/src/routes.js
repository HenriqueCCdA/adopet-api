import { Route, Routes} from "react-router-dom"

import Home from "./pages/Home"
import Login from "./pages/Login"
import PetList from "./pages/PetList"
import Logout from "./pages/Logout"
import PetDetail from "./pages/PetDetail"


const MyRoutes = () => {
  return (
    <Routes>
      <Route element={<Home/>} path="/" />
      <Route element={<Login/>} path="/login" />
      <Route element={<Logout/>} path="/logout" />
      <Route element={<PetList/>} path="/pets-list" />
      <Route element={<PetDetail/>} path="/pet/:id" />
    </Routes>
  )
}

export default MyRoutes
