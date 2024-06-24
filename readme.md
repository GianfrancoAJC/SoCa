# SoCa for users

SoCa es una aplicación web diseñada en el marco del curso de Gerencia de Productos Digitales I de la Universidad de Ingeniería y Tecnología, en adelante UTEC, Lima, Perú. La aplicación le permite a sus usuarios determinar si presentan comportamientos que podrían describir afecciones como el FOMO o sufren de algún tipo de dependencia de sus redes sociales. De esta manera, SoCa busca concientizar a los usuarios sobre el uso de las redes sociales y promover un uso saludable de las mismas. Nuestra meta es que en algún momento SoCa sea utilizada, de forma nativa, por cualquier persona en el mundo que lo necesite e incluso esté integrada en todas las redes sociales que usamos en nuestro día a día.

## Funcionalidades

- Test de FOMO: Permite a los usuarios responder un cuestionario rápido para determinar si presentan comportamientos que podrían describir afecciones como el FOMO.
- Simulador: Permite a los usuarios interactuar con un simulador de red social para determinar si presentan comportamientos que podrían describir afecciones como el FOMO.

## Proyect setup

1. Clona el repositorio:

```bash
git clone https://github.com/GianfrancoAJC/SoCa.git
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Cambia las rutas del backend en config/qa.py y config/local.py:

```bash
cd backend/config
```

4. Inicie la ejecución del servidor backend:

```bash
source backend/ejecutar.sh
```

5. Inicie la ejecución del servidor frontend:

```bash
cd frontend
npm run serve
```

## Uso

1. Abre tu navegador web y visita http://localhost:8080.

2. Create una cuenta empleando un correo electrónico.

3. Ingresa al test rápido o al simulador e interactúa con él.

4. Revisa los resultados obtenidos.


# SoCa for developers

## Tecnologías Utilizadas

- Python
- Flask
- Vue.js
- Node.js
- JavaScript
- SQLAlchemy
- PostgreSQL
- UUID
- CORS
- JWT
- Axios
- Blueprint
- Scikit-learn
- Smtplib
- Pandas
- Bootstrap
- HTML
- CSS

## Structure Project

```
SoCa/
│
├── backend/                                     # Directorio del backend
│   ├── app/                                     # Directorio de la aplicación Flask
│   │   ├── __init__.py                          # Archivo de inicialización y endpoints de la aplicación
│   │   ├── authentication.py                    # Archivo con las funciones de autenticación
│   │   ├── models.py                            # Archivo con los modelos de la base de datos
│   │   ├── users_controller.py                  # Archivo con los endpoints de autenticación
│   │   └── utilities.py                         # Archivo con los servicios de la aplicación
├── ├── config/                                  # Directorio de configuración de la aplicación
│   │   ├── local.py                             # Archivo con la ruta local de la base de datos
│   │   ├── production.py                        # Archivo con la ruta de producción de la base de datos
│   │   └── qa.py                                # Archivo con la ruta de control de calidad de la base de datos
├── ├── static/                                  # Directorio de archivos estáticos
│   │   ├── Facebook-Icon.png                    # Imagen logo de Facebook
│   │   ├── favicon.ico                          # Ícono de la página
│   │   ├── Instagram-Icon.jpg                   # Imagen logo de Instagram
│   │   └── logo.ico                             # Ícono alternativo de la página
├── ├── ejecutar.sh                              # Archivo para ejecutar el servidor backend de la aplicación
├── └── requirement.txt                          # Archivo de requerimientos para instalar las dependencias
├── frontend/                                    # Directorio del frontend
│   ├── public/                                  # Directorio de archivos públicos
│   │   ├── favicon.ico                          # Ícono de la página
│   │   └── index.html                           # Página de inicio
│   ├── src/                                     # Directorio de archivos fuente
│   │   ├── assets/                              # Directorio de archivos de recursos
│   │   │   └── logo.png                         # Imagen de logo de la aplicación
│   │   ├── components/                          # Directorio de componentes
│   │   │   ├── ChatApp.vue                      # Componente de generación de chats
│   │   │   ├── ChatList.vue                     # Componente de la lista de chats
│   │   │   ├── ChatWindow.vue                   # Componente de vistas de chat
│   │   │   ├── MessageImput.vue                 # Componente de entrada de mensajes
│   │   │   └── UserQuestionnaire.vue            # Componente de cuestionario inicial para usuarios
│   │   ├── router/                              # Directorio de rutas
│   │   │   └── index.js                         # Archivo de rutas de la aplicación
│   │   ├── App.vue                              # Archivo principal de la aplicación Vue
│   │   └── main.js                              # Archivo de inicialización de la aplicación Vue
│   ├── .browserslistrc                          # Archivo de configuración de navegadores
│   ├── .eslintrc.js                             # Archivo de configuración de ESLint
│   ├── babel.config.js                          # Archivo de configuración de Babel
│   ├── package.json                             # Archivo de configuración de npm
│   └── vue.config.js                            # Archivo de configuración de Vue
├── .gitignore                                   # Archivo de git para ignorar archivos y directorios locales
└── README.md                                    # Archivo de documentación del proyecto
```

## Operations

### Create User

```
curl -F "username=Juan" -F "password=Perez" -F "confirmationPassword=Perez" -F "utoken=1234" -F "rtoken=1234" -X POST http://localhost:5001/users

{
  "user_created_id": "27b79c53-edeb-4caf-9bcb-3725669eaa9d",
  "token": "token",
  "success": True
}

curl -X POST http://localhost:5001/users

{
  "errors": [
    "username is required",
    "password is required",
    "confirmationPassword is required",
    "utoken is required",
    "rtoken is required"
  ],
  "message": "Error creating a new user",
  "success": False
}
```

## Contribución

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del proyecto.

2. Crea una nueva rama con tu nombre:

```bash
git checkout -b <nombre-de-la-rama>
```

3. Realiza tus cambios y haz un commit:

```bash
git commit -am "Descripción de los cambios"
```

4. Sube tus cambios a tu repositorio:

```bash
git push origin <nombre-de-la-rama>
```

5. Crea un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - mira el archivo [LICENSE]

## Contacto

Si tienes alguna pregunta o sugerencia, por favor contáctame a través de mi correo electrónico: aldo.jaimes@utec.edu.pe