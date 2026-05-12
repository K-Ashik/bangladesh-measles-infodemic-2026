import os
import pdfplumber
import pandas as pd
import re

# 1. Dictionaries
bengali_to_english_digits = {
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', 
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
}

division_map = {
    'ঢাকা': 'Dhaka', 'রাজশাহী': 'Rajshahi', 'বরিশাল': 'Barishal',
    'চট্টগ্রাম': 'Chattogram', 'ময়মনসিংহ': 'Mymensingh',
    'সিলেট': 'Sylhet', 'খুলনা': 'Khulna', 'রংপুর': 'Rangpur'
}

def convert_bengali_num(bengali_str):
    if not bengali_str: return 0
    # Clean out commas, spaces, and percent signs
    clean_str = str(bengali_str).replace(',', '').replace(' ', '').replace('%', '').strip()
    english_str = ''.join([bengali_to_english_digits.get(char, char) for char in clean_str])
    try:
        return float(english_str)
    except ValueError:
        return 0

# 2. Setup
pdf_folder = "raw_pdfs"
epi_data = [] # For Cases/Deaths
vax_data = [] # For Vaccination Coverage

print("Starting Dual-Engine Extraction...")

# 3. Process PDFs
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(pdf_folder, filename)
        
        try:
            with pdfplumber.open(filepath) as pdf:
                # Find Date
                full_text = ""
                for page in pdf.pages[0:3]:
                    full_text += page.extract_text() or ""
                
                # Find ALL dates in the text
                all_dates = re.findall(r'(\d{2}-\d{2}-\d{4}|[০-৯]{2}-[০-৯]{2}-[০-৯]{4})', full_text)
                
                # Convert all found dates to English digits
                eng_dates = [''.join([bengali_to_english_digits.get(char, char) for char in d]) for d in all_dates]
                
                # Filter out the baseline outbreak date (15-03-2026)
                actual_dates = [d for d in eng_dates if d != '15-03-2026']
                
                # If we found other dates, use the first one available. Otherwise, mark Unknown.
                report_date = actual_dates[0] if actual_dates else "Unknown_Date"
                # Extract Tables
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            # Check if row is for a Division
                            if row and row[0] and any(div in str(row[0]) for div in division_map.keys()):
                                raw_div = str(row[0]).strip()
                                eng_div = next((eng for ben, eng in division_map.items() if ben in raw_div), "Unknown")
                                
                                row_str = "".join(str(cell) for cell in row)
                                
                                # ENGINE 1: Vaccination Data (Contains % sign)
                                if '%' in row_str:
                                    # Convert the row to numbers. The coverage % is usually the 4th or 5th number.
                                    nums = [convert_bengali_num(cell) for cell in row if convert_bengali_num(cell) > 0]
                                    if len(nums) >= 4:
                                        vax_data.append({
                                            'Date': report_date,
                                            'Division': eng_div,
                                            # We grab the first number that looks like a percentage (usually <= 200)
                                            'Reported_Coverage_Pct': next((n for n in nums if n <= 200), 0), 
                                            'Source_File': filename
                                        })
                                
                                # ENGINE 2: Epidemiological Data (Wide tables, no % sign)
                                elif len(row) >= 10:
                                    nums = [convert_bengali_num(cell) for cell in row]
                                    
                                    # Because DGHS shifts columns (Deaths is col 8 on May 11, col 10 on May 3)
                                    # We will extract index 7 (Always Cases) and check both 8 and 10 for Deaths.
                                    epi_data.append({
                                        'Date': report_date,
                                        'Division': eng_div,
                                        'Cumulative_Cases': nums[7] if len(nums) > 7 else 0,
                                        'Deaths_Metric_A': nums[8] if len(nums) > 8 else 0,
                                        'Deaths_Metric_B': nums[10] if len(nums) > 10 else 0,
                                        'Source_File': filename
                                    })
                                    
        except Exception as e:
            print(f"Skipping {filename} due to formatting errors.")

# 4. Save to CSV
df_epi = pd.DataFrame(epi_data).drop_duplicates().sort_values(by=['Date', 'Division'])
df_vax = pd.DataFrame(vax_data).drop_duplicates().sort_values(by=['Date', 'Division'])

df_epi.to_csv("measles_epi_data.csv", index=False)
df_vax.to_csv("measles_vax_data.csv", index=False)

print(f"\nExtraction Complete!")
print(f"Saved {len(df_epi)} Epi records to 'measles_epi_data.csv'")
print(f"Saved {len(df_vax)} Vax records to 'measles_vax_data.csv'")