# Dreamfit Aluche Bot

Este repositorio contiene un bot de Telegram que consulta el aforo actual del gimnasio **Dreamfit Aluche**.

## Características

- Obtiene la ocupación (porcentaje, personas actuales y aforo total) desde la página oficial de Dreamfit.
- Responde a cualquier mensaje en Telegram con el aforo actualizado.
- Utiliza formato HTML y emojis para mostrar la información de forma clara.
- Incluye un bucle de mantenimiento para hacer peticiones periódicas a la API de Telegram.

## Requisitos

- Python 3.8 o superior.
- Dependencias indicadas en `requirements.txt` (requests y beautifulsoup4).

## Uso local

1. Clona este repositorio y navega a la carpeta del proyecto.

   ```bash
   git clone https://github.com/atesoroch-cpu/dreamfitaluchebot.git
   cd dreamfitaluchebot
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Define la variable de entorno `BOT_TOKEN` con el token de tu bot de Telegram:

   ```bash
   export BOT_TOKEN=<tu-token-de-telegram>
   ```

4. Ejecuta el bot:

   ```bash
   python main.py
   ```

El bot comenzará a escuchar mensajes y responderá con el aforo del gimnasio.

## Despliegue en Fly.io

1. Crea una aplicación en [Fly.io](https://fly.io/) y enlaza este repositorio.
2. Define el secreto `BOT_TOKEN` en Fly.io:

   ```bash
   fly secrets set BOT_TOKEN=<tu-token-de-telegram>
   ```

3. Despliega la aplicación desde el dashboard de Fly.io.

Fly.io se encargará de ejecutar el bot de forma continua.

## Notas de seguridad

- **No incluyas tu token de Telegram en el código ni lo subas a repositorios públicos.** Utiliza siempre variables de entorno para configurarlo.
- Este repositorio está configurado para leer `BOT_TOKEN` del entorno y nunca exponer el token en el código.
