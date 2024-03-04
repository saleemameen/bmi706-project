import altair as alt


def hospitalizations_by_state(table):
    df_hospitalizations = table[table['Measure'] == 'Hospitalisations']
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
