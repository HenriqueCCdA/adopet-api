import axios from "axios";

const clientHttp = axios.create({
  baseURL: "http://localhost:8000"
})

export default clientHttp
