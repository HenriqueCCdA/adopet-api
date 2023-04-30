import Button from './Button';

import { motion } from 'framer-motion';
import { useForm } from "react-hook-form";

const Message = () => {
  // destructuring useForm
  const { register, handleSubmit, formState: { errors } } = useForm({
    mode: 'onBlur',
    reValidateMode: 'onChange'
  });


  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <motion.section
      className='message'
      initial={{ width: 0 }}
      animate={{ width: "auto", transition: { duration: 0.5 } }}
      exit={{ x: window.innerWidth, transition: { duration: 0.5 } }}
    >
      <p>Envie uma mensagem para o abrigo que está cuidado do animal:</p>
      <form onSubmit={handleSubmit(onSubmit)}>
        <label htmlFor="name">Nome</label>
        <input
          id='name'
          type="text"
          {...register("name", { required: 'É necessário informar seu nome', maxLength: { value: 40, message: 'O número máximo de caracteres é 40' } })}
          placeholder='Insira seu nome completo'
        />
        {errors.name && <p className="error">{errors.name.message}</p>}

        <label htmlFor="phone">Telefone</label>
        <input
          type="tel"
          id='phone'
          {...register('phone', { required: 'Informe um número de telefone', pattern: /\(?[1-9]{2}\)?\s?9?[0-9]{8}/ })}
          placeholder='Insira seu telefone e/ou whatsapp'
        />
        {errors.phone && <p className="error">{errors.phone.message || 'Por favor, verifique o número digitado'}</p>}

        <label htmlFor="petName">Nome do animal</label>
        <input
          id='petName'
          type="text"
          {...register("petName", { required: 'É necessário informar o nome do animal', maxLength: { value: 25, message: 'O número máximo de caracteres é 25' } })}
          placeholder='Por qual animal você se interessou?'
        />
        {errors.petName && <p className="error">{errors.petName.message}</p>}

        <label htmlFor="msg">Mensagem</label>
        <textarea
          name="msg"
          id="msg"
          cols="30"
          rows="10"
          {...register('msg', { required: 'É necessário escrever uma mensagem', maxLength: { value: 500, message: 'O número máximo de caracteres é 500' } })}
          placeholder='Escreva sua mensagem.'
          spellCheck='false'
        />
        {errors.msg && <p className="error">{errors.msg.message}</p>}

        <Button type='submit' children='Enviar' />
      </form>
    </motion.section>
  );
};

export default Message;
