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
    ).properties(
        title="Hospitalizations by State"
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
    ).properties(
        title="Hospitalizations by Age Group",
        width=600,
        height=400
    )
    return chart


def hospitalizations_by_indigenous_status(table):
    indigenous_status = table[(table['Demographic type'] == 'Indigenous status') & (table['Measure'] == 'Hospitalisations')]
    indigenous_status = indigenous_status.groupby('Demographic')['Count'].sum().reset_index()
    # Plot hospitalizations per indigenous status on a donut chart using mark_arc
    chart = alt.Chart(indigenous_status).mark_arc().encode(
        theta='Count:Q',
        color=alt.Color('Demographic:N', title='Indigenous Status'),
        tooltip=['Demographic:N', 'Count:Q']
    ).properties(
        title="Hospitalizations by Indigenous Status"
    )
    return chart


# df_ac5 = dfs_admitted['Table AC.5']
def hospitalizations_by_indigenous_status(table):
    indigenous_status = table[(table['Demographic type'] == 'Indigenous status') & (table['Measure'] == 'Hospitalisations')]
    indigenous_status = indigenous_status.groupby('Demographic')['Count'].sum().reset_index()
    # Plot hospitalizations per indigenous status on a donut chart using mark_arc
    chart = alt.Chart(indigenous_status).mark_arc().encode(
        theta='Count:Q',
        color=alt.Color('Demographic:N', title='Indigenous Status'),
        tooltip=['Demographic:N', 'Count:Q']
    ).properties(
        title="Hospitalizations by Indigenous Status"
    )
    return chart


def hospitalizations_by_socioeconomic_status(table):
    socioeconomic_status = table[(table['Demographic type'] == 'SEIFA quintile of usual residence') & (table['Measure'] == 'Hospitalisations')]
    socioeconomic_status = socioeconomic_status.groupby('Demographic')['Count'].sum().reset_index()
    chart = alt.Chart(socioeconomic_status).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='SEIFA Quintile'),
        tooltip=['Demographic:N', 'Count:Q'],
    ).properties(
        title="Hospitalizations by Socioeconomic Status"
    )
    return chart


def hospitalizations_by_remoteness(table):
    remoteness = table[(table['Demographic type'] == 'Remoteness area of usual residence') & (table['Measure'] == 'Hospitalisations')]
    remoteness = remoteness.groupby('Demographic')['Count'].sum().reset_index()
    chart = alt.Chart(remoteness).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='Remoteness Area', sort='-y'),
        tooltip=['Demographic:N', 'Count:Q']
    ).properties(
        title="Hospitalizations by Level of Remoteness"
    )
    return chart

def clinical_outcomes(table):
    outcome_groups = table.groupby('Outcome group')['Count'].sum().reset_index()
    chart = alt.Chart(outcome_groups).mark_arc(innerRadius = 50).encode(
        theta='Count:Q',
        color=alt.Color('Outcome group:N', title='Clinical Outcome', scale=alt.Scale(scheme='viridis')),
        tooltip=['Outcome group:N', 'Count:Q']
    ).properties(
        title="Distribution of Clinical Outcomes For Those Receciving Mental Health Care"
    )
    return chart

def diagnoses(table):
    diagnoses = table.groupby('Principal diagnosis')['Count'].sum().reset_index()
    chart = alt.Chart(diagnoses).mark_bar().encode(
        x=alt.Y('Count:Q', title='Diagnoses'),
        y=alt.X('Principal diagnosis:N', title='Diagnosis', sort='-x'),
        tooltip=['Principal diagnosis:N', 'Count:Q']
    ).properties(
        title="Distribution of Diagnoses For Those Receciving Mental Health Care"
    )
    return chart

def distribution_over_time(table):
    #distribution = table.groupby(['Year', 'Principal Diagnoses'])['Count'].sum().reset_index()

    default_diagnoses = ['(F32) Depressive episode', '(F31) Bipolar affective disorders','(F20) Schizophrenia', '(F99) Mental disorder not otherwise specified']
    diagnoses =  st.multiselect("Diagnoses", options=table['Principal diagnosis'].unique(), default=default_diagnoses)

    distribution = table[table['Principal diagnosis'].isin(diagnoses)].groupby(['Year', 'Principal diagnosis'])['Count'].sum().reset_index()

    chart = alt.Chart(distribution).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Count:Q', title='Hospitalizations'),
        tooltip=['Year:O', 'Count:Q'],
        color='Principal diagnosis:N',
    ).properties(
        title="Distribution of Hospitalizations Over Time by Diagnosis"
    )
    return chart

def admission_problems(table):
    problems = table.groupby('HoNOSCA scale')['Count'].sum().reset_index()
    chart = alt.Chart(problems).mark_bar().encode(
        x=alt.Y('Count:Q', title='Admissions'),
        y=alt.X('HoNOSCA scale:N', title='Problem on Admission', sort='-x'),
        tooltip=['HoNOSCA scale:N', 'Count:Q']
    ).properties(
        title="Distribution of Behaviours or People Leading to Admission"
    )
    return chart

def age_sex_hopsitalizations(table):
    table = table[(table['Measure'] == 'Hospitalisations') | (table['Measure'] == 'Patients')]
    table = table[(table['Sex'] == "Female") | (table['Sex'] == 'Male')]

    # age = st.selectbox("Age", options=table['Age group'].unique(), default='25-34 years')
    # table = table[table['Age group'] == age]
    ages = list(table['Age group'].unique())
    default_age = '25–34 years'
    ages.insert(0, ages.pop(ages.index(default_age)))

    age = st.selectbox("Age", options=ages) 

    # Continue with your chart creation code...
    chart = alt.Chart(table).mark_bar().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Count:Q', title='Hospitalizations'),
        tooltip=['Year:O', 'Count:Q'],
        column = 'Sex:N',
        color = "Sex:N"
    ).properties(
        title="Hospitalizations by Year and Age Group"
    )

    return chart


def diagnosis_age(table):
    #some funky non existent category in Age Group
    age_bands = ['11-17 years', '18-64 years', '65 years and over']
    table = table[table['Age band'].isin(age_bands)]

    table = table.groupby(['Principal diagnosis', 'Age band'])['Count'].sum().reset_index()

    chart = alt.Chart(table).mark_bar().encode(
        y=alt.Y('Principal diagnosis:O', title='Diagnosis'),
        x=alt.X('Count:Q', title='Count'),
        color=alt.Color('Age band:N', title='Age Group'),
        tooltip=['Principal diagnosis:O', 'Count:Q', 'Age band:N']
    ).properties(
        title="Hospitalizations by Diagnosis and Age Group"
    )

    return chart
    

