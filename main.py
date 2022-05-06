# encoding: utf-8
# @author: E. Martin Maho

import streamlit as st
import tax_keys as city
import app

current_year = 2022  # TODO implementálni kellene a formra is

st.set_page_config(page_title="Iparűzési adó kalkulátor")

st.title("Iparűzési adó kalkulátor")

lbt_city = st.selectbox('Válaszd ki a székhelyed szerinti települést!', (sorted(city.tax_by_city)))
lbt_tax_percentage = float(list(city.tax_by_city.values())[list(city.tax_by_city.keys()).index(lbt_city)])
st.write(f'A településen érvényes adókulcs: {lbt_tax_percentage:,}%'.replace('.', ','))
lbt_tax_key = app.get_tax_key(lbt_tax_percentage, current_year)

if lbt_city not in city.zero_tax:
    st.subheader("**Alap adatok**")

    colRevenue, colKata = st.columns(2)

    with colRevenue:
        net_revenue = st.number_input("Add meg az éves bevételed!", min_value=0, step=100000,
                                      format="{:,}".replace(",", "."))

    with colKata:
        kata = st.checkbox('A kisadózó vállalkozások tételes adója alá tartozol?')

    st.markdown("---")

    st.subheader("**Elszámolható költségek**")

    colExpenses1, colExpenses2 = st.columns(2)

    with colExpenses1:
        material_cost = st.number_input("Add meg az anyagköltséged értékét!", min_value=0, step=100000)

        pvgs = st.number_input("Add meg az eladott áruid beszerzési értékét!", min_value=0, step=100000)

    with colExpenses2:
        intermed_services = st.number_input("Add meg a közvetített szolgáltatások értékét!", min_value=0, step=100000)

        subcontracting = st.number_input("Add meg az alvállalkozóid teljesítések értékét!", min_value=0, step=100000)

    st.markdown("---")

    if net_revenue and lbt_tax_key:
        main_data = app.main_data
        lbt_options = app.get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                          main_data, lbt_tax_key, kata)
        recommendation = app.get_recommended_lbt(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                                 main_data, lbt_tax_key, kata)

        if len(lbt_options) > 1:
            st.subheader("Lehetőségeid")

            for option in lbt_options:

                if option == 'excise':
                    excise = f'{lbt_options[option]:,}'.replace(',', '.')
                    st.write(f'Tételes iparűzési adó: {excise} Ft')

                elif option == 'simplified':
                    simplified = f'{lbt_options[option]:,}'.replace(',', '.')
                    st.write(f'Egyszerűsített adóalap-megállapítás: {simplified} Ft')

                else:
                    normal = f'{lbt_options[option]:,}'.replace(',', '.')
                    st.write(f'Normál iparűzési adó: {normal} Ft')

            st.subheader("Az általunk ajánlott iparűzési adótípus")

            if recommendation == 'excise':
                st.write('Tételes iparűzési adó')

            elif recommendation == 'simplified':
                st.write('Egyszerűsített adóalap-megállapítás')

            else:
                st.write('Normál iparűzési adó')

        else:
            st.subheader("Egyetlen választási lehetőséged")
            only_one_option = lbt_options.keys()

            for option in lbt_options:
                lbt_option_value = f'{lbt_options[option]:,}'.replace(',', '.')

                if option == 'excise':
                    st.write(f'Tételes iparűzési adó: {lbt_option_value} Ft')

                elif option == 'simplified':
                    st.write(f'Egyszerűsített adóalap-megállapítás: {lbt_option_value} Ft')

                else:
                    st.write(f'Normál iparűzési adó: {lbt_option_value} Ft')

    else:
        st.write('Túl kevés adatot adtál meg!')  # TODO kata=True esetén a tételest ki kellene írni? Hogyan?

else:
    st.write('A megadott településen nincs iparűzési adófizetésre vonatkozó kötelezettség!')

st.markdown("---")
st.write('A kalkulátor jelenleg nem számol adókedvezménnyel, vagy mentességgel!')

