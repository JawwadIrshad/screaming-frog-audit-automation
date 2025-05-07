import subprocess
import logging
from log_utils import setup_logging

# Initialize logger
logger = setup_logging()


def run_screaming_frog_crawl(site_url, output_directory, screaming_frog_cli_path):
    try:
        command = [
            screaming_frog_cli_path,
            "--headless",
            "--crawl", site_url,
            "--output-folder", output_directory,
            "--save-crawl",
            "--export-tabs", "Internal:All,Response Codes:All",
            "--export-format", "csv"
        ]
        # Run the command and capture the output
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
        logger.info(f"Crawl for site '{site_url}' completed successfully.")
        return output_directory
    except subprocess.CalledProcessError as e:
        logger.error(f"Crawl for site '{site_url}' failed: {e.output}")
        raise
