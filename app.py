from lbt import lbt_accounts as lbt
from datetime import date

ITEMIZED_LBT_BASE = 2500000
SIMPLIFIED_COST_SHARE = 0.2
SIMPLIFIED_MAX_REVENUE = 8000000


def _calc_tax_rate(lbt_percentage, current_year):
    discount_year = [2021, 2022]
    if current_year in discount_year:
        return min(0.01, lbt_percentage / 100)
    else:
        return lbt_percentage / 100


def _calc_reduced_tax(tax_base, city_name, lbt_tax_key):
    exemption_limit = get_exemption_limit(city_name)
    if 0 < tax_base <= exemption_limit:
        tax_base = 0

    discount_limit = get_discount(city_name, discount_limit=True)
    if 0 < tax_base <= discount_limit:
        lbt_tax = int(tax_base * lbt_tax_key)
        percent = True if get_discount(city_name, discount_type=True) == 2 else False
        discount = get_discount(city_name, discount=True)
        return lbt_tax * (1 - discount / 100) if percent else lbt_tax - discount
    else:
        return int(tax_base * lbt_tax_key)


def _calc_considerable(net_revenue, pvgs=0):
    def m(num):  # 1 million
        return num * 1000000

    if pvgs <= m(500):
        considerable_max = [net_revenue, 0, 0, 0]
        proportionate = [pvgs, 0, 0, 0]

    elif m(500) < pvgs <= m(20000):
        considerable_max = [m(500), (net_revenue - m(500)) * 0.85, 0, 0]
        proportionate = [m(500) / net_revenue * pvgs, m(19500) / net_revenue * pvgs, 0, 0]

    elif m(20000) < pvgs <= m(80000):
        considerable_max = [m(500), m(19500) * .85, (net_revenue - m(20000)) * .75, 0]
        proportionate = [m(500) / net_revenue * pvgs, m(19500) / net_revenue * pvgs, m(60000) / net_revenue * pvgs, 0]

    else:
        considerable_max = [m(500), m(19500) * .85, m(60000) * .75, (net_revenue - m(80000)) * .70]
        proportionate = [
            m(500) / net_revenue * pvgs,
            m(19500) / net_revenue * pvgs,
            m(60000) / net_revenue * pvgs,
            (net_revenue - m(80000)) / net_revenue * pvgs
        ]

    return sum([
        min(considerable_max[0], proportionate[0]),
        min(considerable_max[1], proportionate[1]),
        min(considerable_max[2], proportionate[2]),
        min(considerable_max[3], proportionate[3])
    ])


def _calc_normal_lbt_base(
        net_revenue,
        material_cost=0,
        pvgs=0,
        intermed_services=0,
        subcontracting=0
):
    considerable = _calc_considerable(net_revenue, pvgs + intermed_services)
    return net_revenue - material_cost - considerable - subcontracting


def _calc_normal_lbt(
        net_revenue,
        city_name,
        material_cost=0,
        pvgs=0,
        intermed_services=0,
        subcontracting=0,
        tax_rate=0
):
    tax_base = _calc_normal_lbt_base(
        net_revenue,
        material_cost,
        pvgs,
        intermed_services,
        subcontracting
    )
    return max(0, _calc_reduced_tax(tax_base, city_name, tax_rate))


def _calc_simplified_lbt(net_revenue, tax_rate, city_name):
    if 0 < net_revenue <= SIMPLIFIED_MAX_REVENUE:
        tax_base = net_revenue * (1 - SIMPLIFIED_COST_SHARE)
        return _calc_reduced_tax(tax_base, city_name, tax_rate)
    else:
        return None


def _calc_itemized_lbt(tax_rate, kata, city_name):
    if kata:
        tax_base = ITEMIZED_LBT_BASE
        return _calc_reduced_tax(tax_base, city_name, tax_rate)
    else:
        return None


def get_lbt_options(
        net_revenue,
        material_cost,
        pvgs,
        intermed_services,
        subcontracting,
        city_name,
        kata,
):
    current_year = get_current_year()
    tax_rate = _calc_tax_rate(
        get_lbt_rate(city_name),
        current_year
    )

    lbt_options = {
        'itemized': _calc_itemized_lbt(
            tax_rate,
            kata,
            city_name
        ),
        'simplified': _calc_simplified_lbt(
            net_revenue,
            tax_rate,
            city_name
        ),
        'normal': _calc_normal_lbt(
            net_revenue,
            city_name,
            material_cost,
            pvgs,
            intermed_services,
            subcontracting,
            tax_rate
        )
    }

    lbt_options = {k: v for k, v in lbt_options.items() if v is not None}  # clean None values

    return lbt_options


def get_recommended_lbt(lbt_options):
    return min(lbt_options, key=lbt_options.get)
    # return list(lbt_options.keys())[list(lbt_options.values()).index(min(lbt_options.values()))]


def get_discount(
        city_name,
        discount_limit=False,
        discount=False,
        discount_type=False
):
    lbt_data = lbt[city_name]
    if discount_limit:
        return lbt_data['discount_limit']
    elif discount:
        return lbt_data['discount']
    elif discount_type:
        return lbt_data['discount_type']


def get_exemption_limit(city_name):
    lbt_data = lbt[city_name]
    return lbt_data['exemption_limit']


def get_lbt_rate(city_name):
    return lbt[city_name]['rate']


def has_lbt_rate(city_name):
    lbt_data = lbt[city_name]
    return True if lbt_data['rate'] else False


def get_all_lbt_account():
    return list(lbt.keys())


def get_current_year():
    return date.today().year
