import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_statistics(year, base_url, path):
    """Fetch the statistics page content for a given year."""
    url = f"{base_url}{path}?year={year}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data for year {year}: {e}")
        return None

def extract_mean_row(soup):
    """Extract the 'Mean' row data from the parsed HTML content."""
    table = soup.find("table", summary="Results")
    if not table:
        print("[WARNING] Table not found on the page.")
        return None
    
    mean_row = table.find("tr", class_="tr-former")
    if not mean_row:
        print("[WARNING] 'Mean' row not found in the table.")
        return None
    
    try:
        # Extract mean values (skip the first cell which is the label)
        mean_values = [float(td.get_text(strip=True)) for td in mean_row.find_all("td")[1:]]
        return mean_values
    except ValueError as e:
        print(f"[ERROR] Parsing 'Mean' row failed: {e}")
        return None

def main():
    BASE_URL = "https://www.imo-official.org"
    PATH = "/year_statistics.aspx"
    YEARS = range(1984, 2025) 
    # Since 1984, the problems {1, 2, 3} and {4, 5, 6} have been in an order of ascending difficulty.
    results = {}

    for year in YEARS:
        print(f"[INFO] Fetching data for year {year}...")
        content = fetch_statistics(year, BASE_URL, PATH)
        if not content:
            continue

        soup = BeautifulSoup(content, "html.parser")
        mean_values = extract_mean_row(soup)
        
        if mean_values:
            print(f"[SUCCESS] Extracted data for year {year}: {mean_values}")
            results[year] = mean_values
        else:
            print(f"[INFO] No valid 'Mean' row found for year {year}. Skipping...")
            

    # Create a DataFrame with dynamic column names [1, 2, 3, 4, 5, 6]
    if results:
        column_names = ["P"+i for i in "123456"]
        df = pd.DataFrame.from_dict(results, orient="index", columns=column_names)
        df.index.name = "Year"

        # Save to file
        output_path = "./IMO_means.csv"
        df.to_csv(output_path)
        print(f"[SUCCESS] Data saved to '{output_path}'")
    else:
        print("[INFO] No data collected. Exiting...")

if __name__ == "__main__":
    main()
