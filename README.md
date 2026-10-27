# Documentación de Despliegue [RA2.F]

## Creación de la cuenta
Me registré en la plataforma Render conectando directamente mi cuenta de GitHub para permitir la autorización y vinculación automática de mis proyectos.

## Configuración del repositorio
Creé un repositorio público en GitHub llamado `OPIA-GRUPO-7`. Subí todo el código fuente de la API, el archivo de dependencias y el modelo entrenado (`modelo_california.pkl`) a la rama principal (`main`).

## Comando de despliegue
Desde el panel de Render, importé el repositorio y configuré el servicio web. Establecí el comando de instalación de dependencias (`pip install -r requirements.txt`) y el comando de arranque para ejecutar la aplicación con Uvicorn.

## URL Final
La aplicación se ha desplegado correctamente y el servicio es accesible públicamente en la siguiente dirección: https://opia-grupo-7.onrender.com
