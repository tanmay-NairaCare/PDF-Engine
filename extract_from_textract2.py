from trp import Document
import os, time, cv2
import boto3
import sys
from pprint import pprint
from convert_pdf_to_image import convert_pdf_to_image
import csv,re
import pandas as pd
from test_keywords import pharmeasy_keywords,tata1mg_test_names, metropolis_keywords, trutest_keywords, nm_medical_keywords
from standard_test_mapper import *
from converter import Converter
from image_preprocess1 import ImagePreprocessor
from multiprocessing import Pool, freeze_support
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
def get_table_csv_results2(file_name,file_prefix,option):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)


    session = boto3.Session()
    client = session.client('textract')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
    #getting the raw text data
    formatted_text = ""
    for page in response['Blocks']:
        if page['BlockType'] == 'LINE':
            formatted_text += page['Text'] + "\n"       
    #print("*"*100)
    print(formatted_text)
    print("*"*100)
    if option.lower()=='nm medical':
        extract_data_from_raw_text(formatted_text,file_prefix + "_final_output.csv",option)
        convert_to_standard_form(file_prefix + "_final_output.csv",option)
        return file_prefix + "_final_output.csv"
    # Parse response
    doc = Document(response)

    # Save cell results in a CSV file(For tables)
    csv_file_path = file_prefix + '_output.csv'
    csv_file = open(csv_file_path, 'a', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    #process the tables
    for page in doc.pages:
        for i, table in enumerate(page.tables):
            for r, row in enumerate(table.rows):
                row_data = []
                for c, cell in enumerate(row.cells):
                    row_data.append(cell.text)
                csv_writer.writerow(row_data)
            # Add empty row after each table except the last one
            if i < len(page.tables) - 1:
                csv_writer.writerow([])
    csv_file.close()
    print(csv_file_path)

    # # Save form results in a CSV file(For forms)
    # form_csv_file_path = file_prefix + '_forms_output.csv'
    # form_csv_file = open(form_csv_file_path, 'a', newline='', encoding='utf-8')
    # form_csv_writer = csv.writer(form_csv_file)

    #  # Process forms
    # form_csv_writer.writerow(['key','value'])
    # for page in doc.pages:
    #     for field in page.form.fields:
    #         form_csv_writer.writerow([field.key, field.value])
    # form_csv_file.close()
    # print("Forms csv writer path is: ",form_csv_file_path)
    return read_csv_and_extract_data(formatted_text,csv_file_path,file_prefix + "_final_output.csv",option)

def extract_data_from_raw_text(raw_text,output_table_file_path,option):
    # if option.lower() == 'trutest lab':
    #     try:
    #         test_patterns = {
    #             "TSH Ultra*": r'TSH Ultra\*\n([\d.]+)',
    #             "Hemoglobin (Hb)*": r'Hemoglobin \(Hb\)\*\n([\d.]+)',
    #             "Erythrocyte (RBC) Count*": r'Erythrocyte \(RBC\) Count\*\n([\d.]+)',
    #             "PSA": r'PSA\n([\d.]+)\n',
    #             "Reaction (pH)*" : r'Reaction \(pH\)\*\s*([\d.]+)',
    #             "Specific Gravity" : r'Specific Gravity\*\s*([\d.]+)'
    #         }
    #         df = pd.DataFrame(columns=["Test Description", "Value(s)"])

    #         for test_description, test_pattern in test_patterns.items():
    #             match = re.search(test_pattern, raw_text)

    #             if match:
    #                 test_value = match.group(1)
    #                 print(f"{test_description} value: {test_value}")

    #                 # Create a new row in the DataFrame with the test description and value
    #                 df = df.append({"Test Description": test_description, "Value(s)": test_value},
    #                                ignore_index=True, sort=False)
    #             else:
    #                 print(f"{test_description} value not found in the text file.")

    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()
    #             print("Created empty dataframe!")

    #         # Concatenate the existing DataFrame with the new DataFrame
    #         existing_df = pd.concat([existing_df, df], ignore_index=True)

    #         existing_df.to_csv(output_table_file_path, columns=['Test Description', 'Value(s)'], index=False)
    #         print("Raw data saved in dataframe!")

    #     except Exception as e:
    #         print("An error occurred:", str(e))
    if option.lower() == 'nm medical':
        try:
            test_patterns = {
                'TB-Gold':r"\bFinal Result\b\n\w+\((\d+(?:\.\d+)?)\)",
                'Absolute Lymphocyte Count':r"\bAbsolute Lymphocyte Count\b\n(.+)|\bAbsolute Lymphocyte Count EDTA Whole\b\n([\d.]+)",
                #'Absolute Lymphocyte Count':r'Absolute Lymphocyte Count EDTA Whole\n([\d.]+)',
                'Lymphocytes': r"\bLymphocytes\b\n(.+)|\bLymphocytes EDTA Whole Blood\b\n([\d.]+)",
                #'Lymphocytes':r"Lymphocytes EDTA Whole Blood\n([\d.]+)",
                'Mean Platelet Volume':r"\bMPV\b\n(.+)|\bMPV EDTA Whole Blood\b\n([\d.]+)",
                #'Mean Platelet Volume':r"MPV EDTA Whole Blood\n([\d.]+)",
                #'LDL Cholesterol': r"LDL Cholesterol SERUM\n([\d.]+)",
                #'LDL/HDL Ratio': r"LDLC/HDLC Ratio SERUM\n([\d.]+)",
                #'Total Cholesterol/HDL Cholesterol Ratio':r"TC/HDLC Ratio\n(.+)",
                'Total Cholesterol/HDL Cholesterol Ratio':r"\bTC/HDL Ratio\b\n([\d.]+)|\bTC/HDLC Ratio\b\n([\d.]+)",
                #'Total Cholesterol':r"Total Cholesterol SERUM\n(.+)",
                'LDL/HDL Ratio':r"\bLDL/HDL Ratio\b\n(.+)|\bLDLC/HDLC Ratio\b\n([\d.]+)",
                'VLDL Cholesterol':r"\bVLDL Cholesterol\b\n([\d.]+)|\bVLDL\b\n([\d.]+)",
                'SGPT':r"\bSGPT/ALT\b\n([\d.]+)|\bSGPT\b\s*(?:\n.*\n)?([\d.]+)", ##Updated
                # 'W.B.C. Count':r"Leucocytes Count\n([\d.]+)", # Here before it was Leucocytes Count
                # 'R.B.C. Count':r"Erythrocytes\n([\d.]+)", # Here before it was Erythrocytes Count
                'W.B.C. Count':r"\bW\.B\.C\. Count\b\n(.+)|\bLeucocytes Count\b\n([\d.]+)",
                #'R.B.C. Count':r"\bR\.B\.C\. Count\b\n([.\d]+)|\bErythrocytes\b\n([\d.]+)", #+)" #version 1.0.0
                'R.B.C. Count':r"R\.B\.C\. Count\s*([\d,.]+)|\bErythrocytes\b\n([\d,.]+)", #version 2.0.0
                'Haemoglobin': r"\bHaemoglobin\b\n(.+)",
                'PCV':r"\bPCV\b\n(.+)|\bPacked Cell Volume\b\n([\d.]+)",
                'MCV':r"\bMCV\b\n(.+)",
                'MCH':r"\bMCH\b\n(.+)",
                'MCHC':r"\bMCHC\b\n(.+)",
                'RDW':r"\bRDW\b\n(.+)",
                'Platelet Count':r"\bPlatelet Count\b\n(.+)",
                # Mean Platelet volume was here, it was shifted upwards
                'Neutrophils':r"\bNeutrophils\b\n(.+)",
                'Absolute Neutrophil Count':r"\bAbsolute Neutrophil Count\b\n(.+)",
                #Here Lymphocytes was there,  it was shifted upwards
                #Here Absolute Lymphocytes count was therer, it was shifted upwards.
                'Monocytes':r"\bMonocytes\b\n(.+)",
                'Absolute Monocyte Count':r"\bAbsolute Monocytes Count\b\n(.+)",
                'Eosinophils':r"\bEosinophils\b\n(.+)",
                'Absolute Eosinophil Count':r"\bAbsolute Eosinophil Count\b\n(.+)",
                'Basophils':r"\bBasophils\b\n(.+)",
                'Microcytes':r"\bMicrocytes\b\n(.+)",
                'Macrocytes':r"\bMacrocytes\b\n(.+)",
                'Anisocytosis':r"\bAnisocytosis\b\n(.+)",
                'Poikilocytosis': r"\bPoikilocytosis\b\n(.+)",
                'Hypochromia':r"\bHypochromia\b\n(.+)",
                'ESR':r"\bESR\b\n(.+)",
                'T3 (Tri-iodothyronine)':r"\bT3 \(Tri-iodothyronine\)\b\n(.+)|T3 \(Tri-iodothyronine\)\n(.+)",
                'T4 (Thyroxine)':r"\bT4 \(Thyroxine\)\b\n(.+)|T4 \(Thyroxine\)\n(.+)",
                'TSH':r"\bTSH\b\n(.+)",
                'HbA1c':r"\bHbA1c\b\n(.+)",
                'Estimated Average Glucose (eAG)':r"Estimated Average Glucose \(eAG\)\s*:?[\s\n]*([\d.]+)|Estimated Average Glucose \(eAG\)\s*([\d.]+)",
                'Bicarbonate':r"\bBicarbonate\b\n([\d.]+)",
                'Volume':r"\bQuantity\b\n(.+)",
                'Colour (Urine)':r"Colour(?: \(.+\))?[\n\r]+(.+)",
                'Appearance (Urine)':r"Appearance(?: \(.+\))?[\n\r]+(.+)",
                'Deposit (Urine)':r"Deposit(?: \(.+\))?[\n\r]+(.+)",
                'pH (Urine)':r"pH(?: \(.+\))?[\n\r]+(.+)",
                'Specific Gravity':r"Specific Gravity\n(.+)",
                'Albumin':r"Albumin(?: \(.+\))?[\n\r]+(.+)",
                'Glucose (Urine)':r"Sugar(?: \(.+\))?[\n\r]+(.+)",
                'Ketones (Urine)':r"Ketone Bodies\n(.+)",
                #'Nitrite (Urine)':r"Nitrite \(Urine\)\n(.+)",
                'Nitrite (Urine)':r"Nitrite(?: \(.+\))?[\n\r]+(.+)",
                'Blood (Urine)': r"(?<!EDTA Whole )(?<! EDTA Whole )(?<!Heparin Whole )Blood\n(?<![\d.])(Positive|Negative)(?![\d.])", ## Change has been made here  !
                # 'Bile Salt (Urine)':r"Bile Salts(?: \(.+\))?[\n\r]+(.+)",
                # 'Bile Pigment (Urine)':r"Bile Pigments(?: \(.+\))?[\n\r]+(.+)",
                # 'Bile Salt (Urine)':r"Bile Salt(?: \(.+\))?[\n\r]+(.+)",
                # 'Bile Pigment (Urine)':r"Bile Pigment(?: \(.+\))?[\n\r]+(.+)",
                'Bile Salt (Urine)':r"Bile Salt(?:s)?(?: \(.+\))?[\n\r]+(.+)",
                'Bile Pigment (Urine)':r"Bile Pigment(?:s)?(?: \(.+\))?[\n\r]+(.+)",
                'Urobilinogen (Urine)':r"Urobilinogen(?: \(.+\))?[\n\r]+(.+)",
                'Leukocytes (Urine)':r"Leukocytes(?: \(.+\))?[\n\r]+(.+)",
                'Epithelial Cells (Urine)':r"Epithelial Cells(?: \(.+\))?[\n\r]+(.+)",
                'Pus Cells (Urine)':r"Pus Cells(?: \(.+\))?[\n\r]+(.+)",
                'Red Blood Cells (Urine)':r"Red Blood Cells(?: \(.+\))?[\n\r]+(.+)",
                'Casts': r"\bCasts\b\n(.+)",
                'Crystals':r"\bCrystals\b\n(.+)",
                'Amorphous Materials (Urine)': r"\bAmorphous Materials\b(?: \(.+\))?[\n\r]+(.+)",
                'Bacteria':r"\bBacteria\b\n(.+)",
                'Yeast Cells':r"\bYeast Cells\b\n(.+)",
                'Trichomonas Vaginalis':r"\bTrichomonas Vaginalis\b\n(.+)",
                'Mucus':r"Mucus(?: \(.+\))?[\n\r]+(.+)",
                'Blood Glucose Fasting': r"Blood Sugar Fasting\n([\d.]+)|Blood Glucose Fasting\n([\d.]+)",
                #"SGOT/AST Ratio":r"\bSGOT/AST\b\n([\d.]+)",
                'CPK (Total)':r"CPK \(Total\)\n([\d.]+)",
                'LDH':r"\bLDH\b\n([\d.]+)",
                'GGTP':r"\bGGTP\b\n([\d.]+)",
                'Bilirubin (Total)':r"Bilirubin \(Total\)\n([\d,.]+)", #Not added /b
                #'Bilirubin (Direct)':r"Bilirubin \(Direct\)\n([\d.]+)", #Pattern V1.0.0
                'Bilirubin (Direct)':r"Bilirubin \(Direct\)\n(?:SERUM\n)?([\d,.]+)",# Pattern V2.0.0
                'Bilirubin (Indirect)':r"Bilirubin \(Indirect\)\n([\d,.]+)",  #Not added /b
                'SGOT':r"\bSGOT\b\n(.+)|\bSGOT/AST\b\n([\d.]+)",
                #'SGPT':r"\bSGPT\b\n(.+)",
                'Alkaline Phosphatase':r"\bAlkaline Phosphatase\b\n([\d.]+)",
                #'Total Proteins':r"\bTotal Proteins\b\n([\d.]+)|([\d.]+)\s*(?:\n.*){0,2}\nTotal Proteins", #version 1.0.0
                'Total Proteins':r"Total Proteins\n([\d,.]+)|([\d.]+)\s*(?:\n.*){0,2}\nTotal Proteins", #version 2.0.0
                #'Albumin':r"Albumin\n([\d.]+)",
                #'Globulin':r"\bGlobulin\b\n([\d.]+)", #version 1.0.0
                'Globulin':r"Globulin \n([\d.]+)|([\d.]+)\s*(?:\n.*){0,2}\nGlobulin", #version 2.0.0
                'Albumin/Globulin Ratio':r"\bA/G Ratio\b\n([\d.]+)",
                'Creatinine':r"Creatinine\n([\d.]+)|([\d.]+)\s*(?:\n.*){0,2}\nCreatinine", #version 2.0.0
                #'Creatinine':r"\bCreatinine\b\n([\d,.]+)|([\d.]+)\s*(?:\n.*){0,2}\nCreatinine", #version 1.0.0
                'Blood Urea': r"\bBLOOD UREA\b\n([\d.]+)",
                'Blood Urea Nitrogen':r"\bBLOOD UREA NITROGEN\b\n([\d.]+)",
                'Uric Acid':r"\bUric Acid\b\n([\d.]+)",
                'Calcium':r"\bCalcium\b\n([\d.]+)",
                'Phosphorus':r"\bPhosphorus\b\n([\d.]+)",
                'Sodium':r"\bSodium\b\n([\d.]+)",
                'Potassium':r"\bPotassium\b\n([\d.]+)",
                'Chlorides':r"\bChlorides\b\n([\d.]+)",
                'Triglycerides':r"\bTriglycerides\b\n([\d.]+)",
                'Total Cholesterol':r"\bTotal Cholesterol\b\n([\d.]+)",
                'HDL Cholesterol':r"(?<!Non-)HDL Cholesterol\s*\n([\d.]+)",  ## Updated 
                'Non-HDL Cholesterol':r"\bNon-HDL Cholesterol\b\n([\d.]+)",
                'LDL Cholesterol':r"\b(?<!VLDL Cholesterol)\bLDL Cholesterol\n([\d.]+)", ###TANMAY OP
                #'VLDL Cholesterol':r"\bVLDL\b\n([\d.]+)",
                #'LDL/HDL Ratio':r"\bLDLC/HDLC Ratio\b\n([\d.]+)",
                #'Total Cholesterol/HDL Cholesterol Ratio':r"\bTC/HDLC Ratio\b\n([\d.]+)",
                'G6-PDH Activity':r"\bG6-PDH Activity\b\n([\d.]+)",
                'Magnesium':r"\bMagnesium\b\n\s*:?\s*([\d.]+)|Magnesium \n([\d,.]+)",
                'Absorbance':r"\bAbsorbance\b\n([\d.]+)",
                #'Packed Cell Volume':r"\bPacked Cell Volume\b\n([\d.]+)",
                'Hepatitis C':r"\bDetection of HCV antibodies from the\b\n(.+)",
                'Hepatitis B':r"\bQualitative detection of Hepatitis B\b\n(.+)"
                
            }
            updated_patterns = {'TB-Gold': [r"\bFinal Result\b\n\w+\((\d+(?:\.\d+)?)\)"],
                'Absolute Lymphocyte Count': [r"\bAbsolute Lymphocyte Count\b\n(.+)", r"\bAbsolute Lymphocyte Count EDTA Whole\b\n([\d.]+)"],
                'Lymphocytes': [r"\bLymphocytes\b\n(.+)", r"\bLymphocytes EDTA Whole Blood\b\n([\d.]+)"],
                'Mean Platelet Volume': [r"\bMPV\b\n(.+)", r"\bMPV EDTA Whole Blood\b\n([\d.]+)"],
                'Total Cholesterol/HDL Cholesterol Ratio': [r"\bTC/HDL Ratio\b\n([\d,.]+)", r"\bTC/HDLC Ratio\b\n([\d,.]+)"],
                'LDL/HDL Ratio': [r"\bLDL/HDL Ratio\b\n(.+)", r"\bLDLC/HDLC Ratio\b\n([\d.]+)"],
                'VLDL Cholesterol': [r"\bVLDL Cholesterol\b\n([\d.]+)", r"\bVLDL\b\n([\d.]+)"],
                'SGPT': [r"\bSGPT/ALT\b\n([\d.]+)", r"\bSGPT\b\s*(?:\n.*\n)?([\d.]+)",r"([\d.]+)\s*(?:\n.*){0,2}\nSGPT"],
                'W.B.C. Count': [r"\bW\.B\.C\. Count\b\n(.+)", r"\bLeucocytes Count\b\n([\d.]+)"],
                'R.B.C. Count': [r"R\.B\.C\. Count\s*([\d,.]+)", r"\bErythrocytes\b\n([\d,.]+)"],
                'Haemoglobin': [r"\bHaemoglobin\b\n(.+)"],
                'PCV': [r"\bPCV\b\n(.+)", r"\bPacked Cell Volume\b\n([\d.]+)"],
                'MCV': [r"\bMCV\b\n(.+)"],
                'MCH': [r"\bMCH\b\n(.+)"],
                'MCHC': [r"\bMCHC\b\n(.+)"],
                'RDW': [r"\bRDW\b\n(.+)"],
                'Platelet Count': [r"\bPlatelet Count\b\n(.+)"],
                'Neutrophils': [r"\bNeutrophils\b\n(.+)"],
                'Absolute Neutrophil Count': [r"\bAbsolute Neutrophil Count\b\n(.+)"],
                'Monocytes': [r"\bMonocytes\b\n(.+)"],
                'Absolute Monocyte Count': [r"\bAbsolute Monocytes Count\b\n(.+)"],
                'Eosinophils': [r"\bEosinophils\b\n(.+)"],
                'Absolute Eosinophil Count': [r"\bAbsolute Eosinophil Count\b\n(.+)"],
                'Basophils': [r"\bBasophils\b\n(.+)",r"Basophils\s*(?:.*\n)*\s*([\d.]+)"],
                'Microcytes': [r"\bMicrocytes\b\n(.+)"],
                'Macrocytes': [r"\bMacrocytes\b\n(.+)"],
                'Anisocytosis': [r"\bAnisocytosis\b\n(.+)"],
                'Poikilocytosis': [r"\bPoikilocytosis\b\n(.+)"],
                'Hypochromia': [r"\bHypochromia\b\n(.+)"],
                'ESR': [r"\bESR\b\n(.+)"],
                'T3 (Tri-iodothyronine)': [r"\bT3 \(Tri-iodothyronine\)\b\n(.+)", r"T3 \(Tri-iodothyronine\)\n(.+)"],
                'T4 (Thyroxine)': [r"\bT4 \(Thyroxine\)\b\n(.+)", r"T4 \(Thyroxine\)\n(.+)"],
                'TSH': [r"\bTSH\b\n(.+)"],
                'HbA1c': [r"\bHbA1c\b\n(.+)"],
                'Estimated Average Glucose (eAG)': [r"Estimated Average Glucose \(eAG\)\s*:?[\s\n]*([\d.]+)", r"Estimated Average Glucose \(eAG\)\s*([\d.]+)"],
                'Bicarbonate': [r"\bBicarbonate\b\n([\d.]+)"],
                'Volume': [r"\bQuantity\b\n(.+)"],
                'Colour (Urine)': [r"Colour(?: \(.+\))?[\n\r]+(.+)"],
                'Appearance (Urine)': [r"Appearance(?: \(.+\))?[\n\r]+(.+)"],
                'Deposit (Urine)': [r"Deposit(?: \(.+\))?[\n\r]+(.+)"],
                'pH (Urine)': [r"pH(?: \(.+\))?[\n\r]+(.+)"],
                'Specific Gravity': [r"Specific Gravity\n(.+)"],
                'Albumin': [r"Albumin(?: \(.+\))?[\n\r]+(.+)"],
                'Glucose (Urine)': [r"Sugar(?: \(.+\))?[\n\r]+(.+)"],
                'Ketones (Urine)': [r"Ketone Bodies\n(.+)"],
                'Nitrite (Urine)': [r"Nitrite(?: \(.+\))?[\n\r]+(.+)"],
                'Blood (Urine)': [r"(?<!EDTA Whole )(?<! EDTA Whole )(?<!Heparin Whole )Blood\n(?<![\d.])(Positive|Negative)(?![\d.])"],
                'Bile Salt (Urine)': [r"Bile Salt(?:s)?(?: \(.+\))?[\n\r]+(.+)"],
                'Bile Pigment (Urine)': [r"Bile Pigment(?:s)?(?: \(.+\))?[\n\r]+(.+)"],
                'Urobilinogen (Urine)': [r"Urobilinogen(?: \(.+\))?[\n\r]+(.+)"],
                'Leukocytes (Urine)': [r"Leukocytes(?: \(.+\))?[\n\r]+(.+)"],
                'Epithelial Cells (Urine)': [r"Epithelial Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Pus Cells (Urine)': [r"Pus Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Red Blood Cells (Urine)': [r"Red Blood Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Casts': [r"\bCasts\b\n(.+)"],
                'Crystals': [r"\bCrystals\b\n(.+)"],
                'Amorphous Materials (Urine)': [r"\bAmorphous Materials\b(?: \(.+\))?[\n\r]+(.+)"],
                'Bacteria': [r"\bBacteria\b\n(.+)"],
                'Yeast Cells': [r"\bYeast Cells\b\n(.+)"],
                'Trichomonas Vaginalis': [r"\bTrichomonas Vaginalis\b\n(.+)"],
                'Mucus': [r"Mucus(?: \(.+\))?[\n\r]+(.+)"],
                'Blood Glucose Fasting': [r"Blood Sugar Fasting\n([\d.]+)", r"Blood Glucose Fasting\n([\d.]+)"],
                'CPK (Total)': [r"CPK \(Total\)\n([\d,.]+)"],
                'LDH': [r"\bLDH\b\n([\d.]+)"],
                'GGTP': [r"\bGGTP\b\n([\d.]+)"],
                'Bilirubin (Total)': [r"Bilirubin \(Total\)\n([\d,.]+)"], #Not added /b
                'Bilirubin (Direct)': [r"(\d+(?:[.,]\d+)?)\n(Bilirubin \(Direct\))",r"Bilirubin \(Direct\)\n([\d,.]+)",r"Bilirubin \(Direct\)\n(?:SERUM\n)?([\d,.]+)"],# Pattern V2.0.0
                'Bilirubin (Indirect)': [r"Bilirubin \(Indirect\)\n([\d,.]+)"],  #Not added /b
                'SGOT': [r"\bSGOT\b\n(.+)", r"\bSGOT/AST\b\n([\d.]+)", r"([\d.]+)\s*(?:\n.*){0,2}\nSGOT"],
                'Alkaline Phosphatase': [r"\bAlkaline Phosphatase\b\n([\d.]+)"],
                'Total Proteins': [r"Total Proteins\n([\d,.]+)",r"([\d.]+)\s*(?:\n.*){0,2}\nTotal Proteins"], #version 2.0.0
                'Globulin': [r"\bGlobulin\b\n([\d,.]+)",r"Globulin \n([\d.]+)",r"([\d.]+)\s*(?:\n.*){0,2}\nGlobulin"], #version 2.0.0
                'Albumin/Globulin Ratio': [r"\bA/G Ratio\b\n([\d.]+)"],
                'Creatinine': [r"Creatinine\n([\d.]+)",r"([\d.]+)\s*(?:\n.*){0,2}\nCreatinine"], #version 2.0.0
                'Blood Urea': [r"\bBLOOD UREA\b\n([\d.]+)"],
                'Blood Urea Nitrogen': [r"\bBLOOD UREA NITROGEN\b\n([\d.]+)"],
                'Uric Acid': [r"\bUric Acid\b\n([\d,.]+)",r"\bUrio Acid\b\n([\d,.]+)"],
                'Calcium': [r"\bCalcium\b\n([\d.]+)"],
                'Phosphorus': [r"\bPhosphorus\b\n([\d.]+)"],
                'Sodium': [r"\bSodium\b\n([\d.]+)"],
                'Potassium': [r"\bPotassium\b\n([\d.]+)"],
                'Chlorides': [r"\bChlorides\b\n([\d.]+)"],
                'Triglycerides': [r"\bTriglycerides\b\n([\d.]+)"],
                'Total Cholesterol': [r"\bTotal Cholesterol\b\n([\d,.]+)"],
                'HDL Cholesterol': [r"(?<!Non-)HDL Cholesterol\s*\n([\d,.]+)"],
                'Non-HDL Cholesterol': [r"\bNon-HDL Cholesterol\b\n([\d,.]+)"],
                'LDL Cholesterol': [r"\b(?<!VLDL Cholesterol)\bLDL Cholesterol\n([\d,.]+)"],
                'G6-PDH Activity': [r"\bG6-PDH Activity\b\n([\d.]+)"],
                'Magnesium': [r"\bMagnesium\b\n\s*:?\s*([\d.]+)",r"Magnesium \n([\d,.]+)"],
                'Absorbance': [r"\bAbsorbance\b\n([\d.]+)"],
                'Hepatitis C': [r"\bDetection of HCV antibodies from the\b\n(.+)"],
                'Hepatitis B': [r"\bQualitative detection of Hepatitis B\b\n(.+)"]
                
                }
            df = pd.DataFrame(columns=["Test", "Result"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r'(?:\s*SERUM\s*|\s*FLUORIDE PLASMA\s*|:|\(URINE\))|%|Cells\/c.mm|mEq/L|mg/dl|High|serving|Plasna|servin|Plearing Places|VERUM|SERVICE|SERUN|SERIUM|SERVIM|STRUM|SERIM|SERIIN|SERIOR|SERLIM|SERIOR|Maine|UPROW|VERLIM|Phone Please|Planna|VERIMEN|NEWUM|SERIAM|SERIAN|SERIAR|SERIN|SERIAL|OCHAN|Personal|Reference Range|patient\~s|OBSERVED VALUE|UNITS|Surface Antigen \[HbsAg\] from the|\*', '', line, flags=re.IGNORECASE) for line in lines]
            lines_cleaned=[line for line in lines_cleaned if not line.startswith("Method")]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            print("+"*100)
            print(cleaned_text)
            print("+"*100)
            
            for test_description, test_patterns_list in updated_patterns.items():
                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                test_value = None
                for test_pattern in test_patterns_list:
                    #matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                    match = re.search(test_pattern, cleaned_text, re.IGNORECASE)
                    if matches:
                        #test_value = matches[0]
                        test_value = match.group(1) 
                        print(f"{test_description} : {test_value}")
                        # Create a new DataFrame with the test description and value
                        new_row = pd.DataFrame({"Test": [test_description], "Result": [test_value]})
                         # Concatenate the new row with the existing DataFrame
                        df = pd.concat([df, new_row], ignore_index=True, sort=False)
                        break
                if not test_value:
                    print(f"No match found for {test_description} in the text.")
                # matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                # print(f"{test_description} : {len(matches)}")
                # if matches:
                #     #test_value = match.group(1)
                #     if len(matches) == 1:
                #         #print("hehe")
                #         test_value = matches[0]
                #     else:
                #         #test_value = matches[0][0] or matches[0][1]
                #         test_value = next((value for value in matches[0] if value), None)
                #     print(test_value)
                #     if isinstance(test_value, tuple):
                #         test_value = test_value[0] or test_value[1]
                #     print(f"{test_description} value: {test_value}")
    
                #     # Create a new DataFrame with the test description and value
                #     new_row = pd.DataFrame({"Test": [test_description], "Result": [test_value]})

                #     # Concatenate the new row with the existing DataFrame
                #     df = pd.concat([df, new_row], ignore_index=True, sort=False)
                # else:
                #     print(f"{test_description} value not found in the text file.")
            try:
                column_index=1
                if df.iloc[:, column_index].dtype == 'object':
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('fl', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace(':', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('ML', '') 
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('/hpf', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace(',', '.')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('*', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('-', '0')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('Macrocytes', '0')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('Anisocytosis', '0')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('Poikilocytosis', '0')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('Hypochromia', '0')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('END OF REPORT', '0')
            except:
                print("Issue faced while modifying the Results column.")

            # try:
            #     existing_df = pd.read_csv(output_table_file_path)
            #     print("Existing df is:",existing_df)
            #     #print(existing_df.ndims)
            #     #existing_df = existing_df.iloc[:,0:2]
            #     #print(existing_df.ndims)
            # except:
            existing_df = pd.DataFrame()
            print("Created empty dataframe!")

            # Concatenate the existing DataFrame with the new DataFrame
            existing_df = pd.concat([existing_df, df], ignore_index=True)
            existing_df = existing_df[existing_df.notnull()]
            existing_df.to_csv(output_table_file_path, columns=["Test", "Result"], index=False)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'pharmeasy':
        try:
            pass
            # test_patterns = {
            #     'ESR':,
            #     'Sodium':,
            #     'Potassium':,
            #     'Chlorides':,
            #     'Vitamin D':,
            #     'Vitamin B-12':,
            #     'Iron':,
            #     'TIBC':,
            #     'Transferrin Saturation':,
            #     'UIBC':,
            #     'Total Cholesterol':,
            #     'HDL Cholesterol':,
            #     'HDL/LDL Ratio':,
            #     'LDL Cholesterol':,
            #     'Total Cholesterol/HDL Cholesterol Ratio':,
            #     'Triglycerides/HDL Ratio':,
            #     'Triglycerides':,
            #     'LDL/HDL Ratio':,
            #     'Non-HDL Cholesterol':,
            #     'VLDL Cholesterol':,
            #     'Alkaline Phosphatase':,
            #     'Bilirubin (Total)':,
            #     'Bilirubin (Direct)':,
            #     'Bilirubin (Indirect)':,
            #     'GGTP':,
            #     'SGOT/SGPT Ratio':,
            #     'SGOT':,
            #     'SGPT':,
            #     'Total Proteins':,
            #     'Albumin':,
            #     'Globulin':,
            #     'Albumin/Globulin Ratio':,
            #     'T3 (Tri-iodothyronine)':,
            #     'T4 (Thyroxine)':,
            #     'TSH':,
            #     'Blood Urea':,
            #     'Blood Urea Nitrogen':,
            #     'Urea/Creatinine Ratio':,
            #     'Creatinine':,
            #     'Blood Urea Nitrogen/Creatinine Ratio':,
            #     'Calcium':,
            #     'Uric Acid':,
            #     'eGFR':,
            #     'Volume':,
            #     'Colour (Urine)':,
            #     'Appearance (Urine)':,
            #     'Specific Gravity':,
            #     'pH (Urine)':,
            #     'Protein (Urine)':,
            #     'Glucose (Urine)':,
            #     'Ketones (Urine)':,
            #     'Bilirubin':,
            #     'Urobilinogen (Urine)':,
            #     'Bile Salt (Urine)':,
            #     'Bile Pigment (Urine)':,
            #     'Blood (Urine)':,
            #     'Nitrite (Urine)':,
            #     'Microalbumin':,
            #     'Mucus':,
            #     'Red Blood Cells (Urine)':,
            #     'Pus Cells (Urine)':,
            #     'Epithelial Cells (Urine)':,
            #     'Casts':,
            #     'Crystals':,
            #     'Bacteria':,
            #     'Yeast Cells':,
            #     'Parasite':,
            #     'Blood Glucose Fasting':,
            #     'HbA1c':,
            #     'Leucocytes Count':,
            #     'Neutrophils':,
            #     'Lymphocytes':,
            #     'Monocytes':,
            #     'Eosinophils':,
            #     'Basophils':,
            #     'Immature Granulocyte Percentage':,
            #     'Absolute Neutrophil Count':,
            #     'Absolute Lymphocyte Count':,
            #     'Absolute Monocyte Count':,
            #     'Absolute Basophil Count':,
            #     'Absolute Eosinophil Count':,
            #     'Immature Granulocytes':,
            #     'R.B.C. Count':,
            #     'Nucleated R.B.C.':,
            #     'Nucleated R.B.C. Percentage':,
            #     'Haemoglobin':,
            #     'PCV':,
            #     'MCV':,
            #     'MCH':,
            #     'MCHC':,
            #     'RDW-SD':,
            #     'RDW-CV':,
            #     'PDW':,
            #     'Mean Platelet Volume':,
            #     'Platelet Count':,
            #     'PLCR':,
            #     'PCT':,
            #     'Lipoprotein':,
            #     'HS-CRP':,
            #     'APOLIPOPROTEIN - A1':,
            #     'APOLIPOPROTEIN - B':,
            #     '(APO B/A1)':,
            #}
            updated_patterns = {
                'eGFR' : [r"EST. GLOMERULAR FILTN RATE \(eGFR\)\n([\d,.]+)",r"EST. GLOMERULAR FILTN RATE \(eGFR\n([\d,.]+)",r"EST GLOMERULAR FILTN RATE \(eGFR\)\n([\d,.]+)",r"EST, GLOMERULAR FILTN RATE \(eGFR\)\n([\d,.]+)"],
                'Blood Urea Nitrogen':[r"BLOOD UREA NITROGEN \(BUN\)\n(.+)"],
                'Calcium': [r"CALCIUM\n(.+)"],
                'Average Blood Glucose':[r"AVERAGE BLOOD GLUCOSE \(ABG\)\n(.+)"],
                #'Vitamin D':r"25-OH VITAMIN D \(TOTAL\)\n(.+)",
                'Albumin' : [r"ALBUMIN SERUM\n([\d,.]+)"],
                'Uric Acid' : [r"Uric Acid\n([\d,.]+)"],
                "Blood Urea" : [r"UREA \(CALCULATED\)\n([\d,.]+)"],
                "Urea/Creatinine Ratio" : [r"UREA \/ SR.CREATININE RATIO\n([\d,.]+)"],
                "Creatinine" : [r"CREATININE - SERUM\n([\d,.]+)"],
                'Blood Urea Nitrogen/Creatinine Ratio' : [r"BUN \/ SR.CREATININE RATIO\n([\d,.]+)"],
                'T3 (Tri-iodothyronine)':[r"TOTAL TRIIODOTHYRONINE \(T3\)\n([\d.]+)"],
                'T4 (Thyroxine)':[r"TOTAL THYROXINE \(T4\)\n([\d.]+)"],
                'TSH' : [r"TSH - ULTRASENSITIVE\n([\d.]+)"],
                'Volume':[r"VOLUME\n([\d.]+)"],
                'Colour (Urine)':[r"COLOUR\n(.+)"],
                'Appearance (Urine)':[r"APPEARANCE\n(.+)"],
                'Specific Gravity':[r"SPECIFIC GRAVITY\n([\d.]+)"],
                'pH (Urine)':[r"PH\n([\d.]+)"],
                'Protein (Urine)':[r"URINARY PROTEIN\n(.+)"],
                'Glucose (Urine)':[r"URINARY GLUCOSE\n(.+)"],
                'Ketones (Urine)':[r"URINE KETONE\n(.+)"],
                'Bilirubin (Urine)':[r"URINARY BILIRUBIN\n(.+)"],
                'Urobilinogen (Urine)':[r"UROBILINOGEN\n(.+)"],
                'Bile Salt (Urine)':[r"BILE SALT\n(.+)"],
                'Bile Pigment (Urine)':[r"BILE PIGMENT\n(.+)"],
                'Blood (Urine)':[r"URINE BLOOD\n(.+)"],
                'Nitrite (Urine)':[r'(.+)(?=\nNITRITE)',r"NITRITE\n(.+)"],
                'Microalbumin':[r"MICROALBUMIN\n([\d,.]+)"],
                'Mucus':[ r"MUCUS\n(.+)",r'(.+)(?=\nMUCUS)'],
                'Red Blood Cells (Urine)':[r"(?<!NUCLEATED )RED BLOOD CELLS\b\n(.+)(?!( %))"],
                'Pus Cells (Urine)':[r"URINARY LEUCOCYTES \(PUS CELLS\)\n(.+)"],
                'Epithelial Cells (Urine)':[r"EPITHELIAL CELLS\n(.+)"],
                'Casts':[r"CASTS\n(.+)"],
                'Crystals':[r"CRYSTALS\n(.+)"],
                'Bacteria':[r"BACTERIA\n(.+)"],
                'Yeast Cells':[r"YEAST\n(.+)"],
                'Parasite':[ r'(.+)(?=\nPARASITE)',r"PARASITE\n(.+)"],
                'Alkaline Phosphatase':[r"ALKALINE PHOSPHATASE\n([\d,.]+)"],
                'Bilirubin (Total)':[r"BILIRUBIN TOTAL\n([\d,.]+)",r"BILIRUBIN -TOTAL\n([\d,.]+)",r"BILIRUBIN - TOTAL\n([\d,.]+)"],
                'Bilirubin (Direct)':[r"BILIRUBIN -DIRECT\n([\d,.]+)",r"BILIRUBIN - DIRECT\n([\d,.]+)",r"BILIRUBIN DIRECT\n([\d,.]+)"],
                'Bilirubin (Indirect)':[r"BILIRUBIN \(INDIRECT\)\n([\d,.]+)"],
                'GGTP':[r"GAMMA GLUTAMYL TRANSFERASE \(GGT\)\n([\d,.]+)",r"GAMMA GLUTAMYL TRANSFERASE (GGT)"],
                'SGOT/SGPT Ratio':[r"SGOT \/ SGPT RATIO\n([\d,.]+)",r"SGOT \/ SGPT\n([\d,.]+)",r"SGOT\/SGPT\n([\d,.]+)"],
                'SGOT':[r"ASPARTATE AMINOTRANSFERASE \(SGOT \)\n([\d,.]+)",r"ASPARTATE AMINOTRANSFERASE \(SGOT\)\n([\d,.]+)"],
                'SGPT':[r"ALANINE TRANSAMINASE \(SGPT\)\n([\d,.]+)"],
                'Total Proteins':[r"PROTEIN TOTAL\n([\d,.]+)",r"PROTEIN - TOTAL\n([\d,.]+)",r"PROTEIN -TOTAL\n([\d,.]+)"],
                'Albumin':[r"ALBUMIN SERUM\n([\d,.]+)",r"ALBUMIN \n([\d,.]+)",r"ALBUMIN - SERUM\n([\d,.]+)",r"ALBUMIN -SERUM\n([\d,.]+)"],
                'Globulin':[r"SERUM GLOBULIN\n([\d,.]+)",r"GLOBULIN \n([\d,.]+)",r"GLOBULIN\n([\d,.]+)"],
                'Albumin/Globulin Ratio':[r"SERUM ALB\/GLOBULIN RATIO\n([\d,.]+)",r"SERUM ALB\/GLOBULIN\n(.+)",r"ALB\/GLOBULIN\n(.+)"],
                'Vitamin D' : [r"25OH VITAMIN D \(TOTAL\)\n([\d,.]+)",r"25-OH VITAMIN D \(TOTAL\)\n([\d,.]+)",r"25 OH VITAMIN D \(TOTAL\)\n([\d,.]+)"],
                'Vitamin B-12':[r"VITAMIN B-12\n([\d,.]+)",r"VITAMIN B12\n([\d,.]+)"],
                "Blood Glucose Fasting" : [r"FASTING BLOOD SUGAR\(GLUCOSE\)\n([\d,.]+)"],
                'W.B.C. Count' : [r"TOTAL LEUCOCYTES COUNT \(WBC\)\n([\d,.]+)",r"TOTAL LEUCOCYTES COUNT\(WBC\)\n([\d,.]+),",r"TOTAL LEUCOCYTES COUNT \(WBC\n([\d,.]+)"],
                'Neutrophils':[r"NEUTROPHILS\n([\d,.]+)"],
                'Lymphocytes':[r"LYMPHOCYTE PERCENTAGE\n([\d,.]+)"],
                'Monocytes':[r"MONOCYTES\n([\d,.]+)"],
                'Eosinophils':[r"EOSINOPHILS\n([\d,.]+)"],
                'Basophils':[r"BASOPHILS\n([\d,.]+)"],
                # 'Immature Granulocyte Percentage':[r"\bIMMATURE GRANULOCYTE PERCENTAGE\(IG\%\)\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE \(IG\%\)\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE \(IG\%\b\n([\d,.]+)"],
                'Absolute Neutrophil Count':[r"NEUTROPHILS ABSOLUTE COUNT\n([\d,.]+)",r"NEUTROPHILS  ABSOLUTE COUNT\n([\d,.]+)",r"NEUTROPHILS - ABSOLUTE COUNT\n([\d,.]+)"],
                'Absolute Lymphocyte Count':[r"LYMPHOCYTES ABSOLUTE COUNT\n([\d,.]+)",r"LYMPHOCYTES  ABSOLUTE COUNT\n([\d,.]+)",r"LYMPHOCYTES - ABSOLUTE COUNT\n([\d,.]+)"],
                'Absolute Monocyte Count':[r"MONOCYTES ABSOLUTE COUNT\n([\d,.]+)",r"MONOCYTES - ABSOLUTE COUNT\n([\d,.]+)"],
                'Absolute Basophil Count':[r"BASOPHILS ABSOLUTE COUNT\n([\d,.]+)",r"BASOPHILS  ABSOLUTE COUNT\n([\d,.]+)",r"BASOPHILS - ABSOLUTE COUNT\n([\d,.]+)"],
                'Absolute Eosinophil Count':[r"EOSINOPHILS ABSOLUTE COUNT\n([\d,.]+)",r"EOSINOPHILS  ABSOLUTE COUNT\n([\d,.]+)", r"EOSINOPHILS - ABSOLUTE COUNT\n([\d,.]+)"],

                'Immature Granulocyte Percentage':[r"\bIMMATURE GRANULOCYTE PERCENTAGE\(IG\%\)\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE \(IG\%\)\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE \(IG\%\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE \(IG%\)\b\n([\d,.]+)",r"\bIMMATURE GRANULOCYTE PERCENTAGE\(IG%\b\n([\d,.]+)",r"IMMATURE GRANULOCYTE PERCENTAGE\(IG%\n(.+)",r"IMMATURE GRANULOCYTE PERCENTAGE\(IG\%\)\n([\d,.]+)"],

                'Immature Granulocytes':[r"IMMATURE GRANULOCYTES\(IG\)\n([\d.]+)",r"IMMATURE GRANULOCYTES\(IG\n([\d.]+)",r"IMMATURE GRANULOCYTES \(IG\)\n([\d.]+)"],
                'R.B.C. Count':[r"TOTAL RBC \n([\d.]+)",r"TOTAL RBC\n([\d.]+)"],
                'Nucleated R.B.C.':[r"NUCLEATED RED BLOOD CELLS\n(.+)"],
                'Nucleated R.B.C. Percentage':[r"NUCLEATED RED BLOOD CELLS \%\n(.+)",r"NUCLEATED RED BLOOD CELLS %\n(.+)"],
                'Haemoglobin':[r"HEMOGLOBIN\n([\d.]+)"],
                'PCV':[r"HEMATOCRIT\(PCV\)\n([\d.]+)",r"HEMATOCRIT\(PCV\n([\d.]+)"],
                'MCV':[r"MEAN CORPUSCULAR VOLUME\(MCV\)\n([\d.]+)"],
                'MCH' : [r"MEAN CORPUSCULAR HEMOGLOBIN\(MCH\n([\d,.]+)",r"MEAN CORPUSCULAR HEMOGLOBIN\(MCH\)\n([\d,.]+)"],
                'MCHC' : [r"MEAN CORP.HEMO.CONC\(MCHC\n([\d,.]+)",r"MEAN CORP.HEMO.CONC\(MCHC\)\n([\d,.]+)"],
                'RDW-SD':[r"RED CELL DISTRIBUTION WIDTH SD\(RDW\-SD\)\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH SD\(RDW\-SD\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH SD\(RDW SD\)\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH SD\(RDWSD\)\n([\d,.]+)"],
                'RDW-CV':[r"RED CELL DISTRIBUTION WIDTH \(RDW\-CV\)\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH \(RDW\-CV\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH \(RDW CV\)\n([\d,.]+)",r"RED CELL DISTRIBUTION WIDTH \(RDWCV\)\n([\d,.]+)"],
                'PDW':[r"PLATELET DISTRIBUTION WIDTH\(PDW\)\n([\d,.]+)"],
                'Mean Platelet Volume':[r"MEAN PLATELET VOLUME\(MPV\)\n([\d,.]+)"],
                'Platelet Count':[r"PLATELET COUNT\n([\d,.]+)"],
                'PLCR':[r"PLATELET TO LARGE CELL \(PLCR\)\n([\d,.]+)",r"PLATELET TO LARGE CELL \(PLCR\n([\d,.]+)"],
                'PCT':[r"PLATELETCRIT\(PCT\)\n([\d,.]+)",r"PLATELETCRIT\(PCT\n([\d,.]+)"],
                'Lipoprotein':[r"Lipoprotein \(a\) \[Lp\(a\)\]\n([\d,.]+)",r"Lipoprotein\(a\) \[Lp\(a\)\]\n([\d,.]+)",r"Lipoprotein \(a\)\[Lp\(a\)\]\n([\d,.]+)",r"Lipoprotein \(a\) \[Lp\(a\)\n([\d,.]+)"],
                'HS-CRP':[r"HIGH SENSITIVITY CREACTIVE PROTEIN \(HSCRP\)\n([\d,.]+)",r"HIGH SENSITIVITY CREACTIVE PROTEIN \(HSCRP\n([\d,.]+)",r"HIGH SENSITIVITY C REACTIVE PROTEIN \(HSCRP\)\n([\d,.]+)",r"HIGH SENSITIVITY C REACTIVE PROTEIN \(HSCRP\n([\d,.]+)",r"HIGH SENSITIVITY C-REACTIVE PROTEIN \(HS-CRP\)\n([\d,.]+)",r"HIGH SENSITIVITY C-REACTIVE PROTEIN \(HS CRP\n([\d,.]+)"],
                'APOLIPOPROTEIN - A1':[r"APOLIPOPROTEIN  A1 \(APOA1\)\n([\d,.]+)",r"APOLIPOPROTEIN  A1 \(APOA1\n([\d,.]+)",r"APOLIPOPROTEIN - A1 \(APOA1\)\n([\d,.]+)",r"APOLIPOPROTEIN - A1 \(APO-A1\)\n([\d,.]+)",r"APOLIPOPROTEIN  A1 \(APO-A1\)\n([\d,.]+)",r"APOLIPOPROTEIN  A1 \(APO-A1\n([\d,.]+)"],
                'APOLIPOPROTEIN - B':[r"APOLIPOPROTEIN - B \(APO-B\)\n([\d,.]+)",r"APOLIPOPROTEIN - B \(APO-B\)\n([\d,.]+)",r"APOLIPOPROTEIN  B \(APO-B\)\n([\d,.]+)",r"APOLIPOPROTEIN  B \(APOB\)\n([\d,.]+)",r"APOLIPOPROTEIN  B \(APOB\n([\d,.]+)",r"APOLIPOPROTEIN B \(APOB\)\n([\d,.]+)"],
                'APO B/A1':[r"APO B \/ APO A1  \(APO B\/A1\)\n([\d,.]+)",r"APO B \/ APO A1  \(APOB\/A1\)\n([\d,.]+)",r"APO B \/ APO A1  \(APO B\/A1\)\n([\d,.]+)",r"APO B \/ APO A1  \(APOBA1\)\n([\d,.]+)",r"APO A1 RATIO \(APO B\/A1\)\n([\d,.]+)",r"APO A1 RATIO \(APO B\/A1\n([\d,.]+)"],
                'ESR' : [r"ERYTHROCYTE SEDIMENTATION RATE \(ESR\)\n([\d,.]+)",r"ERYTHROCYTE SEDIMENTATION RATE \(ESR\n([\d,.]+)",r"ERYTHROCYTE SEDIMENTATION RATE\n([\d,.]+)",r"ERYTHROCYTE SEDIMENTATION RATE\(ESR\)\n([\d,.]+)",r"ERYTHROCYTE SEDIMENTATION RATE \(ESR\)\n([\d,.]+)"]
            }
            df = pd.DataFrame(columns=["TEST NAME ", "VALUE "])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED|TECHNOLOGY|UNITS|NORMAL RANGE|mg/dL|Adult|Ratio|ml|CALCULATED|U\/I|<\s*\d+|>\s*\d+|\d+-\d+(\.\d+)?|SERUM |U\/L|Reference Range|VALUE|mg/l|\-|\b\d+(\.\d+)?\s?(\*?10(\^|\*\*)\d+)?\s?\/\s?\w+\b|X|IMMUNOTURBIDIMETRY", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            print("*"*30)
            print("Cleaned lines:",cleaned_text)
            for test_description, test_patterns_list in updated_patterns.items():

                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                test_value = None
                for test_pattern in test_patterns_list:
                    #matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                    match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                    if match:
                        #test_value = matches[0]
                        test_value = match.group(1)
                        print(f"{test_description} : {test_value}")
                        # Create a new DataFrame with the test description and value
                        new_row = pd.DataFrame({"TEST NAME ": [test_description], "VALUE ": [test_value]})
                         # Concatenate the new row with the existing DataFrame
                        df = pd.concat([df, new_row], ignore_index=True, sort=False)
                        break
                if not test_value:
                    print(f"No match found for {test_description} in the text.")

            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                print(existing_df)
                new_columns = ["TEST NAME ","VALUE "]
                existing_df.columns = new_columns
                print(existing_df)
                #existing_df.columns = ["TEST NAME ","VALUE "]
                #print(existing_df.ndims)
                #existing_df = existing_df.iloc[:,0:2]
                #print(existing_df.ndims)
            except:
                existing_df = pd.DataFrame()
                print("Created empty dataframe!")
            
            try:
                column_index=1
                if df.iloc[:, column_index].dtype == 'object':
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('Nil', '0')
            except:
                print("Issue faced while modifying the ['VALUE '] column.")
            if df.empty:
                print("Current pharmeasy columns are: ",existing_df.columns)
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.notnull()]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["TEST NAME ", "VALUE "], index=False)
            else:
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df[existing_df.notnull()]
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["TEST NAME ", "VALUE "], index=False)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'tata 1mg':
        try:
            updated_patterns = {
               
                'Mean Platelet Volume': [r"\bMPV\b\n([\d,.]+)"], #Done
                'Total Cholesterol/HDL Cholesterol Ratio': [r"\bCholesterol:HDL Cholesterol\b\n([\d,.]+)", r"\bCholesterol : HDL Cholesterol\b\n([\d,.]+)",r"\bCholesterol HDL Cholesterol\b\n([\d,.]+)",r"\bCholesterol  HDL Cholesterol\b\n([\d,.]+)"], #Done
                'LDL/HDL Ratio': [r"\bLDL\:HDL Cholesterol\b\n([\d,.]+)",r"\bLDL HDL Cholesterol\b\n([\d,.]+)",r"\bLDL\: HDL Cholesterol\b\n([\d,.]+)",r"LDL \: HDL Cholesterol\n([\d,.]+)"],
                'VLDL Cholesterol': [r"\bCholesterol VLDL\b\n([\d,.]+)",r"\bCholesterol- VLDL\b\n([\d,.]+)",r"\bCholesterol - VLDL\b\n([\d,.]+)",r"\bCholesterol -VLDL\b\n([\d,.]+)"], #Done
                
                'W.B.C. Count': [r"\bTotal Leucocyte Count\b\n([\d.]+)"], #DOne
                'R.B.C. Count': [r"\bRBC\b\n([\d,.]+)"],#Done
                'Haemoglobin': [r"\bHemoglobin\b\n([\d,.]+)"],#Done
                'PCV': [r"HCT\n([\d.]+)"], #Done
                'MCV': [r"\bMCV\b\n([\d,.]+)"], #Done
                'MCH': [r"\bMCH\b\n([\d,.]+)"], #Done
                'MCHC': [r"MCHC\n([\d.]+)"], #Done
                'RDW-CV': [r"\bRDW-CV\b\n([\d.]+)"],#Done
                'Platelet Count': [r"\bPlatelet Count\b\n([\d.]+)"],
                'Neutrophils': [r"\bNeutrophils\b\n(.+)"], #Done
                'Absolute Neutrophil Count': [r"\bAbsolute Neutrophil Count\b\n(.+)"],#Done
                'Absolute Lymphocyte Count': [r"\bAbsolute Lymphocyte Count\b\n([\d,.]+)"],#Done
                'Monocytes': [r"\bMonocytes\b\n(.+)"],#Done
                'Absolute Monocyte Count': [r"\bAbsolute Monocyte Count\b\n([\d,.]+)"], #Done
                'Eosinophils': [r"\bEosinophils\b\n([\d,.]+)"],
                'Absolute Eosinophil Count': [r"\bAbsolute Eosinophil Count\b\n([\d,.]+)"],  #Done
                'Absolute Basophil Count' : [r"\bAbsolute Basophil Count\b\n([\d,.]+)"], #Done
                'Basophils': [r"\bBasophils\b\n([\d.]+)"],
                'Lymphocytes': [r"\bLymphocytes\b\n(.+)"],
                'Microcytes': [r"\bMicrocytes\b\n(.+)"],
                'Macrocytes': [r"\bMacrocytes\b\n(.+)"],
                'Anisocytosis': [r"\bAnisocytosis\b\n(.+)"],
                'Poikilocytosis': [r"\bPoikilocytosis\b\n(.+)"],
                'Hypochromia': [r"\bHypochromia\b\n(.+)"],
                'ESR': [r"\bESR\b\n(.+)"],
                'T3 (Tri-iodothyronine)': [r"T3\, Total\n([\d,.]+)",r"T3 Total\n([\d,.]+)",r"T3  Total\n([\d,.]+)"], #Done
                'T4 (Thyroxine)': [r"T4\, Total\n([\d,.]+)",r"T4 Total\n([\d,.]+)",r"T4 Total\n([\d,.]+)"], #Done
                'TSH': [r"Thyroid Stimulating Hormone - Ultra\n([\d,.]+)",r"Thyroid Stimulating Hormone Ultra\n([\d,.]+)",r"Thyroid Stimulating Hormone  Ultra\n([\d,.]+)",r"Thyroid Stimulating Hormone \- Ultra Sensitive\n([\d,.]+)",r"Thyroid Stimulating Hormone  Ultra Sensitive\n([\d,.]+)",r"Thyroid Stimulating Hormone \-Ultra Sensitive\n([\d,.]+)"], #Done
                "HbA1c":[r"Glycosylated Hemoglobin \(HbA1c\)\n([\d.]+)",r"Glycosylated Hemoglobin \(HbAlc\)\n([\d.]+)"], #Done
                'Estimated Average Glucose (eAG)': [r"Estimated Average Glucose \(eAG\)\n([\,d.]+)"], #Done
                'Bicarbonate': [r"\bBicarbonate\b\n([\d.]+)"],
                'Volume': [r"\bQuantity\b\n(.+)"],
                'Colour (Urine)': [r"Colour(?: \(.+\))?[\n\r]+(.+)"],
                'Appearance (Urine)': [r"Appearance(?: \(.+\))?[\n\r]+(.+)"],
                'Deposit (Urine)': [r"Deposit(?: \(.+\))?[\n\r]+(.+)"],
                'pH (Urine)': [r"pH(?: \(.+\))?[\n\r]+(.+)"],
                'Specific Gravity': [r"Specific Gravity\n(.+)"],
                'Glucose (Urine)': [r"Sugar(?: \(.+\))?[\n\r]+(.+)"],
                'Ketones (Urine)': [r"Ketone Bodies\n(.+)"],
                'Nitrite (Urine)': [r"Nitrite(?: \(.+\))?[\n\r]+(.+)"],
                'Blood (Urine)': [r"(?<!EDTA Whole )(?<! EDTA Whole )(?<!Heparin Whole )Blood\n(?<![\d.])(Positive|Negative)(?![\d.])"],
                'Bile Salt (Urine)': [r"Bile Salt(?:s)?(?: \(.+\))?[\n\r]+(.+)"],
                'Bile Pigment (Urine)': [r"Bile Pigment(?:s)?(?: \(.+\))?[\n\r]+(.+)"],
                'Urobilinogen (Urine)': [r"Urobilinogen(?: \(.+\))?[\n\r]+(.+)"],
                'Leukocytes (Urine)': [r"Leukocytes(?: \(.+\))?[\n\r]+(.+)"],
                'Epithelial Cells (Urine)': [r"Epithelial Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Pus Cells (Urine)': [r"Pus Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Red Blood Cells (Urine)': [r"Red Blood Cells(?: \(.+\))?[\n\r]+(.+)"],
                'Casts': [r"\bCasts\b\n(.+)"],
                'Crystals': [r"\bCrystals\b\n(.+)"],
                'Amorphous Materials (Urine)': [r"\bAmorphous Materials\b(?: \(.+\))?[\n\r]+(.+)"],
                'Bacteria': [r"\bBacteria\b\n(.+)"],
                'Yeast Cells': [r"\bYeast Cells\b\n(.+)"],
                'Trichomonas Vaginalis': [r"\bTrichomonas Vaginalis\b\n(.+)"],
                'Mucus': [r"Mucus(?: \(.+\))?[\n\r]+(.+)"],
                "Blood Glucose Fasting":[r"Glucose - Fasting\n([\d,.]+)",r"Glucose -Fasting\n([\d,.]+)",r"Glucose  Fasting\n([\d,.]+)"], #Done
                'CPK (Total)': [r"CPK \(Total\)\n([\d,.]+)"],
                'LDH': [r"\bLDH\b\n([\d.]+)"],
                'GGTP': [r"Gamma Glutamyltransferase \(GGT\)\n([\d,.]+)",r"Gamma Glutamyltransferase \(GGT\n([\d,.]+)"], #Don
                'Bilirubin (Total)': [r"Bilirubin-Total\n([\d,.]+)",r"Bilirubin Total\n([\d,.]+)",r"Bilirubin- Total\n([\d,.]+)",r"Bilirubin -Total\n([\d,.]+)"], #Done
                'Bilirubin (Direct)': [r"Bilirubin-Direct\n([\d,.]+)",r"Bilirubin Direct\n([\d,.]+)",r"Bilirubin- Direct\n([\d,.]+)",r"Bilirubin -Direct\n([\d,.]+)"],#Done
                'Bilirubin (Indirect)': [r"Bilirubin-Indirect\n([\d,.]+)",r"Bilirubin Indirect\n([\d,.]+)",r"Bilirubin- Indirect\n([\d,.]+)",r"Bilirubin -Indirect\n([\d,.]+)"],  #Done
                'SGOT': [r"Aspartate Transaminase \(SGOT\)\n([\d.]+)",r"Aspartate Transaminase \(SGOT\n([\d.]+)",r"Aspartate Transaminase\(SGOT\)\n([\d.]+)",r"Aspartate Transaminase\(SGOT\n([\d.]+)"], #Done
                'SGPT': [r"Alanine Transaminase \(SGPT\)\n([\d,.]+)", r"Alanine Transaminase \(SGPT\n([\d,.]+)",r"Alanine Transaminase\(SGPT\)\n([\d,.]+)"], #Done
                'SGOT/SGPT Ratio' : [r"SGOT\/SGPT\n([\d.]+)"],#Done
                'Alkaline Phosphatase': [r"\bAlkaline Phosphatase\b\n([\d,.]+)"],#Done
                'Total Proteins': [r"Protein\, Total\n([\d,.]+)",r"Protein Total\n([\d,.]+)"], #Done
                'Albumin':[r"Albumin\n([\d,.]+)"], #Done
                'Globulin': [r"\bGlobulin\b\n([\d,.]+)",r"Globulin \n([\d.]+)"], #Done
                'Albumin/Globulin Ratio': [r"\bA/G Ratio\b\n([\d.]+)",r"\bA\/G Ratio\b\n([\d.]+)"], #Done
                'Creatinine': [r"Creatinine\n([\d,.]+)"], #Done
                "Blood Urea":[r"Urea\n([\d,.]+)"],#Done
                'Blood Urea Nitrogen': [r'Blood Urea Nitrogen\n([\d,.]+)'],#Done
                'Blood Urea Nitrogen/Creatinine Ratio' : [r"BUN\/Creatinine Ratio\n([\d,.]+)"], #Done
                'Uric Acid': [r"Uric Acid\n([\d,.]+)"], #Done
                'Calcium': [r"\bCalcium\b\n([\d.]+)"],
                'Phosphorus': [r"\bPhosphorus\b\n([\d.]+)"],
                'Sodium': [r"\bSodium\b\n([\d,.]+)"], #Done
                'Potassium': [r"\bPotassium\b\n([\d,.]+)"], #Done
                'Chlorides': [r"\bChloride\b\n([\d,.]+)",r"Chloride\n([\d,.]+)"],#Done
                'Triglycerides': [r"\bTriglycerides\b\n([\d,.]+)"], #Done
                'Total Cholesterol': [r"\bCholesterol -Total\b\n([\d,.]+)",r"\bCholesterol - Total\b\n([\d,.]+)",r"\bCholesterol-Total\b\n([\d,.]+)",r"\bCholesterol Total\b\n([\d,.]+)",r"\bCholesterol  Total\b\n([\d,.]+)"], #Done
                'HDL Cholesterol': [r"(?<!Non-)Cholesterol-HDL\n([\d,.]+)",r"(?<!Non-)Cholesterol - HDL\n([\d,.]+)",r"(?<!Non-)Cholesterol HDL\n([\d,.]+)"], #Done
                'Non-HDL Cholesterol': [r"\bNon HDL Cholesterol\b\n([\d,.]+)"], #Done
                'LDL Cholesterol': [r"\b(?<!VLDL Cholesterol)\bCholesterol-LDL\n([\d,.]+)",r"\b(?<!VLDL Cholesterol)\bCholesterol - LDL\n([\d,.]+)",r"\b(?<!VLDL Cholesterol)\bCholesterol LDL\n([\d,.]+)"],#Done
                'G6-PDH Activity': [r"\bG6-PDH Activity\b\n([\d.]+)"],
                'Magnesium': [r"\bMagnesium\b\n\s*:?\s*([\d.]+)",r"Magnesium \n([\d,.]+)"],
                'Absorbance': [r"\bAbsorbance\b\n([\d,.]+)"],
                'PDW' : [r"PDW\n([\d,.]+)"]
            }
            df = pd.DataFrame(columns=["Test Name", "Result"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED|mg\/dl|ng\/ml", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            # for test_description, test_pattern in test_patterns.items():
            #     match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
            #     if match:
            #         test_value = match.group(1)
            #         test_value = test_value
            #         print(f"{test_description} value: {test_value}")
            #         # Create a new DataFrame with the test description and value
            #         new_row = pd.DataFrame({"Test Name": [test_description], "Result": [test_value]})

            #         # Concatenate the new row with the existing DataFrame
            #         df = pd.concat([df, new_row], ignore_index=True, sort=False)
            #     else:
            #         print(f"{test_description} value not found in the text file.")
            for test_description, test_patterns_list in updated_patterns.items():

                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                test_value = None
                for test_pattern in test_patterns_list:
                    #matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                    match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                    if match:
                        #test_value = matches[0]
                        test_value = match.group(1)
                        print(f"{test_description} : {test_value}")
                        # Create a new DataFrame with the test description and value
                        new_row = pd.DataFrame({"Test Name": [test_description], "Result": [test_value]})
                         # Concatenate the new row with the existing DataFrame
                        df = pd.concat([df, new_row], ignore_index=True, sort=False)
                        break
                if not test_value:
                    print(f"No match found for {test_description} in the text.")

            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                existing_df = existing_df.rename(columns=lambda x: x.strip()) #Removing trailing spaces
                print(existing_df.columns)
            except:
                existing_df = pd.DataFrame(columns=["Test Name", "Result"])
                print("Created empty dataframe!")
            if df.empty:
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.notnull()]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["Test Name", "Result"], index=False)
            else:
                # Concatenate the existing DataFrame with the new DataFrame
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df[existing_df.notnull()]
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["Test Name", "Result"], index=False)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'metropolis':
        try:
            updated_patterns = {
                "Uric Acid":[r"Uric Acid\n([\d.]+)"],
                'T3 (Tri-iodothyronine)':[r"Free T3\n([\d.]+)"],
                'T4 (Thyroxine)':[r"Free T4\n([\d.]+)"],
                'Vitamin D' : [r"25 Hydroxy \(OH\) Vit D\n([\d,.]+)"],
                'Vitamin B-12' : [r"Vitamin B12 level\n([\d,.]+)"],
                'Albumin/Globulin Ratio' :[r"A\/G Ratio\n([\d,.]+)",r"([\d.]+)\s+A/G Ratio"],
                'Albumin':[r"Albumin\n([\d,.]+)"],
                'Globulin' : [r"Globulin\n([\d,.]+)"],
                'Total Protein' : [r'Total Protein\n([\d,.]+)'],
                'Alkaline Phosphatase' : [r"(\d+)\s+Alkaline Phosphatase",r"Alkaline Phosphatase\n([\d,.]+)"],
                'SGPT' : [r"SGPT \(ALT\)\n([\d,.]+)",r"(\d+)[\s\S]*?SGPT \(ALT\)"],
                'SGOT' : [r"SGOT \(AST\)\n([\d,.]+)",r"(\d+)[\s\S]*?SGOT \(AST\)"],
                'Blood Glucose Fasting' :[r"Glucose fasting[\s\S]*?([\d.]+)",r"Glucose fasting\n([\d,.]+)",r"Glucose fasting\s*([\d,.]+)"], #Done che
                'Blood Urea Nitrogen' :[r"BUN-Blood Urea Nitrogen\n([\d,.]+)"],
                'Creatinine' : [r"Creatinine\n([\d,.]+)"],
                'Total Cholesterol' : [r"Cholesterol-Total\n([\d,.]+)"],
                'Triglycerides':[r"Triglycerides level\n([\d,.]+)"],
                'Potassium':[r"Potassium\n([\d,.]+)"],
                'Chlorides' : [r"Chlorides\n([\d,.]+)"],
                'LDL Cholesterol' :[r"LDL Cholesterol\n([\d,.]+)"],
                'LDL/HDL Ratio' : [r"LDL\/HDL RATIO\n([\d,.]+)"],
                'Total Cholesterol/HDL Cholesterol Ratio':[r"CHOL\/HDL RATIO\n([\d,.]+)"],
                'VLDL Cholesterol':[r"VLDL Cholesterol\n([\d,.]+)"],
                'Calcium': [r"\bCalcium\b\n([\d,.]+)"],
                'Phosphorous': [r"\bPhosphorous\b\n([\d,.]+)"],
                'Bilirubin (Direct)':[r"Bilirubin-Direct\n([\d,.]+)"],# Pattern V2.0.0
                'Bilirubin (Indirect)':[ r"(\d+)\s+Bilirubin-Indirect",r"Bilirubin-Indirect\n([\d,.]+)",r"(\d+)\s+Bilirubin- Indirect", r"Bilirubin- Indirect\n([\d,.]+)"],  #Not added /b
                'Bilirubin (Total)':[r"Bilirubin-Total\n([\d,.]+)", r"(\d+)\s+Bilirubin-Total"],
                #'Bilirubin (Urine)' :[r'Bilirubin\s*([\w\s-]+)'], Commneted as of now
                'ESR' : [r"ESR Erythrocyte Sedimentation\n([\d,.]+)",r"ESR - Erythrocyte Sedimentation\n([\d,.]+)",r"ESR Erythrocyte Sedimentation Rate\n([\d,.]+)",r"Rate\n([\d,.]+)"],
                'Phosphorous' : [r"Phosphorous\n([\d,.]+)"],
                'W.B.C. Count': [r"\bTotal Leucocytes \(WBC\) Count\b\n([\d,.]+)",r"\bTotal Leucocytes \(WBC Count\b\n([\d,.]+)",r"\bTotal Leucocytes\(WBC\) Count\b\n([\d,.]+)"], #DOne Che
                'R.B.C. Count': [r"\bErythrocyte \(RBC\) Count\b\n([\d,.]+)",r"\bErythrocyte \(RBC Count\b\n([\d,.]+)",r"\bErythrocyte\(RBC\) Count\b\n([\d,.]+)"],# Done Che
                'Haemoglobin': [r"Haemoglobin \(Hb\)\n([\d,.]+)",r"Haemoglobin \(Hb\n([\d,.]+)",r"Haemoglobin Hb\)\n([\d,.]+)"],#Done Che
                'PCV': [r"PCV \(Packed Cell Volume\)\n([\d,.]+)",r"PCV \(Packed Cell Volume\n([\d,.]+)",r"PCV\(Packed Cell Volume\)\n([\d,.]+)"], # Done Che
                'MCV': [r"\bMCV \(Mean Corpuscular Volume\)\b\n([\d,.]+)",r"\bMCV \(Mean Corpuscular Volume\b\n([\d,.]+)",r"\bMCV\(Mean Corpuscular Volume\b\n([\d,.]+)",r"MCV \(Mean Corpuscular Volume\)\n([\d,.]+)"], #Done Che
                'MCH': [r"\bMCH \(Mean Corpuscular Hb\)\n([\d,.]+)",r"\bMCH \(Mean Corpuscular Hb\n([\d,.]+)"], #Done Che
                'MCHC': [r'MCHC \(Mean Corpuscular Hb Concn.\) (\d+\.\d+)',r'MCHC \(Mean Corpuscular Hb Concn. (\d+\.\d+)',r"\bMCH \(Mean Corpuscular Hb Concn\.\)\b\n([\d,.]+)",r"\bMCH \(Mean Corpuscular Hb Concn\b\n([\d,.]+)",r"\bMCH \(Mean Corpuscular Hb Concn\.\b\n([\d,.]+)"] ,#Done Che
                'RDW': [r"RDW \(Red Cell Distribution Width\)\n([\d,.]+)",r"\bRDW \(Red Cell Distribution Width\)\b\n([\d,.]+)"],#Done
                'Absolute Neutrophil Count': [r"\bAbsolute Neutrophils Count\b\n(.+)"],#Done Che
                'Absolute Lymphocyte Count': [r"\bAbsolute Lymphocyte Count\b\n([\d,.]+)"],# Done Che
                'Absolute Monocyte Count': [r"\bAbsolute Monocyte Count\b\n([\d,.]+)"], #Done
                'Absolute Eosinophil Count': [r"\bAbsolute Eosinophil Count\b\n([\d,.]+)"],  #Done
                'Absolute Basophil Count' : [r"\bAbsolute Basophil Count\b\n([\d,.]+)"], #Done
                'Neutrophils': [r"\bNeutrophils\b\n([\d,.]+)"], #Done Che
                'Lymphocytes': [r"\bLymphocytes\b\n([\d,.]+)"], #Done che
                'Monocytes': [r"\bMonocytes\b\n([\d,.]+)"],#Done che
                'Eosinophils': [r"\bEosinophils\b\n([\d,.]+)"],#Done che
                'Basophils': [r"\bBasophils\b\n([\d.]+)"],#Done che
                'Platelet Count': [r"\bPlatelet Count\b\n([\d.]+)"], #Done che
                'Mean Platelet Volume': [r"MPV \(Mean Platelet Volume\)\n([\d,.]+)",r"MPV Mean Platelet Volume\)\n([\d,.]+)",r"\bMPV Mean Platelet Volume\)\b\n([\d,.]+)",r"\bMPV \(Mean Platelet Volume\b\n([\d,.]+)"], #Done
                'PCT' : [r"PCT \( Platelet Haematocrit\)\n([\d,.]+)",r"PCT Platelet Haematocrit\)\n([\d,.]+)",r"PCT Platelet \(Haematocrit\)\n([\d,.]+)"], #Done che
                'PDW' : [r"PDW \(Platelet Distribution Width\)\n([\d,.]+)",r"PDW \(Platelet Distribution Width\)\n([\d,.]+)",r"PDW Platelet Distribution Width\)\n([\d,.]+)",r"PDW \(Platelet Distribution Width\n([\d,.]+)"], #Done che
                'TSH' : [r"TSH \(Ultrasensitive\)\n([\d,.]+)",r"TSH \(Ultrasensitive\n([\d,.]+)",r"TSH Ultrasensitive\)\n([\d,.]+)",r'TSH\(Ultrasensitive\)\n([\d,.]+)',r'TSH\(Ultrasensitive\n([\d,.]+)'],
                "HbA1c":[r"HbA1C. Glycated Haemoglobin\n([\d,.]+)",r"HbA1C - Glycated Haemoglobin\n([\d,.]+)",r"HbA1C - Glycosylated Haemoglobin \(HPLC\)\n([\d,.]+)",r"HbA1C  Glycosylated Haemoglobin\n([\d,.]+)",r"HbA1C - Glycosylated Haemoglobin \(HPLC\n([\d,.]+)",r"HbA1C- Glycosylated Haemoglobin \(HPLC\)\n([\d,.]+)",r"HbA1C Glycosylated Haemoglobin \(HPLC\)\n([\d,.]+)",r"\(HPLC\)\n([\d,.]+)"], #Done Che
                'Estimated Average Glucose (eAG)': [r"Estimated Average Glucose \(eAG\)\n([\d,.]+)",r"Estimated Average Glucose \(eAG\n([\d,.]+)"], #Done Che
                'Colour (Urine)' : [r"Colour\n(.+)"],  #Done Che
                'Appearance (Urine)': [r"Transparency \(Appearance\)\n(.+)",r"Transparency \(Appearance\n(.+)",r"Transparency\(Appearance\)\n(.+)",r"Transparency\(Appearance\n(.+)"], #Done Che
                'Deposit (Urine)': [r"Deposit\n(.+)"],#Done Che
                'pH (Urine)': [r"Reaction \(pH\)\n(.+)",r"Reaction\(pH\)\n(.+)",r"Reaction \(pH\n(.+)",r"Reaction\(pH\n(.+)"],#Done Che
                'Specific Gravity': [r"Specific Gravity\n(.+)"],#Done Che
                'Glucose (Urine)': [r"Urine Glucose \(sugar\)\n(.+)",r"Urine Glucose\(sugar\)\n(.+)",r"Urine Glucose \(sugar\n(.+)",r"Urine Glucose\(sugar\n(.+)"],#Done Che
                'Ketones (Urine)': [r"Urine Ketones \(Acetone\)\n(.+)",r"Urine Ketones \(Acetone\n(.+)",r"Urine Ketones\(Acetone\)\n(.+)",r"Urine Ketones\(Acetone\n(.+)"],#Done Che
                'Protein (Urine)':[r"Urine Protein \(Albumin\)\n(.+)",r"Urine Protein \(Albumin\n(.+)",r"Urine Protein\(Albumin\n(.+)",r"Urine Protein\(Albumin\)\n(.+)"], #Done Che
                'Nitrite (Urine)': [r"Nitrite\n(.+)"],#Done Che
                'Urobilinogen (Urine)': [r"Urobilinogen\n(.+)"], #Done che
                'Epithelial Cells (Urine)': [r"Epithelial Cells\n(.+)"], #Done che
                'Pus Cells (Urine)' : [r'Pus cells \(WBCs\)\n(.+)',r'Pus cells \(WBCs\n(.+)',r'Pus cells\(WBCs\)\n(.+)',r'Pus cells\(WBCs\n(.+)',r'Pus-cells \(WBCs\)\s*([\d-]+)'], #Done che
                'Red Blood Cells (Urine)': [r"Red blood cells\n(.+)"],#Done che
                'Casts': [r"\bCast\b\n(.+)"], #Done che
                'Crystals': [r"\bCrystals\b\n(.+)"], #Done che
                'Amorphous Materials (Urine)': [r"\bAmorphous Deposits\b\n(.+)"],  #Done che
                'Bacteria': [r"\bBacteria\b\n(.+)"],#Done che
                'Yeast Cells': [r"\bYeast Cells\b\n(.+)"], #Done che
                'Trichomonas Vaginalis': [r"\bTrichomonas Vaginalis\b\n(.+)"], #Done che
               
               
            }
            df = pd.DataFrame(columns=["Investigation", "Observed Value"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED|Biological Reference Interval|Observed Value|Unit|\(Plasma-F.Hexokinase\)|Investigation|Invi|mg/dL|\(Serum\,Diazo\)|^.*VID:\s*220081000136689.*$|\*|\%|\d+\.\d+-\d+\.\d+|\(Serum,ECLIA\)", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            # for test_description, test_pattern in test_patterns.items():
            #     match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
            #     if match:
            #         test_value = match.group(1)
            #         test_value = test_value
            #         print(f"{test_description} value: {test_value}")
            #         # Create a new DataFrame with the test description and value
            #         new_row = pd.DataFrame({"Investigation": [test_description], "Observed Value": [test_value]})

            #         # Concatenate the new row with the existing DataFrame
            #         df = pd.concat([df, new_row], ignore_index=True, sort=False)
            #     else:
            #         print(f"{test_description} value not found in the text file.")
            for test_description, test_patterns_list in updated_patterns.items():
                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                test_value = None
                for test_pattern in test_patterns_list:
                    matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                    if matches:
                        test_value = matches[0]
                        print(f"{test_description} : {test_value}")
                        # Create a new DataFrame with the test description and value
                        new_row = pd.DataFrame({"Investigation": [test_description], "Observed Value": [test_value]})
                         # Concatenate the new row with the existing DataFrame
                        df = pd.concat([df, new_row], ignore_index=True, sort=False)
                        break
                if not test_value:
                    print(f"No match found for {test_description} in the text.")
            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                existing_df = existing_df.rename(columns=lambda x: x.strip()) #Removing trailing spaces
                print(existing_df.columns)
                existing_df.columns.values[0] = "Investigation"
                existing_df.columns.values[1] = "Observed Value"
            except:
                existing_df = pd.DataFrame(columns=["Investigation", "Observed Value"])
                print("Created empty dataframe!")
            if df.empty:
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.notnull()]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["Investigation", "Observed Value"], index=False)
            else:
                # Concatenate the existing DataFrame with the new DataFrame
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df[existing_df.notnull()]
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                existing_df.to_csv(output_table_file_path, columns=["Investigation", "Observed Value"], index=False)
            print(existing_df)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'trutest lab':
        try:
            updated_patterns = {
                "Volume":[r"Volume\n(.+)"],
                'Colour (Urine)':[r"Colour\n(.+)"],
                'Appearance (Urine)':[r"Transparency \(Appearance\)\n(.+)",r"Transparency \(Appearance\n(.+)"],
                'Deposit (Urine)':[r"Deposit\n(.+)"],
                "pH (Urine)" : [r'Reaction \(pH\)\n([\d.]+)',r'Reaction \(pH\n([\d.]+)'],
                "Specific Gravity" : [r'Specific Gravity\n([\d.]+)'],
                'Protein (Urine)':[r"Urine Protein \(Albumin\)\n(.+)",r"Urine Protein \(Albumin\n(.+)"],
                'Glucose (Urine)':[r"Urine Glucose \(sugar\)\n(.+)",r"Urine Glucose \(sugar\n(.+)"],
                'Ketones (Urine)':[r"Urine Ketones \(Acetone\)\n(.+)",r"Urine Ketones \(Acetone\n(.+)"],
                'Urobilinogen (Urine)':[r'(.+)(?=\nUrobilinogen)',r"Urobilinogen\n(.+)"],
                'Bile Pigment (Urine)':[r"Bile pigments\n(.+)"],
                'Blood (Urine)':[r"Blood\n(.+)"],
                'Nitrite (Urine)':[r"Nitrite\n(.+)"],
                'Red Blood Cells (Urine)':[r"(?<!NUCLEATED )Red blood Cells\b\n(.+)(?!( %))"],
                "Pus Cells (Urine)":[r"Pus Cells \(WBCs\)\n(.+)",r"Pus Cells \(WBCs\n(.+)"],
                'Epithelial Cells (Urine)':[r'(.+)(?=\nEpithelial Cells)',r"Epithelial Cells\n(.+)"],
                'Casts':[r"Cast\n(.+)"],
                'Crystals':[r"Crystals\n(.+)"],
                'Bacteria':[ r'(.+)(?=\nBacteria)',r"Bacteria\n(.+)"],
                'Yeast Cells':[r"Yeast Cells\n(.+)"],
                'Parasite':[ r'(.+)(?=\nPARASITE)',r"PARASITE\n(.+)"],
                "Trichomonas Vaginalis" :[r"Trichomonas Vaginalis\n(.+)"],
                'Amorphous Materials (Urine)' : [r"Amorphous deposits\n(.+)"],
                "TSH": [r'TSH Ultra\n([\d,.]+)'],
                "Haemoglobin": [r'Hemoglobin \(Hb\)\n([\d.]+)',r'Hemoglobin \(Hb\n([\d.]+)'],
                "R.B.C. Count": [r'Erythrocyte \(RBC\) Count\n([\d.]+)',r'Erythrocyte \(RBC Count\n([\d.]+)'],
                "Prostate Specific Antigen": [r'PSA\n([\d.]+)\n'],
                "Blood Urea" : [r"Urea\n([\d.]+)"],
                "Blood Urea Nitrogen" : [r"BUN\n([\d.]+)"],
                "Urea/Creatinine Ratio" : [r"Urea\/Creatinine Ratio\n([\d,.]+)"],
                "Blood Urea Nitrogen/Creatinine Ratio" : [r"BUN\/Creatinine Ratio\n([\d,.]+)"],
                "Creatinine" : [r"Creatinine\n([\d,.]+)"],
                # 'Total Cholesterol':[],
                # 'HDL Cholesterol':[],
                # 'HDL/LDL Ratio':[],
                # 'LDL Cholesterol':[],
                # 'Total Cholesterol/HDL Cholesterol Ratio':[],
                # 'Triglycerides/HDL Ratio':[],
                'Triglycerides':[r"Triglycerides\n([\d,.]+)"],
                # 'LDL/HDL Ratio':[],
                # 'Non-HDL Cholesterol':[],
                # 'VLDL Cholesterol':[],
                # #'Alkaline Phosphatase':[],
                'Bilirubin (Total)':[r"Bilirubin Total\n([\d,.]+)"],
                'Bilirubin (Direct)':[r"Bilirubin Direct\n([\d,.]+)"],
                'Bilirubin (Indirect)':[r"Bilirubin Indirect\n([\d,.]+)"],
                'Vitamin D':[r"25-OH VITAMIN D \(TOTAL\)\n(.+)"], #
                'GGTP':[r"GAMMA GLUTAMYL TRANSFERASE \(GGT\)\n([\d,.]+)",r"GAMMA GLUTAMYL TRANSFERASE (GGT)"], #
                'SGOT/SGPT Ratio':[r"SGOT \/ SGPT RATIO\n([\d,.]+)",r"SGOT \/ SGPT\n([\d,.]+)",r"SGOT\/SGPT\n([\d,.]+)"], #
                'SGOT':[r"SGOT\n([\d,.]+)"],
                'SGPT':[r"SGPT\n([\d,.]+)"],
                'PCV':[r"Packed Cell Volume\(PCV\)\n([\d,.]+)",r"Packed Cell Volume \(PCV\)\n([\d,.]+)",r"Packed Cell Volume \(PCV\n([\d.]+)"], 
                'MCV':[r"Mean Cell Volume \(MCV\)\n([\d,.]+)",r"Mean Cell Volume \(MCV\n([\d,.]+)"], 
                'MCH' : [r"Mean Cell Haemoglobin \(MCH\)\n([\d,.]+)",r"Mean Cell Haemoglobin \(MCH\n([\d,.]+)"], 
                'MCHC' : [r"Mean Corpuscular Hb Concn\. \(MCHC\)\n([\d,.]+)",r"Mean Corpuscular Hb Concn\. \(MCHC\n([\d,.]+)",r"Mean Corpuscular Hb Concn \(MCHC\)\n([\d,.]+)",r"Mean Corpuscular Hb Concn \(MCHC\n([\d,.]+)"], 
                'PDW':[r"PDW\n([\d,.]+)"], 
                'Mean Platelet Volume':[r"Mean Platelet Volume \(MPV\)\n([\d,.]+)",r"Mean Platelet Volume \(MPV\n([\d,.]+)"], 
                'Platelet Count':[r"Platelet Count\n([\d,.]+)"], 
                'PLCR':[r"PLATELET TO LARGE CELL \(PLCR\)\n([\d,.]+)",r"PLATELET TO LARGE CELL \(PLCR\n([\d,.]+)"],#
                'PCT':[r"PCT\n([\d,.]+)",r"PCT \n([\d,.]+)"], 
                'Absolute Neutrophil Count':[r"Absolute Neutrophil Count\n([\d,.]+)"],
                'Absolute Lymphocyte Count':[r"LYMPHOCYTES ABSOLUTE COUNT\n([\d,.]+)",r"LYMPHOCYTES  ABSOLUTE COUNT\n([\d,.]+)",r"LYMPHOCYTES - ABSOLUTE COUNT\n([\d,.]+)"], #
                'Absolute Monocyte Count':[r"Absolute Monocyte Count\n([\d,.]+)"], 
                'Absolute Basophil Count':[r"Absolute Basophils Count\n([\d,.]+)"], 
                'Absolute Eosinophil Count':[r"Absolute Eosinophil Count\n([\d,.]+)"], 
                'W.B.C. Count' : [r"WBC\n(.+)",r"Total Leucocytes \(WBC\) Count\n([\d,.]+)",r"Total Leucocytes \(WBC Count\n([\d,.]+)"], 
                "Neutrophils":[r"Neutrophils\n([\d,.]+)"], 
                "Lymphocytes" : [r"Lymphocytes\n([\d,.]+)"], 
                "Monocytes" : [r"Monocytes\n([\d,.]+)"], 
                'Eosinophils':[r"Eosinophils\n([\d,.]+)"], 
                'Basophils' : [r"Basophils\n([\d,.]+)"], 
                "Blood Glucose Fasting" : [r"Glucose Fasting\n([\d,.]+)",r"Glucose Fasting \n([\d,.]+)"],
                "RDW" : [r"Red Cell Distribution Width \(RDW\)\n([\d,.]+)",r"Red Cell Distribution Width \(RDW\n([\d,.]+)"],
            }
            
            df = pd.DataFrame(columns=["Test Description", "Value(s)"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\*|\(VCSn Technology\)|cell\/cu\.mm|\/hpf|microscopic examination urine|page 3 of 9", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            
            # for test_description, test_pattern in test_patterns.items():
            #     match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
            #     if match:
            #         test_value = match.group(1)
            #         test_value = test_value
            #         print(f"{test_description} value: {test_value}")
            #         # Create a new DataFrame with the test description and value
            #         new_row = pd.DataFrame({"Test Description": [test_description], "Value(s)": [test_value]})

            #         # Concatenate the new row with the existing DataFrame
            #         df = pd.concat([df, new_row], ignore_index=True, sort=False)
            #     else:
            #         print(f"{test_description} value not found in the text file.")
            # print("MY TURN 2")
            for test_description, test_patterns_list in updated_patterns.items():

                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                test_value = None
                for test_pattern in test_patterns_list:
                    #matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                    match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                    if match:
                        #test_value = matches[0]
                        test_value = match.group(1)
                        print(f"{test_description} : {test_value}")
                        # Create a new DataFrame with the test description and value
                        new_row = pd.DataFrame({"Test Description": [test_description], "Value(s)": [test_value]})
                         # Concatenate the new row with the existing DataFrame
                        df = pd.concat([df, new_row], ignore_index=True, sort=False)
                        break
                if not test_value:
                    print(f"No match found for {test_description} in the text.")
            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                existing_df = existing_df.rename(columns=lambda x: x.strip()) #Removing trailing spaces
                print(existing_df.columns)
                existing_df=existing_df.iloc[:, :2]
            except:
                existing_df = pd.DataFrame(columns=["Test Description", "Value(s)"])
                print("Created empty dataframe!")
            if df.empty:
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df = existing_df[existing_df.notnull()]
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                if existing_df.iloc[:, 1].dtype=='object' and not existing_df.iloc[:, 1].str.isnumeric().all():
                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].where(existing_df.iloc[:, 1].str.isnumeric(), existing_df.iloc[:, 1].str.replace(',', '.'))
                existing_df.to_csv(output_table_file_path, columns=["Test Description", "Value(s)"], index=False)
            else:
                # Concatenate the existing DataFrame with the new DataFrame
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df[existing_df.notnull()]
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
               
                existing_df = existing_df[existing_df.iloc[:, 1].notnull() & existing_df.iloc[:, 0].notnull()]
                if existing_df.iloc[:, 1].dtype=='object' and not existing_df.iloc[:, 1].str.isnumeric().all():
                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].apply(lambda x: x.replace(',', '.') if pd.notnull(x) and not x.isnumeric() else x) 
                existing_df.to_csv(output_table_file_path, index=False)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))

def test_name_standardizer(output_csv_file_path,option):
    if option.lower()=='tata 1mg':
        try:
                    existing_df = pd.read_csv(output_csv_file_path)
                    print("here the existing df is: ",existing_df)
                    test_names = tata1mg_test_names()
                    mapper = Mapper('tata 1mg',test_names) 
                    standardized_names = mapper.test_mapper('tata 1mg')
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].str.rstrip()  # Remove trailing whitespace
                    print("*"*200)
                    #existing_df.iloc[:,0]
                    print("*"*200)
                    # Replace with standardized names
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names) 
                    # Convert the standardized test names to lowercase
                    standardized_test_names = set(map(str.lower, tata1mg_test_names()))
                    print("Standardized test names are: ",standardized_test_names)
                    mask = existing_df.iloc[:, 1].isin(standardized_test_names)
                    # Filter the DataFrame to keep rows where the second column does not contain values from the standardized test names
                    df_filtered = existing_df[~mask]
                    print("Filtered Dataframe: ",df_filtered)
                    df_filtered.to_csv(output_csv_file_path, index=False)
                    #existing_df.to_csv(output_csv_file_path, index=False)
        except KeyError:
                    print("Name of the first column is not 'Test Name'")
    elif option.lower()=='metropolis':
        try:
                    existing_df = pd.read_csv(output_csv_file_path)
                    print("here the existing df is: ",existing_df)
                    test_names = metropolis_keywords()
                    mapper = Mapper('metropolis',test_names) 
                    standardized_names = mapper.test_mapper('metropolis')
                    # existing_df.iloc[:,0] = existing_df.iloc[:,0].str.rstrip()  # Remove trailing whitespace
                    # existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names)  # Replace with standardized names
                    # existing_df.iloc[:,1] = existing_df.iloc[:,1].str.rstrip()  # Remove trailing whitespace
                    existing_df.iloc[:, 0] = existing_df.iloc[:, 0].astype(str).str.rstrip()  # Convert to string and remove trailing whitespace
                    existing_df.iloc[:, 0] = existing_df.iloc[:, 0].replace(standardized_names)  # Replace with standardized names
                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].astype(str).str.rstrip()  # Convert to string and remove trailing whitespace

                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
                    # Convert the standardized test names to lowercase
                    standardized_test_names = set(map(str.lower, metropolis_keywords()))
                    print("Standardized test names are: ",standardized_test_names)
                    # Create a boolean mask to identify rows where the second column contains values from the standardized test names
                    mask = existing_df.iloc[:, 1].isin(standardized_test_names)
                    print("Mask is: ",mask)
                    # Filter the DataFrame to keep rows where the second column does not contain values from the standardized test names
                    df_filtered = existing_df[~mask]
                    print("Filtered Dataframe: ",df_filtered)
                    df_filtered.to_csv(output_csv_file_path, index=False)
                    # #getting all test name values
                    # standardized_test_names = standardized_names.values()
                    # mask = existing_df.iloc[:, 1].isin(standardized_test_names)
                    # # Filter the DataFrame to keep rows where the second column does not contain values from the standardized test names
                    # df_filtered = existing_df[~mask]
                    # print("After removing extra space in columns")
                    # print(df_filtered)
                    # df_filtered.to_csv(output_csv_file_path, index=False)
        except Exception as inst:
                    print(inst)
                    print(type(inst))
                    print("Name of the first column is not 'Investigation'")
    elif option.lower()=='trutest lab':
        try:
                    existing_df = pd.read_csv(output_csv_file_path)
                    print("here the existing df is: ",existing_df)
                    test_names = trutest_keywords()
                    mapper = Mapper('trutest lab',test_names)
                    standardized_names = mapper.test_mapper('trutest lab')
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].str.rstrip()  # Remove trailing whitespace
                    print("*"*200)
                    #existing_df.iloc[:,0]
                    print("*"*200)
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names)  # Replace with standardized names
                    #print(existing_df)
                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)

                    # Convert the standardized test names to lowercase
                    standardized_test_names = set(map(str.lower, trutest_keywords()))
                    # Remove '*' character at the end of each word
                    standardized_test_names = {name.rstrip('*') for name in standardized_test_names}
                    print("Standardized test names are: ",standardized_test_names)
                    # Create a boolean mask to identify rows where the second column contains values from the standardized test names
                    mask = existing_df.iloc[:, 1].isin(standardized_test_names)
                    #print("Mask is: ",mask)
                    # Filter the DataFrame to keep rows where the second column does not contain values from the standardized test names
                    df_filtered = existing_df[~mask]
                    print("Filtered Dataframe: ",df_filtered)
                    df_filtered.to_csv(output_csv_file_path, index=False)
                    #existing_df.to_csv(output_csv_file_path, index=False)
        except:
                    print("Name of the first column is not 'Test Description'")  
    elif option.lower()=='pharmeasy':
            try:
                    existing_df = pd.read_csv(output_csv_file_path)
                    print("here the existing df is: ",existing_df)
                    test_names = pharmeasy_keywords()
                    mapper = Mapper('pharmeasy',test_names)
                    standardized_names = mapper.test_mapper('pharmeasy')
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].str.rstrip()  # Remove trailing whitespace
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names)  # Replace with standardized names
                    
                    existing_df.iloc[:, 1] = existing_df.iloc[:, 1].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)

                    # Convert the standardized test names to lowercase
                    standardized_test_names = set(map(str.lower, pharmeasy_keywords()))
                    print("Standardized test names are: ",standardized_test_names)
                    # Create a boolean mask to identify rows where the second column contains values from the standardized test names
                    mask = existing_df.iloc[:, 1].isin(standardized_test_names)
                    print("Mask is: ",mask)
                    # Filter the DataFrame to keep rows where the second column does not contain values from the standardized test names
                    df_filtered = existing_df[~mask]
                    print("Filtered Dataframe: ",df_filtered)
                    df_filtered.to_csv(output_csv_file_path, index=False)
                    #existing_df.to_csv(output_csv_file_path, index=False)
            except KeyError:
                print("Name of the first column is not 'TEST NAME'")
            except:
                print("No data found!")
                return
    else:
        return    

