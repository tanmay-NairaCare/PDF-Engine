import streamlit as st
from extract_from_textract2 import *
import pandas as pd
import time

# Code for uploading the PDF/image file
st.title("Welcome to Naira HealthCare ")
def upload_file():
    temp_folder = "temp"
    # Check if the "temp" folder exists, and create it if it doesn't
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "png"])
    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        with open(os.path.join("temp", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved as temp/{uploaded_file.name}")
        return os.path.join("temp", uploaded_file.name)
    else:
        return None


# Call the upload_file function to upload file
file_path = upload_file()
option = st.selectbox(
    'Please select the name of testing center',
    ('Pharmeasy', 'TATA 1Mg', 'Metropolis','NM Medical', 'TruTest Lab'))
st.write('You selected:', option)


def main(file_path):
    print("Current File path is: ",file_path)
    file_prefix = os.path.splitext(file_path)[0]
    start_time = time.time()
    table_csv_file=extract_all(file_path,option)
    print(table_csv_file)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    #st.write("Time elapsed: ", elapsed_time, "seconds")
    if table_csv_file==None:
        st.write("No meaningful data present.")
    else:
        if os.stat(table_csv_file).st_size == 0:
            st.write("File is empty!")
        else:
            df = pd.read_csv(table_csv_file)
            st.write(df)

# If a file is uploaded, call the main function to process the file
if file_path is not None:
    main(file_path)


