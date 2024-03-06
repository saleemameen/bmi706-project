import streamlit as st


def chart_card(title, desc, plot):
    with st.container(border=True):
        # Card title
        st.markdown(
            f'''
            <div class="banner">
                <h1 class="card-title">{title}</h1>
                <p class="card-desc">{desc}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        # Execute the function passed into chart_func
        st.altair_chart(plot, use_container_width=True)


def banner(title, desc, withFilters=False):
    st.markdown(
        f'''
            <div class="{'banner with-filters' if withFilters else 'banner'}">
                <h1 class="card-title">{title}</h1>
                <p class="card-desc">{desc}</p>
            </div>
            ''',
        unsafe_allow_html=True
    )
