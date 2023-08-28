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
sheet1 = client.open('total_EOM_test').sheet1
sheet2 = client.open('total_WAU_test').sheet1
total_eom_sheet = sheet1.get_all_records()
total_wau_sheet = sheet2.get_all_records()

# Convert sheets to dict format using unique id as key
total_eom_dict = {row['id']: row for row in total_eom_sheet}
total_wau_dict = {row['id']: row for row in total_wau_sheet}

# Identify differences
differences = []
for unique_id, eom_row in total_eom_dict.items():
    wau_row = total_wau_dict.get(unique_id)
    if wau_row and eom_row != wau_row:
        differences.append({
            'Row in Total EOM': eom_row,
            'Row in Total WAU': wau_row
        })

# Added rows
added_to_eom_not_in_wau = [row for unique_id, row in total_eom_dict.items() if unique_id not in total_wau_dict]
added_to_wau_not_in_eom = [row for unique_id, row in total_wau_dict.items() if unique_id not in total_eom_dict]

# Output
print("\n--------------------------------------------------------------------------------------------\n")
print("Differences:")
if differences:
    pp_diff = pprint.PrettyPrinter()
    pp_diff.pprint(differences)
else:
    print("The sheets are identical")
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
