# encoding: utf-8
# @author: E. Martin Maho

import streamlit as st
import tax_keys as city
import app

st.set_page_config(page_title="Iparűzési adó kalkulátor")

st.title("Iparűzési adó kalkulátor")

st.header("**Alap adatok**")
st.subheader("Bevétel és székhely adatok")

colRevenue, colCity = st.columns(2)

with colRevenue:
    net_revenue = st.number_input("Add meg az éves bevételed!", min_value=0, step=100000)

with colCity:
    lbt_city = st.selectbox('Válaszd ki a székhelyed szerinti települést!', (sorted(city.tax_by_city)))
    lbt_tax_key = float(list(city.tax_by_city.values())[list(city.tax_by_city.keys()).index(lbt_city)])
    st.write('Érvényes adókulcs:', str(lbt_tax_key) + '%')

st.subheader("Kata adatok")
str_kata = st.selectbox('A kisadózó vállalkozások tételes adója alá tartozol?', ('Igen', 'Nem'))
kata = True if str_kata == 'Igen' else False

st.markdown("---")

st.header("**Elszámolható költségek**")

colExpenses1, colExpenses2 = st.columns(2)

with colExpenses1:
    material_cost = st.number_input("Add meg az anyagköltséged értékét!", min_value=0, step=100000)

    pvgs = st.number_input("Add meg az eladott áruid beszerzési értékét!", min_value=0, step=100000)

with colExpenses2:
    intermed_services = st.number_input("Add meg a közvetített szolgáltatások értékét!", min_value=0, step=100000)

    subcontracting = st.number_input("Add meg az alvállalkozóid teljesítések értékét!", min_value=0, step=100000)

if lbt_city not in city.zero_tax:
    if net_revenue and lbt_tax_key:
        main_data = app.main_data
        lbt_options = app.get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                          main_data, lbt_tax_key, kata)
        recommendation = app.get_recommended_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                                 main_data, lbt_tax_key, kata)

        if len(lbt_options) > 1:
            st.header("Lehetőségeid")

            for option in lbt_options:
                if option == 'excise':
                    st.write(f'Tételes iparűzési adó')
                elif option == 'simplified':
                    st.write(f'Egyszerűsített adóalap-megállapítás')
                else:
                    st.write(f'Normál iparűzési adó')

            st.header("Az általunk ajánlott iparűzési adótípus")
            if recommendation == 'excise':
                st.write(f'Tételes iparűzési adó')
            elif recommendation == 'simplified':
                st.write(f'Egyszerűsített adóalap-megállapítás')
            else:
                st.write(f'Normál iparűzési adó')

        else:
            st.header("Egyetlen választási lehetőséged")
            if lbt_options.keys() == 'excise':
                st.write(f'Tételes iparűzési adó')
            elif lbt_options.keys() == 'simplified':
                st.write(f'Egyszerűsített adóalap-megállapítás')
            else:
                st.write(f'Normál iparűzési adó')

    else:
        st.write(f'Túl kevés adatot adtál meg!')

else:
    st.write('A megadott településen nincs iparűzési adófizetésre vonatkozó kötelezettség!')

st.markdown("---")
st.write('A kalkulátor jelenleg nem számol az esetleges adómentességgel, vagy adókedvezménnyel,'
         ' illetve tört év esetén a kalkuláció nem pontos!')