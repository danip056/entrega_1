import React from 'react'
import { Link } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSignIn } from "@fortawesome/free-solid-svg-icons";
import { faFileZipper } from "@fortawesome/free-solid-svg-icons";
import { faRightFromBracket } from "@fortawesome/free-solid-svg-icons";

const Navbar = () => {
  return (
    <nav className="navbar-padding navbar navbar-expand-lg navbar-dark bg-primary me-auto" style={{ paddingLeft: '10vh' }}>
      <Link className="navbar-brand " to="/singup">
        <button className='btn btn-light'>Registro</button>
      </Link>
      <button className="navbar-toggler" type="button">
        Relll
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div className="navbar-nav">
          <Link className="nav-item nav-link active fa-sign-in" to="/"><FontAwesomeIcon icon={faSignIn} /> Iniciar sesión </Link>
          <Link className="nav-item nav-link active" to="/tasks"><FontAwesomeIcon icon={faFileZipper} /> Conversor archivos</Link>
        </div>
        <ul className="navbar-nav ms-auto">
          <li className="nav-item"  style={{ paddingRight: '3vh' }}>
            <Link className="nav-item nav-link active ms-auto" to="/singout"><FontAwesomeIcon icon={faRightFromBracket} /> Cerrar sesión</Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default Navbar
