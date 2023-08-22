import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

#Authorizes the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

#Fetch the sheet
sheet1 = client.open('total_EOM_test').sheet1
sheet2 = client.open('total_WAU_test').sheet1
total_eom_sheet = sheet1.get_all_records()
total_wau_sheet = sheet2.get_all_records()

added_rows = []

# Identify differences
differences = []
for row1, row2 in zip(total_eom_sheet, total_wau_sheet):
    if row1 != row2:
        differences.append({
            'Row in Total EOM': row1,
            'Row in Total WAU': row2
        })

#Output
print("\n--------------------------------------------------------------------------------------------\n")
print("Differences:")
pp_diff = pprint.PrettyPrinter()
pp_diff.pprint(differences)
print("\n--------------------------------------------------------------------------------------------\n")

#Added rows

added_to_eom_not_in_wau = []

for row1 in total_eom_sheet:
    if row1 not in total_wau_sheet and row1 not in [diff['Row in Total EOM'] for diff in differences]:
        added_to_eom_not_in_wau.append(row1)

added_to_wau_not_in_eom = []

for row2 in total_wau_sheet:
    if row2 not in total_eom_sheet and row2 not in [diff['Row in Total WAU'] for diff in differences]:
        added_to_wau_not_in_eom.append(row2)

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
