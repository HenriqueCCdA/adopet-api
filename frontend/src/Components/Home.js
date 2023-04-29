import { motion } from 'framer-motion';
import CardPet from './CardPet.js';
import { useEffect, useState } from 'react';

import clientHttp from '../adapters/axios_client.js';

  const petSizes = { "S": "Pequeno", "M": "Pédio", "B": "Grande"}


const Home = () => {

  const [pets, setPets] = useState([]);

  const pets_list = async () => {
      const user = localStorage.getItem("adopet-user");

      try{
        const token = JSON.parse(user).token
        const config = {headers: {"Authorization": `Bearer ${token}`}}
        const resp = await clientHttp.get("pet/", config)
        setPets(resp.data.results)
      }catch(error){
        console.log(error)
      }
  }

  useEffect( () => { pets_list()} , []);


  return (
    <motion.section
      className='home'
      initial={{ width: 0 }}
      animate={{ width: "auto", transition: { duration: 0.5 } }}
      exit={{ x: window.innerWidth, transition: { duration: 0.5 } }}
    >
      <p>Olá! <br /> Veja os amigos disponíveis para adoção!</p>
      <div className='cards'>
        {
          pets.map((pet, i) => (
            <CardPet
              age={pet.age}
              size={petSizes[pet.size]}
              behavior={pet.behavior}
              city='Rio de Janeiro (RJ)'
              name={pet.name}
              img={pet.photo}
              shelter={pet.shelter}
              key={i}
            />
          ))
        }
      </div>
    </motion.section >
  );
};

export default Home;
