import axios from "axios";
import { useEffect, useState } from "react";

function ListPet(){

  const [pets, setPets] = useState(['doi']);

  async function pets_list(){

      const token = localStorage.getItem("adopet-token");

      const config = {headers: {"Authorization": `Bearer ${token}`}}

      try{
        const resp = await axios.get("http://localhost:8000/pet/", config)
        setPets(resp.data.results)
      }catch(error){
        console.log(error)
      }
  }

  useEffect( () => { pets_list()} , []);

  return (
    <div>
    <h1>Listas de Pets</h1>
    {
      pets.map( (pet, index) => {
        return <p key={index}>{pet.name}</p>
      }
    )}
    </div>
  )
}

export default ListPet;
