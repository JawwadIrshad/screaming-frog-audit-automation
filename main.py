# main.py
from dotenv import load_dotenv
import os
import pandas as pd
from google_sheets import get_or_create_worksheet, update_sheet_with_data
from screaming_frog import run_screaming_frog_crawl
from categorize_urls import categorize_url, custom_sort
from log_utils import setup_logging

logger = setup_logging()

# Load environment variables
load_dotenv()

# Dictionary with domain names as keys and website URLs as values
websites = {

    # Add more sites as needed
}

# Check if environment variables were loaded correctly
output_directory_base = os.getenv('OUTPUT_DIRECTORY_BASE')
screaming_frog_cli_path = os.getenv('SCREAMING_FROG_CLI_PATH')

if output_directory_base is None or screaming_frog_cli_path is None:
    logger.error("Environment variables not set correctly.")
    exit(1)


def print_dataframe_row_wise(df):
    for index, row in df.iterrows():
        logger.info(f"Row {index}:")
        logger.info(row)


for domain, site_url in websites.items():
    # Sanitize domain for sheet title
    sanitized_domain = domain.replace('.', '_')
    output_directory = os.path.join(output_directory_base, sanitized_domain)

    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logger.info(f"Created directory: {output_directory}")

    # Check if the CSV file exists
    csv_file_path = os.path.join(output_directory, 'internal_all.csv')
    if not os.path.isfile(csv_file_path):
        # If the CSV file doesn't exist, run the crawl
        logger.info(f"Starting crawl for {domain} as CSV file does not exist.")
        try:
            crawl_output = run_screaming_frog_crawl(
                site_url, output_directory, screaming_frog_cli_path)
            logger.info(f"Crawl completed for {domain}")
        except Exception as e:
            logger.error(f"Error running crawl for {domain}: {e}")
            continue  # Skip to the next domain if crawl fails
    else:
        logger.info(f"CSV file already exists for {domain}, skipping crawl.")

        try:
            # Read the CSV into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Define all possible columns
            all_possible_columns = [
                'Address', 'Content Type', 'Status Code', 'Status', 'Indexability',
                'Indexability Status', 'Title 1', 'Title 1 Length', 'Title 1 Pixel Width',
                'Title 2', 'Title 2 Length', 'Title 2 Pixel Width', 'Meta Description 1',
                'Meta Description 1 Length', 'Meta Description 1 Pixel Width', 'Meta Keywords 1',
                'Meta Keywords 1 Length', 'H1-1', 'H1-1 Length', 'H1-2', 'H1-2 Length',
                'H2-1', 'H2-1 Length', 'H2-2', 'H2-2 Length', 'Meta Robots 1', 'X-Robots-Tag 1',
                'Meta Refresh 1', 'Canonical Link Element 1', 'rel="next" 1', 'rel="prev" 1',
                'HTTP rel="next" 1', 'HTTP rel="prev" 1', 'amphtml Link Element', 'Size (bytes)',
                'Word Count', 'Sentence Count', 'Average Words Per Sentence',
                'Flesch Reading Ease Score', 'Readability', 'Text Ratio', 'Crawl Depth', 'Link Score',
                'Inlinks', 'Unique Inlinks', 'Unique JS Inlinks', '% of Total', 'Outlinks',
                'Unique Outlinks', 'Unique JS Outlinks', 'External Outlinks', 'Unique External Outlinks',
                'Unique External JS Outlinks', 'Closest Similarity Match', 'No. Near Duplicates',
                'Spelling Errors', 'Grammar Errors', 'Hash', 'Response Time', 'Last Modified',
                'Redirect URL', 'Redirect Type', 'Cookies', 'HTTP Version', 'URL Encoded Address',
                'Crawl Timestamp', 'Category'
            ]

            # Filter the list to only include columns that exist in the DataFrame
            columns_to_include = [
                col for col in all_possible_columns if col in df.columns]

            # Reorder DataFrame columns based on the filtered list
            df = df[columns_to_include]

            # Apply custom sorting
            df.sort_values(by='Address', key=lambda x: x.map(
                custom_sort), inplace=True)

            # Apply categorization function to each URL
            df['Category'] = df['Address'].apply(categorize_url)

            # Replace NaN values with an empty string
            df.fillna('', inplace=True)

            # Convert DataFrame to a list of lists, where each sublist is a row
            data_to_upload = df.values.tolist()  # This excludes the header row

            # Get the worksheet for the domain
            worksheet = get_or_create_worksheet(sanitized_domain)

            # Update the worksheet with the new data
            update_sheet_with_data(worksheet, data_to_upload)
            logger.info(
                f"Data for {domain} has been updated in Google Sheets on tab '{sanitized_domain}'.")

        except Exception as e:
            logger.error(f"Error processing data for {domain}: {e}")
