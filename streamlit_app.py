import altair as alt
import pandas as pd
import streamlit as st
import re
import numpy as np

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
    return dfs

##########################################################################
# LOAD DATA
##########################################################################
dfs_admitted = load_admitted_patients_data()

##########################################################################
# DASHBOARD
##########################################################################
st.write("## Mental Health in Australia")

df_ac1 = dfs_admitted['Table AC.1']
year = st.slider(
    label="Year",
    min_value=df_ac1["Year"].min(),
    max_value=df_ac1["Year"].max(),
    value=2012
)
subset = df_ac1[df_ac1["Year"] == year]