def convert_to_standard_form(output_csv_file_path,option):
    try:
        converted_values = {}
        data = pd.read_csv(output_csv_file_path)
        option=option.lower()
        converter = Converter(option)
        converted_values=converter.process_data(data)
        print("Converted values are\n",converted_values)
        # Save the converted values to CSV
        new_df = pd.DataFrame(list(converted_values.items()), columns=['Test Name', 'Converted Value'])
        new_df.to_csv(output_csv_file_path, index=False)
        print(f"Converted values saved to '{output_csv_file_path}'")
    except:
        print("Some error occured!Couldn't convert values.")
def convert_to_standard_form2(output_csv_file_path, option):
    try:
        # Check if the CSV file exists
        if not os.path.isfile(output_csv_file_path):
            print(f"File not found: {output_csv_file_path}")
            return

        # Read the CSV file into a dataframe
        data = pd.read_csv(output_csv_file_path)

        # Check if the dataframe is empty
        if data.empty:
            print(f"Empty dataframe found in file: {output_csv_file_path}")
            return

        option = option.lower()
        converter = Converter(option)
        converted_values = converter.process_data(data)
        print("Converted values are:\n", converted_values)

        # Save the converted values to CSV
        new_df = pd.DataFrame(list(converted_values.items()), columns=['Test Name', 'Converted Value'])
        new_df.to_csv(output_csv_file_path, index=False)
        print(f"Converted values saved to '{output_csv_file_path}'")

    except:
        print("An error occurred! Couldn't convert values.")

