import streamlit as st
import app
from datetime import date

today = date.today()
current_year = today.year
net_revenue, material_cost, pvgs, intermed_services, subcontracting = 0, 0, 0, 0, 0

# --------------------------------------

st.set_page_config(page_title="Iparűzési adó kalkulátor", page_icon="🧊")

st.title("Iparűzési adó kalkulátor")

lbt_city = st.selectbox("Válaszd ki a székhelyed szerinti települést!", (["Válassz!"] + app.get_all_lbt_account()))

if lbt_city != 'Válassz!':
    lbt_rate = app.get_lbt_rate(lbt_city)
    st.write(f"A településen érvényes adókulcs: {lbt_rate:,}%".replace('.', ','))

    if app.has_lbt_rate(lbt_city):
        st.subheader("**Alap adatok**")

        colRevenue, colKata = st.columns(2)

        with colRevenue:
            net_revenue = st.number_input("Add meg az éves bevételed!", min_value=100000, step=100000,
                                          format="%d".replace(",", "."))

        with colKata:
            kata = st.checkbox("A kata adó hatálya alá tartozol?")
            acc_costs = st.checkbox("Vannak elszámolható költségeid?")

        if acc_costs:
            st.markdown("---")
            st.subheader("**Elszámolható költségek**")
            colExpenses1, colExpenses2 = st.columns(2)

            with colExpenses1:
                material_cost = st.number_input("Add meg az anyagköltséged értékét!", min_value=0, step=100000)
                pvgs = st.number_input("Add meg az eladott áruid beszerzési értékét!", min_value=0, step=100000)

            with colExpenses2:
                intermed_services = st.number_input("Add meg a közvetített szolgáltatások értékét!",
                                                    min_value=0, step=100000)
                subcontracting = st.number_input("Add meg az alvállalkozóid teljesítések értékét!", min_value=0,
                                                 step=100000)

        st.markdown("---")

        if net_revenue and lbt_rate:
            main_data = app.main_data
            lbt_options = app.get_lbt_options(net_revenue, material_cost, pvgs, intermed_services, subcontracting,
                                              main_data, lbt_city, kata, current_year)
            recommendation = app.get_recommended_lbt(net_revenue, material_cost, pvgs, intermed_services,
                                                     subcontracting, main_data, lbt_city, kata, current_year)

            st.subheader("Lehetőségeid")
            for option in lbt_options:

                if option == 'itemized':
                    itemized = f"{lbt_options[option]:,}".replace(',', '.')
                    if recommendation == 'itemized':
                        st.success(f"Tételes iparűzési adó: {itemized} Ft")
                    else:
                        st.info(f"Tételes iparűzési adó: {itemized} Ft")

                elif option == 'simplified':
                    simplified = f"{lbt_options[option]:,}".replace(',', '.')
                    if recommendation == 'simplified':
                        st.success(f"Egyszerűsített adóalap-megállapítás: {simplified} Ft")
                    else:
                        st.info(f"Egyszerűsített adóalap-megállapítás: {simplified} Ft")

                else:
                    normal = f"{lbt_options[option]:,}".replace(',', '.')
                    if recommendation == 'normal':
                        st.success(f"Normál iparűzési adó: {normal} Ft")
                    else:
                        st.info(f"Normál iparűzési adó: {normal} Ft")

        else:
            st.warning("Túl kevés adatot adtál meg!")
    else:
        st.success("A megadott településen nincs iparűzési adófizetésre vonatkozó kötelezettség!")

st.markdown("---")
st.write("@author: E. Martin Maho")
