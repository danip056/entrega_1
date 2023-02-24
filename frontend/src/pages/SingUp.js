import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserPlus } from "@fortawesome/free-solid-svg-icons";
import PasswordChecklist from "react-password-checklist"

const API = process.env.REACT_APP_API;

export const SingUp = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordAgain, setPasswordAgain] = useState("")
    const [isPasswordValid, setIsPasswordValid] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        {
            const res = await fetch(`${API}/auth/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user,
                    email,
                    password,
                }),
            });
            await res.json();
            if (res.status == 200) {
                alert("Usuario creado exitosamente")
                navigate("/login")
            }
            if (res.status == 500) {
                alert("El email o el usuario ya está registrado en el servidor, intente uno nuevo")
            }
        }

        setUser("");
        setEmail("");
        setPassword("");
        setPasswordAgain("");
    };


    return (
        <div>
            <div className="row center">
                <div className={`col-md-3`}>
                    <form onSubmit={handleSubmit} className="card card-body">
                        <div className="text-center">
                            <h3 className="mb-5">Crea tu cuenta</h3>
                        </div>
                        <div className="form-outline mb-4 ">
                            <input
                                type="user"
                                onChange={(e) => setUser(e.target.value)}
                                value={user}
                                className="form-control form-control-lg"
                                placeholder="Usuario"
                                required="True"
                            />
                        </div>
                        <div className="form-outline mb-4 ">
                            <input
                                type="email"
                                onChange={(e) => setEmail(e.target.value)}
                                value={email}
                                className="form-control form-control-lg"
                                placeholder="Correo"
                                required="True"
                            />
                        </div>
                        <div className="form-outline mb-4 ">
                            <input
                                type="password"
                                onChange={(e) => setPassword(e.target.value)}
                                value={password}
                                className="form-control form-control-lg"
                                placeholder="Contraseña"
                                required="True"
                            />
                        </div>
                        <PasswordChecklist
                            rules={["minLength", "specialChar", "number", "capital", "match"]}
                            minLength={5}
                            value={password}
                            valueAgain={passwordAgain}
                            messages={{
                                minLength: "La contraseña tiene más de 8 caracteres.",
                                specialChar: "La contraseña tiene caracteres especiales.",
                                number: "La contraseña tiene un número.",
                                capital: "La contraseña tiene una letra mayúscula.",
                                match: "Las contraseñas coinciden.",
                            }}
                            onChange={(isValid) => setIsPasswordValid(isValid)}
                        />
                        <div className="form-outline mb-4">
                            <input
                                type="password"
                                name="passwordAgain"
                                onChange={(e) => setPasswordAgain(e.target.value)}
                                value={passwordAgain}
                                className="form-control form-control-lg"
                                placeholder="Confirme su contraseña"
                            />
                        </div>
                        <button className="btn btn-primary btn-block btn-lg" disabled={!isPasswordValid}>
                            <span>
                                <FontAwesomeIcon icon={faUserPlus} />&nbsp;
                            </span>
                            Registro
                        </button>
                        <br />
                        <hr />
                        <div className="text-center">
                            <p className="mb-5 pb-lg-2 register">¿Ya tienes una cuenta? <Link to="/login" className="register link">Inicia sesión aquí</Link></p>
                        </div>
                    </form>
                </div>

            </div>
        </div>
    );
};