# CSV File Reader and Post-processing function
def read_csv_and_extract_data(raw_text, input_table_file_path, output_table_file_path, option):

    # Open input CSV file and create output CSV file
    with open(input_table_file_path, 'r') as input_file, open(output_table_file_path, 'w', newline='') as output_file:
        # Create CSV reader and writer objects
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Below given header file works for all reports Pharmeasy, TATA 1MG and NM Medical as for now
        # header_pattern = re.compile(r'test|test\s*(name|investigation)|investigation\s*name|investigation', re.
        
        # Find index of "Test Name", "Test", or "Investigation" cell and skip all rows before it
        if option.lower() == "pharmeasy":
            # header_pattern = re.compile(r'\bNAME(?!=\s)(?!\s*=)(?!\s*:)|test\s*(name|investigation)|investigation\s*name|investigation', re.IGNORECASE)
            # header_pattern = re.compile(r'\b(?!NAME\s*:)(NAME(?!=\s)(?!\s*=)(?!\s*:)|test\s*(name|investigation)|investigation\s*name|investigation)', re.IGNORECASE)
            header_pattern = re.compile(r'\b(?<!NAME:)(?<!NAME : )(NAME(?!\s*=)(?!\s*:)|test\s*(name|investigation)|investigation\s*name|investigation)', re.IGNORECASE)

            
        if option.lower() == "trutest lab":
            print("hello from Trutest labs!")
            #header_pattern = re.compile(r'Volume*|Volume |test description|test\s*(name|Description)|investigation\s*name|investigation/', re.IGNORECASE)
            header_pattern = re.compile(r'test description|test\s*(name|Description)|investigation\s*name|investigation/Volume*|Urine Glucose |Microscopic Examination Urine|Volume |Urea ', re.IGNORECASE)

        if option.lower() == "tata 1mg":
            header_pattern = re.compile(r'test\s*(name|investigation)|investigation\s*name|investigation', re.IGNORECASE)
            
        if option.lower() == 'nm medical':
            #header_pattern = re.compile(r'\b(test|investigation)\b', re.IGNORECASE)
            header_pattern = re.compile(r'\b(test|investigation|PHYSICAL|CHEMICAL\sEXAMINATION)\b|Crystals', re.IGNORECASE)
        #header_pattern = re.compile(r'test|investigation', re.IGNORECASE)

        if option.lower() == 'metropolis':
            print("Metropolis Header selected!")
            #header_pattern = re.compile(r'\bInvestigation\b(?!\s*Outside\s*Reference\s*Range)|Sodium', re.IGNORECASE)
            #header_pattern = re.compile(r'\bInvestigation\b(?!\s*Outside\s*Reference\s*Range)|Sodium', re.IGNORECASE)
            #header_pattern = re.compile(r'\b(Investigation|Sodium|Total Protein \(Serum,Biuret\))\b(?!\s*Outside\s*Reference\s*Range)', re.IGNORECASE)
            header_pattern = re.compile(r'\b(Investigation|Sodium|Total Protein \(Serum,Biuret\))\b(?!\s*Outside\s*Reference\s*Range)', re.IGNORECASE)
            #header_pattern = re.compile(r'\b(Investigation)\b(?!\s*Outside\s*Reference\s*Range)|Sodium|.*Total Protein.*', re.IGNORECASE)

        if option.lower() == 'metropolis':
            start_index = None
            total_protein_row_encountered = False
            for row in csv_reader:
                if total_protein_row_encountered:
                    csv_writer.writerow(row[start_index:])
                else:
                    for i, cell in enumerate(row):
                        if header_pattern.search(cell):
                            start_index = i
                            csv_writer.writerow(row[start_index:])
                            break
                    if start_index is not None:
                        total_protein_row_encountered = True
                if start_index is None:
                    print('Error: "Test Name", "Test", "Test Description", "Investigation", or "Sodium" cell not found in CSV file')
                    # return <-- I have commented this code

            # Write rows to output CSV file starting from the "Test Name", "Test", "Investigation", or "Sodium" cell
            for row in csv_reader:
                if not any(row):  # Stop if blank row encountered
                    break
                csv_writer.writerow(row[start_index:])

        elif option.lower() == 'trutest lab':
            predefined_test_names=trutest_keywords()
            start_index = None
            start_extraction = False
            blank_row_encountered = False
            for row in csv_reader:
                if not start_extraction:
                    for i, cell in enumerate(row):
                        if header_pattern.search(cell):
                            start_index = i
                            csv_writer.writerow(row[start_index:])
                            start_extraction = True
                            break
                else:
                    if not any(cell.strip() for cell in row):  # Check if the row is blank
                        next_row = next(csv_reader, None)  # Get the next row
                        next_to_next_row = next(csv_reader, None) 
                        if next_row or next_to_next_row and any(cell.strip() in predefined_test_names for cell in next_row):
                            csv_writer.writerow(row[start_index:])  # Write the current blank row
                            continue  # Continue reading until another blank row is encountered
                        else:
                            break  # Stop reading if a blank row is encountered and there are no predefined test names after that
                    csv_writer.writerow(row[start_index:start_index+2])
            if start_index is None or not start_extraction:
                    print('Error: "Test Name", "Test", "Test Description", "Investigation", or "Volume" cell not found in CSV file')
        elif option.lower()=='nm medical':
            predefined_test_names = nm_medical_keywords()
            start_extraction=False
            start_index = None
            for row in csv_reader:
                if not start_extraction:
                    for i, cell in enumerate(row):
                        if header_pattern.search(cell):
                            start_index = i
                            csv_writer.writerow(row[start_index:])
                            start_extraction = True
                            break
                else:
                    if not any(cell.strip() for cell in row):  # Check if the row is blank
                        next_row = next(csv_reader, None)  # Get the next row
                        #next_to_next_row = next(csv_reader, None) 
                        if next_row and any(any(test_name.strip() in cell for cell in next_row) for test_name in predefined_test_names):
                            csv_writer.writerow(row[start_index:])  # Write the current blank row
                            continue  # Continue reading until another blank row is encountered
                        else:
                            break  # Stop reading if a blank row is encountered and there are no predefined test names after that
                    csv_writer.writerow(row[start_index:start_index+2])

            if start_index is None or not start_extraction:
                print('Error: "Test Name", "Test", "Test Description", "Investigation", or "Volume" cell not found in CSV file')
            #df = pd.read_csv(output_table_file_path)

        else:
            start_index = None
            for row in csv_reader:
                for i, cell in enumerate(row):
                    if header_pattern.search(cell):
                        start_index = i
                        csv_writer.writerow(row[start_index:])
                        break
                if start_index is not None:
                    break
            if start_index is None:
                print('Error: "Test Name", "Test", "Test Description" or "Investigation" cell not found in CSV file')
                #return <-- I have commented this code

            # Write rows to output CSV file starting from the "Test Name", "Test", or "Investigation" cell
            for row in csv_reader:
                if not any(row):  # Stop if blank row encountered
                    break
                csv_writer.writerow(row[start_index:])
    #df2 = pd.read_csv(output_table_file_path)
    #print("Output Table DataFrame: ",df2)
    table_value_corrector(output_table_file_path,option)
    #print("Input Form file path is: ",input_form_file_path)
    #form_value_corrector(input_form_file_path,output_table_file_path,option)
    #lastly let us process the raw data
    extract_data_from_raw_text(raw_text,output_table_file_path,option)
    test_name_standardizer(output_table_file_path,option)
    convert_to_standard_form2(output_table_file_path,option)
    return output_table_file_path

