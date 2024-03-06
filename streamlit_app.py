import streamlit as st
import altair as alt
import plots
import load_data
import ui

##########################################################################
# INITIALISE LAYOUT
##########################################################################

# Since the dashboard will use multiple graphs, we will default to a wide layout
st.set_page_config(layout="wide")
# Inject custom CSS stylesheet
load_data.load_css("styles.css")

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
    st.markdown(
        f'''
            <div class="tab-explainer">
                <h1 class="card-title">Overview: Key Trends and Statistics</h1>
                <p class="card-desc italics">
                    Below we show a snapshot of the mental health crisis in Australia. 
                    For a more detailed and interactive exploration, select the explore in more detail tab above.
                </p>
            </div>
            ''',
        unsafe_allow_html=True
    )
    # Setup three columns
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        ui.chart_card(
            "Hospitalizations by State",
            "The number of mental health hospital admissions across each of the states in Australia.",
            plots.hospitalizations_by_state(dfs_admitted['Table 4'])
        )
        ui.chart_card(
            "Hospitalizations by Socioeconomic Status",
            "Mental health is influenced by socioeconomic status. The population living in the 20% of areas with the greatest overall level of disadvantage is described as the lowest socioeconomic group (Quintile 1). The 20% at the other end of the scale (the top fifth - Quintile 5) is described as the highest socioeconomic group.",
            plots.hospitalizations_by_socioeconomic_status(dfs_admitted['Table 5'])
        )
    with col2:
        ui.chart_card(
            "Hospitalizations by Age",
            "The number of Australian hospital admissions across different age groups.",
            plots.hospitalizations_by_age(dfs_admitted['Table 3'])
        )
        ui.chart_card(
            "Hospitalizations by Remoteness",
            "Location can have an influence on mental health. Below you can see the distribution based on the level of remoteness.",
            plots.hospitalizations_by_remoteness(dfs_admitted['Table 5'])
        )
    with col3:
        ui.chart_card(
            "Hospitalizations by Diagnosis and Age Group",
            "There are a range of mental health diagnoses and the type of diagnosis can be influenced by age group.",
            plots.diagnosis_age(dfs_outcomes['Table 12'])
        )
        ui.chart_card(
            "Hospitalizations by Indigenous Status",
            "The distribution of mental health hospital admissions in Australia across Indigenous and non-Indigenous communities.",
            plots.hospitalizations_by_indigenous_status(dfs_admitted['Table 5'])
        )

with tab2:

    # Year Slider
    year = st.slider(
        label="Year",
        min_value=2014,  # set to 2014 as it is the earliest year in the dfs_outcome dataset
        max_value=dfs_admitted['Table 1']["Year"].max(),
        value=2016
    )

    # Example of filtering via year
    st.altair_chart(plots.hospitalizations_by_state(dfs_admitted['Table 4'][dfs_admitted['Table 4']['Year'] == year]), use_container_width=True)

    st.altair_chart(plots.clinical_outcomes(dfs_outcomes['Table 21'][dfs_outcomes['Table 21']['Year'] == year]), use_container_width=True)

    st.altair_chart(plots.diagnoses(dfs_outcomes['Table 12'][dfs_outcomes['Table 12']['Year'] == year]), use_container_width=True)

    st.altair_chart(plots.distribution_over_time(dfs_outcomes['Table 12']), use_container_width=True)

    st.altair_chart(plots.admission_problems(dfs_outcomes['Table 8'][dfs_outcomes['Table 8']['Year'] == year]), use_container_width=True)
    # st.dataframe(dfs_outcomes['Table 8'])

    st.altair_chart(plots.age_sex_hopsitalizations(dfs_admitted['Table 3']))

    st.altair_chart(plots.pick_own_variables(dfs_admitted['Table 3']))
