// dependencies
import { useLocation } from "react-router-dom";

const Footer = () => {
  const location = useLocation();

  return (
    <>
      {location.pathname === '/' && <img className="footer__img" src="pets.svg" alt="" aria-hidden='true' />}
      <footer className="footer">
        <ul>
          <li>2022 - Frontend desenvolvido por <a href="https://angelacaldas.vercel.app/" target='_blank' rel="noreferrer">Angela Caldas</a>.</li>
          <li>2023 - Modificado e integrado com a API por <a href="https://github.com/HenriqueCCdA" target='_blank' rel="noreferrer">Henrique de Andrade</a>.</li>
        </ul>
      </footer>
    </>
  );
};

export default Footer;
