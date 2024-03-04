import streamlit as st
import numpy as np
import pandas as pd
import re


def clean_table(xls, sheet_name):
    # This is used to prevent pandas from silently automatically downcasting data types
    pd.set_option('future.no_silent_downcasting', True)
    # Step 1: Read in the data and start at row 4, which are the column names
    df = xls.parse(sheet_name=sheet_name, header=4)
    # Step 2: Handle replacing missing values as defined in the General Information sheet
    replacements = {
        "—": 0,  # "Rounded to zero"
        ". .": np.nan,  # "Not applicable"
        "n.a.": np.nan,  # "Not available"
        "n.p.": np.nan,  # "Not published"
        "nan": np.nan,  # nan string
        ' ': np.nan
    }
    df.replace(replacements, inplace=True)
    # Step 3: Remove any rows where there exists the words Total | Subtotal | All
    rows_to_drop = df.apply(lambda row: any(str(cell) == "Total" or str(cell) == "Subtotal" or str(cell) == "All" for cell in row), axis=1)
    df = df[~rows_to_drop]
    # Step 4: Standardize Year Columns to extract only the YYYY
    # - Since sometimes the years are separated with hyphens OR dashes, we need to standardize the names first
    df.columns = [re.sub(r'[-–]', '-', col) for col in df.columns]
    # - Then extract the years for the column name
    df.columns = [col.split('-')[0] if '-' in col else col for col in df.columns]
    # Step 5: Drop columns that start with "Average annual\n change" (specific for consumer-outcomes table)
    df = df.drop([col for col in df.columns if re.match(r"^Average.*annual.*change", col, re.DOTALL)], axis=1)
    # Step 6: Drop any rows where all the year columns are empty
    year_columns = [col for col in df.columns if col.isdigit()]
    # - Now drop any rows where all the year_columns are NaN values
    df = df.dropna(subset=year_columns, how='all')
    # Rename any generic columns
    df.rename(columns={"State\nTerritory": "State", "State/Territory": "State", "Count": "Count_Desc"}, inplace=True)
    # Step 7: Melt the DataFrame
    id_vars = [col for col in df.columns if col not in year_columns]
    df_melted = pd.melt(df, id_vars=id_vars, value_vars=year_columns, var_name='Year', value_name='Count')
    # Step 8: Convert Year from string to int
    df_melted['Year'] = df_melted['Year'].astype(int)
    return df_melted


@st.cache_data
def admitted_patients_data():
    # Load the data
    xls = pd.ExcelFile('./data/admitted-patients-2012-22.xlsx')
    # Pull in all the sheets that start with Table AC
    sheets = [sheet for sheet in xls.sheet_names if re.match(r'Table AC\.\d+', sheet)]
    # Clean the data for each sheet
    dfs = {'Table {}'.format(i + 1): clean_table(xls, sheet_name) for i, sheet_name in enumerate(sheets)}
    # For Table AC.6 remove the rows with an aggregate total for the Financial Year
    dfs['Table 6'] = dfs['Table 6'][~dfs['Table 6']['Quarter'].str.contains("Financial Year", na=False)]
    # For Table AC.6 map the quarters to numerical representations
    unique_quarters = dfs['Table 6']['Quarter'].unique()
    quarter_mapping = {quarter: i for i, quarter in enumerate(unique_quarters, start=1)}
    dfs['Table 6']['Quarter'] = dfs['Table 6']['Quarter'].map(quarter_mapping)
    # For Table AC.3 we need to remove redundant age groups (85 and older and 85 and over are the same group)
    dfs['Table 3']['Age group'] = dfs['Table 3']['Age group'].replace('85 years and over', '85 years and older')
    # For Table AC.5, rename quantiles 1 and 5 to ensure similar formatting
    dfs['Table 5']['Demographic'] = dfs['Table 5']['Demographic'].replace('Quintile 1 (most disadvantaged)', 'Quintile 1')
    dfs['Table 5']['Demographic'] = dfs['Table 5']['Demographic'].replace('Quintile 5 (least disadvantaged)', 'Quintile 5')
    return dfs


@st.cache_data
def consumer_outcomes_data():
    # Load the data
    xls = pd.ExcelFile('./data/consumer-outcomes-2012-22.xlsx')
    # Pull in all the sheets that start with Table NOCC
    sheets = [sheet for sheet in xls.sheet_names if re.match(r'Table NOCC\.\d+', sheet)]
    # Clean the data for each sheet
    dfs = {'Table {}'.format(i + 1): clean_table(xls, sheet_name) for i, sheet_name in enumerate(sheets)}
    return dfs
