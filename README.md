# Proyecto Scuba cat

## Descripción
Este repositorio contiene el código fuente del proyecto **Scuba cat**, cuyo objetivo es a través de la identififación del gesto, que se despliegue un GIF animado.

**Nota importante sobre la versión de Python**  
El proyecto **DEBE ejecutarse utilizando Python 3.10**, ya que existen incompatibilidades y excepciones en librerías críticas cuando se utiliza una versión diferente.

## Requisitos de Python

- **Python 3.10.x (obligatorio)**
- No se garantiza compatibilidad con:
  - Python 3.11+
  - Python 3.9 o versiones anteriores

### Motivo
Algunas de las librerías utilizadas en el proyecto:
- tienen dependencias aún no compatibles,
- o generan excepciones de ejecución fuera de Python 3.10.

Por esta razón, el branch `main` está **validado y soportado únicamente en Python 3.10**.

## Ejemplo de uso

Usando el gestor de proyectos **uv**:

```bash
# Instalar Python 3.10 si aún no está presente
uv python install 3.10
# Crear entorno virtual con esta versión
uv venv --python 3.10
# Activar el entorno
source .venv/bin/activate # Linux
.venv\Scripts\activate # Windows Powershell
# Instalar dependencias
uv pip install opencv-python mediapipe==0.10.21 imageio
# Correr
uv run main.py
```