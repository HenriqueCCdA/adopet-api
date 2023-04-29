import { useEffect, useState } from "react";
import PetCard from "../../Components/PetCard";
import clientHttp from "../../http";
import { useParams } from "react-router-dom";
import { Container } from "@mui/material";

function DetailPetView() {

  const [pet, petSet] = useState(null)
  const {id} = useParams()


  async function pet_by_id(id){

    const token = localStorage.getItem("adopet-token");

    const config = {headers: {"Authorization": `Bearer ${token}`}}
    try{
      const resp = await clientHttp.get(`pet/${id}/`, config)
      petSet(resp.data)
    }catch(error){
      console.log(error)
    }
  }

  useEffect( () => { pet_by_id(id)} , [id]);

  return (
    <Container maxWidth="sm">
      { pet ? <PetCard pet={pet}/> : ""}
    </Container>
   )

}

export default DetailPetView;
