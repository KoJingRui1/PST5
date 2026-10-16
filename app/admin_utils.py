# app/admin_utils.py
import logging
import shutil
import datetime
import os


def init_logger(log_file="msms.log"):
    """Configures the root logger to write to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=log_file,
        filemode="a",
    )
    print(f"Logging configured. Outputting to {log_file}")


def backup_data(data_path="data/msms.json", backup_dir="data/backups"):
    """Creates a timestamped backup of the main data file."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    if not os.path.exists(data_path):
        logging.warning(f"Data file {data_path} does not exist yet. Skipping backup.")
        return False

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"msms_backup_{timestamp}.json"
    backup_filepath = os.path.join(backup_dir, backup_filename)

    try:
        shutil.copy(data_path, backup_filepath)
        logging.info(f"Data successfully backed up to {backup_filepath}")
        return True
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
        return False