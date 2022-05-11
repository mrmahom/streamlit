import streamlit as st


def options(lbt_options, recommendation):
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