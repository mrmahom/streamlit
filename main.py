import streamlit as st
import app
from datetime import date

import render

today = date.today()
current_year = today.year

net_revenue = 0
material_cost = 0
pvgs = 0
intermed_services = 0
subcontracting = 0

# --------------------------------------

st.set_page_config(page_title="Iparűzési adó kalkulátor")

st.title("Iparűzési adó kalkulátor")

lbt_city = st.selectbox(
    "Válaszd ki a székhelyed szerinti települést!",
    (["Válassz!"] + app.get_all_lbt_account())
)

if lbt_city != 'Válassz!':
    lbt_rate = app.get_lbt_rate(lbt_city)
    st.write(f"A településen érvényes adókulcs: {lbt_rate:,}%".replace('.', ','))

    if app.has_lbt_rate(lbt_city):
        st.subheader("**Alap adatok**")

        col_revenue, col_kata = st.columns(2)

        with col_revenue:
            net_revenue = st.number_input(
                "Add meg az éves bevételed!",
                min_value=100000,
                step=100000,
                format="%d".replace(",", ".")
            )

        with col_kata:
            kata = st.checkbox("A kata adó hatálya alá tartozol?")
            acc_costs = st.checkbox("Vannak elszámolható költségeid?")

        if acc_costs:
            st.markdown("---")
            st.subheader("**Elszámolható költségek**")
            col_expenses1, col_expenses2 = st.columns(2)

            with col_expenses1:
                material_cost = st.number_input("Add meg az anyagköltséged értékét!", min_value=0, step=100000)
                pvgs = st.number_input("Add meg az eladott áruid beszerzési értékét!", min_value=0, step=100000)

            with col_expenses2:
                intermed_services = st.number_input("Add meg a közvetített szolgáltatások értékét!",
                                                    min_value=0, step=100000)
                subcontracting = st.number_input("Add meg az alvállalkozóid teljesítések értékét!", min_value=0,
                                                 step=100000)

        st.markdown("---")

        if net_revenue and lbt_rate:
            lbt_options = app.get_lbt_options(
                net_revenue,
                material_cost,
                pvgs,
                intermed_services,
                subcontracting,
                lbt_city,
                kata,
            )

            recommendation = app.get_recommended_lbt(lbt_options)

            st.subheader("Lehetőségeid")
            render.options(lbt_options, recommendation)

        else:
            st.warning("Túl kevés adatot adtál meg!")
    else:
        st.success("A megadott településen nincs iparűzési adófizetésre vonatkozó kötelezettség!")

st.markdown("---")
st.write("@author: E. Martin Maho")
