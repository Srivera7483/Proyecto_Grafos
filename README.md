## Instalación y ejecución del simulador

El proyecto **Simulador interactivo de laberintos y rutas alternativas** representa un grafo dirigido y permite seleccionar configuraciones JSON, cambiar la entrada (`s`) y la salida (`t`), agregar, bloquear y restablecer pasillos, y recalcular tres resultados: camino mínimo (BFS), familia máxima de caminos disjuntos en arcos (Edmonds-Karp) y corte mínimo. PyVis destaca visualmente los arcos de cada resultado dentro de la interfaz Streamlit.

### Requisitos previos

- **Python 3.12 recomendado** (la base de código utiliza sintaxis compatible con Python 3.10 o superior).
- **Git** para clonar el repositorio.
- Navegador web moderno.
- Dependencias de Python incluidas en `requirements.txt`.

> **Nota sobre versiones:** `requirements.txt` contiene versiones fijadas de las **dependencias externas directas** (`streamlit` y `pyvis`).

### 1. Clonar el repositorio

```bash
git clone https://github.com/Srivera7483/Proyecto_Grafos
cd Proyecto_Grafos
```

### 2. Crear y activar el entorno virtual

**Windows (PowerShell, desde VS Code o una terminal):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Para comprobar que se utiliza el intérprete del entorno virtual:

```bash
python --version
```

Si Windows PowerShell bloquea la activación, ejecutar los comandos con `.\.venv\Scripts\python.exe` en lugar de `python`, sin activar el entorno.

### 3. Instalar las dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Ejecutar la interfaz web

Desde la **raíz del proyecto**

```bash
python -m streamlit run app.py
```

La aplicación se abrirá normalmente en `http://localhost:8501`. Si no se abre automáticamente, copiar la dirección dada en consola y pegarla en el navegador.

En la barra lateral se puede seleccionar un JSON desde `data/`, cambiar los terminales, bloquear/restablecer/agregar arcos y restablecer la configuración. Pulsar **Recalcular resultados** después de cambiar la red para actualizar las métricas y los resaltados del camino mínimo, caminos disjuntos y corte mínimo. Los cambios interactivos se conservan en la sesión y **no modifican los JSON originales**.

### 5. Ejecutar las verificaciones del backend (modo consola)

```bash
python app.py
```

Este modo carga `data/config_inicial.json`, comprueba restricciones y ejecuta las verificaciones del backend sin abrir Streamlit.

### 6. Ejecutar las pruebas

Para ejecutar las pruebas disponibles en `/tests`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Para descubrir todas las pruebas compatibles con `unittest`:

```bash
python -m unittest discover -s tests -v
```

### Configuraciones disponibles

- `data/config_inicial.json`: configuración principal G0.
- `data/config_12v.json`: configuración alternativa de 12 vértices.
- `data/mod_1.json`: primera modificación G1 (bloqueo de un pasillo).
- `data/mod_2.json`: segunda modificación G2 (ampliación de pasillos).
- `data/ejercicio_manual.json`: configuración de prueba; **provisional** en la versión compartida y no debe confundirse con el ejemplo manual definitivo exigido por la pauta.

### Solución de problemas frecuentes

- **`ModuleNotFoundError: No module named 'streamlit'` o `'pyvis'`:** activa el entorno `.venv` e instala las dependencias mediante `python -m pip install -r requirements.txt`.
- **No aparece la interfaz y solo ves salida de consola:** inicia con `python -m streamlit run app.py`, no con `python app.py`.
- **No se encuentran los archivos JSON:** ejecuta los comandos desde la raíz del repositorio y verificar que exista la carpeta `data/`.
- **La vista mantiene resultados anteriores:** pulsa **Recalcular resultados** tras modificar la red.
