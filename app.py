import tax_keys as lbt

zero_tax_cities = lbt.zero_tax
tax_by_city = lbt.tax_by_city

test = {
    'bev': 1000000,
    'elabe': 0,
    'kozv': 0,
    'anyag': 0,
    'alvall': 0,
    'kulcs': .01,
    'kata': True
}

main = {
    'teteles_adoalap': 2500000,
    'egysz_hanyad': .8,
    'egysz_max': 8000000
}


def m(szam):
    return szam * 1000000


def eft(szam):
    round(szam / 1000) * 1000


def aranyosito(arbev, elabe):
    if elabe <= m(500):
        maxx = [elabe, 0, 0, 0]
        arany = [elabe, 0, 0, 0]
    elif m(500) < elabe <= m(20000):
        maxx = [m(500), (elabe - m(500)) * 0.8, 0, 0]
        arany = [m(500) / arbev * elabe, m(19500) / arbev * elabe, 0, 0]
    elif m(20000) < elabe <= m(80000):
        maxx = [m(500), m(19500) * .80, (elabe - m(20000)) * .75, 0]
        arany = [m(500) / arbev * elabe, m(19500) / arbev * elabe, m(60000) / arbev * elabe, 0]
    else:
        maxx = [m(500), m(19500) * .80, m(60000) * .75, (elabe - m(80000)) * .70]
        arany = [m(500) / arbev * elabe, m(19500) / arbev * elabe, m(60000) / arbev * elabe,
                 (arbev - m(80000)) / arbev * elabe]
    return sum([min(maxx[0], arany[0]), min(maxx[1], arany[1]),
               min(maxx[2], arany[2]), min(maxx[3], arany[3])])


def adoalap(dic):
    return dic['bev'] - dic['anyag'] - aranyosito(dic['bev'], (dic['elabe'] + dic['kozv'])) - dic['alvall']


def ado(dic):
    return int(adoalap(dic) * dic['kulcs'])


def teteles(dic, dic2):
    return int(dic2['teteles_adoalap'] * dic['kulcs']) if dic['kata'] else 0


def egyszeru(dic, dic2):
    return int(dic['bev'] * dic2['egysz_hanyad'] * dic['kulcs']) if dic['bev'] <= dic2['egysz_max'] else 0


def megeri(dic, dic2, dic3):
    if teteles(dic, dic2):
        dic3['teteles'] = teteles(dic, dic2)
    if egyszeru(dic, dic2):
        dic3['egyszeru'] = egyszeru(dic, dic2)
    if ado(dic):
        dic3['normal'] = ado(dic)
    return list(dic3.keys())[list(dic3.values()).index(min(dic3.values()))]


valasztas = {}
print(valasztas)
print(megeri(test, main, valasztas))
print(valasztas)
