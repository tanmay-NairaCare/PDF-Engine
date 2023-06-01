from trp import Document
import os
import boto3
import sys
from pprint import pprint
from convert_pdf_to_image import convert_pdf_to_image
import csv,re
import pandas as pd
from test_keywords import pharmeasy_keywords,tata1mg_test_names, metropolis_keywords, trutest_keywords, nm_medical_keywords
from standard_test_mapper import *
from converter import Converter

def get_table_csv_results2(file_name,file_prefix,option):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # Amazon Textract client
    session = boto3.Session()
    client = session.client('textract')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES','FORMS'])
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

    # Save form results in a CSV file(For forms)
    form_csv_file_path = file_prefix + '_forms_output.csv'
    form_csv_file = open(form_csv_file_path, 'a', newline='', encoding='utf-8')
    form_csv_writer = csv.writer(form_csv_file)

     # Process forms
    form_csv_writer.writerow(['key','value'])
    for page in doc.pages:
        for field in page.form.fields:
            form_csv_writer.writerow([field.key, field.value])
    form_csv_file.close()
    print("Forms csv writer path is: ",form_csv_file_path)
    return read_csv_and_extract_data(formatted_text,csv_file_path,file_prefix + "_final_output.csv",form_csv_file_path,option)


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
                'SGPT':r"\bSGPT/ALT\b\n([\d.]+)|\bSGPT\b\n(.+)", ##Updated
                # 'W.B.C. Count':r"Leucocytes Count\n([\d.]+)", # Here before it was Leucocytes Count
                # 'R.B.C. Count':r"Erythrocytes\n([\d.]+)", # Here before it was Erythrocytes Count
                'W.B.C. Count':r"\bW\.B\.C\. Count\b\n(.+)|\bLeucocytes Count\b\n([\d.]+)",
                'R.B.C. Count':r"\bR\.B\.C\. Count\b\n([.\d]+)|\bErythrocytes\b\n([\d.]+)",
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
                'T3 (Tri-iodothyronine)':r"\bT3 \(Tri-iodothyronine\)\b\n(.+)",
                'T4 (Thyroxine)':r"\bT4 \(Thyroxine\)\b\n(.+)",
                'TSH':r"\bTSH\b\n(.+)",
                'HbA1c':r"\bHbA1c\b\n(.+)",
                'Estimated Average Glucose (eAG)':r"Estimated Average Glucose \(eAG\)\s*:?[\s\n]*([\d.]+)",
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
                'Bilirubin (Total)':r"Bilirubin \(Total\)\n([\d.]+)", #Not added /b
                #'Bilirubin (Direct)':r"Bilirubin \(Direct\)\n([\d.]+)", #Pattern V1.0.0
                'Bilirubin (Direct)':r"Bilirubin \(Direct\)\n(?:SERUM\n)?([\d.]+)",# Pattern V2.0.0
                'Bilirubin (Indirect)':r"Bilirubin \(Indirect\)\n([\d.]+)",  #Not added /b
                'SGOT':r"\bSGOT\b\n(.+)|\bSGOT/AST\b\n([\d.]+)",
                #'SGPT':r"\bSGPT\b\n(.+)",
                'Alkaline Phosphatase':r"\bAlkaline Phosphatase\b\n([\d.]+)",
                'Total Proteins':r"\bTotal Proteins\b\n([\d.]+)",
                #'Albumin':r"Albumin\n([\d.]+)",
                'Globulin':r"\bGlobulin\b\n([\d.]+)",
                'Albumin/Globulin Ratio':r"\bA/G Ratio\b\n([\d.]+)",
                'Creatinine':r"\bCreatinine\b\n([\d.]+)",
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
                'Magnesium':r"\bMagnesium\b\n\s*:?\s*([\d.]+)",
                'Absorbance':r"\bAbsorbance\b\n([\d.]+)",
                #'Packed Cell Volume':r"\bPacked Cell Volume\b\n([\d.]+)",
                'Hepatitis C':r"\bDetection of HCV antibodies from the\b\n(.+)",
                'Hepatitis B':r"\bQualitative detection of Hepatitis B\b\n(.+)"
                
            }
            df = pd.DataFrame(columns=["Test", "Result"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r'(?:\s*SERUM\s*|\s*FLUORIDE PLASMA\s*|:|\(URINE\))', '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            print("+"*100)
            print(cleaned_text)
            print("+"*100)
            
            for test_description, test_pattern in test_patterns.items():
                #test_pattern_with_word_boundary = r"\b" + test_pattern + r"\b"
                matches = re.findall(test_pattern, cleaned_text, re.IGNORECASE)
                print(f"{test_description} : {len(matches)}")
                if matches:
                    #test_value = match.group(1)
                    if len(matches) == 1:
                        #print("hehe")
                        test_value = matches[0]
                    else:
                        #test_value = matches[0][0] or matches[0][1]
                        test_value = next((value for value in matches[0] if value), None)
                    print(test_value)
                    if isinstance(test_value, tuple):
                        test_value = test_value[0] or test_value[1]
                    print(f"{test_description} value: {test_value}")
    
                    # Create a new DataFrame with the test description and value
                    new_row = pd.DataFrame({"Test": [test_description], "Result": [test_value]})

                    # Concatenate the new row with the existing DataFrame
                    df = pd.concat([df, new_row], ignore_index=True, sort=False)
                else:
                    print(f"{test_description} value not found in the text file.")
            try:
                column_index=1
                if df.iloc[:, column_index].dtype == 'object':
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('fl', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace(':', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('ML', '') 
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('/hpf', '')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace(',', '.')
                    df.iloc[:, 1] = df.iloc[:, 1].str.replace('*', '')
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
            test_patterns = {
                'Vitamin B-12':r"VITAMIN B-12\n(.+)",
                'Blood Urea Nitrogen':r"BLOOD UREA NITROGEN \(BUN\)\n(.+)",
                'Calcium': r"CALCIUM\n(.+)",
                'Average Blood Glucose':r"AVERAGE BLOOD GLUCOSE \(ABG\)\n(.+)"
                #'Vitamin D':r"25-OH VITAMIN D \(TOTAL\)\n(.+)"
            }
            df = pd.DataFrame(columns=["TEST NAME ", "VALUE "])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            for test_description, test_pattern in test_patterns.items():
                match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                if match:
                    test_value = match.group(1)
                    test_value = test_value
                    print(f"{test_description} value: {test_value}")

                    # Create a new row in the DataFrame with the test description and value
                    #df = df.append({"Test": test_description, "Result": test_value},ignore_index=True, sort=False)
                    
                    # Create a new DataFrame with the test description and value
                    new_row = pd.DataFrame({"TEST NAME ": [test_description], "VALUE ": [test_value]})

                    # Concatenate the new row with the existing DataFrame
                    df = pd.concat([df, new_row], ignore_index=True, sort=False)
                else:
                    print(f"{test_description} value not found in the text file.")

            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                existing_df.columns = ["TEST NAME ","VALUE "]
                #print(existing_df.ndims)
                #existing_df = existing_df.iloc[:,0:2]
                #print(existing_df.ndims)
            except:
                existing_df = pd.DataFrame()
                print("Created empty dataframe!")
            if df.empty:
                existing_df.to_csv(output_table_file_path, columns=["TEST NAME ", "VALUE "], index=False)
            else:
                # Concatenate the existing DataFrame with the new DataFrame
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df[existing_df.notnull()]
                duplicates = existing_df.iloc[:,0].duplicated()
                # Filter out the duplicates
                existing_df = existing_df[~duplicates]
                existing_df.to_csv(output_table_file_path, columns=["TEST NAME ", "VALUE "], index=False)
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'tata 1mg':
        try:
            test_patterns = {
                "Creatinine":r"Creatinine\n(.+)",
                "Blood Glucose Fasting":r"Glucose - Fasting\n([\d.]+)",
                "PCV": r"HCT\n([\d.]+)",
                "MCHC":r"MCHC\n([\d.]+)"
                #'Vitamin D':r"25-OH VITAMIN D \(TOTAL\)\n(.+)"
            }
            df = pd.DataFrame(columns=["Test Name", "Result"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            for test_description, test_pattern in test_patterns.items():
                match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                if match:
                    test_value = match.group(1)
                    test_value = test_value
                    print(f"{test_description} value: {test_value}")
                    # Create a new DataFrame with the test description and value
                    new_row = pd.DataFrame({"Test Name": [test_description], "Result": [test_value]})

                    # Concatenate the new row with the existing DataFrame
                    df = pd.concat([df, new_row], ignore_index=True, sort=False)
                else:
                    print(f"{test_description} value not found in the text file.")

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
            test_patterns = {
                "Uric Acid":r"Uric Acid\n([\d.]+)",
                'T3 (Tri-iodothyronine)':r"Free T3\n([\d.]+)",
                'T4 (Thyroxine)':r"Free T4\n([\d.]+)"
                #'Vitamin D':r"25-OH VITAMIN D \(TOTAL\)\n(.+)"
            }
            df = pd.DataFrame(columns=["Investigation", "Observed Value"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\bC\.L\.I\.A\b|PHOTOMETRY|CALCULATED", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            for test_description, test_pattern in test_patterns.items():
                match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                if match:
                    test_value = match.group(1)
                    test_value = test_value
                    print(f"{test_description} value: {test_value}")
                    # Create a new DataFrame with the test description and value
                    new_row = pd.DataFrame({"Investigation": [test_description], "Observed Value": [test_value]})

                    # Concatenate the new row with the existing DataFrame
                    df = pd.concat([df, new_row], ignore_index=True, sort=False)
                else:
                    print(f"{test_description} value not found in the text file.")

            try:
                existing_df = pd.read_csv(output_table_file_path)
                print("Existing df is:",existing_df)
                existing_df = existing_df.rename(columns=lambda x: x.strip()) #Removing trailing spaces
                print(existing_df.columns)
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
            print("Raw data saved in dataframe!")
        except Exception as e:
            print("An error occurred:", str(e))
    elif option.lower() == 'trutest lab':
        try:
            test_patterns = {
                "Volume":r"Volume\n(.+)",
                'Colour (Urine)':r"Colour\n(.+)",
                'Appearance (Urine)':r"Transparency \(Appearance\)\n(.+)",
                'Deposit (Urine)':r"Deposit\n(.+)",
                "TSH": r'TSH Ultra\n([\d.]+)',
                "Haemoglobin": r'Hemoglobin \(Hb\)\n([\d.]+)',
                "R.B.C. Count": r'Erythrocyte \(RBC\) Count\n([\d.]+)',
                "Prostate Specific Antigen": r'PSA\n([\d.]+)\n',
                "pH (Urine)" : r'Reaction \(pH\)\n([\d.]+)',
                "Specific Gravity" : r'Specific Gravity\n([\d.]+)',
                'Urea/Creatinine Ratio':r"Urea/Creatinine Ratio\n([\d.]+)",
                "Pus Cells (Urine)":r"Pus Cells \(WBCs\)\n(.+)"
                #'Vitamin D':r"25-OH VITAMIN D \(TOTAL\)\n(.+)"
            }
            
            df = pd.DataFrame(columns=["Test Description", "Value(s)"])
            df.columns = df.columns.astype(str)
            lines = raw_text.split('\n')  # Split the raw text into lines
            lines_cleaned = [re.sub(r"\*", '', line, flags=re.IGNORECASE) for line in lines]
            cleaned_lines = [line.strip() for line in lines_cleaned if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            
            for test_description, test_pattern in test_patterns.items():
                match = re.search(test_pattern, cleaned_text,re.IGNORECASE)
                if match:
                    test_value = match.group(1)
                    test_value = test_value
                    print(f"{test_description} value: {test_value}")
                    # Create a new DataFrame with the test description and value
                    new_row = pd.DataFrame({"Test Description": [test_description], "Value(s)": [test_value]})

                    # Concatenate the new row with the existing DataFrame
                    df = pd.concat([df, new_row], ignore_index=True, sort=False)
                else:
                    print(f"{test_description} value not found in the text file.")
            print("MY TURN 2")
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
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names)  # Replace with standardized names
                    print(existing_df)
                    existing_df.to_csv(output_csv_file_path, index=False)
        except KeyError:
                    print("Name of the first column is not 'Test Name'")
    elif option.lower()=='metropolis':
        try:
                    existing_df = pd.read_csv(output_csv_file_path)
                    print("here the existing df is: ",existing_df)
                    test_names = tata1mg_test_names()
                    mapper = Mapper('metropolis',test_names) 
                    standardized_names = mapper.test_mapper('metropolis')
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].str.rstrip()  # Remove trailing whitespace
                    existing_df.iloc[:,0] = existing_df.iloc[:,0].replace(standardized_names)  # Replace with standardized names
                    existing_df.iloc[:,1] = existing_df.iloc[:,1].str.rstrip()  # Remove trailing whitespace
                    print(existing_df)
                    existing_df.to_csv(output_csv_file_path, index=False)
        except:
                    print("Name of the first column is not 'Test Name'")
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
                    print(existing_df)
                    existing_df.to_csv(output_csv_file_path, index=False)
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
                    print(existing_df)
                    existing_df.to_csv(output_csv_file_path, index=False)
            except KeyError:
                print("Name of the first column is not 'TEST NAME'")
    else:
        return    

def convert_to_standard_form(output_csv_file_path,option):
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

# CSV File Reader and Post-processing function
def read_csv_and_extract_data(raw_text, input_table_file_path, output_table_file_path, input_form_file_path, option):

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
    form_value_corrector(input_form_file_path,output_table_file_path,option)
    #lastly let us process the raw data
    extract_data_from_raw_text(raw_text,output_table_file_path,option)
    test_name_standardizer(output_table_file_path,option)
    convert_to_standard_form(output_table_file_path,option)
    return output_table_file_path

def form_value_corrector(input_form_file_path,output_table_file_path,option):
    # This function is going to process the form data 
    # Extract the CHLORIDE test name, transform its value
    # and append it to the final_output csv
 
    if option.lower()=="pharmeasy":
        print("Pharmeasy report selected!")
        if os.path.exists(input_form_file_path):
            print("Forms file is present at location",input_form_file_path)
        #print("Input Form File Path inside form_value_corrector() is: ",input_form_file_path)
        try:
            df = pd.read_csv(input_form_file_path)
            #print("Input Form DataFrame: ",df)
        except:
            print("Unable to open the Forms CSV. No content found!")
            return
        try:
            # search for the row that contains the key "CHLORIDE"
            chloride_row = df[df['key'] == 'CHLORIDE']
        
            # extract the value from the corresponding cell in the same row
            chloride_value = chloride_row['value'].iloc[0]
            
            # extract the numerical part of the value (assuming it's always formatted like "I.S.E 103,7 mmol/l")
            chloride_numerical = float(chloride_value.split()[1].replace(',', '.'))
            print(chloride_numerical)

            existing_df = pd.read_csv(output_table_file_path)

            # create new DataFrame with extracted values
            #new_df = pd.DataFrame({'CHLORIDE': [chloride_numerical]})
            new_df = pd.DataFrame({
                'TEST NAME ': ['CHLORIDE'],
                'TECHNOLOGY ': [' '],
                'VALUE ': [chloride_numerical],
                'UNITS ': [' ']
            })

            # append new DataFrame to existing DataFrame
            updated_df = existing_df.append(new_df, ignore_index=True)
            #updated_df = pd.concat([existing_df,new_df])

            # write updated DataFrame back to CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')

        except IndexError:
            print('No value found for Chloride')
    elif option.lower()=="tata 1mg":
        print("Hello from TATA 1mg")
        try:
            df = pd.read_csv(input_form_file_path)
            #print("Input Form DataFrame: ",df)
        except:
            print("Unable to open the Forms CSV. No content found!")
            return
        try:
            # Extract Urea row and value
            urea_row = df[df['key'] == 'Urea']
            urea_value = float(urea_row['value'].iloc[0])
        
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Urea'],
                    'Result': [urea_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Urea'],
                    'Result': [urea_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for Urea')
        try:
            # Extract Blood Urea Nitrogen row and value
            blood_urea_nitrogen_row = df[df['key'] == 'Blood Urea Nitrogen']
            blood_urea_nitrogen_value = float(blood_urea_nitrogen_row['value'].iloc[0])
        
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Blood Urea Nitrogen'],
                    'Result': [blood_urea_nitrogen_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Blood Urea Nitrogen'],
                    'Result': [blood_urea_nitrogen_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            #print("Writing updated CSV for Blood Urea Nitrogen!")
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for Blood Urea Nitrogen')
        try:
            # Extract Urea row and value
            uric_acid_row = df[df['key'] == 'Uric Acid']
            uric_acid_value = float(uric_acid_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Uric Acid'],
                    'Result': [uric_acid_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Name': ['Uric Acid'],
                    'Result': [uric_acid_value],
                    'Unit': [' '],
                    'Bio. Ref. Interval': [' '],
                    'Method': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for Uric Acid.')
    elif option.lower()=='metropolis':
        try:
            df = pd.read_csv(input_form_file_path)
            #print("Input Form DataFrame: ",df)
        except:
            print("Unable to open the Forms CSV. No content found!")
            return
        try:
            # Extract Urea row and value
            tsh_row = df[df['key'] == 'TSH(Ultrasensitive) (Serum,ECLIA)']
            tsh_value = float(tsh_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['TSH'],
                    'Observed Value ': [tsh_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['TSH'],
                    'Observed Value ': [tsh_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            print(updated_df)
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for TSH(Ultrasensitive).')
        try:
            # Extract Urea row and value
            t3_row = df[df['key'] == 'Free T3 (Serum,ECLIA)']
            t3_value = float(t3_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['T3 (Tri-iodothyronine)'],
                    'Observed Value ': [t3_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['T3 (Tri-iodothyronine)'],
                    'Observed Value ': [t3_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for Free T3.')
        try:
            # Extract Urea row and value
            hydroxy_row = df[df['key'] == '25 Hydroxy (OH) Vit D (Serum,ECLIA)']
            hydroxy_value = float(hydroxy_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['Vitamin D'],
                    'Observed Value ': [hydroxy_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Investigation ': ['Vitamin D'],
                    'Observed Value ': [hydroxy_value],
                    'Unit': [' '],
                    'Biological Reference Interval ': [' ']
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for 25 Hydroxy (OH) Vit D.')
    elif option.lower()=="trutest lab":
        print("TrueTest report selected!")
        try:
            df = pd.read_csv(input_form_file_path)
            #print("Input Form DataFrame: ",df)
        except:
            print("Unable to open the Forms CSV. No content found!")
            return
        try:
            # Extract BUN(Blood Urea Nitrogen) row and value
            bun_row = df[df['key'] == 'BUN*']
            bun_value = float(bun_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Description': ['BUN'],
                    'Value(s)': [bun_value],
                    'Reference Range': [' '],
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Description': ['BUN'],
                    'Value(s)': [bun_value],
                    'Reference Range': [' '],
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for BUN*.')
        try:
            # Extract BUN(Blood Urea Nitrogen) row and value
            urea_row = df[df['key'] == 'UREA*']
            urea_value = float(urea_row['value'].iloc[0])
           
            # Read existing DataFrame from output CSV file
            try:
                existing_df = pd.read_csv(output_table_file_path)
            except:
                existing_df = pd.DataFrame()

            # Check if existing DataFrame is empty
            if existing_df.empty:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Description': ['UREA'],
                    'Value(s)': [urea_value],
                    'Reference Range': [' '],
                })
                updated_df = new_df
                #print("Updated DataFrame is: ", updated_df)
            else:
                # Create new DataFrame with extracted values
                new_df = pd.DataFrame({
                    'Test Description': ['UREA'],
                    'Value(s)': [urea_value],
                    'Reference Range': [' '],
                })
                # Append new DataFrame to existing DataFrame
                updated_df = existing_df.append(new_df, ignore_index=True)
                updated_df = pd.concat([existing_df, new_df])
            # Write updated DataFrame back to output CSV file
            updated_df.to_csv(output_table_file_path, index=False, mode='w')
        except IndexError:
            print('No value found for UREA*.')
    else:
        return


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
                    given_test_names = ['IRON','TOTAL IRON BINDING CAPACITY (TIBC)', '% TRANSFERRIN SATURATION', 'UNSAT.IRON-BINDING CAPACITY(UIBC)','APOLIPOPROTEIN - A1','APOLIPOPROTEIN - B']
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
        
            df.to_csv(csv_path,index=False)
    
        elif option.lower()=='tata 1mg':
            print("TATA 1mg Selected!")
            test_names = tata1mg_test_names() # list of all tata 1MG test names
            
            #print(df['Result '].dtype)
            try:
                if df['Test Name '].str.startswith("0-1 major ASCVD").any():
                    mask = df['Test Name '].str.startswith("0-1 major ASCVD")
                    df.loc[mask, 'Test Name '] = None 
                    pass
                if df['Result '].dtype == 'object':
                    if df['Result '].str.contains('\s').any() or df['Result '].str.startswith('Glycosylated Hemoglobin').any():
                        #print("HELOOOOOOOOOOO")
                        df[['Result1', 'Result2']] = df['Result '].str.split(' ', n=1, expand=True)
                        #print( df[['Result1', 'Result2']])
                        df_new = pd.concat([df[['Test Name ', 'Result1']], pd.DataFrame({'Test Name ': ['Estimated average glucose (eAG)'], 'Result1': [df['Result2'].iloc[0]]})], ignore_index=True)
                        #print("New DataFrame is: ",df_new)
                        # rename 'Result1' to 'Result'
                        df_new = df_new.rename(columns={'Result1': 'Result '})
                        df_new.to_csv(csv_path,index=False)
                    else:
                        print("df['Result'] column only contains one value.SAFE!")
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

            df['Test Name '].dropna(inplace=True)
            df = df[df['Test Name '].notnull()]
            #df.dropna(inplace=True)
            df.to_csv(csv_path,index=False)

        elif option.lower()=='metropolis':
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
            try:
                df = pd.read_csv(csv_path)
                for index, row in df.iterrows():
                    name = row['Investigation ']
                    print(name)
                    for test_name in test_names:
                        if name.startswith(test_name):
                            df.at[index, 'Investigation '] = test_name
                            print(f"Replaced '{name}' with '{test_name}' at index {index}")
                            break
            except:
                print("Investigation column only contains a single test name OR Name of the Investigation is not in our Metropolis database.")
            ## Handling special case 
            '''Below given try catch block checks if the given TEST is present in our Metropolis test names database. If not present then we don't want that particular row as it contains some garbage text which we don't need.'''
            try:
                for index, row in df.iterrows():
                    name = row['Investigation ']
                    # TODO: I have commented the below line
                    # if (pd.notna(name) and not any(name.startswith(test_name.strip()) for test_name in test_names)) or not any(name.contains(test_name.strip()) for test_name in test_names):

                    if pd.notna(name) and not any(test_name.strip() in name for test_name in test_names):
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
            if 'Sodium (Serum,ISE) ' in df.columns:
                    #s=pd.Series(['Investigation ', 'Observed Value ', 'Unit ', 'Biological Reference Interval '])
                    # frame = {'Investigation':pd.Series() ,'Observed Value ':pd.Series(),'Unit ':pd.Series(), 'Biological Reference Interval ':pd.Series()}
                    # df1=pd.DataFrame(frame,index=None)
                    # df1.append(df)
                    column_list = list(df.columns)
                    column_list_dataframe = pd.DataFrame(column_list)
                    df.loc[len(df)] = column_list
                    columns=["Investigation", "Observed Value", "Unit", "Biological Reference Interval"]
                    df.columns=columns
            df.to_csv(csv_path,index=False)
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
                        if name.startswith(test_name):
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

def extract_all(file_path,option):
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
            #table_csv_files += get_table_csv_results2(image_path, file_prefix)
            table_csv_files.append(get_table_csv_results2(image_path, file_prefix,option))
        print(table_csv_files)
    else:
        file_prefix = file_name
        table_csv_files = get_table_csv_results2(file_path, file_prefix,option)
        print(table_csv_files)
    return table_csv_files

if __name__ == "__main__":
    file_name = sys.argv[1]
    #option = sys.argv[2]
    extract_all(file_name,option='pharmeasy')