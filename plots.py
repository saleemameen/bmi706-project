import altair as alt
import streamlit as st


def hospitalizations_by_state(table):
    df_hospitalizations = table[table['Measure'] == 'Hospitalisations']
    df_hospitalizations = df_hospitalizations[df_hospitalizations['State'] != 'National']
    df_hospitalizations = df_hospitalizations.groupby('State')['Count'].sum().reset_index()
    chart = alt.Chart(df_hospitalizations).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('State:N', title='State', sort='-y'),
        tooltip=['State:N', 'Count:Q']
    )
    return chart


def hospitalizations_by_age(table):
    # For private hospitals they refer to the measure as "Patients" instead of "Hospitalisations",
    # We want to look at both
    df_ages = table[(table['Measure'] == 'Hospitalisations') | (table['Measure'] == 'Patients')]
    df_ages = df_ages.groupby('Age group')['Count'].sum().reset_index()
    # Plot hospitalizations per age group on a bar chart
    chart = alt.Chart(df_ages).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Age group:N', title='Age Group'),
        tooltip=['Age group:N', 'Count:Q']
    )
    return chart


def hospitalizations_by_indigenous_status(table):
    indigenous_status = table[(table['Demographic type'] == 'Indigenous status') & (table['Measure'] == 'Hospitalisations')]
    indigenous_status = indigenous_status.groupby('Demographic')['Count'].sum().reset_index()

    # Calculate the total to find percentages
    total_count = indigenous_status['Count'].sum()
    indigenous_status['Percentage'] = (indigenous_status['Count'] / total_count * 100).round(1)

    # Plot hospitalizations per indigenous status on a donut chart using mark_arc
    chart = alt.Chart(indigenous_status).mark_arc().encode(
        theta='Count:Q',
        color=alt.Color('Demographic:N', title='Indigenous Status'),
        tooltip=['Demographic:N', 'Count:Q', alt.Tooltip('Percentage:Q', title='Percentage')]
    )
    return chart


def hospitalizations_by_socioeconomic_status(table):
    socioeconomic_status = table[(table['Demographic type'] == 'SEIFA quintile of usual residence') & (table['Measure'] == 'Hospitalisations')]
    socioeconomic_status = socioeconomic_status.groupby('Demographic')['Count'].sum().reset_index()
    chart = alt.Chart(socioeconomic_status).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='SEIFA Quintile'),
        tooltip=['Demographic:N', 'Count:Q'],
    )
    return chart


def hospitalizations_by_remoteness(table):
    remoteness = table[(table['Demographic type'] == 'Remoteness area of usual residence') & (table['Measure'] == 'Hospitalisations')]
    remoteness = remoteness.groupby('Demographic')['Count'].sum().reset_index()
    chart = alt.Chart(remoteness).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='Remoteness Area', sort='-y'),
        tooltip=['Demographic:N', 'Count:Q']
    )
    return chart


def clinical_outcomes(table):
    consumer_groups = list(table['Consumer group'].unique())
    selected_consumer_group = st.selectbox("Consumer group", options=consumer_groups)
    table = table[table['Consumer group'] == selected_consumer_group]

    outcome_groups = table.groupby('Outcome group')['Count'].sum().reset_index()
    chart = alt.Chart(outcome_groups).mark_arc(innerRadius=50).encode(
        theta='Count:Q',
        color=alt.Color('Outcome group:N', title='Clinical Outcome', scale=alt.Scale(scheme='viridis')),
        tooltip=['Outcome group:N', 'Count:Q']
    )
    return chart


def diagnoses(table):
    # filter for clinical setting
    # clinical_setting = list(table['Setting'].unique()) has an empty string
    clinical_setting = ['Acute inpatient', 'Ambulatory']
    selected_setting = st.radio("Setting", options=clinical_setting, horizontal=True)
    table = table[table['Setting'] == selected_setting]
    # filter for age  band
    age_bands = list(table['Age band'].unique())
    selected_age_band = st.selectbox("Age band", options=age_bands)
    table = table[table['Age band'] == selected_age_band]
    diagnoses = table.groupby('Principal diagnosis')['Count'].sum().reset_index()
    chart = alt.Chart(diagnoses).mark_bar().encode(
        x=alt.Y('Count:Q', title='Diagnoses'),
        y=alt.X('Principal diagnosis:N', title='Diagnosis', sort='-x'),
        tooltip=['Principal diagnosis:N', 'Count:Q']
    )
    return chart


def admission_problems(table):
    problems = table.groupby('HoNOSCA scale')['Count'].sum().reset_index()
    chart = alt.Chart(problems).mark_bar().encode(
        x=alt.Y('Count:Q', title='Admissions'),
        y=alt.X('HoNOSCA scale:N', title='Problem on Admission', sort='-x'),
        tooltip=['HoNOSCA scale:N', 'Count:Q']
    )
    return chart


def hospitalizations_by_diagnosis_over_time(table):
    default_diagnoses = ['(F32) Depressive episode', '(F31) Bipolar affective disorders', '(F20) Schizophrenia', '(F99) Mental disorder not otherwise specified']
    diagnoses = st.multiselect("Diagnoses", options=table['Principal diagnosis'].unique(), default=default_diagnoses)
    distribution = table[table['Principal diagnosis'].isin(diagnoses)].groupby(['Year', 'Principal diagnosis'])['Count'].sum().reset_index()
    chart = alt.Chart(distribution).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Count:Q', title='Hospitalizations'),
        tooltip=['Year:O', 'Count:Q'],
        color='Principal diagnosis:N',
    ).interactive()
    return chart


def hospitalizations_by_age_sex_over_time(table):
    table = table[(table['Measure'] == 'Hospitalisations') | (table['Measure'] == 'Patients')]
    table = table[(table['Sex'] == "Female") | (table['Sex'] == 'Male')]
    ages = list(table['Age group'].unique())
    default_age = '25–34 years'
    ages.insert(0, ages.pop(ages.index(default_age)))
    age = st.selectbox("Select Age Group", options=ages)
    table = table[table['Age group'] == age].groupby(['Year', 'Sex'])['Count'].sum().reset_index()
    chart = alt.Chart(table).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Count:Q', title='Hospitalizations'),
        tooltip=['Year:O', 'Count:Q'],
        color='Sex:N',
    ).interactive()

    # chart = alt.Chart(table).mark_bar().encode(
    #     x=alt.X('Year:O', title='Year'),
    #     y=alt.Y('Count:Q', title='Hospitalizations'),
    #     tooltip=['Year:O', 'Count:Q'],
    #     column='Sex:N',
    #     color="Sex:N"
    # )

    return chart


def diagnosis_age(table):
    # some funky non existent category in Age Group
    age_bands = ['11-17 years', '18-64 years', '65 years and over']
    table = table[table['Age band'].isin(age_bands)]

    table = table.groupby(['Principal diagnosis', 'Age band'])['Count'].sum().reset_index()

    chart = alt.Chart(table).mark_bar().encode(
        y=alt.Y('Principal diagnosis:O', title='Diagnosis'),
        x=alt.X('Count:Q', title='Count'),
        color=alt.Color('Age band:N', title='Age Group'),
        tooltip=['Principal diagnosis:O', 'Count:Q', 'Age band:N']
    )

    return chart


def pick_own_variables(table):
    # pick your own variables
    x = st.selectbox("X", options=table.columns)
    y = st.selectbox("Y", options=table.columns)
    chart = alt.Chart(table).mark_point().encode(
        x=alt.X(x),
        y=alt.Y(y)
    )
    return chart
