import { useState } from "react";
import axios from "axios";

const LoginForm = () => {

  const [username, setUsername] = useState("asd")
  const [password, setPassword] = useState("")

  function handleChange({target}) {
    if(target.name === "username"){
      setUsername(target.value)
    } else if(target.name === "password"){
      setPassword(target.value)
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data =  `username=${username}&password=${password}`
    try{
      const resp = await axios.post("http://localhost:8000/login/", data)
      localStorage.setItem('adopet-token', resp.data.token);
    }catch(error){
      console.log(error)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <fieldset>
        <div>
          <label>Username</label>
          <input
            type="txt"
            value={username}
            name="username"
            placeholder="user@email.com"
            onChange={handleChange}
          />
        </div>
      </fieldset>
      <fieldset>
        <div>
          <label>password</label>
          <input
            type="password"
            name="password"
            onChange={handleChange}
          />
        </div>
      </fieldset>
      <button type="submit">Entra</button>
    </form>
  )
}


export default LoginForm;