#def form_value_corrector(input_form_file_path,output_table_file_path,option):
    # This function is going to process the form data 
    # Extract the CHLORIDE test name, transform its value
    # and append it to the final_output csv
 
    # if option.lower()=="pharmeasy":
    #     print("Pharmeasy report selected!")
    #     if os.path.exists(input_form_file_path):
    #         print("Forms file is present at location",input_form_file_path)
    #     #print("Input Form File Path inside form_value_corrector() is: ",input_form_file_path)
    #     try:
    #         df = pd.read_csv(input_form_file_path)
    #         #print("Input Form DataFrame: ",df)
    #     except:
    #         print("Unable to open the Forms CSV. No content found!")
    #         return
    #     try:
    #         # search for the row that contains the key "CHLORIDE"
    #         chloride_row = df[df['key'] == 'CHLORIDE']
        
    #         # extract the value from the corresponding cell in the same row
    #         chloride_value = chloride_row['value'].iloc[0]
            
    #         # extract the numerical part of the value (assuming it's always formatted like "I.S.E 103,7 mmol/l")
    #         chloride_numerical = float(chloride_value.split()[1].replace(',', '.'))
    #         print(chloride_numerical)

    #         existing_df = pd.read_csv(output_table_file_path)

    #         # create new DataFrame with extracted values
    #         #new_df = pd.DataFrame({'CHLORIDE': [chloride_numerical]})
    #         new_df = pd.DataFrame({
    #             'TEST NAME ': ['CHLORIDE'],
    #             'TECHNOLOGY ': [' '],
    #             'VALUE ': [chloride_numerical],
    #             'UNITS ': [' ']
    #         })

    #         # append new DataFrame to existing DataFrame
    #         updated_df = existing_df.append(new_df, ignore_index=True)
    #         #updated_df = pd.concat([existing_df,new_df])

    #         # write updated DataFrame back to CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')

    #     except IndexError:
    #         print('No value found for Chloride')
    # if option.lower()=="tata 1mg":
    #     print("Hello from TATA 1mg")
    #     try:
    #         df = pd.read_csv(input_form_file_path)
    #         #print("Input Form DataFrame: ",df)
    #     except:
    #         print("Unable to open the Forms CSV. No content found!")
    #         return
    #     try:
    #         # Extract Urea row and value
    #         urea_row = df[df['key'] == 'Urea']
    #         urea_value = float(urea_row['value'].iloc[0])
        
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Urea'],
    #                 'Result ': [urea_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Urea'],
    #                 'Result ': [urea_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for Urea')
    #     try:
    #         # Extract Blood Urea Nitrogen row and value
    #         blood_urea_nitrogen_row = df[df['key'] == 'Blood Urea Nitrogen']
    #         blood_urea_nitrogen_value = float(blood_urea_nitrogen_row['value'].iloc[0])
        
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Blood Urea Nitrogen'],
    #                 'Result ': [blood_urea_nitrogen_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Blood Urea Nitrogen'],
    #                 'Result ': [blood_urea_nitrogen_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         #print("Writing updated CSV for Blood Urea Nitrogen!")
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for Blood Urea Nitrogen')
    #     try:
    #         # Extract Urea row and value
    #         uric_acid_row = df[df['key'] == 'Uric Acid']
    #         uric_acid_value = float(uric_acid_row['value'].iloc[0])
           
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Uric Acid'],
    #                 'Result ': [uric_acid_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Name ': ['Uric Acid'],
    #                 'Result ': [uric_acid_value]
    #                 # 'Unit': [' '],
    #                 # 'Bio. Ref. Interval': [' '],
    #                 # 'Method': [' ']
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for Uric Acid.')
    # if option.lower()=='metropolis':
    #     try:
    #         df = pd.read_csv(input_form_file_path)
    #         print("Input Form DataFrame: ",df)
    #     except:
    #         print("Unable to open the Forms CSV. No content found!")
    #         return
    #     try:
    #         # Extract Urea row and value
    #         tsh_row = df[df['key'] == 'TSH(Ultrasensitive) (Serum,ECLIA)']
    #         tsh_value = tsh_row['value'].iloc[0]
           
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Investigation ': ['TSH'],
    #                 'Observed Value ': [tsh_value]
    #                 # 'Unit': [' '],
    #                 # 'Biological Reference Interval ': [' ']
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Investigation ': ['TSH'],
    #                 'Observed Value ': [tsh_value]
    #                 # 'Unit': [' '],
    #                 # 'Biological Reference Interval ': [' ']
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         print(updated_df)
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for TSH(Ultrasensitive).')
    #     try:
    #         # Extract Urea row and value
    #         t3_row = df[df['key'] == 'Free T3 (Serum,ECLIA)']
    #         t3_value = float(t3_row['value'].iloc[0])
           
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Investigation ': ['T3 (Tri-iodothyronine)'],
    #                 'Observed Value ': [t3_value]
    #                 # 'Unit': [' '],
    #                 # 'Biological Reference Interval ': [' ']
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Investigation ': ['T3 (Tri-iodothyronine)'],
    #                 'Observed Value ': [t3_value]
    #                 # 'Unit': [' '],
    #                 # 'Biological Reference Interval ': [' ']
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for Free T3.')
        # try:
        #     # Extract Urea row and value
        #     hydroxy_row = df[df['key'] == '25 Hydroxy (OH) Vit D (Serum,ECLIA)']
        #     hydroxy_value = float(hydroxy_row['value'].iloc[0])
           
        #     # Read existing DataFrame from output CSV file
        #     try:
        #         existing_df = pd.read_csv(output_table_file_path)
        #     except:
        #         existing_df = pd.DataFrame()

        #     # Check if existing DataFrame is empty
        #     if existing_df.empty:
        #         # Create new DataFrame with extracted values
        #         new_df = pd.DataFrame({
        #             'Investigation ': ['Vitamin D'],
        #             'Observed Value ': [hydroxy_value]
        #             # 'Unit': [' '],
        #             # 'Biological Reference Interval ': [' ']
        #         })
        #         updated_df = new_df
        #         #print("Updated DataFrame is: ", updated_df)
        #     else:
        #         # Create new DataFrame with extracted values
        #         new_df = pd.DataFrame({
        #             'Investigation ': ['Vitamin D'],
        #             'Observed Value ': [hydroxy_value]
        #             # 'Unit': [' '],
        #             # 'Biological Reference Interval ': [' ']
        #         })
        #         # Append new DataFrame to existing DataFrame
        #         updated_df = existing_df.append(new_df, ignore_index=True)
        #         updated_df = pd.concat([existing_df, new_df])
        #     # Write updated DataFrame back to output CSV file
        #     updated_df.to_csv(output_table_file_path, index=False, mode='w')
        # except IndexError:
        #     print('No value found for 25 Hydroxy (OH) Vit D.')
    # elif option.lower()=="trutest lab":
    #     print("TrueTest report selected!")
    #     try:
    #         df = pd.read_csv(input_form_file_path)
    #         #print("Input Form DataFrame: ",df)
    #     except:
    #         print("Unable to open the Forms CSV. No content found!")
    #         return
    #     try:
    #         # Extract BUN(Blood Urea Nitrogen) row and value
    #         bun_row = df[df['key'] == 'BUN*']
    #         bun_value = float(bun_row['value'].iloc[0])
           
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Description': ['BUN'],
    #                 'Value(s)': [bun_value],
    #                 'Reference Range': [' '],
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Description': ['BUN'],
    #                 'Value(s)': [bun_value],
    #                 'Reference Range': [' '],
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for BUN*.')
    #     try:
    #         # Extract BUN(Blood Urea Nitrogen) row and value
    #         urea_row = df[df['key'] == 'UREA*']
    #         urea_value = float(urea_row['value'].iloc[0])
           
    #         # Read existing DataFrame from output CSV file
    #         try:
    #             existing_df = pd.read_csv(output_table_file_path)
    #         except:
    #             existing_df = pd.DataFrame()

    #         # Check if existing DataFrame is empty
    #         if existing_df.empty:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Description': ['UREA'],
    #                 'Value(s)': [urea_value],
    #                 'Reference Range': [' '],
    #             })
    #             updated_df = new_df
    #             #print("Updated DataFrame is: ", updated_df)
    #         else:
    #             # Create new DataFrame with extracted values
    #             new_df = pd.DataFrame({
    #                 'Test Description': ['UREA'],
    #                 'Value(s)': [urea_value],
    #                 'Reference Range': [' '],
    #             })
    #             # Append new DataFrame to existing DataFrame
    #             updated_df = existing_df.append(new_df, ignore_index=True)
    #             updated_df = pd.concat([existing_df, new_df])
    #         # Write updated DataFrame back to output CSV file
    #         updated_df.to_csv(output_table_file_path, index=False, mode='w')
    #     except IndexError:
    #         print('No value found for UREA*.')
    # else:
    #     return

