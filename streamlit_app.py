import altair as alt
import pandas as pd
import streamlit as st
import re
import numpy as np
import json

##########################################################################
# PRE-PROCESS DATA
##########################################################################
def clean_table(xls, sheet_name):
    # Step 1: Read in the data and start at row 4, which are the column names
    df = xls.parse(sheet_name=sheet_name, header=4)
    # Step 2: Handle replacing missing values as defined in the General Information sheet
    replacements = {
        "—": 0,  # "Rounded to zero"
        ". .": np.nan,  # "Not applicable"
        "n.a.": np.nan,  # "Not available"
        "n.p.": np.nan  # "Not published"
    }
    df.replace(replacements, inplace=True)
    # Step 3: Remove any rows where there exists the words Total | Subtotal
    rows_to_drop = df.apply(lambda row: any("Total" in str(
        cell) or "Subtotal" in str(cell) for cell in row), axis=1)
    df = df[~rows_to_drop]
    # Step 4: Standardize Year Columns to extract only the YYYY
    # - Since sometimes the years are separated with hyphens OR dashes, we need to standardize the names first
    df.columns = [re.sub(r'[-–]', '-', col) for col in df.columns]
    # - Then extract the years for the column name
    df.columns = [
        col.split('-')[0] if '-' in col else col for col in df.columns]
    # Step 5: Drop any rows where all the year columns are empty
    year_columns = [col for col in df.columns if col.isdigit()]
    df = df.dropna(subset=year_columns, how='all')
    # Step 6: Melt the DataFrame
    id_vars = [col for col in df.columns if col not in year_columns]
    df_melted = pd.melt(df, id_vars=id_vars, value_vars=year_columns,
                        var_name='Year', value_name='Count')
    # Step 7: Convert Year from string to int
    df_melted['Year'] = df_melted['Year'].astype(int)
    return df_melted


@st.cache_data
def load_admitted_patients_data():
    xls = pd.ExcelFile('./data/admitted-patients-2012-22.xlsx')
    ac_sheets = [sheet for sheet in xls.sheet_names if re.match(
        r'Table AC\.\d+', sheet)]
    dfs = {sheet_name: clean_table(xls, sheet_name)
           for sheet_name in ac_sheets}
    # For Table AC.4 rename the State column
    dfs['Table AC.4'] = dfs['Table AC.4'].rename(
        columns={"State\nTerritory": "State"})
    # For Table AC.6 remove the rows with an aggregate total for the Financial Year
    dfs['Table AC.6'] = dfs['Table AC.6'][~dfs['Table AC.6']
                                          ['Quarter'].str.contains("Financial Year", na=False)]
    # For Table AC.6 map the quarters to numerical representations
    unique_quarters = dfs['Table AC.6']['Quarter'].unique()
    quarter_mapping = {quarter: i for i,
                       quarter in enumerate(unique_quarters, start=1)}
    dfs['Table AC.6']['Quarter'] = dfs['Table AC.6']['Quarter'].map(
        quarter_mapping)
    #for Table AC.3 we need to remove redundant age groups (85 and older and 85 and over are the same group)
    dfs['Table AC.3']['Age group'] = dfs['Table AC.3']['Age group'].replace('85 years and over', '85 years and older')
    #for Table AC.5, rename quantiles 1 and 5 to ensure similar formatting
    dfs['Table AC.5']['Demographic'] = dfs['Table AC.5']['Demographic'].replace('Quintile 1 (most disadvantaged)', 'Quintile 1')
    dfs['Table AC.5']['Demographic'] = dfs['Table AC.5']['Demographic'].replace('Quintile 5 (least disadvantaged)', 'Quintile 5')
    return dfs

##########################################################################
# LOAD DATA
##########################################################################
dfs_admitted = load_admitted_patients_data()




##########################################################################
# PLOTTING FUNCTIONS
##########################################################################
def geographical_breakdown(year):

    
    df_ac4 = dfs_admitted['Table AC.4']
    #just for debugging
    #saleem --> year in the df is shown with a comma (2,012 instead of 2012) and i think this is making us not be able to filer the data
    #st.dataframe(df_ac4)

    df_hospitalizations = df_ac4[df_ac4['Measure'] == 'Hospitalisations']
    df_hospitalizations = df_hospitalizations.groupby('State')['Count'].sum().reset_index()
    # Plot hospitalizations per state on a bar chart
    chart = alt.Chart(df_hospitalizations).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('State:N', title='State', sort='-y'),
        tooltip=['State:N', 'Count:Q'],
        title = "Hospitalizations by State"
    )
    return chart

