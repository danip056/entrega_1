import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const API = process.env.REACT_APP_API;


export const Events = (props) => {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [category, setCategory] = useState("");
    const [place, setPlace] = useState("");
    const [address, setAddress] = useState("");
    const [start_date, setStartDate] = useState("");
    const [end_date, setEndDate] = useState("");
    const [virtual, setVirtual] = useState("");

    const [editing, setEditing] = useState(false);
    const [id, setId] = useState("");

    const nameInput = useRef(null);

    let [events, setEvents] = useState([]);


    const [token, setToken] = useState(localStorage.getItem('token'))
    let getToken
    const [userId, setUserId] = useState(localStorage.getItem('id'))


    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!editing) {
            let virtual_bool = (virtual == 'true' || virtual == true || virtual === "")
            let category_selected = (category == '' ? 'Conferencia' : category)

            const res = await fetch(`${API}/user/${userId}/events`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ` + token
                },
                body: JSON.stringify({
                    name,
                    category: category_selected,
                    place,
                    address,
                    start_date,
                    end_date,
                    virtual: virtual_bool
                }),
            });
            await res.json();
            if (res.status == 409) {
                alert('El usuario ya tiene un evento con el mismo nombre')
            }
        } else {
            let virtual_bool = (virtual == 'true' || virtual == true)

            const res = await fetch(`${API}/event/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ` + token
                },
                body: JSON.stringify({
                    name,
                    category,
                    place,
                    address,
                    start_date,
                    end_date,
                    virtual: virtual_bool
                }),
            });
            const data = await res.json();
            setEditing(false);
            setId("");
        }
        await getEvents();

        setName("");
        setCategory("");
        setPlace("");
        setAddress("");
        setStartDate("");
        setEndDate("");
        setVirtual("");
        nameInput.current.focus();
    };

    const getEvents = async () => {
        const res = await fetch(`${API}/user/${userId}/events`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        setEvents(data);
        return res
    };

    const deleteEvent = async (id) => {
        const userResponse = window.confirm("Are you sure you want to delete it?");
        if (userResponse) {

            const res = await fetch(`${API}/event/${id}`, {
                method: "DELETE",
                headers: { "Authorization": 'Bearer ' + token }
            });
            await getEvents();
        }
    };

    const editEvent = async (id) => {
        const res = await fetch(`${API}/event/${id}`, {
            headers: { "Authorization": 'Bearer ' + token }
        });
        const data = await res.json();

        setEditing(true);
        setId(id);

        // Reset
        setName(data.name);
        setCategory(data.category);
        setPlace(data.place);
        setAddress(data.address);
        setStartDate(data.start_date);
        setEndDate(data.end_date);
        setVirtual(data.virtual);
        nameInput.current.focus();
    };

    useEffect(() => {
        getToken = localStorage.getItem('token')
        if (!getToken) {
            alert("Debe iniciar sesión primero")
            navigate("/login")
        }
        getEvents();
    }, []);

    return (
        <div className="row center">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="card card-body">
                    <h3>Formulario evento</h3>
                    <div className="form-group">
                        <label>
                            Nombre del evento:
                            <input
                                required="True"
                                type="text"
                                onChange={(e) => setName(e.target.value)}
                                value={name}
                                className="form-control"
                                placeholder="Event's name"
                                ref={nameInput}
                                autoFocus
                            />
                        </label>
                    </div>

                    <div className="form-group">
                        <label>
                            Categoría:
                            <select type="category"
                                onChange={(e) =>
                                    setCategory(e.target.value)}
                                value={category}
                                className="form-control">
                                <option value="Conferencia">Conferencia</option>
                                <option value="Seminario">Seminario</option>
                                <option value="Congreso">Congreso</option>
                                <option value="Curso">Curso</option>
                            </select>
                        </label>
                    </div>


                    <div className="form-group">
                        <label>
                            Lugar del evento:
                            <input
                                type="place"
                                onChange={(e) => setPlace(e.target.value)}
                                value={place}
                                className="form-control"
                                placeholder="Event's place"
                                required="True"
                            /></label>
                    </div>
                    <div className="form-group">
                        <label>
                            Dirección:
                            <input
                                type="address"
                                onChange={(e) => setAddress(e.target.value)}
                                value={address}
                                className="form-control"
                                placeholder="Event's address"
                                required="True"
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Fecha de inicio:
                            <input
                                type="date"
                                onChange={(e) => setStartDate(e.target.value)}
                                value={start_date}
                                className="form-control"
                                placeholder="Event's start date"
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Fecha de fin:
                            <input
                                type="date"
                                onChange={(e) => setEndDate(e.target.value)}
                                value={end_date}
                                className="form-control"
                                placeholder="Event's end date"
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Modalidad:
                            <select type="virtual" onChange={(e) => setVirtual(e.target.value)} value={virtual} className="form-control">
                                <option value="true">Virtual</option>
                                <option value="false">Presencial</option>
                            </select>
                        </label>
                    </div>



                    <button className="btn btn-primary btn-block">
                        {editing ? "Update" : "Create"}
                    </button>
                </form>
            </div>
            <div className="col-md-6">
            <h3>Eventos</h3>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Category</th>
                            <th>Place</th>
                            <th>Address</th>
                            <th>Start date</th>
                            <th>End date</th>
                            <th>Virtual</th>
                            <th>Operations</th>
                        </tr>
                    </thead>
                    <tbody>
                        {[].concat(events).sort((a, b) => a.id > b.id ? -1 : 1).map((event) => (
                            <tr key={event.id}>
                                <td>{event.name}</td>
                                <td>{event.category}</td>
                                <td>{event.place}</td>
                                <td>{event.address}</td>
                                <td>{event.start_date}</td>
                                <td>{event.end_date}</td>
                                <td>{event.virtual == true ? 'Virtual' : 'Presencial'}</td>
                                <td>
                                    <button
                                        className="btn btn-secondary btn-sm btn-block"
                                        onClick={(e) => editEvent(event.id)}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm btn-block"
                                        onClick={(e) => deleteEvent(event.id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};