def table_value_corrector(csv_path,option):
    try:
        df = pd.read_csv(csv_path)
        print("Read csv file successfully!")
        print("*"*60)
        print(df)
        print("*"*60)
        # define a regular expression to match unwanted characters
        if option.lower()=='pharmeasy':
            test_names = pharmeasy_keywords()
            for col_name in df.columns:
                if 'normal range ' in col_name.lower() or 'reference range ' in col_name.lower():
                    if df[col_name].dtype=='str':
                        df[col_name] = df[col_name].apply(lambda x: x.rstrip())
                        df[col_name] = df[col_name].apply(lambda x: x.replace(' ', '-') if ' ' in str(x) else x)
                        df[col_name] = df[col_name].apply(lambda x: re.sub('<', '0', str(x)))
                        df[col_name] = df[col_name].apply(lambda x: re.sub(':', '.', str(x)))
                    #df[col_name] = df[col_name].apply(lambda x: re.sub('[^0-9\., ]', '', str(x)))
                    
                if 'value ' in col_name.lower():
                    try:
                        # perform desired operations on the column
                        if df[col_name].dtype == 'float64':
                            #df[col_name] = df[col_name].fillna(0).astype(float)  <-- Uncomment this line
                            df[col_name] = df[col_name].fillna('').astype(str) #Experimenting
                            df[col_name] = df[col_name].replace(',', '.')
                        else:
                        # df[col_name] = df[col_name].str.replace('Nil', '0') <-- Uncomment this line
                            df[col_name] = df[col_name].str.replace('Nil', '') #Experimenting
                            #df[col_name] = df[col_name].str.replace(',', '.').astype(float) <-- Uncomment this line (Doesnt work for Pharmeasy 05-01-23 Page 12)
                            df[col_name] = df[col_name].str.replace(',', '.').astype(str)
                    except:
                        print("Issue faced while modifying the df['VALUE '] column.")
            #print(df)
            try:
                for index, row in df.iterrows():
                    value = row['VALUE ']
                    if ' ' in value:
                        value = value.split(' ')[0]
                        df.at[index, 'VALUE '] = value
            except:
                print("Only one value present in the df['VALUE'] column.")
            try:
                for index, row in df.iterrows():
                    name = row['TEST NAME ']
                    given_test_names = ['IRON','TOTAL IRON BINDING CAPACITY (TIBC)', '% TRANSFERRIN SATURATION', 'UNSAT.IRON-BINDING CAPACITY(UIBC)','UNSAT.IRON-BINDING CAPACITY (UIBC)','APOLIPOPROTEIN - A1','APOLIPOPROTEIN - B']
                    for test_name in given_test_names:
                        if name.startswith(test_name):
                            df.at[index, 'TEST NAME '] = test_name
                            print(f"Replaced '{name}' with '{test_name}' at index {index}")
                            break
            except:
                print("Name of the first column is not TEST NAME")
            # try:
            #     replaced_indices = []  # List to store the indices where replacements have been made
            #     for index, row in df.iterrows():
            #         if index in replaced_indices:
            #             continue  # Skip this iteration if the test name has already been replaced

            #         name = row['TEST NAME ']
            #         for test_name in test_names:
            #             if name.startswith(test_name):
            #                 df.at[index, 'TEST NAME '] = test_name
            #                 replaced_indices.append(index)  # Add the index to the list of replaced indices
            #                 print(f"Replaced '{name}' with '{test_name}' at index {index}")
            #                 break
            # except KeyError:
            #     print("Name of the first column is not 'TEST NAME'")
            try:
                for index, row in df.iterrows():
                    name = row[0]
                    # TODO: I have commented the below line
                    # if (pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names)) or not any(name.contains(test_name.strip()) for test_name in test_names):
                    print("Current test name is: ",name)
                    if pd.notna(name) and not any(test_name.strip() in name.strip() for test_name in test_names):
                        print("Went inside")
                        df = df.drop(index)
                        print(f"Removed row with test name '{name}' at index {index}")
            except:
                print("Test Name column doesn't contain any garbage value.")
            try:
                df = df[(df['TECHNOLOGY '].notna()) & (df['VALUE '].notna()) & (df['VALUE ']!='')]
            except:
                print("TECHNOLOGY column was not found!")
            
            try:
                df[['TEST NAME ','VALUE ']].to_csv(csv_path,index=False)
                return
            except:
                print("Unable to save results from table corrector!")
            try:
                df[['TEST NAME ','OBSERVATION ']].to_csv(csv_path,index=False)
                return
            except:
                print("Unable to save results from table corrector!")
            try:
                df.to_csv(csv_path,index=False)
                return
            except:
                print("Unable to save results from table corrector!")
    
        elif option.lower()=='tata 1mg':
            print("TATA 1mg Selected!")
            test_names = tata1mg_test_names() # list of all tata 1MG test names
            
            #print(df['Result '].dtype)
            try:
                if df['Test Name '].str.startswith("0-1 major ASCVD").any():
                    mask = df['Test Name '].str.startswith("0-1 major ASCVD")
                    df.loc[mask, 'Test Name '] = None 
                    pass
                # if df['Result '].dtype == 'object':
                #     if df['Result '].str.contains('\s').any() or df['Result '].str.startswith('Glycosylated Hemoglobin').any():
                #         #print("HELOOOOOOOOOOO")
                #         df[['Result1', 'Result2']] = df['Result '].str.split(' ', n=1, expand=True)
                #         #print( df[['Result1', 'Result2']])
                #         df_new = pd.concat([df[['Test Name ', 'Result1']], pd.DataFrame({'Test Name ': ['Estimated average glucose (eAG)'], 'Result1': [df['Result2'].iloc[0]]})], ignore_index=True)
                #         #print("New DataFrame is: ",df_new)
                #         # rename 'Result1' to 'Result'
                #         df_new = df_new.rename(columns={'Result1': 'Result '})
                #         df_new.to_csv(csv_path,index=False)
                #     else:
                #         print("df['Result'] column only contains one value.SAFE!")
            except:
                    print("df['Result'] doesn't haver space after Result.")
            try:
                df = pd.read_csv(csv_path)
                for index, row in df.iterrows():
                    name = row['Test Name ']
                    for test_name in test_names:
                        if name.startswith(test_name):
                            df.at[index, 'Test Name '] = test_name
                           #print(f"Replaced '{name}' with '{test_name}' at index {index}")
                            break
            except:
                print("TEST NAME column only contains a single test name OR Name of the TEST is not in our TATA 1mg database.")

            #print("DataFrame before:",df)
            '''Below given try catch block checks if the given TEST is present in our TATA 1mg test names database. If not present then we don't want that particular row as it contains some garbage text which we don't need.'''
            try:
                for index, row in df.iterrows():
                    name = row['Test Name ']
                    #print("Name is",name)
                    if pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names):
                        df = df.drop(index)
                        print(f"Removed row with test name '{name}' at index {index}")
            except:
                print("TEST NAME column doesn't contain any garbage value.")

            # df['Test Name '].dropna(inplace=True)
            # df = df[df['Test Name '].notnull()]
            df = df[df.iloc[:, 0].notnull()]
            df.iloc[:,0:2].to_csv(csv_path,index=False)
            #df[['Test Name ', 'Result ']].to_csv(csv_path,index=False)

        elif option.lower()=='metropolis':
            df.to_csv("before.csv",index=False)
            print("Metropolis TABLE")
            #drop row which has length of cell value greater than 13
            #print(df['Observed Value '].dtype)
            try:
                if df['Observed Value '].dtype=='object':
                    df.drop(df[df['Observed Value '].str.len() > 13].index,inplace=True)
                    df.to_csv(csv_path,index=False)
            except:
                print('Observed Value column not present.')
            #print(df['Investigation '])
            test_names=metropolis_keywords()
            print("Before replacing names*****", df.columns)
            if '0' in df.columns:
                df = df.drop('0', axis=1)
            try:
                df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'\(Serum\) ', '')
                print("%"*20)
                print(df)
                print("%"*20)
            except:
                print("Serum not present in any row")
            try:
                for index, row in df.iterrows():
                    value = row[1]
                    if ' ' in value:
                        value = value.split(' ')[0]
                        df.at[index, df.columns[1]] = value
            except:
                print("Only one value present in the df['Observed Value'] column.")
            try:
                #df = pd.read_csv(csv_path)
                for index, row in df.iterrows():
                    #name = row['Investigation ']
                    name = row[0]
                    found_match = False
                    print(name)
                    for test_name in test_names:
                        if name.startswith(test_name):
                            #df.at[index, 'Investigation '] = test_name
                            #df.at[index, 0] = test_name
                            df.at[index, df.columns[0]] = test_name
                            #df.iloc[index, 0] = test_name
                            #df.at[index, 'Replaced Investigation'] = test_name
                            print(f"Replaced '{name}' with '{test_name}' at index {index}")
                            print(df.iloc[index, 0])
                            #print(df.at[index, 'Replaced Investigation'])
                            found_match = True
                            break
                    if not found_match:
                        print("No match found for name:", name)
            except:
                print("Investigation column only contains a single test name OR Name of the Investigation is not in our Metropolis database.")
            print("Currently the df is:\n",df)

            ## Handling special case 
            '''Below given try catch block checks if the given TEST is present in our Metropolis test names database. If not present then we don't want that particular row as it contains some garbage text which we don't need.'''
            try:
                for index, row in df.iterrows():
                    #name = row['Investigation ']
                    name = str(row[0])
                    #name = row.iloc[0]
                    print(name)
                    # TODO: I have commented the below line
                    # if (pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names)) or not any(name.contains(test_name.strip()) for test_name in test_names):
                    print("Yahan tak aa gaye!")
                    if pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names):
                    #if pd.notna(name) and not any(test_name in name for test_name in test_names):
                        print("Went inside")
                        df = df.drop(index)
                        print(f"Removed row with test name '{name}' at index {index}")
            except:
                print("Investigation column doesn't contain any garbage value.")
            try:
                df = df[df['Observed Value '].notnull()]
            except:
                print("No column of Observed Value found!")
            print(df.columns)
            #df.to_csv(csv_path,index=False,header=True)
            print("No. of columns in dataframe are: ",len(df.columns))
            pattern = r'\bSodium\b'
            df_columns = list(df.columns)
            # Check if "sodium" is present in any column name
            sodium_present = any(re.search(pattern, column, re.IGNORECASE) for column in df_columns)
            # if 'Sodium (Serum,ISE) ' in df.columns or 'Sodium ' in df.columns or 'Sodium' in df.columns or '(Serum,Uricase) Sodium (Serum,ISE) ' in df.columns or 'Sodium (Serum.ISE) ' in df.columns:
            if sodium_present:
                    #s=pd.Series(['Investigation ', 'Observed Value ', 'Unit ', 'Biological Reference Interval '])
                    # frame = {'Investigation':pd.Series() ,'Observed Value ':pd.Series(),'Unit ':pd.Series(), 'Biological Reference Interval ':pd.Series()}
                    # df1=pd.DataFrame(frame,index=None)
                    # df1.append(df)
                    print("Inside Sodium thing")
                    column_list = list(df.columns)
                    print("Column list is: ",column_list)
                    #column_list =  column_list[:2]
                    column_list_dataframe = pd.DataFrame(column_list)
                    df.loc[len(df)] = column_list
                    if len(df.columns) == 2:
                        columns = ["Investigation", "Observed Value"]
                    elif len(df.columns) == 5:
                        columns = ["Investigation", "Observed Value", "Unit", "Biological Reference Interval", ""]
                    elif len(df.columns) == 4:
                        columns = ["Investigation", "Observed Value", "Unit", "Biological Reference Interval"]
                    df.columns = columns
            print("Currently the columns are: ",df.columns)
            print(df.iloc[:,:2])
            df.iloc[:,:2].to_csv(csv_path,index=False)
        elif option.lower()=='trutest lab':
            print("Inside Trutest lab table corrector!")
            test_names = trutest_keywords()
            print("Before replacing test names: ",df)
            try:
                df = pd.read_csv(csv_path, header=None)
                column_index = df.columns[0]  # Get the index of the first column
                for index, row in df.iterrows():
                    name = row[column_index]
                    if pd.isnull(name):
                        continue
                    for test_name in test_names:
                        if name.startswith(test_name) and name.lower()!='urea/creatinine ratio ((calculated)) ':
                            df.at[index, column_index] = test_name
                            print(f"Replaced '{name}' with '{test_name}' at index {index}")
                            break
            except:
                print("Test Description column only contains a single test name or the name of the Test Description is not in our TruTest Lab database.")

            #df.to_csv(csv_path,index=False)
            print("After replacing test names: ",df)
            try:
                for index, row in df.iterrows():
                    name = row[0]
                    # TODO: I have commented the below line
                    # if (pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names)) or not any(name.contains(test_name.strip()) for test_name in test_names):

                    if pd.notna(name) and not any(test_name.strip() in name for test_name in test_names):
                        print("Went inside")
                        df = df.drop(index)
                        print(f"Removed row with test name '{name}' at index {index}")
            except:
                print("Test Description column doesn't contain any garbage value.")
            print(df.columns)
            print('DataFrame columns printed')
            if 'Urine Glucose (sugar)* ' in df.columns or 'Urine Glucose (sugar)*' in df.columns:
                    #s=pd.Series(['Investigation ', 'Observed Value ', 'Unit ', 'Biological Reference Interval '])
                    # frame = {'Investigation':pd.Series() ,'Observed Value ':pd.Series(),'Unit ':pd.Series(), 'Biological Reference Interval ':pd.Series()}
                    # df1=pd.DataFrame(frame,index=None)
                    # df1.append(df)
                    print("YO!")
                    column_list = list(df.columns)
                    df.loc[len(df)] = column_list
                    columns=["Test Description", "Value(s)", "Reference Range"]
                    df.columns=columns
            if 'Test Description' not in df.columns or 'Test Description ' not in df.columns: ##Remember I have added "not" here
                if len(df.columns)==3:
                    columns=["Test Description", "Value(s)", "Reference Range"]
                else:
                    columns=["Test Description", "Value(s)", "Reference Range","Extra_column"]
                df.columns=columns
            print("Updated df columns: ", df.columns)
            try:
                # Filter rows where the first and second columns are not null or empty
                df = df[(df.iloc[:, 0].notna()) & (df.iloc[:, 1].notna()) & (df.iloc[:, 1] != '')]
            except:
                print("Columns at index 0 and 1 were not found!")
            df.iloc[:,0:2].to_csv(csv_path,index=False)
        # elif option.lower()!='nm medical':
        #     print("Inside Trutest lab table corrector!")
        #     test_names = nm_medical_keywords()
        #     print("Before replacing test names: ",df)
        #     try:
        #         df = pd.read_csv(csv_path, header=None)
        #         column_index = df.columns[0]  # Get the index of the first column
        #         for index, row in df.iterrows():
        #             name = row[column_index]
        #             if pd.isnull(name):
        #                 continue
        #             for test_name in test_names:
        #                 if name.startswith(test_name) or test_name in name:
        #                     df.at[index, column_index] = test_name
        #                     print(f"Replaced '{name}' with '{test_name}' at index {index}")
        #                     break
        #     except:
        #         print("Test column only contains a single test name or the name of the Test is not in our NM Medical database.")

        #     #df.to_csv(csv_path,index=False)
        #     print("After replacing test names: ",df)
        #     try:
        #         for index, row in df.iterrows():
        #             name = row[0]
        #             # TODO: I have commented the below line
        #             # if (pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names)) or not any(name.contains(test_name.strip()) for test_name in test_names):

        #             if pd.notna(name) and not any(test_name.strip() in name for test_name in test_names):
        #                     print(name)
        #                     #print("Went inside")
        #                     df = df.drop(index)
        #                     print(f"Removed row with test name '{name}' at index {index}")
        #     except:
        #         print("Test column doesn't contain any garbage value.")
        #     print(df.columns)
        #     print('DataFrame columns printed')
        #     try:
        #         column_index=1
        #         if df.iloc[:, column_index].dtype == 'object':
        #             df.iloc[:, 1] = df.iloc[:, 1].str.replace('fl', '')
        #             df.iloc[:, 1] = df.iloc[:, 1].str.replace(':', '')
        #             df.iloc[:, 1] = df.iloc[:, 1].str.replace('ML', '') 
        #             df.iloc[:, 1] = df.iloc[:, 1].str.replace('/hpf', '')
        #     except:
        #         print("Issue faced while modifying the Results column.")
        #     df.columns = df.columns.astype(str) 
        #     if 'Test' not in df.columns or 'Test ' not in df.columns:
        #         print("HELLO THERE!")
        #         if len(df.columns)==3:
        #             columns=["Test", "Result", "Unit"]
        #         elif len(df.columns)==2:
        #             columns=["Test", "Result"]
        #         elif len(df.columns==5):
        #             columns=["Test", "Result", "Unit","Reference Range","Extra Column"]
        #         else:
        #             columns=["Test", "Result", "Unit","Reference Range"]
        #         print("TIKA TIKA!")
        #         #df.columns=columns
        #         df = df.rename(columns=dict(zip(df.columns, columns)))
        #     df = df[df.iloc[:, 1].notnull() & df.iloc[:, 0].notnull()]
        #     df.to_csv(csv_path,index=False)
        # else:
        #     return
    except:
        print("CSV File is empty!")

