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

# Fetch the sheet
sheet1 = client.open('July Hours Comparison EOM Test').sheet1
sheet2 = client.open('July Hours Comparison WAU Test').sheet1
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
    for row1 in total_eom_sheet:
        if row1 not in total_wau_sheet:
            differences.append({'Row in Total EOM': row1})

    for row2 in total_wau_sheet:
        if row2 not in total_eom_sheet:
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