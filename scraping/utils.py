def clean_text(text):
    """Limpia el texto eliminando espacios y caracteres no deseados."""
    return text.strip() if text else "No disponible"

def split_format_and_pages(pages_format):
    """Separa el formato y número de páginas del libro."""
    if pages_format:
        parts = pages_format.split(",")
        if len(parts) == 2:
            return parts[1].strip(), parts[0].strip()
    return "Formato no encontrado", "Número de páginas no encontrado"

def get_ratings(driver):
    """Extrae calificaciones y reseñas de un libro."""
    try:
        rating = driver.find_element(By.CSS_SELECTOR, "div.RatingStatistics__rating").text
        ratings_count = driver.find_element(By.CSS_SELECTOR, "span[data-testid='ratingsCount']").text
        reviews_count = driver.find_element(By.CSS_SELECTOR, "span[data-testid='reviewsCount']").text
        return rating, ratings_count, reviews_count
    except Exception:
        return "Calificación no encontrada", "No disponible", "No disponible"
