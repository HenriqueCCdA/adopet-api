import { Link } from "react-router-dom"


function Home() {

  return (
    <>
      <p>
        <Link  to="/login">login</Link>
      </p>
      <p>
        <Link  to="/pets-list">Pets</Link>
      </p>
    </>
  )
}

export default Home
