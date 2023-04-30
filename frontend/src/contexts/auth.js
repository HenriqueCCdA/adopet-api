// dependencies
import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import clientHttp from "../adapters/axios_client.js"


export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const navigate = useNavigate();

    // Num primeiro momento, usaremos dados fixos para o login/logout
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const recoveredUser = localStorage.getItem('adopet-user');

        if (recoveredUser) {
            setUser(JSON.parse(recoveredUser));
        }

        // to avoid page loading without properly gathering the user info from localStorage, we must use a state to wait for it. When the data fetch is ended, then we set Loading to false and then we render the page (this last one is made on Routes file)
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        console.log('login auth', { email, password });

        const data =  `username=${email}&password=${password}`
        try{
          const resp = await clientHttp.post("login/", data)
          const token = resp.data.token
          const id = resp.data.id

          // creating a session api
          const loggedUser = { token, id, email};

        // saving user on localStorage
          localStorage.setItem('adopet-user', JSON.stringify(loggedUser));

          setUser(loggedUser);
          navigate('/home');

        }catch(error){
          console.log('Resposta', error)
          console.log(error.response.data['non_field_errors']) // TODO: Colocar um feedback no front
          // return error
        }
    };

    const logout = () => {
        console.log('logout');
        localStorage.removeItem('adopet-user');
        setUser(null);
        navigate('/');
    };

    // !!user:
    // user != null, then authenticated = true
    // user == null, then authenticated = false

    return (
        <AuthContext.Provider value={{ authenticated: !!user, user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

/*
O contexto é como se fosse uma memória central disponível para gravar certas informações globais, por exemplo, um usuário logado.
Esse contexto deverá ser importado no arquivo de rotas e deve envolver todas as rotas que precisam ter acesso aos dados desse contexto. Usaremos o localStorage para armazenar os dados.
*/
