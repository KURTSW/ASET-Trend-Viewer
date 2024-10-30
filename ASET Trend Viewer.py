import os
import tkinter as tk
from tkinter import filedialog, messagebox

def read_csv_files(directory):
    """
    Reads all CSV files in the specified directory and extracts wafer data.

    Args:
        directory (str): The path to the directory containing the CSV files.

    Returns:
        list: A list of lists containing the extracted data.
    """
    all_data = []
    header = ['collection time', 'Wafer ID', 'Lot ID', 'Slot', 'Recipe', 'Data Type', 'Site #', 'thickness', 'gof', 'X', 'Y']
    num_columns = len(header)

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.normpath(os.path.join(directory, filename))
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin1') as file:
                    lines = file.readlines()

            collection_date_time = None
            wafer_id = None
            lot_id = None
            slot = None
            recipe = None
            data_type = None
            site_data = []
            for line in lines:
                if line.startswith('COLLECTION DATE/TIME'):
                    collection_date_time = line.split(':', 1)[1].strip()
                elif line.startswith('WAFER ID'):
                    if wafer_id and site_data:
                        wafer_id_clean = ''.join(filter(str.isalnum, wafer_id))
                        lot_id_clean = ''.join(filter(str.isalnum, lot_id))
                        slot_clean = ''.join(filter(str.isalnum, slot))
                        recipe_clean = ''.join(filter(str.isalnum, recipe))
                        data_type_clean = ''.join(filter(str.isalnum, data_type))
                        for site in site_data:
                            row = [
                                collection_date_time, wafer_id_clean, lot_id_clean, slot_clean, recipe_clean, data_type_clean,
                                site['Site #'], site['Value1'], site['Value2'], site['X'], site['Y']
                            ]
                            if len(row) == num_columns:
                                all_data.append(row)
                        site_data = []

                    wafer_id = line.split(',', 1)[1].strip().strip('"')
                elif line.startswith('LOT ID'):
                    lot_id = line.split(',', 1)[1].strip().strip('"')
                elif line.startswith('SLOT'):
                    slot = line.split(',', 1)[1].strip().strip('"')
                elif line.startswith('RECIPE'):
                    recipe = line.split(',', 1)[1].strip().strip('"')
                elif line.startswith('DATA TYPE'):
                    data_type = line.split(',', 1)[1].strip().strip('"')
                elif line.startswith('Site #'):
                    site_data = []
                    continue
                elif wafer_id and lot_id and slot and recipe and data_type and line.strip() and not line.startswith('Site #'):
                    site_info = line.split(',')
                    if len(site_info) >= 5:
                        site_data.append({
                            'Site #': site_info[0].strip(),
                            'Value1': site_info[1].strip(),
                            'Value2': site_info[2].strip(),
                            'X': site_info[3].strip(),
                            'Y': site_info[4].strip()
                        })

            if wafer_id and site_data:
                wafer_id_clean = ''.join(filter(str.isalnum, wafer_id))
                lot_id_clean = ''.join(filter(str.isalnum, lot_id))
                slot_clean = ''.join(filter(str.isalnum, slot))
                recipe_clean = ''.join(filter(str.isalnum, recipe))
                data_type_clean = ''.join(filter(str.isalnum, data_type))
                for site in site_data:
                    row = [
                        collection_date_time, wafer_id_clean, lot_id_clean, slot_clean, recipe_clean, data_type_clean,
                        site['Site #'], site['Value1'], site['Value2'], site['X'], site['Y']
                    ]
                    if len(row) == num_columns:
                        all_data.append(row)

    return all_data

def process_files():
    """
    Opens a file dialog to select a directory, processes the CSV files in the directory,
    and writes the combined data to 'output.csv' in the same directory.
    """
    directory = filedialog.askdirectory()
    if not directory:
        return

    data = read_csv_files(directory)
    output_file_path = os.path.join(directory, 'output.csv')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('blank,collection time,Wafer ID,Lot ID,Slot,Recipe,Data Type,Site #,thickness,gof,X,Y\n')
        for row in data:
            output_file.write(','.join(row) + '\n')

    messagebox.showinfo("Success", f"Combined data has been written to {output_file_path}")

# Create the main window
root = tk.Tk()
root.title("CSV Processor")

# Create and place the button with padding
process_button = tk.Button(root, text="Select Directory and Process Files", command=process_files)
process_button.pack(padx=20, pady=20)

# Run the application
root.mainloop()