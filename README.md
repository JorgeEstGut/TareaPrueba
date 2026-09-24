# CRUD de Tareas — Flask + Neon (PostgreSQL)

## Pasos para ejecutar

1. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Edita el archivo `.env` y coloca tu cadena de conexión de Neon:
   ```
   DATABASE_URL=postgresql://usuario:password@ep-xxxxx.neon.tech/nombredb?sslmode=require
   ```
   La obtienes desde el dashboard de Neon (Connection Details).

4. Ejecuta la aplicación:
   ```
   python app.py
   ```
   La tabla `tareas` se crea automáticamente al iniciar (init_db()).

5. Abre en el navegador:
   ```
   http://127.0.0.1:5000
   ```

## Estructura del proyecto
```
crud_tareas/
├── app.py
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── index.html
│   └── form.html
└── static/
    └── style.css
```

## Funcionalidades
- Crear tarea
- Listar tareas
- Editar tarea
- Eliminar tarea
- Marcar como completada
