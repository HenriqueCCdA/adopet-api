import clientHttp from "../../http";
import { useEffect, useState } from "react";
import PetCard from "../../Components/PetCard";
import { Container, Grid } from "@mui/material";
import { Navigate } from "react-router-dom";

function ListPet(){

  const [pets, setPets] = useState([]);

  async function pets_list(){

      const token = localStorage.getItem("adopet-token");

      const config = {headers: {"Authorization": `Bearer ${token}`}}

      try{
        const resp = await clientHttp.get("pet/", config)
        setPets(resp.data.results)
      }catch(error){
        console.log(error)
      }
  }

  useEffect( () => { pets_list()} , []);

  return (
    <Container maxWidth="sm">
      <h1>Listas de Pets</h1>
      <Grid container spacing={4} >
      {
        pets.map( pet => {
          return (
            <Grid key={pet.id} item xs={5}>
              <PetCard pet={pet}/>
            </Grid>
          )
        }
      )}
      </Grid>
    </Container>
  )
}

export default ListPet;
