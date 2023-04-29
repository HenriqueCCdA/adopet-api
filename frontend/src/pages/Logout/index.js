function Logout() {

  localStorage.removeItem('adopet-token')

  return <p> Logout </p>
}

export default Logout
