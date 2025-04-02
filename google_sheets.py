# google_sheets.py
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from log_utils import setup_logging

logger = setup_logging()

# Define the scope
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Load environment variables for the path to the credentials
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')

# Authenticate using the credentials file and the defined scope
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)

def get_or_create_worksheet(sheet_name):
    try:
        # Open the spreadsheet
        sh = client.open_by_url(os.getenv('SPREADSHEET_URL'))
        
        # Try to get the worksheet if it exists or create a new one
        try:
            worksheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=sheet_name, rows="1000", cols="20")
        logger.info(f"Worksheet '{sheet_name}' accessed or created successfully.")
        return worksheet
    except Exception as e:
        logger.error(f"Error in get_or_create_worksheet for '{sheet_name}': {e}")
        raise

def update_sheet_with_data(worksheet, data):
    try:

        worksheet.update('A2', data)
        logger.info(f"Worksheet '{worksheet.title}' updated with new data.")
    except Exception as e:
        logger.error(f"Error updating worksheet '{worksheet.title}': {e}")
        raise
