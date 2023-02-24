import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronRight, faRotateRight, faEye, faDownload, faTrashCan, faXmark } from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";
import Modal from 'react-modal';

library.add(faChevronRight);

const API = process.env.REACT_APP_API;

Modal.setAppElement("#root"); // set the root element for accessibility

export const Tasks = () => {
    const navigate = useNavigate();

    const [file, setFile] = useState("");
    const [format, setFormat] = useState(".zip");
    const [max, setMax] = useState(100);
    const [order, setOrder] = useState(1);
    const nameInput = useRef(null);
    let [tasks, setTasks] = useState("");
    const [token, setToken] = useState("")
    const refreshInterval = 500000
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedData, setSelectedData] = useState(null);
    const [destinationFormat, setDestinationFormat] = useState(null);


    const handleSubmit = async (e) => {
        e.preventDefault();
        {//Task creation
            console.log("file", file)
            console.log("file", format)
            const formData = new FormData();
            formData.append('file', file);
            formData.append('target_file_ext', format);
            const res = await fetch(`${API}/tasks`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ` + token
                },
                body: formData
            });
            await res.json();
            if (res.status == 409) {
                alert('El usuario ya tiene un evento con el mismo nombre')
            }
            console.log(res)

        }
        await getTasks();

        setFile("")
        setFormat(".zip")

    };


    const getTasks = async () => {
        const res = await fetch(`${API}/tasks?max=${max}&order=${order}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        setTasks(data);
        return res
    };

    const deleteTask = async (id) => {
        const userResponse = window.confirm("Are you sure you want to delete it?");
        if (userResponse) {

            const res = await fetch(`${API}/tasks/${id}`, {
                method: "DELETE",
                headers: { "Authorization": 'Bearer ' + token }
            });
            await getTasks();
        }
    };

    const DownloadFile = async (task, original) => {
        let final_extension = ""
        const file_name = task.original_file_name.split(".")[0];
        let file_name_api = task.original_stored_file_name
        if (original){
            final_extension = task.original_file_ext
        }else{
            final_extension = task.target_file_ext
            file_name_api = task.target_stored_file_name
        }
        console.log(task.target_stored_file_name)
        const res = await fetch(`${API}/files/${file_name_api}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", file_name+final_extension);
        document.body.appendChild(link);
        link.click();
    };

    useEffect(() => {
        if (token) {
            setToken(token)
            getTasks()
        }
        console.log("use effect")
    }, [token, max, order]);

    useEffect(() => {
        const intervalId = setInterval(() => {
            getTasks()
        }, refreshInterval)
        return () => clearInterval(intervalId);
    }, [])

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setToken(token);
        }
        else {
            alert("Debe iniciar sesión primero")
            navigate("/login")
        }
    }, []);


    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
    };
    const openModal = (data) => {
        setSelectedData(data);
        setModalOpen(true);
    };

    const closeModal = () => {
        setSelectedData(null);
        setModalOpen(false);
    };
    const formStyle = {
        label: {
            display: 'inline-block',
            marginLeft: '10px',
            marginRight: '10px'
        },
        input: {
            display: 'inline-block',
            marginRight: '10px',
        },
        select: {
            display: 'inline-block',
            marginRight: '10px',
        },
    };

    const customStyles = {
        content: {
            top: "50%",
            left: "50%",
            right: "auto",
            bottom: "auto",
            marginRight: "-50%",
            transform: "translate(-50%, -50%)",
        },
    };

    return (
        <div className="row center">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="card card-body">
                    <h3>Conversor de archivos</h3>
                    <label>Selecciona el archivo a cargar:</label>
                    <div className="form- mt-2">
                        <input type="file"
                            required="True"
                            onChange={handleFileChange}
                            id="inputFile" />
                        <div>{file && `${file.name} - ${file.type}`}</div>
                    </div>

                    <div className="form-group mt-3">
                        <label>
                            Formato de salida:
                            <select type="format"
                                onChange={(e) =>
                                    setFormat(e.target.value)}
                                value={format}
                                className="form-control">
                                <option value=".zip">Zip</option>
                                <option value=".tar.gz">Tar.gz</option>
                                <option value=".tar.bz2">Tar.bz2</option>
                            </select>
                        </label>
                    </div>

                    <div className="mt-2"></div>


                    <button className="btn btn-primary btn-block">
                        <span>
                            <FontAwesomeIcon icon={faChevronRight} /> &nbsp;
                        </span>
                        Empezar
                    </button>
                </form>
            </div>
            <div className="col-md-6">

                <h3>Tareas</h3>
                <div>
                    <label style={formStyle.label}>Máx. elementos:</label>
                    <input
                        type="number"
                        min={1}
                        max={1000}
                        step={1}
                        name="max"
                        placeholder="Max"
                        onChange={(e) =>
                            setMax(e.target.value)}
                        defaultValue={100} />
                    <label style={formStyle.label}>Orden:</label>
                    <select style={formStyle.select}
                        type="order"
                        onChange={(e) =>
                            setOrder(e.target.value)}
                        value={order} defaultValue={1}>
                        <option value={0}>Asc</option>
                        <option value={1}>Desc</option>
                    </select>
                    <button className="btn btn-light" onClick={() => getTasks()}>
                        <span>
                            <FontAwesomeIcon icon={faRotateRight} /> &nbsp;
                            Recargar
                        </span>
                    </button>

                </div>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Nombre original del archivo</th>
                            <th>Extensión original</th>
                            <th>Extensión de salida</th>
                            <th>Estado</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        {[].concat(tasks).map((task) => (
                            <tr key={task.task_id}>
                                <td>{task.task_id}</td>
                                <td><a href="#" onClick={(e) => DownloadFile(task, true)}>
                                    {task.original_file_name}</a>
                                    </td>
                                <td>{task.original_file_ext}</td>
                                <td>{task.target_file_ext}</td>
                                <td>{task.status == 'processed' ? 'Finalizado' : 'Pendiente'}</td>
                                <td>
                                    <button
                                        className="btn btn-info btn-sm btn-block"
                                        onClick={() => openModal(task)}
                                    >
                                        <span>
                                            <FontAwesomeIcon icon={faEye} /> &nbsp;
                                            Ver
                                        </span>
                                    </button>

                                    {task.status == 'processed' ? (

                                        <button
                                            className="btn btn-secondary btn-sm btn-block"
                                            onClick={(e) => DownloadFile(task, false)}
                                        >
                                            <span>
                                                <FontAwesomeIcon icon={faDownload} /> &nbsp;
                                                Descargar
                                            </span>
                                        </button>

                                    ) : (
                                        <button
                                            className="btn btn-secondary btn-sm btn-block"
                                            disabled
                                        >
                                            <span>
                                                <FontAwesomeIcon icon={faDownload} /> &nbsp;
                                                Descargar
                                            </span>
                                        </button>
                                    )}
                                    <button
                                        className="btn btn-danger btn-sm btn-block"
                                        onClick={(e) => deleteTask(task.task_id)}
                                    >
                                        <span>
                                            <FontAwesomeIcon icon={faTrashCan} /> &nbsp;
                                            Eliminar
                                        </span>
                                    </button>
                                </td>
                            </tr>
                        ))}

                    </tbody>


                </table >
                <Modal isOpen={modalOpen} onRequestClose={closeModal} style={customStyles}>
                    {selectedData && (
                        <div>
                            <h2>Información tarea: {selectedData.task_id}

                            </h2>
                            <div className="ml-auto">

                                <button className="btn btn-outline-dark ml-auto"
                                    onClick={closeModal}
                                    style={{ float: "right" }}>
                                    <FontAwesomeIcon icon={faXmark} />
                                </button>
                            </div>
                            <table className="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Nombre original del archivo</th>
                                        <th>Estensión original</th>
                                        <th>Formato de salida</th>
                                        <th>Fecha de carga</th>
                                        <th>Estado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{selectedData.original_file_name}</td>
                                        <td>{selectedData.original_file_ext}</td>
                                        <td>{selectedData.target_file_ext}</td>
                                        <td>{selectedData.uploaded_at}</td>
                                        <td>{selectedData.status}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    )}

                </Modal>
            </div>
        </div >
    );
};