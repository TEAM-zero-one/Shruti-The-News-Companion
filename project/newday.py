import os
import nltk
from pathlib import Path
from process import start_new
nltk.download('punkt')
nltk.download('stopwords')

csv_folder = Path(__file__).resolve().parent  # Get the directory of the script
files = [
    csv_folder/'data/india.csv',
    csv_folder/'data/world.csv',
    csv_folder/'data/business.csv',
    csv_folder/'data/tech.csv',
    csv_folder/'data/sports.csv'
         ]

for filepath in files:
    # Check if the file exists
    if os.path.exists(filepath):
        # Open the file in binary write mode
        with open(filepath, "wb") as f:
            # Truncate the file
            f.truncate()
        print(f"File '{filepath}' truncated successfully.")
    else:
        print(f"File '{filepath}' does not exist.")

start_new()