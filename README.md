

# Proyecto con Docker y Django

Este proyecto utiliza Docker, Django y MySQL para facilitar el despliegue y desarrollo. Sigue los pasos a continuación para configurar y ejecutar el entorno.

## Próposito del proyecto

Aplicación que conecta con diversas APIs para obtener países, fronteras y temperaturas. El usuario puede realizar una búsqueda de país lo que devolverá su temperatura y países fronterizos. Finalmente, las muestra al usuario de forma interactiva.

## Tecnologías
<a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a>
<a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a>

## 🚀 Configuración y ejecución

### 1️⃣ Levantar los servicios con Docker
```sh
docker compose up -d
```
### 2️⃣ Crear un entorno virtual en Python
```sh
python -m venv venv
```
### 3️⃣ Activar el entorno virtual
```sh
.\venv\Scripts\activate
```
### 4️⃣ Instalar las dependencias del proyecto
```sh
pip install -r .\requirements.txt
```
### 5️⃣ Generar las migraciones de la base de datos
```sh
python .\manage.py makemigrations
```
### 6️⃣ Aplicar las migraciones
```sh
python .\manage.py migrate
```
### 7️⃣ Ejecutar el servidor de desarrollo
```sh
python .\manage.py runserver
```
## 📌 Notas
Asegúrate de tener Docker y Python correctamente instalados en tu sistema.