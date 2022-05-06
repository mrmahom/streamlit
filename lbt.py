with open('city_names_alphabet.csv', 'r', encoding='utf-8-sig') as file:
    city_names = [city_name.strip() for city_name in file]

with open('lbt.csv', 'r') as file:
    lbt_accounts = dict.fromkeys(city_names)
    for i, row in enumerate(file):
        if i:
            row_id, created, modified, account, city_name, census_number, rate, county_code, exemption_limit, \
                discount_limit, discount, discount_type = row.strip().split(',')[:12]
            lbt_accounts[city_name] = {
                'rate': 0.0 if rate == '' else float(rate),
                'exemption_limit': 0.0 if exemption_limit == '' else float(exemption_limit),
                'discount_limit': 0.0 if discount_limit == '' else float(discount_limit),
                'discount': 0.0 if discount == '' else float(discount),
                'discount_type': None if discount_type == '' else 1 if int(discount_type) else 2
            }

for city_name in lbt_accounts:
    if lbt_accounts[city_name]['discount'] or lbt_accounts[city_name]['discount_limit']:
        print(city_name, lbt_accounts[city_name])
