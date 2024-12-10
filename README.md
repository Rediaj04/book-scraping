# Book Scraping Management

**Book Scraping Management** es un proyecto que automatiza la recolección, gestión y almacenamiento de datos sobre libros desde una fuente web, convirtiendo la información recopilada en un formato estructurado y almacenándola en una base de datos.

Este proyecto tiene como objetivo facilitar la importación, organización y actualización de libros para una base de datos o sistema de gestión de inventario.

## Funcionalidades

- **Scraping de libros:** Recopila información de libros desde una página web (ej. Goodreads).
- **Gestión de categorías:** Extrae y organiza libros por categorías específicas.
- **Exportación a CSV:** Los datos recolectados se guardan en un archivo CSV para su posterior procesamiento.
- **Importación a base de datos:** Los datos CSV se pueden importar a una base de datos para su gestión a largo plazo.

## Requisitos

- Python 3.8 o superior
- Selenium
- Pandas
- MySQL o cualquier otro sistema de base de datos compatible

## Instalación

### Clonación del repositorio

```bash
git clone https://github.com/tu-usuario/book-scraping-management.git
cd book-scraping-management
```

### Instalación de dependencias
1. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
```
2. Activa el entorno virtual:
* En Windows:
```bash
.\venv\Scripts\activate
```
* En Mac/Linux:
```bash
source venv/bin/activate
```
3. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Configura el archivo `.env` o las variables de entorno con la información de conexión a la base de datos y otros parámetros de configuración si es necesario.

2. Si no tienes las credenciales necesarias para acceder a la fuente de datos (por ejemplo, Goodreads API), deberás obtenerlas e ingresarlas en la configuración.

## Uso
Para iniciar el proceso de scraping y gestionar los datos de los libros:
```bash
python main.py
```
Este comando ejecutará el scraper, recopilando datos de las categorías especificadas y guardándolos en un archivo CSV. Luego, el archivo CSV se puede importar en una base de datos, si así se desea.

## Opciones de ejecución

- **CSV exportado**: Después de ejecutar el scraper, se generará un archivo CSV dentro de la carpeta `data/` con los datos de los libros extraídos.
- **Base de datos**: La información puede ser importada a la base de datos configurada usando los scripts correspondientes.

## Manejo de errores

- Los errores relacionados con la conexión a la página web o la base de datos se registran en un archivo de log (`logs/scraping.log`).
- Los libros duplicados se verifican antes de ser añadidos a la base de datos.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto o corregir errores, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b mi-nueva-rama`).
3. Realiza los cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a tu rama (`git push origin mi-nueva-rama`).
5. Abre un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

Desarrollado por [Rediaj04].
