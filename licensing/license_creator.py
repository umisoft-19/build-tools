import sys
import os
import hmac 
import hashlib
import json
import datetime


def generate_license():
    if not os.path.exists('key.txt'):
        print('No key text was found!')
        input('Press Enter key to exit.')
        sys.exit()

    hid = None
    with open('key.txt') as f:
        hid = f.read()

    
    customer = input('Enter a customer name: ')
    users = input('Enter the number of users the software can manage: ')
    employees = input('Enter the number of employees the software can manage: ')
    print("Select a license type:")
    print("1. Trial(1 month)")
    print("2. 6 months")
    print("3. 1 Year")
    print("4. 2 Years")
    print("5. Indefinite")

    license_type = None
    while license_type not in '1 2 3 4 5'.split(' '):
        license_type = input('Select a license type: ')

    print('Generating License')
    timestamp = datetime.datetime.now()

    def get_expiry(type):
        mapping = {
            '1': datetime.timedelta(days=30),
            '2': datetime.timedelta(days=180),
            '3': datetime.timedelta(days=365),
            '4': datetime.timedelta(days=731),
        }
        today = datetime.date.today()
        return (today + mapping[type]).strftime("%d/%m/%Y")

    expiry = "*" if license_type == '5' else get_expiry(license_type)
    
    license_data = {
        'customer': customer,
        'number_users': users,
        'number_employees': employees,
        'date_issued': timestamp.strftime("%d/%m/%Y"),
        'expiry_date': expiry,
        'timestamp': timestamp.strftime('%d-%m-%Y %H:%M:%S'),
    }
    license_str = json.dumps(license_data)
    data_string = hid + license_str

    byte_data = bytes(data_string, 'ascii')
    hash = hashlib.sha3_512(byte_data).hexdigest()

    license = {
        'signature': hash,
        'license':license_data
    }
    with open('license.json', 'w') as lic_file:
        json.dump(license, lic_file)

    registry =None 
    if not os.path.exists('customer_registry.json'):
        with open('customer_registry.json', 'w') as reg:
            json.dump({"customers": []}, reg)

    with open('customer_registry.json', 'r') as reg:
        registry = json.load(reg)
        registry["customers"].append({
            'id': hid,
            'name': customer,
            'license': license
        })

    with open('customer_registry.json', 'w') as reg:
            json.dump(registry, reg)

    input('Generated license successfully! Press Enter key to exit.')



print('UMISOFT License Creator.')
print("=========================")
print(os.getcwd())
print("""Select an option:
1. Generate a license
2. Exit""")
option = input("> ")
while option not in ['1', '2']:
    option = input("> ")

if option == '2':
    sys.exit()

else:
    generate_license()

