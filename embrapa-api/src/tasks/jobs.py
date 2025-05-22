from src.scraper.embrapa_scraper import run_scraper

def run_scraper_task_bg(output_dir):
    return run_scraper(output_dir=output_dir)


