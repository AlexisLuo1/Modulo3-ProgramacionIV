Biblioteca Personal con SQLAlchemy y PyMySQL

Aplicación de consola en Python para administrar una biblioteca personal usando MySQL/MariaDB, SQLAlchemy como ORM y PyMySQL como conector.

Objetivo

Permitir gestionar libros mediante una aplicación de línea de comandos, utilizando SQLAlchemy para manejar la base de datos de forma orientada a objetos.

Funcionalidades

La aplicación permite:

Agregar libros

Actualizar datos de un libro

Eliminar libros

Ver el listado completo

Buscar por título, autor o género

Salir del programa

Tecnologías utilizadas

Python 3

SQLAlchemy

PyMySQL

MariaDB o MySQL

Instalación de dependencias

Ejecute el siguiente comando: 

pip install -r requirements.txt

Configuración de la base de datos

Instalar MariaDB o MySQL.

Crear una base de datos:

CREATE DATABASE biblioteca_db;


Asegurarse de tener un usuario con permisos:

CREATE USER 'root'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON biblioteca_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;


Verificar que en el archivo Python la cadena de conexión sea:

mysql+pymysql://root:1234@localhost/biblioteca_db

Ejecución del programa

Ejecute:

python app.py

Estructura recomendada del proyecto
biblioteca/
│── app.py
│── requirements.txt

Notas

La tabla libros se crea automáticamente mediante SQLAlchemy.

Si aparece un error de conexión, revise usuario, contraseña y que el servidor de MariaDB esté iniciado.
