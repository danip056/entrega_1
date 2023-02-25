
# Instrucciones de despliegue **frontend**
## Prerrequisitos
---
La presente aplicación está construida en React 18.2.0, asegúrese de contar con:
1. Node y npm instalado. Las versiones a utilizadas en esta aplicación son:
```
$ node --version
v16.19.0
```

```
$ npm --version
9.4.0
```
> Puede utilizar los comandos `npm` o `npx`.

2. Tener Git instalado:

## Procedimiento para desplegar:

1. Clone el repositorio:
```
$ git clone https://github.com/danip056/entrega_1.git
```
2. Ejecute el comando:
```
npm run build
```
3. Mueva la carpeta `build` y su contenido a la carpeta para ser utilizada por su servidor.


En caso de desplegarlo con nginx ejecute los siguientes comandos:
```
sudo apt-get install nginx
sudo systemctl status nginx
```
Cree la carpeta asociada al proyecto:

```
sudo mkdir /var/www/project_one.com
sudo chown -R $USER:$USER /var/www/project_one.com
```
Mueva el contenido de la carpeta `build` a la carpeta `/var/www/project_one.com`.
```
mv build/* /var/www/project_one.com
```

Reinicie nginx:
```
sudo systemctl restart nginx
```