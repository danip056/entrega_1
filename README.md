# Desarrollo de soluciones cloud 2023-10
Integrantes:
* Danny Pineda Echeverri - d.pinedae@uniandes.edu.co
* Felipe Alejandro Paez Guerrero - f.paezg@uniandes.edu.co
* Vihlai Maldonado Cuevas - v.maldonado1@uniandes.edu.co

## Entrega 1

Video funcionamiento aplicación: https://youtu.be/Ctk3vgGU-Rc

### Documentación
* Documento con la arquitectura se encuentra en el archivo `Entrega 1 - Arquitectura, conclusiones y consideraciones.pdf`.
* Las instrucciones de despliegue del frontend y backend se encuentran en los archivos `README.md` en cada carpeta respectivamente.
* Documento pruebas de Postman se encuentra en el archivo `entregable_1.postman_collection.json` y la documentación publicada en: https://documenter.getpostman.com/view/10770816/2s93CPrsHf

### Endpoints abiertos
---
* Login: `POST /api/auth/login`
* Signup: `POST /api/auth/signup`

### Endpoints que requieren autenticación
---
Los siguientes endpoints requieren que el usuario previamente haya iniciado sesión con un usuario válido ya que requieren enviar un encabezado adicional con el token de autenticación:
* Get Tasks: `GET /tasks`
* Create a Task: `POST /tasks`
* Get a Task: `GET /tasks/{id_task}`
* Delete a Task: `DELETE /tasks/{id_task}`
* Get file: `GET /api/files/{filename}`
 
A continuación se describe detalladamente cada endpoint:
## Endpoints abiertos
---
### Registro del usuario
| Endpoint            | /api/auth/signup  |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Descripción         | Permite crear una cuenta de usuario, con los campos usuario, correo electrónico y contraseña. El usuario y el correo electrónico deben ser únicos en la plataforma, la contraseña debe seguir unos lineamientos mínimos de seguridad, además debe ser solicitada dos veces para que el usuario confirme que ingresa la contraseña
correctamente. |
| Método | POST  |
| Retorno| application/json, con un mensaje de confirmación si la cuenta pudo o no ser creada.|
| Parámetros Endpoint | username (String),  password1 (String), password2 (String), email(String)|

Requerimientos de la contraseña:
* La contraseña debe contener más de 8 caracteres.
* La contraseña debe contener caracteres especiales.
* La contraseña debe contener un número.
* La contraseña debe contener una letra mayúscula.

### Inicio de sesión
| Endpoint            | /api/auth/login              |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Descripción         | Permite recuperar el token de autorización para consumir los recursos del API suministrando un nombre de usuario y una contraseña correcta de una cuenta registrada. |
| Método              | POST                         |
| Retorno             | application/json, con un token de autorización.                                                                                                                      |
| Parámetros Endpoint | username (String, password (String)                                                                                                                                  |

## Endpoints que requieren autenticación
---

### Recuperar tareas
| Endpoint            | /api/auth/login|
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Descripción         | Permite recuperar todas las tareas de conversión de un usuario autorizado en la aplicación.
| Método              | GET            |
| Retorno             | Bearer Token.  |
| Parámetros Endpoint | max (int). Parámetro opcional que filtra la cantidad de resultados de una consulta. order (int). Especifica si los resultados se ordenan de forma ascendente (0) o de forma descendente (1) según el ID de la tarea. 
| Parámetros de autorización | Bearer Token.                                                                 |


### Crear una tarea
| Endpoint            | /api/tasks            |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Descripción         | Permite crear una nueva tarea de conversión de formatos. El usuario requiere autorización.|
| Método              |POST|
| Retorno             | application/json. Mensaje de confirmación indicando que la tarea fue creada.                                                                                  |
| Parámetros Endpoint | fileName (File). Ruta del archivo a subir a la aplicación. newFormat (String). Formato al que desea cambiar el archivo cargado. Los campos id, timeStamp, y status se generan de forma automática en la aplicación. El id es un campo único y auto-numérico. El timeStamp corresponde a la fecha y hora de carga del archivo. Finalmente, el status corresponde a la notificación en la aplicación siel archivo ya fue o no procesado. Para los archivos cargados su estado por defecto es uploaded, en el momento de realizar la conversión este campo pasa a processed. |
| Parámetros de autorización | Bearer Token.                                                                 |

### Recuperar tarea
| Endpoint                   | /api/tasks/< int:id_task>                                                                   |
|----------------------------|--------------------------------------------------------------------------------------------|
| Descripción                | Permite recuperar la información de una tarea en la aplicación. El usuario requiere autorización.|
| Método                     | GET                                                                                        |
| Retorno                    | application/json. Con un diccionario de la tarea especificada por un usuario.              |
| Parámetros de autorización | Bearer Token.                                                                              |

### Eliminar una tarea
| Endpoint                   | /api/tasks/< int:id_task>                                                      |
|----------------------------|-------------------------------------------------------------------------------|
| Descripción                | Permite eliminar una tarea en la aplicación. El usuario requiere autorización |
| Método                     | DELETE                                                                        |
| Retorno                    | Ninguno                                                                       |
| Parámetros de autorización | Bearer Token.                                                                 |


### Recuperar archivo
| Endpoint                   | /api/files < filename>
|----------------------------|---------------------------------------------------|
| Descripción                | Permite recuperar el archivo original o procesado |
| Método                     | GET                                               |
| Retorno                    | Retorna el archivo                                |
| Parámetros de autorización | Bearer Token.                                     |



## Entrega 3

Video funcionamiento aplicación: https://youtu.be/alpgrW_Lo3I

### Documentación
* Documento con la arquitectura se encuentra en el archivo `Entrega 3 - Arquitectura, conclusiones y consideraciones.pdf`.

### Entrega 4 

Video funcionamiento aplicación: https://youtu.be/o2vIBhF86aA 

### Documentación 

Documento con la arquitectura se encuentra en el archivo `Entrega 4 - Arquitectura, conclusiones y consideraciones.pdf`.
