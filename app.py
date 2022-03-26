
main_data = {
    'excise_lbt_base': 2500000,
    'simplified_cost_share': .2,
    'simplified_max_revenue': 8000000
}


def m(num):
    return num * 1000000


def get_considerable(net_revenue, pvgs):
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


def normal_lbt_tax_base(net_revenue, material_cost, pvgs, intermed_services, subcontracting):
    return net_revenue - material_cost - get_considerable(net_revenue, pvgs + intermed_services) - subcontracting


def get_normal_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting, lbt_tax_key):
    normal_lbt = int(normal_lbt_tax_base(net_revenue, material_cost, pvgs, intermed_services, subcontracting) *
                     lbt_tax_key)
    return normal_lbt if normal_lbt >= 0 else 0



def get_excise_lbt(data, lbt_tax_key, kata):
    if kata:
        return int(float(data['excise_lbt_base']) * lbt_tax_key)
    else:
        return 'Null'


def get_simplified_lbt(data, net_revenue, lbt_tax_key):
    if net_revenue <= data['simplified_max_revenue']:
        return int(net_revenue * (1 - data['simplified_cost_share']) * lbt_tax_key)
    else:
        return 'Null'


def get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data, lbt_tax_key, kata):
    lbt_opinions = {}
    if get_excise_lbt(data, lbt_tax_key, kata) != 'Null':
        lbt_opinions['excise'] = get_excise_lbt(data, lbt_tax_key, kata)
    if get_simplified_lbt(data, net_revenue, lbt_tax_key) != 'Null':
        lbt_opinions['simplified'] = get_simplified_lbt(data, net_revenue, lbt_tax_key)
    lbt_opinions['normal'] = get_normal_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                            lbt_tax_key)
    return lbt_opinions


def get_recommended_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data, lbt_tax_key, kata):
    lbt_opinions = get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting, data,
                                   lbt_tax_key, kata)

    return list(lbt_opinions.keys())[list(lbt_opinions.values()).index(min(lbt_opinions.values()))]
