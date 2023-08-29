import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# Authorizes the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

# Prompt the user to input the names of the two spreadsheets to be compared
spreadsheet1_name = input("Please enter the exact name of the End of The Month Spreadsheet: ")
spreadsheet2_name = input("Please enter the exact name of the Combined Weekly Add Up Spreadsheet: ")

# Fetch the sheets
try:
    sheet1 = client.open(spreadsheet1_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    print(f"Error: Spreadsheet '{spreadsheet1_name}' not found. Please check the name and try again.")
    exit()

try:
    sheet2 = client.open(spreadsheet2_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    print(f"Error: Spreadsheet '{spreadsheet2_name}' not found. Please check the name and try again.")
    exit()

total_eom_sheet = sheet1.get_all_records()
total_wau_sheet = sheet2.get_all_records()

differences = []
added_to_eom_not_in_wau = []
added_to_wau_not_in_eom = []

# Check if "id" column is present
if total_eom_sheet and "id" in total_eom_sheet[0] and total_wau_sheet and "id" in total_wau_sheet[0]:
    total_eom_dict = {row['id']: row for row in total_eom_sheet}
    total_wau_dict = {row['id']: row for row in total_wau_sheet}

    for unique_id, eom_row in total_eom_dict.items():
        wau_row = total_wau_dict.get(unique_id)
        if wau_row:
            if eom_row != wau_row:
                differences.append({
                    'Row in Total EOM': eom_row,
                    'Row in Total WAU': wau_row
                })
        else:
            added_to_eom_not_in_wau.append(eom_row)

    for unique_id, wau_row in total_wau_dict.items():
        if unique_id not in total_eom_dict:
            added_to_wau_not_in_eom.append(wau_row)
else:
    # If no ID column, only list the discrepancies
    total_eom_set = {frozenset(row.items()) for row in total_eom_sheet}
    total_wau_set = {frozenset(row.items()) for row in total_wau_sheet}

    for row1 in total_eom_sheet:
        if frozenset(row1.items()) not in total_wau_set:
            differences.append({'Row in Total EOM': row1})

    for row2 in total_wau_sheet:
        if frozenset(row2.items()) not in total_eom_set:
            differences.append({'Row in Total WAU': row2})

# Output
print("\n--------------------------------------------------------------------------------------------\n")
print("Differences:")
if differences:
    pp_diff = pprint.PrettyPrinter()
    pp_diff.pprint(differences)
else:
    print("The sheets are identical")

if total_eom_sheet and "id" in total_eom_sheet[0] and total_wau_sheet and "id" in total_wau_sheet[0]:
    print("\n--------------------------------------------------------------------------------------------\n")
    print("Added Rows in Total EOM not in Total WAU:")
    if added_to_eom_not_in_wau:
        pp_added_eom = pprint.PrettyPrinter()
        pp_added_eom.pprint(added_to_eom_not_in_wau)
    else:
        print("NONE")

    print("\n--------------------------------------------------------------------------------------------\n")

    print("Added Rows in Total WAU not in Total EOM:")
    if added_to_wau_not_in_eom:
        pp_added_wau = pprint.PrettyPrinter()
        pp_added_wau.pprint(added_to_wau_not_in_eom)
    else:
        print("NONE")

print("\n--------------------------------------------------------------------------------------------\n")

print("Number of differences is ", len(differences))