def extract_all(file_path, option):
    file_name, file_ext = os.path.splitext(file_path)
    if file_ext.lower() not in ['.pdf', '.jpg', '.jpeg', '.png']:
        print('Unsupported file format:', file_ext)
        return []

    if file_ext.lower() == '.pdf':
        folder_path = convert_pdf_to_image(file_path)
        image_list = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        table_csv_files = []
        for image in image_list:
            image_path = os.path.join(folder_path, image)
            file_prefix = os.path.splitext(image_path)[0]
            #preprocessed_image = image_preprocess(image_path)
            #if preprocessed_image is not None:
            table_csv_files.append(get_table_csv_results2(image_path, file_prefix, option))
        print(table_csv_files)
        
        valid_dataframes = []
        for csv_file in table_csv_files:
            # Check if the CSV file exists
            if not os.path.isfile(csv_file):
                print(f"File not found: {csv_file}")
                continue
            try:
                # Read the CSV file into a dataframe
                df = pd.read_csv(csv_file)

                # Check if the dataframe is not empty
                if not df.empty:
                    valid_dataframes.append(df)
                else:
                    print(f"Skipping empty CSV file: {csv_file}")
            except pd.errors.EmptyDataError:
                print(f"Skipping empty CSV file: {csv_file}")

        # Check if any valid dataframes exist
        if valid_dataframes:
            # Concatenate the valid dataframes
            merged_df = pd.concat(valid_dataframes, ignore_index=True)

            # Define the path for the merged CSV file
            merged_csv_path = os.path.join(folder_path, "merged.csv")

            # Save the merged dataframe as a CSV file
            merged_df.to_csv(merged_csv_path, index=False)

            # Return the path of the merged CSV file
            return merged_csv_path
        else:
            print("No valid dataframes found.")
        # if table_csv_files:
        #     merged_df = pd.concat([pd.read_csv(csv_file) for csv_file in table_csv_files], ignore_index=True)
        #     merged_csv_path = os.path.join(folder_path, "merged.csv")
        #     merged_df.to_csv(merged_csv_path, index=False)
        #     return merged_csv_path
    else:
        print("Image filepath is: ", file_path)
        preprocessed_image, file_path = image_preprocess(file_path)
        if preprocessed_image is not None:
            file_name, file_ext = os.path.splitext(file_path)
            file_prefix = file_name
            print("here the given path after processing the image is: ",file_path)
            table_csv_files = get_table_csv_results2(file_path, file_prefix, option)
            print(table_csv_files)
        else:
            table_csv_files = []
    return table_csv_files

def image_preprocess(file_path):
    start_time = time.time()
    preprocessor = ImagePreprocessor(file_path)
    preprocessed_image = preprocessor.preprocess()
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    #print("Time taken by pre-processing module: ", elapsed_time)

    if preprocessed_image is None or preprocessed_image.size == 0:
        print("Image is empty!")
        return None, None
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    processed_file_name = file_name + "_processed" + file_ext
    processed_file_path = os.path.join(os.path.dirname(file_path), processed_file_name)

    # Display the pre-processed image
    cv2.imwrite(file_path, preprocessed_image)
    return preprocessed_image, processed_file_path

if __name__ == "__main__":
    freeze_support()
    file_name = sys.argv[1]
    #option = sys.argv[2]
    extract_all(file_name,option='pharmeasy')