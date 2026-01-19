# 🤖 SQL AI Agent (Python + Groq)

Este proyecto es una implementación ligera de un **Agente de IA Text-to-SQL**. Utiliza la potencia de la LPU de **Groq** (modelo Llama 3) para traducir preguntas en lenguaje natural a consultas SQL ejecutables, interactuando en tiempo real con una base de datos SQLite en memoria.

## 🚀 Características

* **Traducción Natural:** Convierte preguntas como *"¿Cuál es el producto más caro?"* en SQL válido.
* **Velocidad Extrema:** Usa la API de Groq para inferencia casi instantánea.
* **Base de Datos Volátil:** Implementa SQLite en memoria (`:memory:`) para pruebas rápidas sin configuración de servidores.
* **Seguro:** Gestión de credenciales mediante variables de entorno.

## 🛠️ Stack Tecnológico

* **Python 3.12+**
* **Groq SDK** (LLM Inference)
* **SQLite3** (Motor de base de datos)
* **Python-Dotenv** (Manejo de config)

## 📦 Instalación

1.  **Clonar el repositorio**
    ```bash
    git clone [https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git](https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git)
    cd NOMBRE_DEL_REPO
    ```

2.  **Crear y activar entorno virtual**
    * En Windows:
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * En Linux/Mac:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1.  Copia el archivo de ejemplo de variables de entorno:
    ```bash
    cp .env.example .env
    # En Windows CMD: copy .env.example .env
    ```

2.  Abre el archivo `.env` y pega tu API Key de Groq:
    ```text
    GROQ_API_KEY=gsk_tu_api_key_super_secreta...
    ```

## ▶️ Uso

Ejecuta el script principal pasando tu pregunta como argumento entre comillas:

```bash
python main.py "cuantos productos hay en stock?"