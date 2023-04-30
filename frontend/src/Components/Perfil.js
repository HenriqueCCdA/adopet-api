import Button from './Button';

import { motion } from 'framer-motion';
import { useForm } from "react-hook-form";

import loggedUser from '../assets/logged-user.png';
import clientHttp from '../adapters/axios_client';
import { useEffect, useState } from 'react';

const Perfil = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    mode: 'onBlur',
    reValidateMode: 'onChange'
  });

  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [phone, setPhone] = useState('');
  const [about, setAbout] = useState('');

  const get_tutor = async () => {
      const user = localStorage.getItem("adopet-user");

      try{
        const {id, token} = JSON.parse(user)
        const config = {headers: {"Authorization": `Bearer ${token}`}}
        const resp = await clientHttp.get(`tutores/${id}/`, config)
        setName(resp.data.name)
        setCity(resp.data.city)
        setPhone(resp.data.phone)
        setAbout(resp.data.about)
      }catch(error){
        console.log(error)
      }
  }

  useEffect( () => { get_tutor()} , []);

  const onSubmit = async (data) => {
    const user = localStorage.getItem("adopet-user");

    try{
      const {id, token} = JSON.parse(user)
      const config = {headers: {"Authorization": `Bearer ${token}`}}
      const userDate = {"name": name, "city": city, "about": about, "phone": phone}
      const resp = await clientHttp.patch(`tutores/${id}/`, userDate, config)
      console.log("update", data.about, data.name, resp.data)
    }catch(error){
      console.log(error)
    }
  };

  return (
    <motion.section
      className='message'
      initial={{ width: 0 }}
      animate={{ width: "auto", transition: { duration: 0.5 } }}
      exit={{ x: window.innerWidth, transition: { duration: 0.5 } }}
    >
      <p>Esse é o perfil que aparece para ONGs que recebem sua mensagem.</p>
      <form onSubmit={handleSubmit(onSubmit)}>
        <legend>Perfil</legend>
        <label htmlFor='user-pic'>Foto</label>
        <input type="image" id='userPic' src={loggedUser} alt="Usuário logado" />
        <a href="#">Clique na foto para editar</a>

        <label htmlFor="name">Nome</label>
        <input
          id='name'
          type="text"
          // # TODO: Usar useForm da forma correta
          // {
          //   ...register("name", {
          //     required: 'É necessário informar seu nome',
          //     maxLength: { value: 40, message: 'O número máximo de caracteres é 40' }
          // })}
          placeholder='Insira seu nome completo'
          value={name || ''}
          onChange={e => setName(e.target.value)}
        />
        {errors.name && <p className="error">{errors.name.message}</p>}

        <label htmlFor="phone">Telefone</label>
        <input
          type="tel"
          id='phone'
          // {
          //   ...register('phone', {
          //     required: 'Informe um número de telefone',
          //     pattern: /\(?[1-9]{2}\)?\s?9?[0-9]{8}/
          // })}
          placeholder='Insira seu telefone e/ou whatsapp'
          value={phone || '' }
          onChange={e => setPhone(e.target.value)}
        />
        {errors.phone && <p className="error">{errors.phone.message || 'Por favor, verifique o número digitado'}</p>}

        <label htmlFor="city">Cidade</label>
        <input
          type="text"
          id='city'
          // {...register('city', { required: 'Informe a cidade em que você mora' })}
          placeholder='Informe a cidade em que você mora'
          value={city || '' }
          onChange={e => setCity(e.target.value)}
        />

        <label htmlFor="about">Sobre</label>
        <textarea
          spellCheck='false'
          name="about"
          id="about"
          cols="30"
          rows="8"
          placeholder='Escreva sobre você.'
          value={about || ''}
          onChange={e => setAbout(e.target.value)}
        />
        <Button type='submit' children='Salvar' />
      </form>
    </motion.section>
  );
};

export default Perfil;
