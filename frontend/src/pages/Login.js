import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from "@fortawesome/fontawesome-svg-core";
import { faRightFromBracket } from "@fortawesome/free-solid-svg-icons";
library.add(faRightFromBracket);

const API = process.env.REACT_APP_API;

const Login = () => {
    const navigate = useNavigate();
    const [user_or_email, setUser] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_or_email,
                password,
            }),
        })
        const response = await res.json();
        console.log(res.ok)
        localStorage.setItem('token', response.token)
        if (!res.ok) {
            alert("Usuario o contraseña incorrectas")
        } else {
            navigate("/tasks");
        }


    };

    return (
        <div className="row center">
            <div className="col-md-3">
                <form onSubmit={handleSubmit} className="card card-body ">
                    <div className="text-center">
                        <h3 className="mb-5">Inicie sesión</h3>
                    </div>
                    <div className="form-outline mb-4 ">
                        <input
                            type="user_or_email"
                            onChange={(e) => setUser(e.target.value)}
                            value={user_or_email}
                            className="form-control form-control-lg"
                            placeholder="Usuario"
                        />
                    </div>
                    <div className="form-outline mb-4">
                        <input
                            type="password"
                            onChange={(e) => setPassword(e.target.value)}
                            value={password}
                            className="form-control form-control-lg"
                            placeholder="Contraseña"
                        />
                    </div>
                    
                    <button className="btn btn-primary btn-block btn-lg">
                        <span>
                            <FontAwesomeIcon icon={faRightFromBracket} /> &nbsp;
                        </span>
                        Iniciar sesión
                    </button>
                    <br />
                    <hr />
                    <div className="text-center">
                        <p className="mb-5 pb-lg-2 register">¿No tienes una cuenta? <Link to="/singup" className="register link">Regístrate  aquí</Link></p>
                    </div>
                </form>
            </div>

        </div>
    );
};

export default Login