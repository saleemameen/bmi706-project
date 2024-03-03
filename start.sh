#!/bin/bash

# Get the current username
USERNAME=$(whoami)

# Allow the user to specify the environment name as the first argument
ENV_NAME=$1

# Check if the environment name was provided
if [ -z "$ENV_NAME" ]; then
    echo "Usage: $0 <environment_name>"
    exit 1
fi

# Activate the Conda environment
source /Users/$USERNAME/anaconda3/bin/activate && conda activate /Users/$USERNAME/anaconda3/envs/$ENV_NAME

# Check if the Conda environment was activated successfully
if [ $? -ne 0 ]; then
    echo "Failed to activate Conda environment '$ENV_NAME'. Please check the environment name and try again."
    exit 1
fi

# Run the Streamlit app
streamlit run streamlit_app.py

# Check if Streamlit started successfully
if [ $? -ne 0 ]; then
    echo "Failed to start Streamlit app. Please check if 'streamlit_app.py' exists and try again."
    exit 1
fi
