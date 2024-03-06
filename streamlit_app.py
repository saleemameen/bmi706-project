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
tab1, tab2, tab3 = st.tabs(["Overview", "Analysis by Year", "Trends Over Time"])

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
    # Provide a Title for the Tab
    st.markdown(
        f'''
            <div class="tab-explainer">
                <h1 class="card-title">Analysis by Year</h1>
                <p class="card-desc italics">
                    Below we show a more detailed snapshot of the mental health crisis and how it has changed year on year. 
                    The charts are designed to be filterable and interactive.
                </p>
            </div>
            ''',
        unsafe_allow_html=True
    )

    # Year Slider
    year = st.slider(
        label="Select a Year",
        min_value=2014,  # set to 2014 as it is the earliest year in the dfs_outcome dataset
        max_value=dfs_admitted['Table 1']["Year"].max(),
        value=2016
    )

    # Setup two columns
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            ui.banner("Hospitalizations by State", "While hospital admissions for mental health have historically been the highest in New South Wales, followed by Victoria and then Queensland; in recent years, the number of admissions in these states have started to become equivalent.")
            st.altair_chart(plots.hospitalizations_by_state(dfs_admitted['Table 4'][dfs_admitted['Table 4']['Year'] == year]), use_container_width=True)
        with st.container(border=True):
            ui.banner("Clinical Outcomes Relative to Consumer Group", "Depending on the patient's admission status, clinical outcomes can vary. For example, those who complete an acute inpatient admission more often experience significant improvement.", withFilters=True)
            st.altair_chart(plots.clinical_outcomes(dfs_outcomes['Table 21'][dfs_outcomes['Table 21']['Year'] == year]), use_container_width=True)
    with col2:
        with st.container(border=True):
            ui.banner("Reasons Leading to Hospital Admissions", "There are several different behaviours identified and reported that lead to a mental health admission. The reasons and their frequency of being reported can be observed below.")
            st.altair_chart(plots.admission_problems(dfs_outcomes['Table 8'][dfs_outcomes['Table 8']['Year'] == year]), use_container_width=True)
        with st.container(border=True):
            ui.banner("Diagnosis Based on Admission Status and Age", "Here we show the ICD-10 codes that reveal the types of diagnoses and their frequency based on age and admission setting.", withFilters=True)
            st.altair_chart(plots.diagnoses(dfs_outcomes['Table 12'][dfs_outcomes['Table 12']['Year'] == year]), use_container_width=True)

    with tab3:
        # Provide a Title for the Tab
        st.markdown(
            f'''
                <div class="tab-explainer">
                    <h1 class="card-title">Trends Over Time</h1>
                    <p class="card-desc italics">
                        Below you can observe how the diagnostic landscape has been changing over time. If you scroll over a line chart, it will zoom in to provide greater detail.
                    </p>
                </div>
                ''',
            unsafe_allow_html=True
        )
        with st.container(border=True):
            ui.banner("Number of Hospitalizations by Diagnosis Over Time", "Diagnostic trends have been changing over time. You can select specific diagnoses based on ICD-10 codes below and compare how they have changed over time.")
            st.altair_chart(plots.hospitalizations_by_diagnosis_over_time(dfs_outcomes['Table 12']), use_container_width=True)
        with st.container(border=True):
            ui.banner("Hospitalizations by Year and Age Group Over Time", "The number of hospitalizations based according to Age and Sex has also been changing over time. Explore the trends in the changing landscape below.", withFilters=True)
            st.altair_chart(plots.hospitalizations_by_age_sex_over_time(dfs_admitted['Table 3']), use_container_width=True)

    # st.altair_chart(plots.pick_own_variables(dfs_admitted['Table 3']))
