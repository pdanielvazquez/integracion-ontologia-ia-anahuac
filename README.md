# Integración de una ontología en un sistema multiagente

Proyecto académico que integra una ontología de dominio universitario como base de conocimiento para un equipo de agentes. El agente consultor obtiene información de la ontología, el agente validador revisa la respuesta y el agente coordinador prepara un informe consolidado.

La implementación principal está en [`integracion.ipynb`](./integracion.ipynb). La ontología de ejemplo está en [`ontologia-ia-anahuac-ejemplo-1.owx`](./ontologia-ia-anahuac-ejemplo-1.owx). El archivo [`prueba.py`](./prueba.py) permite inspeccionar por separado los elementos de la ontología.

## Requisitos previos

- Windows 10/11 (los comandos de instalación de esta guía son para PowerShell).
- Python 3.12 recomendado (el notebook se creó con Python 3.12).
- [Ollama](https://ollama.com/) instalado y ejecutándose localmente.
- Git, si se va a clonar el repositorio.
- Para abrir el notebook: VS Code con la extensión **Jupyter**, o JupyterLab instalado en el entorno.

El notebook configura el modelo `ollama/llama3.2` con la API local de Ollama en `http://localhost:11434`; no requiere una clave de API externa.

## Componentes del proyecto

### Ontología

El archivo OWX contiene las clases, relaciones, atributos, restricciones y datos de ejemplo del dominio académico.

**Clases:** `Persona`, `Alumno`, `Empleado`, `Academico`, `Administrativo`, `Coordinador`, `JefeDepartamento`, `Profesor`, `Visitante` y `Materia`.

**Jerarquía principal:**

- `Alumno`, `Empleado` y `Visitante` son subclases de `Persona`.
- `Academico` y `Administrativo` son subclases de `Empleado`.
- `Coordinador`, `JefeDepartamento` y `Profesor` son subclases de `Academico`.

**Propiedades de objeto** (relaciones entre individuos): `atiendeA`, `esImpartidaPor`, `esProfesorDe`, `estaInscritoEn`, `imparteClaseA`, `registraA`, `solicitaAtencion`, `solicitaRegistro`, `tieneInscrtos` y `tomaClaseCon`.

**Propiedades de datos** (atributos literales): `tieneClave`, `tieneCreditos`, `tieneEdad`, `tieneGenero`, `tieneNoCuenta`, `tieneNombre`, `tieneNombreMateria` y `tienePeso`.

La ontología incluye individuos de ejemplo como `alumno_001`, `alumno_002`, `alumno_003`, `materia_001`, `materia_002`, `profesor_001` y `profesor_002`, así como axiomas de jerarquía, disyunción y cardinalidad.

### Herramienta de consulta

En el notebook, `consultar_ontologia` carga el archivo OWX usando Owlready2 y ofrece consultas que los agentes pueden invocar:

- `buscar_alumno`: busca un individuo por su identificador y devuelve su nombre y número de cuenta cuando están disponibles.
- `materias_inscritas`: consulta las materias relacionadas con el individuo mediante `estaInscritoEn`.
- `profesor_materia`: intenta obtener el profesor asociado a una materia.
- `resumen_clases`: devuelve los nombres de las clases de la ontología.

Los identificadores de ejemplo usan nombres como `alumno_001` y `materia_001`. La ruta del OWX es relativa al directorio desde el que se ejecuta el notebook o el script, por lo que ambos archivos deben permanecer juntos.

### Agentes y tareas

El notebook define tres agentes con responsabilidades distintas:

1. **Agente consultor (`agente_consultor`)**: interpreta la solicitud y utiliza la herramienta para consultar la ontología. Sus instrucciones le indican que no invente datos que no estén disponibles.
2. **Agente validador (`agente_validador`)**: revisa la pertinencia y coherencia del resultado frente a la ontología.
3. **Agente coordinador (`agente_coordinador`)**: consolida la consulta y el dictamen en un informe final.

Las tareas correspondientes son `tarea_consulta`, `tarea_validacion` y `tarea_informe_final`. El objeto `equipo` de CrewAI agrupa agentes y tareas con `Process.sequential`, de modo que se ejecuten en ese orden.

### Ejecución asíncrona

La función `main()` espera el resultado de `equipo.kickoff_async()` y lo imprime. El notebook se debe ejecutar en orden para que primero se inicialicen el modelo, la herramienta, los agentes, las tareas y el equipo.

## Instalación paso a paso (Windows PowerShell)

Abre PowerShell en la carpeta raíz del proyecto. Si aún no tienes el repositorio, clónalo y entra en su carpeta:

```powershell
git clone https://github.com/pdanielvazquez/integracion-ontologia-ia-anahuac.git
cd integracion-ontologia-ia-anahuac
```

1. **Crea un entorno virtual con Python 3.12:**

   ```powershell
   py -3.12 -m venv integracion-env
   ```

2. **Activa el entorno virtual:**

   ```powershell
   .\integracion-env\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, permite scripts solo para la sesión actual y vuelve a activarlo:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\integracion-env\Scripts\Activate.ps1
   ```

3. **Actualiza pip e instala las dependencias declaradas:**

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   El archivo [`requirements.txt`](./requirements.txt) contiene las versiones fijadas de CrewAI, Owlready2, IPykernel y sus dependencias.

4. **Descarga el modelo utilizado por el notebook:**

   ```powershell
   ollama pull llama3.2
   ```

5. **Inicia Ollama**, si no se está ejecutando ya. En una terminal aparte:

   ```powershell
   ollama serve
   ```

   Deja esa terminal abierta mientras ejecutas el notebook. La aplicación de escritorio de Ollama también puede mantener el servicio activo.

## Ejecución paso a paso

### Opción A: VS Code (recomendada)

1. Abre la carpeta del proyecto en VS Code e instala/habilita la extensión **Jupyter** si es necesario.
2. Abre [`integracion.ipynb`](./integracion.ipynb).
3. Selecciona como kernel el Python del entorno `integracion-env` (por ejemplo, `.\integracion-env\Scripts\python.exe`).
4. Confirma que Ollama está ejecutándose y que `ollama list` muestra el modelo `llama3.2`.
5. Ejecuta las celdas desde el inicio, en orden. Las celdas crean el cliente de Ollama, registran la herramienta, definen los tres agentes y sus tareas, y construyen el equipo.
6. Ejecuta la última celda (`await main()`). CrewAI procesará las tareas secuencialmente y mostrará el informe en la salida del notebook.

### Opción B: JupyterLab

Con el entorno virtual activado, instala JupyterLab si todavía no está disponible:

```powershell
python -m pip install jupyterlab
python -m jupyter lab integracion.ipynb
```

Selecciona el kernel de `integracion-env` y sigue los pasos 4–6 de la opción anterior.

### Inspección independiente de la ontología

Para listar las clases, propiedades de objeto, propiedades de datos e individuos del archivo OWX sin iniciar CrewAI ni Ollama:

```powershell
python prueba.py
```

Este script es una comprobación básica de lectura de la ontología; no ejecuta el flujo multiagente.

## Limitaciones conocidas

- La consulta `profesor_materia` de la herramienta comprueba una propiedad llamada `impartidaPor`, mientras que la ontología declara `esImpartidaPor`. Por esta diferencia de nombres, esa consulta puede no recuperar el profesor hasta que se armonicen la herramienta y la ontología.
- La herramienta y el flujo de consulta son ejemplos académicos sobre datos incluidos en el OWX; no están conectados a un sistema escolar real.
- Si aparece un error de conexión o de modelo, confirma que Ollama esté activo en `http://localhost:11434` y que el modelo `llama3.2` ya se haya descargado.

## Estructura del repositorio

```text
.
├── integracion.ipynb                    # Implementación del flujo CrewAI
├── ontologia-ia-anahuac-ejemplo-1.owx    # Ontología y datos de ejemplo
├── prueba.py                             # Inspección de clases y propiedades
├── requirements.txt                      # Dependencias Python fijadas
└── README.md                             # Esta documentación
```
