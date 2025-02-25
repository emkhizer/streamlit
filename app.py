import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set the page configuration first
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        /* Custom button style */
        .css-1v3fvcr {
            background-color: #4CAF50; /* Green background */
            color: white; /* White text */
            font-weight: bold; /* Bold text */
        }

        /* Custom header styling */
        .css-18e3th9 {
            background-color: #f0f0f5; /* Light grey background */
            padding: 20px; /* Add some padding around */
            border-radius: 8px; /* Rounded corners */
        }

        /* Make the file uploader a little more stylish */
        .css-1kv4pvp {
            background-color: #e8f5e9; /* Very light green background */
            border-radius: 10px; /* Rounded corners */
            padding: 10px; /* Add some padding */
        }

        /* Custom background for the whole app */
        body {
            background-color: #f4f7fc; /* Light blue background */
        }

        /* Styling for data preview table */
        .stDataFrame {
            border-radius: 10px; /* Rounded table corners */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Soft shadow effect */
        }
    </style>
""", unsafe_allow_html=True)

# Set up the app
st.title("✨ Data Sweeper ✨")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File Upload Section
uploaded_files = st.file_uploader("Upload your Files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # Get file extension and read accordingly
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file type: {file_ext}. Please upload a valid CSV or Excel file.")
            continue

        # File info
        st.subheader(f"📄 File Information for: {file.name}")
        file_size = file.size / 1024  # KB
        st.write(f"**File Size:** {file_size:.2f} KB")
        
        # Show preview of the dataframe
        st.write("🔍 Preview the first few rows of the dataset:")
        st.dataframe(df.head())

        # Data Cleaning Section
        st.subheader("🧹 Data Cleaning Options")

        # Remove Duplicates
        if st.checkbox("Remove Duplicates"):
            st.write("Removing duplicate rows...")
            before_cleaning = df.shape[0]
            df.drop_duplicates(inplace=True)
            after_cleaning = df.shape[0]
            st.success(f"Removed {before_cleaning - after_cleaning} duplicate rows.")

        # Fill Missing Values
        if st.checkbox("Fill Missing Values"):
            numeric_cols = df.select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success("Filled missing values with column means.")

        # Column Selection for Conversion
        st.subheader("🔲 Select Columns to Keep")
        columns_to_keep = st.multiselect("Choose columns to retain:", df.columns, default=df.columns)
        df = df[columns_to_keep]
        st.write("Columns after selection:", df.columns)

        # Data Visualization Section
        st.subheader("📊 Data Visualization")
        if st.checkbox("Visualize Data"):
            st.write("Visualizing the first two numeric columns...")
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options: CSV or Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"🔽 Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
