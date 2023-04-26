import { Route, Routes} from "react-router-dom"

import Home from "./pages/Home"
import Login from "./pages/Login"
import ListPet from "./pages/ListPet"


const MyRoutes = () => {
  return (
    <Routes>
      <Route element={<Home/>} path="/" />
      <Route element={<Login/>} path="/login" />
      <Route element={<ListPet/>} path="/pets-list" />
    </Routes>
  )
}

export default MyRoutes
