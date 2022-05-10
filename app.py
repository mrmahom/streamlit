from lbt import lbt_accounts as lbt

main_data = {
    'itemized_lbt_base': 2500000,
    'simplified_cost_share': .2,
    'simplified_max_revenue': 8000000
}


def m(num):
    return num * 1000000


def get_considerable(net_revenue, pvgs=0):
    if pvgs <= m(500):
        considerable_max = [pvgs, 0, 0, 0]
        proportionate = [pvgs, 0, 0, 0]

    elif m(500) < pvgs <= m(20000):
        considerable_max = [m(500), (pvgs - m(500)) * 0.8, 0, 0]
        proportionate = [m(500) / net_revenue * pvgs, m(19500) / net_revenue * pvgs, 0, 0]

    elif m(20000) < pvgs <= m(80000):
        considerable_max = [m(500), m(19500) * .80, (pvgs - m(20000)) * .75, 0]
        proportionate = [m(500) / net_revenue * pvgs, m(19500) / net_revenue * pvgs, m(60000) / net_revenue * pvgs, 0]

    else:
        considerable_max = [m(500), m(19500) * .80, m(60000) * .75, (pvgs - m(80000)) * .70]
        proportionate = [m(500) / net_revenue * pvgs, m(19500) / net_revenue * pvgs, m(60000) / net_revenue * pvgs,
                         (net_revenue - m(80000)) / net_revenue * pvgs]

    return sum([min(considerable_max[0], proportionate[0]), min(considerable_max[1], proportionate[1]),
               min(considerable_max[2], proportionate[2]), min(considerable_max[3], proportionate[3])])


def get_normal_lbt_base(net_revenue, material_cost=0, pvgs=0, intermed_services=0, subcontracting=0):
    return net_revenue - material_cost - get_considerable(net_revenue, pvgs + intermed_services) - subcontracting


def get_normal_lbt(net_revenue, city_name, material_cost=0, pvgs=0, intermed_services=0, subcontracting=0,
                   tax_rate=0):
    tax_base = get_normal_lbt_base(net_revenue, material_cost, pvgs, intermed_services, subcontracting)
    normal_lbt = get_reduced_tax(tax_base, city_name, tax_rate)
    return normal_lbt if normal_lbt >= 0 else 0


def get_itemized_lbt(data, tax_rate, kata, city_name):
    if kata:
        tax_base = float(data['itemized_lbt_base'])
        return get_reduced_tax(tax_base, city_name, tax_rate)
    else:
        return None


def get_simplified_lbt(data, net_revenue, tax_rate, city_name):
    if 0 < net_revenue <= data['simplified_max_revenue']:
        tax_base = net_revenue * (1 - data['simplified_cost_share'])
        return get_reduced_tax(tax_base, city_name, tax_rate)
    else:
        return None


def get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data, city_name, kata, year):
    lbt_options = {}
    tax_rate = get_tax_rate(get_lbt_rate(city_name), year)

    if get_itemized_lbt(data, tax_rate, kata, city_name) is not None:
        lbt_options['itemized'] = get_itemized_lbt(data, tax_rate, kata, city_name)

    if get_simplified_lbt(data, net_revenue, tax_rate, city_name) is not None:
        lbt_options['simplified'] = get_simplified_lbt(data, net_revenue, tax_rate, city_name)

    lbt_options['normal'] = get_normal_lbt(net_revenue, city_name, material_cost, pvgs, intermed_services,
                                           subcontracting, tax_rate)
    return lbt_options


def get_recommended_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data, city_name,
                        kata, year):
    lbt_opinions = get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data,
                                   city_name, kata, year)

    return list(lbt_opinions.keys())[list(lbt_opinions.values()).index(min(lbt_opinions.values()))]


def get_tax_rate(lbt_percentage, current_year):
    discount_year = [2021, 2022]
    if current_year in discount_year:
        if lbt_percentage >= 1.0:
            return 0.01
    else:
        return lbt_percentage / 100


def get_discount(city_name, discount_limit=False, discount=False, discount_type=False):
    lbt_data = lbt[city_name]
    return lbt_data['discount_limit'] if discount_limit else lbt_data['discount'] \
        if discount else lbt_data['discount_type'] if discount_type else None


def get_exemption_limit(city_name):
    lbt_data = lbt[city_name]
    return lbt_data['exemption_limit']


def get_lbt_rate(city_name):
    return lbt[city_name]['rate']


def has_lbt_rate(city_name):
    lbt_data = lbt[city_name]
    return True if lbt_data['rate'] else False


def get_reduced_tax(tax_base, city_name, lbt_tax_key):
    if 0 < tax_base <= get_exemption_limit(city_name):
        tax_base = 0
    if 0 < tax_base <= get_discount(city_name, discount_limit=True):
        lbt_tax = int(tax_base * lbt_tax_key)
        percent = True if get_discount(city_name, discount_type=True) == 2 else False
        discount = get_discount(city_name, discount=True)
        return lbt_tax * (1 - discount / 100) if percent else lbt_tax - discount
    else:
        return int(tax_base * lbt_tax_key)


def get_all_lbt_account():
    return list(lbt.keys())
