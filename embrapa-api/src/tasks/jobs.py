from celery import Celery
from src.scraper.embrapa_scraper import run_scraper

celery_app = Celery("scraper_tasks")
celery_app.config_from_object("src.tasks.celery")

@celery_app.task
def run_scraper_task():
    return run_scraper(output_dir="data/vitibrasil")
