import os
import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import clean_text, split_format_and_pages, get_ratings
from config import BASE_URL, WAIT_TIME

# Crear carpetas si no existen
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configuración de logging
logging.basicConfig(
    filename="logs/scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Configuración de Selenium
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, WAIT_TIME)

# Archivo CSV para almacenar los resultados
csv_file_path = "data/books.csv"
fieldnames = [
    "Título",
    "Autor",
    "Descripción",
    "Formato",
    "Número de páginas",
    "Fecha de publicación",
    "Calificación promedio",
    "Número de calificaciones",
    "Número de reseñas",
    "URL de la imagen de portada",
    "URL del libro",
    "Categoría",
]

# Crear o inicializar el archivo CSV
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Función principal
try:
    driver.get(BASE_URL)
    logging.info("Página principal cargada.")

    # Obtener enlaces de categorías
    category_links = driver.find_elements(By.CSS_SELECTOR, "div.u-defaultType a.gr-hyperlink")
    categories = {clean_text(link.text): link.get_attribute("href") for link in category_links}
    logging.info(f"Se encontraron {len(categories)} categorías: {list(categories.keys())}")

    # Limitar a categorías hasta "More genres"
    filtered_categories = {}
    for category_name, category_url in categories.items():
        if category_name == "More genres":
            break
        filtered_categories[category_name] = category_url

    logging.info(f"Scrapeando {len(filtered_categories)} categorías.")

    for category_name, category_url in filtered_categories.items():
        try:
            logging.info(f"Scrapeando la categoría: {category_name}")
            driver.get(category_url)

            # Validar libros visibles
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.bookTitle")))
            time.sleep(2)
            book_links = [link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR, "a.bookTitle")]

            if not book_links:
                logging.warning(f"No se encontraron libros en la categoría: {category_name}")
                continue

            for book_url in book_links:
                try:
                    driver.get(book_url)
                    book_data = {"URL del libro": book_url, "Categoría": category_name}

                    # Extraer información del libro
                    book_data["Título"] = clean_text(
                        wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'h1[data-testid="bookTitle"]')
                        )).text
                    )
                    book_data["Autor"] = clean_text(
                        driver.find_element(By.CSS_SELECTOR, 'span.ContributorLink__name').text
                    )
                    book_data["Descripción"] = clean_text(
                        driver.find_element(By.CSS_SELECTOR, "div[data-testid='description'] span.Formatted").text
                    )
                    pages_format = driver.find_element(By.CSS_SELECTOR, "p[data-testid='pagesFormat']").text
                    book_data["Formato"], book_data["Número de páginas"] = split_format_and_pages(pages_format)
                    book_data["Fecha de publicación"] = clean_text(
                        driver.find_element(By.CSS_SELECTOR, "p[data-testid='publicationInfo']").text
                    )
                    book_data["Calificación promedio"], book_data["Número de calificaciones"], book_data["Número de reseñas"] = get_ratings(driver)
                    book_data["URL de la imagen de portada"] = driver.find_element(By.CSS_SELECTOR, "img.ResponsiveImage").get_attribute("src")

                    # Guardar en el archivo CSV
                    with open(csv_file_path, mode="a", newline="", encoding="utf-8") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(book_data)

                    logging.info(f"Libro scrapeado: {book_data['Título']}")
                except Exception as book_error:
                    logging.error(f"Error al procesar el libro {book_url}: {book_error}")

        except Exception as category_error:
            logging.error(f"Error al procesar la categoría '{category_name}': {category_error}")

except Exception as e:
    logging.critical(f"Error durante la ejecución principal: {e}")
finally:
    driver.quit()
    logging.info("Navegador cerrado.")