def age_breakdown(year):
    df_ac3 = dfs_admitted['Table AC.3']
    #st.dataframe(df_ac3) used for debgugging, will delete after
    #for private hopsitals they refer to the measure as "Patients" instead of "Hospitalisations", we want to look at both
    df_ages = df_ac3[(df_ac3['Measure'] == 'Hospitalisations') | (df_ac3['Measure'] == 'Patients')]
    df_ages = df_ages.groupby('Age group')['Count'].sum().reset_index()

    #plot hospitalizations per age group on a bar chart
    chart = alt.Chart(df_ages).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Age group:N', title='Age Group'),
        tooltip=['Age group:N', 'Count:Q'],
        title = "Hospitalizations by Age Group"
    ).properties(
        width=600,
        height=400
    )

    return chart

def demographic_breakdown(year):
    df_ac5 = dfs_admitted['Table AC.5']
    #st.dataframe(df_ac5) #used for debgugging, will delete after

    #indigenous breakdown
    indigenous_status = df_ac5[(df_ac5['Demographic type'] == 'Indigenous status') & (df_ac5['Measure'] == 'Hospitalisations')]
    indigenous_status = indigenous_status.groupby('Demographic')['Count'].sum().reset_index()
    #st.dataframe(indigenous_status)

    # Plot hospitalizations per indigenous status on a donut chart using mark_arc
    indigenous_breakdown = alt.Chart(indigenous_status).mark_arc().encode(
        theta='Count:Q',
        color=alt.Color('Demographic:N', title='Indigenous Status'),
        tooltip=['Demographic:N', 'Count:Q'],
        title = "Hospitalizations by Indigenous Status"
    )
    #Plot hospitalizations per socioeconomic status on a bar chart
    socioeconomic_status = df_ac5[(df_ac5['Demographic type'] == 'SEIFA quintile of usual residence') & (df_ac5['Measure'] == 'Hospitalisations')]
    socioeconomic_status = socioeconomic_status.groupby('Demographic')['Count'].sum().reset_index()

    socioeconomic_breakdown = alt.Chart(socioeconomic_status).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='SEIFA Quintile'),
        tooltip=['Demographic:N', 'Count:Q'],
        title = "Hospitalizations by Socioeconomic Status"
    )

    #Plot hospitalizations per remoteness
    remoteness = df_ac5[(df_ac5['Demographic type'] == 'Remoteness area of usual residence') & (df_ac5['Measure'] == 'Hospitalisations')]
    remoteness = remoteness.groupby('Demographic')['Count'].sum().reset_index()

    remoteness_breakdown = alt.Chart(remoteness).mark_bar().encode(
        y=alt.Y('Count:Q', title='Hospitalizations'),
        x=alt.X('Demographic:N', title='Remoteness Area', sort = '-y'),
        tooltip=['Demographic:N', 'Count:Q'],
        title = "Hospitalizations by Level of Remoteness"
    )
    
    return indigenous_breakdown, socioeconomic_breakdown, remoteness_breakdown

    
    
   


##########################################################################
# DASHBOARD
##########################################################################
st.write("## Mental Health in Australia")
st.write("Mental Health is a serious concern in Australia. Explore the data to learn more.")


#make tabs
tab1, tab2 = st.tabs(["Overview", "Explore in More Detail"])

with tab1:
    st.write("### Key Trends and Statistics")

    #year is the same range for all tables
    df_ac1 = dfs_admitted['Table AC.1']
    year = st.slider(
        label="Year",
        min_value=df_ac1["Year"].min(),
        max_value=df_ac1["Year"].max(),
        value = 2023
    )


    #hopsitalizations by geographical location
    hopsitalizations_location = geographical_breakdown(year)
    st.altair_chart(hopsitalizations_location, use_container_width=True)


    #hopsitalizations by age group
    hopsitalizations_age = age_breakdown(year)
    st.altair_chart(hopsitalizations_age, use_container_width=True)

    #hopsitalizations by indigenous status, SES and remoteness
    indigenous_breakdown, SES_breakdown, remoteness_breakdown = demographic_breakdown(year)
    #socioeconomic_breakdown = demographic_breakdown(year)

    #combined_chart = alt.hconcat(indigenous_breakdown, SES_breakdown, remoteness_breakdown)
    #st.altair_chart(combined_chart, use_container_width=True)

    indigenous_chart = st.altair_chart(indigenous_breakdown, use_container_width=True)
    SES_chart = st.altair_chart(SES_breakdown, use_container_width=True)
    remoteness_chart = st.altair_chart(remoteness_breakdown, use_container_width=True)


    #diagnosis we need the second data set
    

    








