# Montecarlo Tree Search en el ajedrez vikingo: Introducción a la búsqueda de la heurística perfecta

Este es el proyecto para la asignatura de Machine Learning Engineering del Máster en Ingeniería Informática: Cloud, Datos y Gestión TI en el curso 2023-2024. Realizado por Vicente Cambrón Tocados y Alejandro García Fernández.

# Guía para lanzar el proyecto

## Requisitos previos al lanzamiento del proyecto

- Tener instalado [Node.JS](https://nodejs.org/es/download/) y con él su gestor de paquetes: npm
- Tener instalado [Git](https://git-scm.com/downloads) en nuestro ordenador
- Tener instalado [Python](https://www.python.org/downloads/) y su correspondiente gestor de paquetes [pip](https://pypi.org/project/pip/)

## Instalación de paquetes de python externos

Para el correcto funcionamiento de la palicación, será necesario contar con los siguientes paquetes en python.
Estos pueden instalarse utilizando pip. Son los que siguen:

- Flask
- Flask CORS

## ¿Cómo arrancar el servidor del proyecto localmente?

En primer lugar, nos dirigimos al directorio en el que deseemos guardar el proyecto. Lo clonamos y accedemos:

```
git clone https://github.com/Alex-GF/ajedrez-vikinga.git
cd montecarlo
cd backend
```

Desde esta carpeta ejecutamos el siguiente comando para lanzar el servidor:

```
python server.py
```

Si todo ha ido bien, el servidor debería estar arrancado en el puerto 8080 por defecto. Al no tener ninguna vista definida, no se recomienda acceder a localhost:8080.

## Configuración de variables de entorno

1. Entrar a la carpeta client:

```
cd ./client/
```

2. Dentro de la carpeta, crear un nuevo archivo con el nombre **.env.local**.

3. Rellenar **.env.local** con las variables de entorno que aparecen en **.env.example**, sustituyendo los guiones entre comillas por la dirección en la que se ejecuta la api REST de nuestro servidor. Si el servidor está lanzado en el puerto 8080, quedarían así:

```
REACT_APP_API_BASE_URL = "http://localhost:8080/api/v1/"
```

**Es importante no olvidar la barra final**

## ¿Cómo arrancar el frontend?

Dentro de la carpeta principal del proyecto, nos dirigimos a ./client/:

```
cd ./client/
```

Dentro de esta carpeta, instalamos los paquetes necesarios y lanzamos el servidor de frontend con el siguiente flujo de comandos:

```
npm install -g yarn
yarn install
yarn start
```

Si el último comando da error, ejecutar lo siguiente:

```
yarn add react-scripts
```

A continuación, arrancamos de nuevo:

```
yarn start
```

Si todo ha ido bien, debería abrirse de manera automática una pestaña en su navegador con la página del proyecto.
