import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMessage } from "@fortawesome/free-solid-svg-icons";

function LogoutMessage() {
  return (
    <div className='' style={{ whiteSpace: 'pre-wrap', textAlign: 'center', paddingTop: "20vh" }}>
      <span>
        <FontAwesomeIcon icon={faMessage} size="3x" />
      </span>
      <h3 >¡Gracias por utilizar nuestros servicios de conversión!</h3>
      <br />
      <p>
        Esperamos que nuestra página web haya sido de su utilidad, por favor vuelva pronto.
      </p>
      <a href="/login" className="btn btn-primary btn-lg">Inicio de sesión</a>
    </div>
  );
}

export default LogoutMessage;