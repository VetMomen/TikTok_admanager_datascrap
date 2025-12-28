from datetime import datetime
import os
import time
import subprocess
from logger import setup_logger

logger = setup_logger("scheduler")

log_path = os.path.join(os.getcwd(), "log")
os.makedirs(log_path, exist_ok=True)
last_run_time_file = os.path.join(log_path, "last_time_run.txt")
main_script = "main.py"
time_interval = 12


def get_last_time_run():
    if not os.path.exists(last_run_time_file):
        return None

    with open(last_run_time_file, "r") as file:
        last_time_run = datetime.fromisoformat(file.read().strip())
        return last_time_run


def save_report_time():
    with open(last_run_time_file, "w") as file:
        file.write(datetime.now().isoformat())


def should_run():
    last_time = get_last_time_run()
    if last_time == None:
        return True, 0

    else:
        elapsed = ((datetime.now() - last_time).total_seconds()) / (60 * 60)
        return elapsed > time_interval, elapsed


def running_scrap():
    can_run, elapsed = should_run()
    if can_run:
        logger.info("Time to run the scraper.")
        subprocess.run(["python3", main_script])
        save_report_time()
        logger.info("Scraper execution finished.")
    else:
        logger.info(
            f"Only {elapsed:.2f} hours passed, please wait for {time_interval - elapsed:.2f} remaining hours"
        )


if __name__ == "__main__":
    running_scrap()
