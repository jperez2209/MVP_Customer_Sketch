# INSTRUCCIONES

en el archivo requirements.txt se indican las librerías necesarias para correr el aplicativo
se adjunta script de sql con la estructura de la base de datos (MySQL) necesaria para las operaciones CRUD

## Pasos
1. Crear descargar archivos
2. Abrir la carpeta donde se guardan los archivos mediante el editor de código o IDE  de preferencia
3. Iniciar una nueva terminal en el IDE
4. crear entorno virtual de python comando: python -m venv .venv
5. Activar entorno virtual .venv\Scripts\activate
6. Actualizar pip: python.exe -m pip install --upgrade pip
7. instalar librerías acorde a lo indicado en requirements.txt, se recomienda eempezar instalando streamlit (pip install streamlit) ya que con ello se instalarán por default algunas de las librerías indicadas
8. Abrir una terminal y escribir comando streamlit run app.py
9. Para que el aplicativo sea funcional se debe crear previamente la base de datos, el usuario para ingresar no puede crearse mediante la interfaz, por lo cuál debe crearse directamente en el gestor de MySQL

