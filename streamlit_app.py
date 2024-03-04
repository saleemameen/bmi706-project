import streamlit as st
import altair as alt
import plots
import load_data

##########################################################################
# INITIALISE LAYOUT
##########################################################################

# Since the dashboard will use multiple graphs, we will default to a wide layout
st.set_page_config(layout="wide")

##########################################################################
# LOAD DATA
##########################################################################

dfs_admitted = load_data.admitted_patients_data()
dfs_outcomes = load_data.consumer_outcomes_data()
# st.dataframe(table) used for debgugging

##########################################################################
# DASHBOARD
##########################################################################

# Provide a title to the page
st.write("## Mental Health in Australia")
st.write("Mental Health is a serious concern in Australia. Explore the data to learn more.")

# Setup the Tabs
tab1, tab2 = st.tabs(["Overview", "Explore in More Detail"])

# Create Tab 1: Overview Tab
with tab1:
    # Provide a Title for the Tab
    st.write("### Key Trends and Statistics")
    # Setup three columns
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        # Chart 1: Plot hospitalizations by state
        st.altair_chart(plots.hospitalizations_by_state(dfs_admitted['Table 4']), use_container_width=True)
        # Chart 4: Plot Hospitalizations by SES status
        st.altair_chart(plots.hospitalizations_by_socioeconomic_status(dfs_admitted['Table 5']), use_container_width=True)
    with col2:
        # Chart 2: Plot Hospitalizations by age
        st.altair_chart(plots.hospitalizations_by_age(dfs_admitted['Table 3']), use_container_width=True)
        # Chart 5: Plot Hospitalizations by Remoteness
        st.altair_chart(plots.hospitalizations_by_remoteness(dfs_admitted['Table 5']), use_container_width=True)
    with col3:
        # Chart 3: Plot Hospitalizations by Indigenous status
        st.altair_chart(plots.hospitalizations_by_indigenous_status(dfs_admitted['Table 5']), use_container_width=True)

with tab2:

    # Year Slider
    year = st.slider(
        label="Year",
        min_value=dfs_admitted['Table 1']["Year"].min(),
        max_value=dfs_admitted['Table 1']["Year"].max(),
        value=2016
    )
