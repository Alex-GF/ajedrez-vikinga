# Comparando Modelos de Q-Learning y Montecarlo Tree Search en el Desarrollo de Agentes para el Ajedrez Vikingo

Este es el proyecto para la asignatura de Machine Learning Engineering del Máster en Ingeniería Informática: Cloud, Datos y Gestión TI en el curso 2023-2024. Realizado por Vicente Cambrón Tocados y Alejandro García Fernández.

# Guía para lanzar el proyecto

## Requisitos previos al lanzamiento del proyecto

- Tener instalado [Git](https://git-scm.com/downloads) en nuestro ordenador
- Tener instalado [Python](https://www.python.org/downloads/) y su correspondiente gestor de paquetes [pip](https://pypi.org/project/pip/)

## Instalación de paquetes de python externos

Para el correcto funcionamiento de la palicación, será necesario instalar todos los paquetes que se encuentran en el fichero *requirements.txt*, localizado en la raíz del proyecto, con el siguiete comando:

```
pip install -r requirements.txt
```

Además se deberá de instalar el entorno para [Gymnasium](https://gymnasium.farama.org/index.html) de *hnefatafl* mediante el siguiente comando desde la raíz del proyeto:

```
pip install -e hnefatafl
```

## Estructura del proyecto

```
- /ajedrez-vikinga
  | ...
  |
  ├─ /analysis
  |  |
  |  ├─ /results
  |  |  | ...
  |  |
  |  └─ agents_analysis.ipynb
  |
  └─ /backend
     | ...
     |
     └─ /agents
        |
        ├─ /MCTS
        |  | ...
        |  |
        |  ├─ /trainings
        |  |  | ...
        |  |  |
        |  |  └─ hnefataflWhites.py
        |  |
        |  └─ mctsAgent.py
        |
        └─ /QLearning
           | ...
           |
           ├─ /trainings
           |  | ...
           |  |
           |  └─ hnefataflWhites.py
           |
           └─ qlearningAgent.py

```

Los ficheros *mctsAgent.py* y *qlearningAgent.py* son donde se han implementado cada agente, mientras que los ficheros *hnefataflWhites.py* son donde, en nuestro caso, hacemos uso de los agentes, dandole una configuración de hiperparámetros, configurando el tablero, número de episodios ... 
En la carpeta *analysis* se encuentra el fichero *agents_analysis.ipynb*, donde se evalua la mejor configuración de hiperparámetros y cual es el mejor agente, y los csv obtenidos de la rama *results*.

## ¿Cómo ver los agentes en funcionamiento?

Una vez instalado los paquetes solo tendremos que lanzar cualquiera de los ficheros *hnefataflWhites.py*, realizando cualquier modificación sobre los agentes o el entorno si asi lo queremos:

```
python backend/agents/MCTS/trainings/hnefataflWhites.py
```
o
```
python backend/agents/QLearning/trainings/hnefataflWhites.py
```
