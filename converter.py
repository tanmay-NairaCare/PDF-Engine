import pandas as pd

class Converter:
    def __init__(self, option):
        self.option=option
        self.standard_test_data = {
        "Microcytes":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "Macrocytes":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "Anisocytosis":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "Poikilocytosis":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "Hypochromia":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "G6-PDH Activity": {
            "unit": "U/g Hb",
            "reference_range": {"min": 4.6, "max": 13.5}
        },
        "Absorbance":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "CPK (Total)":{
            "unit": 'IU/L',
            "reference_range": {
                "min":46, "max":171
            }
        },
        "Leukocytes (Urine)":{ #Doubt
            "unit": 'None',
            "reference_range": {
                "value": "Negative"
            }
        },
        "LDH":{
            "unit": 'IU/L',
            "reference_range": {
                "min":0, "max":73
            }
        },
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {
                "men":  {"min": 0, "max": 15},
                "women":  {"min": 0, "max": 20}
            }
        },
        "Immature Granulocyte Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.4}
        },
        "Sodium": {
            "unit": "mmol/L",
            "reference_range": {"min": 135, "max": 145}
        },

        "Potassium": {
            "unit": "mmol/L",
            "reference_range": {"min": 3.5, "max": 5.5}
        },

        "Chlorides": {
            "unit": "mmol/L",
            "reference_range": {"min": 95, "max": 109}
        },

        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 30, "max": 100}
        },

        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 200, "max": 911}
        },

        "Iron": {
            "unit": "ug/dL",
            "reference_range": {
                "men": {"min": 65, "max": 176},
                "women": {"min": 50, "max": 170}
            }
        },
        "TIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 250, "max": 450}
        },

        "Transferrin Saturation": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 50}
        },

        "UIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 150, "max": 375}
        },

        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 240}
        },

        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 60}
        },

        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "HDL/LDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.40, "max":1}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 5}
        },
        "Triglycerides/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 2}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 500}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 5, "max": 40}
        },
        "Alkaline Phosphatase": {
            "unit": "IU/L",
            "reference_range": {"min": 44, "max": 147}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.9}
        },
        "GGTP": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 55}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1}
        },
        "SGOT": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 40}
        },
        "SGPT": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 41}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 6.0, "max": 8.3}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.4, "max": 5.4}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 2.3, "max": 3.5}
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {"min": 1.0, "max": 2.5}
        }, 
        "T3 (Tri-iodothyronine)": { #Reference range DOUBT! (Not sure)
            "unit": "ng/dL",
            "reference_range": {"min": 80, "max": 200}
        },
        "T4 (Thyroxine)": { #Not sure about the reference range!
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12}
        },
        "TSH": { # standard values are in Litre (Check later!)
            "unit": "uIU/mL",
            "reference_range": {"min": 0.35, "max": 8.9} #Max value in TruTest lab for 55yr-87yr old.
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 20}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 20}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.6, "max": 1.2}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {"min": 8.5, "max": 10.5}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 7.5}
        },
        "eGFR": {
            "unit": "mL/min/1.73m2",
            "reference_range": {"min": 90, "max": float("inf")}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value": "None"}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.005, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8.0}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value":"None"}
        },
        "Glucose (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 15}
        },
        "Ketones (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 5}
        },
        "Bilirubin (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Urobilinogen (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "Bile Salt (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Microalbumin": {
            "unit": "mg/L",
            "reference_range": {"min": 0, "max": 20}
        },
        "Mucus": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "/hpf",
            "reference_range":  {"min":0 ,"max":2}
        },
        "Pus Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min":0 ,"max":5}
        },
        "Epithelial Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min":0, "max" : 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Parasite": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },

        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "Bicarbonate": {
            "unit": "mmol/L",
            "reference_range": {"min": 20.0, "max": 31.0}
        },
        "Immature Granulocytes": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "R.B.C. Count": {
            "unit": "*10^6/uL",
            "reference_range": {"min": 4.0, "max": 5.5}
        },
        "W.B.C. Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 4.0, "max": 11.0}
        },
        "Nucleated R.B.C.": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0, "max": 2}
        },
        "Nucleated R.B.C. Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.5, "max": 17.5}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 38.8, "max": 50.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 80, "max": 100}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 33}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 32, "max": 36}
        },
        "RDW-SD": {
            "unit": "fL",
            "reference_range": {"min": 29, "max": 46}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.6}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 14}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9.0, "max": 17}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.5, "max": 11.5}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 450}
        },
        "PLCR": {
            "unit": "%",
            "reference_range": {"min": 13.5, "max": 43.5}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.108, "max": 0.5}
        },
        "Lipoprotein": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 130}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "APOLIPOPROTEIN - A1": {
            "unit": "mg/dL",
            "reference_range": {"min": 110, "max": 160}
        },
        "APOLIPOPROTEIN - B": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 130}
        },
        "APO B/A1": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1.5}
        },
        "Phosphorus": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 4.5}
        },
        "HS-CRP": {
            "unit": "mg/L",
            "reference_range": {"min": 0.0, "max": 10}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },
        "Deposit (Urine)": {
            "unit": "None",
            "reference_range": {"value" : "None"}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Prostate Specific Antigen": {
            "unit": "ng/mL",
            "reference_range": {"min": 0, "max": 4}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 1}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0, "max": 2} #confirm the ranges
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.0, "max": 0.5}
        },
        "Average Blood Glucose":{
            "unit": "mg/dL",
            "reference_range": {"min": 90.0, "max": 150}
        },
        "Magnesium": {
            "unit": "mg/dL",
            "reference_range": {"min": 1.6, "max": 2.6}
        },
        "Hepatitis C": {
            "unit": "None",
            "reference_range": {"min": 0.0, "max": 0.9}
        },
        "Hepatitis B": {
            "unit": "S/CO",
            "reference_range": {"min": 0.0, "max": 0.9}
        },
        "TB-Gold": {
            "unit": "IU/mL",
            "reference_range": {"min": 0.0, "max": 0.35}
        },
    }
        self.metropolis_test_data = {
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {"min": 0, "max": 15}
        },
        "Sodium": {
            "unit": "mmol/L",
            "reference_range": {"min": 136, "max": 145}
        },
        "Potassium": {
            "unit": "mmol/L",
            "reference_range": {"min": 3.5, "max": 5.1}
        },
        "Chlorides": {
            "unit": "mmol/L",
            "reference_range": {"min": 98, "max": 107}
        },
        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 10, "max": 100}
        },
        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 197, "max": 771}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                    "min": 0,
                    "max": 200
            }
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 60
            }
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 160
            }
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 3.5,
                "max": 5
            }
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 200
            }
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 2.5,
                "max": 3.5
            }
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 190
            }
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 6,
                "max": 38
            }
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {
                "min": 40,
                "max": 129
            }
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 1.2
            }
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.0,
                "max": 0.3
            }
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.1,
                "max": 1.0
            }
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {
                "min": 0,
                "max": 40
            }
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {
                "min": 0,
                "max": 41
            }
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {
                "min": 6.4,
                "max": 8.3
            }
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {
                "min": 3.5,
                "max": 5.2
            }
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {
                "min": 1.8,
                "max": 3.6
            }
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 1.1,
                "max": 2.2
            }
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "pg/mL",
            "reference_range": {
                "min": 2.0,
                "max": 4.4
            }
        },
        "T4 (Thyroxine)": {
            "unit": "ng/dL",
            "reference_range": {
                "min": 0.93,
                "max": 1.7
            }
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {
                "min": 0.54,
                "max": 5.3
            }
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 8.9,
                "max": 20.6
            }
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.90,
                "max": 1.30
            }
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 8.6,
                "max": 10.0
            }
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 3.4,
                "max": 7.0
            }
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.010, "max": 1.030}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Normal"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 2, "max": 4}
        },
        "Epithelial Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 70, "max": 126}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {
                "non_diabetic": {"min": 0, "max": 6.5},
            }
        },
        "W.B.C. Count": {
            "unit": "cells/cu.mm",
            "reference_range": {"min": 4300, "max": 10300}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 1}
        },
        "Hemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 12.0, "max": 15.5}
        },
        # "Hematocrit": {
        #     "unit": "%",
        #     "reference_range": {"min": 34.9, "max": 44.5}
        # },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 34}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 36}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 82, "max": 101}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 140, "max": 440}
        },
        "R.B.C. Count": {
            "unit": "mill/cu.mm",
            "reference_range": {"min": 4.4, "max": 6.0}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.8}
        },
        # "RDW-SD": {
        #     "unit": "fL",
        #     "reference_range": {"min": 39, "max": 46}
        # },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.8, "max": 11}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.2, "max": 0.5}
        },
        "Phosphorus": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 4.5}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": None, "max": None}
        },
        "Deposit (Urine)": {
            "unit": None,
            "reference_range": {"min": "Absent", "max": "Absent"}
        },
        "Absolute Neutrophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 2000, "max": 7000}
        },
        "Absolute Lymphocyte Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 1000, "max": 3000}
        },
        "Absolute Monocyte Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 200, "max": 1000}
        },
        "Absolute Basophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 20, "max": 100}
        },
        "Absolute Eosinophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 20, "max": 500}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 14, "max": 18}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 42, "max": 52}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9, "max": 22}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
    }
        self.pharmeasy_test_data = {
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {
                "male": {"min": 0, "max": 15},
                "female": {"min": 0, "max": 20}
            }
        },
        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 30, "max": 100}
        },
        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 211, "max": 911}
        },
        "Iron": {
            "unit": "ug/dL",
            "reference_range": {
                "male": {"min": 65, "max": 175},
                "female": {"min": 50, "max": 170}
            }
        },
        "TIBC": {
            "unit": "ug/dL",
            "reference_range": {
                "male": {"min": 225, "max": 535},
                "female": {"min": 215, "max": 535}
            }
        },
        "Transferrin Saturation": {
            "unit": "%",
            "reference_range": {"min": 13, "max": 45}
        },
        "UIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 162, "max": 368}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 200}
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 40, "max": 60}
        },
        "HDL/LDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.40, "max":1}
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 3, "max": 5}
        },
        "Triglycerides/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 3.12}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 150}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 1.5, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 5, "max": 40}
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {"min": 45, "max": 129}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.9}
        },
        "GGTP": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 38}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 2}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 31}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 34}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 5.7, "max": 8.2}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.2, "max": 4.8}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 2.5, "max": 3.4}
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.9, "max": 2}
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "ng/dL",
            "reference_range": {"min": 60, "max": 200}
        },
        "T4 (Thyroxine)": {
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {"min": 0.35, "max": 4.94}
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 17, "max": 43}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 25}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 52}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.55, "max": 1.02}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": "9:1", "max": "23:1"}
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {"min": 8.8, "max": 10.6}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.2, "max": 6.1}
        },
        "eGFR": {
            "unit": "mL/min/1.73m2",
            "reference_range": {"min": 90,"max":float('inf')}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value":"None"}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.003, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Bile Salt (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Microalbumin": {
            "unit": "mg/L",
            "reference_range": {"min": 0, "max": 20}
        },
        "Mucus": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Epithelial Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Parasite": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "Average Blood Glucose":{
            "unit": "mg/dL",
            "reference_range": {"min": 90.0, "max": 150}
        },
        "W.B.C. Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 4.0, "max": 10.0}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 10.0}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.0}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 2}
        },
        "Immature Granulocyte Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.4}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.1}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.5}
        },
        "Immature Granulocytes": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "R.B.C. Count": {
            "unit": "*10^6/uL",
            "reference_range": {"min": 3.9, "max": 4.8}
        },
        "Nucleated R.B.C.": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.01}
        },
        "Nucleated R.B.C. Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.01}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 12.0, "max": 15.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 36.0, "max": 46.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 83.0, "max": 101.0}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27.0, "max": 32.0}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 34.5}
        },
        "RDW-SD": {
            "unit": "fL",
            "reference_range": {"min": 39.0, "max": 46.0}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.0}
        },
        "PDW": {
            "unit": "fL",
            "reference_range": {"min": 9.6, "max": 15.2}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 6.5, "max": 12.0}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 400}
        },
        "PLCR": {
            "unit": "%",
            "reference_range": {"min": 19.7, "max": 42.4}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.19, "max": 0.39}
        },
        "Lipoprotein": {
            "unit": "mg/dL",
            "reference_range": {"min":0,"max": 30}
        },
        "HS-CRP": {
            "unit": "mg/L",
            "reference_range": {"min": 0.0, "max": 10}
        },
        "APOLIPOPROTEIN - A1": {
            "unit": "mg/dL",
            "reference_range": {"male": {"min": 86, "max": 152}, "female": {"min": 94, "max": 162}}
        },
        "APOLIPOPROTEIN - B": {
            "unit": "mg/dL",
            "reference_range": {"male": {"min": 56, "max": 145}, "female": {"min": 53, "max": 138}}
        },
        "APO B/A1": {
            "unit": "None",
            "reference_range": {"male": {"min": 0.4, "max": 1.26}, "female": {"min": 0.38, "max": 1.14}}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": None, "max": None}
        }
    }
        self.trutest_test_data = {
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0, "max": 240
            }
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0, "max": 200
            }
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 50}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 50}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {
                "21yr-54yr": {"min": 0.4, "max": 4.2},
                "55yr-87yr": {"min": 0.5, "max": 8.9}
            }
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 17, "max": 43}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 18.0}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 40, "max": 100}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.67, "max": 1.17}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.5, "max": 7.2}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.010, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Normal"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min": 0, "max": 5}
        },
        "Epithelial Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min": 0, "max": 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 70, "max": 125}
        },
        "W.B.C. Count": {
            "unit": "cells/cu.mm",
            "reference_range": {"min": 4000, "max": 10000}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 2}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1, "max": 2}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.0, "max": 0.5}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.5, "max": 18.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 42, "max": 52}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 78, "max": 100}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 31}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 32, "max": 36}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 15.0}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9, "max": 17}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.2, "max": 11.7}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 450}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.2, "max": 0.5}
        },
        "Deposit (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Prostate Specific Antigen": {
            "unit": "ng/mL",
            "reference_range": {"min": 0, "max": 4}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value": "None"}
        },
        "R.B.C. Count": {
            "unit": "mil/cu.mm",
            "reference_range": {"min":4.7, "max":6}
        }
        
    }
        self.tata1mg_test_data = {
        "Albumin/Globulin Ratio":{
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 4, "max": 5.6}
        },
        "Sodium": {
            "unit": "mEq/L",
            "reference_range": {"min": 132.0, "max": 146.0}
        },
        "Potassium": {
            "unit": "mEq/L",
            "reference_range": {"min": 3.5, "max": 5.5}
        },
        "Chlorides": {
            "unit": "mEq/L",
            "reference_range": {"min": 99.0, "max": 109.0}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 240}
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 60}
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 3.5, "max": 5}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 200}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 2.5, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 10, "max": 30}
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {"min": 45, "max": 129}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "GGTP": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 73}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 34}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"value":"None"}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 10, "max": 49}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 5.7, "max": 8.2}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.4, "max": 4.8}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 1.8, "max": 3.6}
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "ng/mL",
            "reference_range": {"min": 0.60, "max": 1.81}
        },
        "T4 (Thyroxine)": {
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12.6}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {"min": 0.55, "max": 4.78}
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 19.26, "max": 49.22}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 9.0, "max": 23.0}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.70, "max": 1.30}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": "12:1", "max": "20:1"}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.7, "max": 9.2}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 100}
        },
        "W.B.C. Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 4, "max": 10}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 1.0, "max": 10.0}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1.0, "max": 6.0}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 2}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.1}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.5}
        },
        "R.B.C. Count": {
            "unit": "mili/cu.mm",
            "reference_range": {"min": 4.5, "max": 5.5}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.0, "max": 17.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 40.0, "max": 50.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 83, "max": 101}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 32}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 34.5}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 14}
        },
        "PDW": {
            "unit": "fL",
            "reference_range": {"min": 11, "max": 22}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 6.5, "max": 12}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 410}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "None",
            # We can also put None here.
            "reference_range": {"value": "Undefined"}
        }
    }
        self.nm_medical_test_data = {
    "Leukocytes (Urine)":{ #Doubt
        "unit": 'None',
        "reference_range": {
                "value": "Negative"
            }
    },
    "ESR": {
        "unit": "mm/hr",
        "reference_range": {"min": 0, "max": 10}
    },
    "Sodium": {
        "unit": "mEq/L",
        "reference_range": {"min": 136, "max": 145}
    },
    "Potassium": {
        "unit": "mEq/L",
        "reference_range": {"min": 3.5, "max": 5.1}
    },
    "Chlorides": {
        "unit": "mEq/L",
        "reference_range": {"min": 98, "max": 107}
    },
    "Total Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0, "max": 200}
    },
    "HDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 40, "max": 60}
    },
    "LDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0, "max": 160}
    },
    "Total Cholesterol/HDL Cholesterol Ratio": {
        "unit": "None",
        "reference_range": {"min": 3.0, "max": 5.0}
    },
    "Triglycerides": {
        "unit": "mg/dL",
        "reference_range": {"min": 0,"max": 199}
    },
    "LDL/HDL Ratio": {
        "unit": "None",
        "reference_range": {"min": 0,"max": 3.5}
    },
    "Non-HDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0,"max": 190}
    },
    "VLDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 7, "max": 35}
    },
    "Alkaline Phosphatase": {
        "unit": "U/L",
        "reference_range": {"min": 40, "max": 150}
    },
    "Bilirubin (Total)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.2, "max": 1.2}
    },
    "Bilirubin (Direct)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.0, "max": 0.5}
    },
    "Bilirubin (Indirect)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.1, "max": 1.0}
    },
    "GGTP": {
        "unit": "U/L",
        "reference_range": {"min": 0,"max": 73}
    },
    "SGOT": {
        "unit": "U/L",
        "reference_range": {"min":0,"max": 35.0}
    },
    "SGPT": {
        "unit": "U/L",
        "reference_range": {"min": 10, "max": 49}
    },
    "Total Proteins": {
        "unit": "g/dL",
        "reference_range": {"min": 5.7, "max": 8.3}
    },
    "Albumin": {
        "unit": "g/dL",
        "reference_range": {"min": 3.2, "max": 5.2}
    },
    "Globulin": {
        "unit": "g/dL",
        "reference_range": {"min": 2.3, "max": 3.5}
    },
    "Albumin/Globulin Ratio": {
        "unit": "None",
        "reference_range": {"min": 1.1, "max": 2.20}
    },
    "T3 (Tri-iodothyronine)": {
        "unit": "ng/dL",
        "reference_range": {"min": 86, "max": 192}
    },
    "T4 (Thyroxine)": {
        "unit": "ug/dL",
        "reference_range": {"min": 4.5, "max": 10.9}
    },
    "TSH": {
        "unit": "uIU/mL",
        "reference_range": {"min": 0.48, "max": 4.17}
    },
    "Blood Urea": {
        "unit": "mg/dL",
        "reference_range": {"min": 14.98, "max": 44.9}
    },
    "Blood Urea Nitrogen": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.90, "max": 23.0}
    },
    "Creatinine": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.69, "max": 1.3}
    },
    "Blood Urea Nitrogen/Creatinine Ratio": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.3, "max": 10.6}
    },
    "Calcium": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.3, "max": 10.6}
    },
    "Uric Acid": {
        "unit": "mg/dL",
        "reference_range": {"min": 3.5, "max": 9.2}
    },
    "Volume": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Colour (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Appearance (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Specific Gravity": {
        "unit": "None",
        "reference_range": {"min": 1.003, "max": 1.035}
    },
    "pH (Urine)": {
        "unit": "None",
        "reference_range": {"min": 4.6, "max": 8.0}
    },
    "Protein (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Glucose (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Ketones (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Bilirubin (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Urobilinogen (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Normal"}
    },
    "Bile Salt (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Bile Pigment (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Blood (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Nitrite (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Red Blood Cells (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Pus Cells (Urine)": {
        "unit": "/hpf",
        "reference_range": {"min": 0, "max": 5}
    },
    "Epithelial Cells (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Casts": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Crystals": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Bacteria": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Yeast Cells": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Blood Glucose Fasting": {
        "unit": "mg/dL",
        "reference_range": {"min": 70, "max": 105}
    },
    "HbA1c": {
        "unit": "None",
        "reference_range": {
            "min": 0, "max": 6
        }
    },
    "W.B.C. Count": {
        "unit": "/c.mm",
        "reference_range": {"min": 4000, "max": 10000}
    },
    "Neutrophils": {
        "unit": "%",
        "reference_range": {"min": 40, "max": 80}
    },
    "Lymphocytes": {
        "unit": "%",
        "reference_range": {"min": 20, "max": 40}
    },
    "Monocytes": {
        "unit": "%",
        "reference_range": {"min": 2, "max": 10}
    },
    "Eosinophils": {
        "unit": "%",
        "reference_range": {"min": 1, "max": 6}
    },
    "Basophils": {
        "unit": "%",
        "reference_range": {"min": 0, "max": 2}
    },
    "Absolute Neutrophil Count": {
        "unit": "cells/cu.mm",
        "reference_range": {"min": 2000, "max": 7000}
    },
    "Absolute Lymphocyte Count": {
        "unit": "cells/cu.mm",
        "reference_range": {"min": 1000, "max": 3000}
    },
    "Absolute Monocyte Count": {
        "unit": "cells/c.mm",
        "reference_range": {"min": 200, "max": 1000}
    },
    "Absolute Eosinophil Count": {
        "unit": "cells/c.mm",
        "reference_range": {"min": 20, "max": 500}
    },
    "R.B.C. Count": {
        "unit": "mill/c.mm",
        "reference_range": {"min": 4.5, "max": 5.5}
    },
    "Haemoglobin": {
        "unit": "gm%",
        "reference_range": {"min": 13.0, "max": 17.0}
    },
    "PCV": {
        "unit": "%",
        "reference_range": {"min": 40, "max": 50}
    },
    "MCV": {
        "unit": "fL",
        "reference_range": {"min": 83, "max": 101}
    },
    "MCH": {
        "unit": "pg",
        "reference_range": {"min": 27, "max": 32}
    },
    "MCHC": {
        "unit": "g/dL",
        "reference_range": {"min": 31.5, "max": 34.5}
    },
    "Mean Platelet Volume": {
        "unit": "fL",
        "reference_range": {"min": 9.0, "max": 13.0}
    },
    "Platelet Count": {
        "unit": "*10^3/c.mm",
        "reference_range": {"min": 150, "max": 410}
    },
    "Phosphorus": {
        "unit": "mg/dL",
        "reference_range": {"min": 2.3, "max": 5.1}
    },
    "Estimated Average Glucose (eAG)": {
        "unit": "mg/dL",
        "reference_range": {"value":"None"}
    },
    "Deposit (Urine)": {
        "unit": "None",
        "reference_range": {"value": "Absent"} 
    },
    "Amorphous Materials (Urine)": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "CPK (Total)": {
        "unit": "U/L",
        "reference_range": {"min": 30, "max": 171}
    },
    "LDH": {
        "unit": "U/L",
        "reference_range": {"min": 120, "max": 246}
    },
    "Bicarbonate": {
        "unit": "mmol/L",
        "reference_range": {"min": 20.0, "max": 31.0}
    },
    "Microcytes": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "Macrocytes": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "Anisocytosis": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Poikilocytosis": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Hypochromia": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "RDW": {
        "unit": "%",
        "reference_range": {"min": 11.6, "max": 14.0}
    },
    "Magnesium": {
        "unit": "None",
        "reference_range": {"min": 1.6, "max": 2.6}
    },
    "Trichomonas Vaginalis": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "G6-PDH Activity": {
        "unit": "U/g Hb",
        "reference_range": {"min": 4.6, "max": 13.5}
    },
    "Absorbance": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Hepatitis C": {
        "unit": "None",
        "reference_range": {"min": 0, "max": 0.9}
    },
    "Hepatitis B": {
        "unit": "S/CO",
        "reference_range": {"min": 0, "max": 0.9}
    },
    "TB-Gold": {
        "unit": "IU/mL",
        "reference_range": {"min": 0.0, "max": 0.35}
    },
    "Mucus": {
        "unit": "None",
        "reference_range": {"value": "None"}
    }
}

    def convert_value(self, value, from_unit, to_unit, test_name, gender=None):
        # Define conversion factors for different units
        conversion_factors = {
            "mg/dL": {
                "ug/dL": 10,
                "ng/mL": 1000,
                "umol/L": 0.02238
            },
            "pg": {
                "ng": 0.001,
                "ug": 0.000001
            },
            "fL": {
                "uL": 0.000001,
                "mL": 0.000000001,
                "%":1
            },
            "uiU/dL": {
                "mIU/L": 0.1
            },
            "/c.mm": {
                "*10^9/L": 0.001,
                "*10^6/uL": 0.001
            },
            "*10^9/L": {
                "/c.mm": 1000,
                "*10^6/uL": 1000
            },
            "*10^6/uL": {
                "/c.mm": 1000,
                "*10^9/L": 1000
            },
            "mill/cu.mm": {
                "*10^6/uL": 1
            },
            "mil/cu.mm": {
                "*10^6/uL": 1
            },
            "mili/cu.mm": {
                "*10^6/uL": 1
            },
            "mill/c.mm": {
                "*10^6/uL": 1
            },
            "*10^6/uL": {
                "mill/cu.mm": 1
            },
            'cells/cu.mm':{
                "*10^3/uL" : 0.001,
                '*10^9/L' : 0.001
            },
            "cells/c.mm":{
                "*10^3/uL" : 0.001,
                '*10^9/L' : 0.001
            },
            "*10^3/uL" :{
                'cells/cu.mm':1,
                "*10^9/L":1
            },
            "ng/dL": {
                "pg/mL": 10
            },
            "pg/mL": {
                "ng/dL": 0.1
            },
            "U/L":{
                "IU/L": 1
            },
            "uIU/mL": {
                "mIU/mL": 1.0,
                "uIU/L": 1000.0,
                "uIU/mL" :1
            },
            "ng/dL":{
                "ug/dL":0.001
            },
            "ng/mL":{
                "ng/dL":100
            },
            "mEq/L":{
                "mmol/L":1
            },
            "gm%":{
                "g/dL" : 1
            },
            "*10^3/c.mm":{
                "*10^3/uL" : 1
            },
        }

        # Conversion factor for gender-specific reference range adjustment
        gender_conversion_factor = {
            "men": 1.0,
            "women": 1.2
        }

        if (from_unit is None or to_unit is None) or (from_unit == "None" or to_unit == "None"):
            return value

        if gender is not None and gender in gender_conversion_factor:
            value *= gender_conversion_factor[gender]

        if isinstance(value, str) and value.isnumeric():
            value = float(value)

        if from_unit == to_unit:
            return value
        elif from_unit in conversion_factors and to_unit in conversion_factors[from_unit]:
            conversion_factor = conversion_factors[from_unit][to_unit]
            if isinstance(value, str) and "," in value:
                value = value.replace(",", "")
            if isinstance(value, str) and value.lower() == "within normal limits":
                return value
            converted_value = float(value) * float(conversion_factor)
            return converted_value
        else:
            raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")

    def convert_test_values(self, test_name, test_value):
        standard_unit = self.standard_test_data[test_name]["unit"]
        if self.option.lower()=='metropolis':
            source_unit = self.metropolis_test_data[test_name]["unit"]
        elif self.option.lower()=='pharmeasy':
            source_unit = self.pharmeasy_test_data[test_name]["unit"]
        elif self.option.lower()=='tata 1mg':
            source_unit = self.tata1mg_test_data[test_name]["unit"]
        elif self.option.lower()=="trutest lab":
            source_unit = self.trutest_test_data[test_name]["unit"]
        elif self.option.lower()=='nm medical':
            source_unit = self.nm_medical_test_data[test_name]["unit"]
        print("Current test name:", test_name)
        converted_value = self.convert_value(test_value, source_unit, standard_unit, test_name)
        print(f"Converted value of {test_name} is:", converted_value)
        return converted_value

    def process_data(self, nm_data):
        converted_values = {}
        for _, row in nm_data.iterrows():
           
            test_name = row[0]
            test_value = row[1]

            converted_value = self.convert_test_values(test_name, test_value)
            converted_values[test_name] = converted_value

        print("*" * 50)
        sr_no = 0
        for test_name, converted_value in converted_values.items():
            sr_no = sr_no + 1
            print(f"{sr_no}. {test_name}: {converted_value}")
        return converted_values


def get_standard_test_data():
    standard_test_data = {
        "Microcytes":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "Macrocytes":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "Anisocytosis":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "Poikilocytosis":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "Hypochromia":{
            "unit": '%',
            "reference_range": {
                "value": "None"
            }
        },
        "G6-PDH Activity": {
            "unit": "U/g Hb",
            "reference_range": {"min": 4.6, "max": 13.5}
        },
        "Absorbance":{
            "unit": 'None',
            "reference_range": {
                "value": "None"
            }
        },
        "CPK (Total)":{
            "unit": 'IU/L',
            "reference_range": {
                "min":46, "max":171
            }
        },
        "Leukocytes (Urine)":{ #Doubt
            "unit": 'None',
            "reference_range": {
                "value": "Negative"
            }
        },
        "LDH":{
            "unit": 'IU/L',
            "reference_range": {
                "min":0, "max":73
            }
        },
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {
                "men":  {"min": 0, "max": 15},
                "women":  {"min": 0, "max": 20}
            }
        },
        "Immature Granulocyte Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.4}
        },
        "Sodium": {
            "unit": "mmol/L",
            "reference_range": {"min": 135, "max": 145}
        },

        "Potassium": {
            "unit": "mmol/L",
            "reference_range": {"min": 3.5, "max": 5.5}
        },

        "Chlorides": {
            "unit": "mmol/L",
            "reference_range": {"min": 95, "max": 109}
        },

        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 30, "max": 100}
        },

        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 200, "max": 911}
        },

        "Iron": {
            "unit": "ug/dL",
            "reference_range": {
                "men": {"min": 65, "max": 176},
                "women": {"min": 50, "max": 170}
            }
        },
        "TIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 250, "max": 450}
        },

        "Transferrin Saturation": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 50}
        },

        "UIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 150, "max": 375}
        },

        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 240}
        },

        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 60}
        },

        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "HDL/LDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.40, "max":1}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 5}
        },
        "Triglycerides/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 2}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 500}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 5, "max": 40}
        },
        "Alkaline Phosphatase": {
            "unit": "IU/L",
            "reference_range": {"min": 44, "max": 147}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.9}
        },
        "GGTP": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 55}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1}
        },
        "SGOT": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 40}
        },
        "SGPT": {
            "unit": "IU/L",
            "reference_range": {"min": 0, "max": 41}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 6.0, "max": 8.3}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.4, "max": 5.4}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 2.3, "max": 3.5}
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {"min": 1.0, "max": 2.5}
        }, 
        "T3 (Tri-iodothyronine)": { #Reference range DOUBT! (Not sure)
            "unit": "ng/dL",
            "reference_range": {"min": 80, "max": 200}
        },
        "T4 (Thyroxine)": { #Not sure about the reference range!
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12}
        },
        "TSH": { # standard values are in Litre (Check later!)
            "unit": "uIU/mL",
            "reference_range": {"min": 0.35, "max": 8.9} #Max value in TruTest lab for 55yr-87yr old.
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 20}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 20}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.6, "max": 1.2}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {"min": 8.5, "max": 10.5}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 7.5}
        },
        "eGFR": {
            "unit": "mL/min/1.73m2",
            "reference_range": {"min": 90, "max": float("inf")}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value": "None"}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.005, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8.0}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value":"None"}
        },
        "Glucose (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 15}
        },
        "Ketones (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 5}
        },
        "Bilirubin (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Urobilinogen (Urine)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "Bile Salt (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Microalbumin": {
            "unit": "mg/L",
            "reference_range": {"min": 0, "max": 20}
        },
        "Mucus": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "/hpf",
            "reference_range":  {"min":0 ,"max":2}
        },
        "Pus Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min":0 ,"max":5}
        },
        "Epithelial Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min":0, "max" : 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Parasite": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },

        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "Bicarbonate": {
            "unit": "mmol/L",
            "reference_range": {"min": 20.0, "max": 31.0}
        },
        "Immature Granulocytes": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "R.B.C. Count": {
            "unit": "*10^6/uL",
            "reference_range": {"min": 4.0, "max": 5.5}
        },
        "W.B.C. Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 4.0, "max": 11.0}
        },
        "Nucleated R.B.C.": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0, "max": 2}
        },
        "Nucleated R.B.C. Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.5, "max": 17.5}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 38.8, "max": 50.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 80, "max": 100}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 33}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 32, "max": 36}
        },
        "RDW-SD": {
            "unit": "fL",
            "reference_range": {"min": 29, "max": 46}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.6}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 14}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9.0, "max": 17}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.5, "max": 11.5}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 450}
        },
        "PLCR": {
            "unit": "%",
            "reference_range": {"min": 13.5, "max": 43.5}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.108, "max": 0.5}
        },
        "Lipoprotein": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 130}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "APOLIPOPROTEIN - A1": {
            "unit": "mg/dL",
            "reference_range": {"min": 110, "max": 160}
        },
        "APOLIPOPROTEIN - B": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 130}
        },
        "APO B/A1": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1.5}
        },
        "Phosphorus": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 4.5}
        },
        "HS-CRP": {
            "unit": "mg/L",
            "reference_range": {"min": 0.0, "max": 10}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },
        "Deposit (Urine)": {
            "unit": "None",
            "reference_range": {"value" : "None"}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "Prostate Specific Antigen": {
            "unit": "ng/mL",
            "reference_range": {"min": 0, "max": 4}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 1}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0, "max": 2} #confirm the ranges
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.0, "max": 0.5}
        },
        "Average Blood Glucose":{
            "unit": "mg/dL",
            "reference_range": {"min": 90.0, "max": 150}
        },
        "Magnesium": {
            "unit": "mg/dL",
            "reference_range": {"min": 1.6, "max": 2.6}
        },
        "Hepatitis C": {
            "unit": "None",
            "reference_range": {"min": 0.0, "max": 0.9}
        },
        "Hepatitis B": {
            "unit": "S/CO",
            "reference_range": {"min": 0.0, "max": 0.9}
        },
        "TB-Gold": {
            "unit": "IU/mL",
            "reference_range": {"min": 0.0, "max": 0.35}
        },
    }
    return standard_test_data


def get_metropolis_test_data():
    metropolis_data = {
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {"min": 0, "max": 15}
        },
        "Sodium": {
            "unit": "mmol/L",
            "reference_range": {"min": 136, "max": 145}
        },
        "Potassium": {
            "unit": "mmol/L",
            "reference_range": {"min": 3.5, "max": 5.1}
        },
        "Chlorides": {
            "unit": "mmol/L",
            "reference_range": {"min": 98, "max": 107}
        },
        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 10, "max": 100}
        },
        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 197, "max": 771}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                    "min": 0,
                    "max": 200
            }
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 60
            }
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 160
            }
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 3.5,
                "max": 5
            }
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 200
            }
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 2.5,
                "max": 3.5
            }
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 190
            }
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 6,
                "max": 38
            }
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {
                "min": 40,
                "max": 129
            }
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0,
                "max": 1.2
            }
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.0,
                "max": 0.3
            }
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.1,
                "max": 1.0
            }
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {
                "min": 0,
                "max": 40
            }
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {
                "min": 0,
                "max": 41
            }
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {
                "min": 6.4,
                "max": 8.3
            }
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {
                "min": 3.5,
                "max": 5.2
            }
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {
                "min": 1.8,
                "max": 3.6
            }
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {
                "min": 1.1,
                "max": 2.2
            }
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "pg/mL",
            "reference_range": {
                "min": 2.0,
                "max": 4.4
            }
        },
        "T4 (Thyroxine)": {
            "unit": "ng/dL",
            "reference_range": {
                "min": 0.93,
                "max": 1.7
            }
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {
                "min": 0.54,
                "max": 5.3
            }
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 8.9,
                "max": 20.6
            }
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0.90,
                "max": 1.30
            }
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 8.6,
                "max": 10.0
            }
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 3.4,
                "max": 7.0
            }
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.010, "max": 1.030}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Normal"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Negative"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 2, "max": 4}
        },
        "Epithelial Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 1}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 70, "max": 126}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {
                "non_diabetic": {"min": 0, "max": 6.5},
            }
        },
        "W.B.C. Count": {
            "unit": "cells/cu.mm",
            "reference_range": {"min": 4300, "max": 10300}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 1}
        },
        "Hemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 12.0, "max": 15.5}
        },
        # "Hematocrit": {
        #     "unit": "%",
        #     "reference_range": {"min": 34.9, "max": 44.5}
        # },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 34}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 36}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 82, "max": 101}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 140, "max": 440}
        },
        "R.B.C. Count": {
            "unit": "mill/cu.mm",
            "reference_range": {"min": 4.4, "max": 6.0}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.8}
        },
        # "RDW-SD": {
        #     "unit": "fL",
        #     "reference_range": {"min": 39, "max": 46}
        # },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.8, "max": 11}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.2, "max": 0.5}
        },
        "Phosphorus": {
            "unit": "mg/dL",
            "reference_range": {"min": 2.5, "max": 4.5}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": None, "max": None}
        },
        "Deposit (Urine)": {
            "unit": None,
            "reference_range": {"min": "Absent", "max": "Absent"}
        },
        "Absolute Neutrophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 2000, "max": 7000}
        },
        "Absolute Lymphocyte Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 1000, "max": 3000}
        },
        "Absolute Monocyte Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 200, "max": 1000}
        },
        "Absolute Basophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 20, "max": 100}
        },
        "Absolute Eosinophil Count": {
            "unit": "/c.mm",
            "reference_range": {"min": 20, "max": 500}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 14, "max": 18}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 42, "max": 52}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9, "max": 22}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
    }

    return metropolis_data


def get_pharmeasy_test_data():
    pharmeasy_test_data = {
        "ESR": {
            "unit": "mm/hr",
            "reference_range": {
                "male": {"min": 0, "max": 15},
                "female": {"min": 0, "max": 20}
            }
        },
        "Vitamin D": {
            "unit": "ng/mL",
            "reference_range": {"min": 30, "max": 100}
        },
        "Vitamin B-12": {
            "unit": "pg/mL",
            "reference_range": {"min": 211, "max": 911}
        },
        "Iron": {
            "unit": "ug/dL",
            "reference_range": {
                "male": {"min": 65, "max": 175},
                "female": {"min": 50, "max": 170}
            }
        },
        "TIBC": {
            "unit": "ug/dL",
            "reference_range": {
                "male": {"min": 225, "max": 535},
                "female": {"min": 215, "max": 535}
            }
        },
        "Transferrin Saturation": {
            "unit": "%",
            "reference_range": {"min": 13, "max": 45}
        },
        "UIBC": {
            "unit": "ug/dL",
            "reference_range": {"min": 162, "max": 368}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 200}
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 40, "max": 60}
        },
        "HDL/LDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.40, "max":1}
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 3, "max": 5}
        },
        "Triglycerides/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 3.12}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 150}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 1.5, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 5, "max": 40}
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {"min": 45, "max": 129}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.9}
        },
        "GGTP": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 38}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 2}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 31}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 34}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 5.7, "max": 8.2}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.2, "max": 4.8}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 2.5, "max": 3.4}
        },
        "Albumin/Globulin Ratio": {
            "unit": "None",
            "reference_range": {"min": 0.9, "max": 2}
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "ng/dL",
            "reference_range": {"min": 60, "max": 200}
        },
        "T4 (Thyroxine)": {
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {"min": 0.35, "max": 4.94}
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 17, "max": 43}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 25}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 52}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.55, "max": 1.02}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": "9:1", "max": "23:1"}
        },
        "Calcium": {
            "unit": "mg/dL",
            "reference_range": {"min": 8.8, "max": 10.6}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.2, "max": 6.1}
        },
        "eGFR": {
            "unit": "mL/min/1.73m2",
            "reference_range": {"min": 90,"max":float('inf')}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value":"None"}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.003, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Bile Salt (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Microalbumin": {
            "unit": "mg/L",
            "reference_range": {"min": 0, "max": 20}
        },
        "Mucus": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Epithelial Cells (Urine)": {
            "unit": "None",
            "reference_range": {"min": 0, "max": 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Parasite": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 126}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.5}
        },
        "Average Blood Glucose":{
            "unit": "mg/dL",
            "reference_range": {"min": 90.0, "max": 150}
        },
        "W.B.C. Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 4.0, "max": 10.0}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 10.0}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 6.0}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 2}
        },
        "Immature Granulocyte Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.4}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.1}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.5}
        },
        "Immature Granulocytes": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.3}
        },
        "R.B.C. Count": {
            "unit": "*10^6/uL",
            "reference_range": {"min": 3.9, "max": 4.8}
        },
        "Nucleated R.B.C.": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.01}
        },
        "Nucleated R.B.C. Percentage": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 0.01}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 12.0, "max": 15.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 36.0, "max": 46.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 83.0, "max": 101.0}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27.0, "max": 32.0}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 34.5}
        },
        "RDW-SD": {
            "unit": "fL",
            "reference_range": {"min": 39.0, "max": 46.0}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.6, "max": 14.0}
        },
        "PDW": {
            "unit": "fL",
            "reference_range": {"min": 9.6, "max": 15.2}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 6.5, "max": 12.0}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 400}
        },
        "PLCR": {
            "unit": "%",
            "reference_range": {"min": 19.7, "max": 42.4}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.19, "max": 0.39}
        },
        "Lipoprotein": {
            "unit": "mg/dL",
            "reference_range": {"min":0,"max": 30}
        },
        "HS-CRP": {
            "unit": "mg/L",
            "reference_range": {"min": 0.0, "max": 10}
        },
        "APOLIPOPROTEIN - A1": {
            "unit": "mg/dL",
            "reference_range": {"male": {"min": 86, "max": 152}, "female": {"min": 94, "max": 162}}
        },
        "APOLIPOPROTEIN - B": {
            "unit": "mg/dL",
            "reference_range": {"male": {"min": 56, "max": 145}, "female": {"min": 53, "max": 138}}
        },
        "APO B/A1": {
            "unit": "None",
            "reference_range": {"male": {"min": 0.4, "max": 1.26}, "female": {"min": 0.38, "max": 1.14}}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "mg/dL",
            "reference_range": {"min": None, "max": None}
        }
    }
    return pharmeasy_test_data


def get_tata1mg_test_data():
    tata1mg_test_data = {
        "Albumin/Globulin Ratio":{
            "unit": "None",
            "reference_range": {"value": "None"}
        },
        "HbA1c": {
            "unit": "%",
            "reference_range": {"min": 4, "max": 5.6}
        },
        "Sodium": {
            "unit": "mEq/L",
            "reference_range": {"min": 132.0, "max": 146.0}
        },
        "Potassium": {
            "unit": "mEq/L",
            "reference_range": {"min": 3.5, "max": 5.5}
        },
        "Chlorides": {
            "unit": "mEq/L",
            "reference_range": {"min": 99.0, "max": 109.0}
        },
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 240}
        },
        "HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 60}
        },
        "LDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 160}
        },
        "Total Cholesterol/HDL Cholesterol Ratio": {
            "unit": "None",
            "reference_range": {"min": 3.5, "max": 5}
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 200}
        },
        "LDL/HDL Ratio": {
            "unit": "None",
            "reference_range": {"min": 2.5, "max": 3.5}
        },
        "Non-HDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 190}
        },
        "VLDL Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {"min": 10, "max": 30}
        },
        "Alkaline Phosphatase": {
            "unit": "U/L",
            "reference_range": {"min": 45, "max": 129}
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.0, "max": 0.3}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "GGTP": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 73}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 34}
        },
        "SGOT/SGPT Ratio": {
            "unit": "None",
            "reference_range": {"value":"None"}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 10, "max": 49}
        },
        "Total Proteins": {
            "unit": "g/dL",
            "reference_range": {"min": 5.7, "max": 8.2}
        },
        "Albumin": {
            "unit": "g/dL",
            "reference_range": {"min": 3.4, "max": 4.8}
        },
        "Globulin": {
            "unit": "g/dL",
            "reference_range": {"min": 1.8, "max": 3.6}
        },
        "T3 (Tri-iodothyronine)": {
            "unit": "ng/mL",
            "reference_range": {"min": 0.60, "max": 1.81}
        },
        "T4 (Thyroxine)": {
            "unit": "ug/dL",
            "reference_range": {"min": 4.5, "max": 12.6}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {"min": 0.55, "max": 4.78}
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 19.26, "max": 49.22}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 9.0, "max": 23.0}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.70, "max": 1.30}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": "12:1", "max": "20:1"}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.7, "max": 9.2}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {"min": 70, "max": 100}
        },
        "W.B.C. Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 4, "max": 10}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 1.0, "max": 10.0}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1.0, "max": 6.0}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 0, "max": 2}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0, "max": 0.1}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 0.02, "max": 0.5}
        },
        "R.B.C. Count": {
            "unit": "mili/cu.mm",
            "reference_range": {"min": 4.5, "max": 5.5}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.0, "max": 17.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 40.0, "max": 50.0}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 83, "max": 101}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 32}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 31.5, "max": 34.5}
        },
        "RDW-CV": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 14}
        },
        "PDW": {
            "unit": "fL",
            "reference_range": {"min": 11, "max": 22}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 6.5, "max": 12}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 410}
        },
        "Estimated Average Glucose (eAG)": {
            "unit": "None",
            # We can also put None here.
            "reference_range": {"value": "Undefined"}
        }
    }
    return tata1mg_test_data


def get_trutest_test_data():
    trutest_lab_test_data = {
        "Total Cholesterol": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0, "max": 240
            }
        },
        "Triglycerides": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 0, "max": 200
            }
        },
        "Bilirubin (Total)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.3, "max": 1.2}
        },
        "Bilirubin (Direct)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0, "max": 0.2}
        },
        "Bilirubin (Indirect)": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.1, "max": 1.0}
        },
        "SGOT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 50}
        },
        "SGPT": {
            "unit": "U/L",
            "reference_range": {"min": 0, "max": 50}
        },
        "TSH": {
            "unit": "uIU/mL",
            "reference_range": {
                "21yr-54yr": {"min": 0.4, "max": 4.2},
                "55yr-87yr": {"min": 0.5, "max": 8.9}
            }
        },
        "Blood Urea": {
            "unit": "mg/dL",
            "reference_range": {"min": 17, "max": 43}
        },
        "Blood Urea Nitrogen": {
            "unit": "mg/dL",
            "reference_range": {"min": 7, "max": 18.0}
        },
        "Urea/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 40, "max": 100}
        },
        "Creatinine": {
            "unit": "mg/dL",
            "reference_range": {"min": 0.67, "max": 1.17}
        },
        "Blood Urea Nitrogen/Creatinine Ratio": {
            "unit": "None",
            "reference_range": {"min": 10, "max": 20}
        },
        "Uric Acid": {
            "unit": "mg/dL",
            "reference_range": {"min": 3.5, "max": 7.2}
        },
        "Colour (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Pale Yellow"}
        },
        "Appearance (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Clear"}
        },
        "Specific Gravity": {
            "unit": "None",
            "reference_range": {"min": 1.010, "max": 1.030}
        },
        "pH (Urine)": {
            "unit": "None",
            "reference_range": {"min": 4.5, "max": 8}
        },
        "Protein (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Glucose (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Ketones (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bilirubin (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Urobilinogen (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Normal"}
        },
        "Bile Pigment (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Nitrite (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Red Blood Cells (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Pus Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min": 0, "max": 5}
        },
        "Epithelial Cells (Urine)": {
            "unit": "/hpf",
            "reference_range": {"min": 0, "max": 4}
        },
        "Casts": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Crystals": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Bacteria": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Yeast Cells": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Blood Glucose Fasting": {
            "unit": "mg/dL",
            "reference_range": {
                "min": 70, "max": 125}
        },
        "W.B.C. Count": {
            "unit": "cells/cu.mm",
            "reference_range": {"min": 4000, "max": 10000}
        },
        "Neutrophils": {
            "unit": "%",
            "reference_range": {"min": 40, "max": 80}
        },
        "Lymphocytes": {
            "unit": "%",
            "reference_range": {"min": 20, "max": 40}
        },
        "Monocytes": {
            "unit": "%",
            "reference_range": {"min": 2, "max": 10}
        },
        "Eosinophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 6}
        },
        "Basophils": {
            "unit": "%",
            "reference_range": {"min": 1, "max": 2}
        },
        "Absolute Neutrophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 2.0, "max": 7.0}
        },
        "Absolute Lymphocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1.0, "max": 3.0}
        },
        "Absolute Monocyte Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.2, "max": 1.0}
        },
        "Absolute Basophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 1, "max": 2}
        },
        "Absolute Eosinophil Count": {
            "unit": "*10^9/L",
            "reference_range": {"min": 0.0, "max": 0.5}
        },
        "Haemoglobin": {
            "unit": "g/dL",
            "reference_range": {"min": 13.5, "max": 18.0}
        },
        "PCV": {
            "unit": "%",
            "reference_range": {"min": 42, "max": 52}
        },
        "MCV": {
            "unit": "fL",
            "reference_range": {"min": 78, "max": 100}
        },
        "MCH": {
            "unit": "pg",
            "reference_range": {"min": 27, "max": 31}
        },
        "MCHC": {
            "unit": "g/dL",
            "reference_range": {"min": 32, "max": 36}
        },
        "RDW": {
            "unit": "%",
            "reference_range": {"min": 11.5, "max": 15.0}
        },
        "PDW": {
            "unit": "%",
            "reference_range": {"min": 9, "max": 17}
        },
        "Mean Platelet Volume": {
            "unit": "fL",
            "reference_range": {"min": 7.2, "max": 11.7}
        },
        "Platelet Count": {
            "unit": "*10^3/uL",
            "reference_range": {"min": 150, "max": 450}
        },
        "PCT": {
            "unit": "%",
            "reference_range": {"min": 0.2, "max": 0.5}
        },
        "Deposit (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Prostate Specific Antigen": {
            "unit": "ng/mL",
            "reference_range": {"min": 0, "max": 4}
        },
        "Trichomonas Vaginalis":{
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Amorphous Materials (Urine)": {
            "unit": "None",
            "reference_range": {"value": "Absent"}
        },
        "Volume": {
            "unit": "mL",
            "reference_range": {"value": "None"}
        },
        "R.B.C. Count": {
            "unit": "mil/cu.mm",
            "reference_range": {"min":4.7, "max":6}
        }
        
    }
    return trutest_lab_test_data

def get_nm_medical_test_data():
    nm_medical_test_data = {
    "Leukocytes (Urine)":{ #Doubt
        "unit": 'None',
        "reference_range": {
                "value": "Negative"
            }
    },
    "ESR": {
        "unit": "mm/hr",
        "reference_range": {"min": 0, "max": 10}
    },
    "Sodium": {
        "unit": "mEq/L",
        "reference_range": {"min": 136, "max": 145}
    },
    "Potassium": {
        "unit": "mEq/L",
        "reference_range": {"min": 3.5, "max": 5.1}
    },
    "Chlorides": {
        "unit": "mEq/L",
        "reference_range": {"min": 98, "max": 107}
    },
    "Total Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0, "max": 200}
    },
    "HDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 40, "max": 60}
    },
    "LDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0, "max": 160}
    },
    "Total Cholesterol/HDL Cholesterol Ratio": {
        "unit": "None",
        "reference_range": {"min": 3.0, "max": 5.0}
    },
    "Triglycerides": {
        "unit": "mg/dL",
        "reference_range": {"min": 0,"max": 199}
    },
    "LDL/HDL Ratio": {
        "unit": "None",
        "reference_range": {"min": 0,"max": 3.5}
    },
    "Non-HDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 0,"max": 190}
    },
    "VLDL Cholesterol": {
        "unit": "mg/dL",
        "reference_range": {"min": 7, "max": 35}
    },
    "Alkaline Phosphatase": {
        "unit": "U/L",
        "reference_range": {"min": 40, "max": 150}
    },
    "Bilirubin (Total)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.2, "max": 1.2}
    },
    "Bilirubin (Direct)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.0, "max": 0.5}
    },
    "Bilirubin (Indirect)": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.1, "max": 1.0}
    },
    "GGTP": {
        "unit": "U/L",
        "reference_range": {"min": 0,"max": 73}
    },
    "SGOT": {
        "unit": "U/L",
        "reference_range": {"min":0,"max": 35.0}
    },
    "SGPT": {
        "unit": "U/L",
        "reference_range": {"min": 10, "max": 49}
    },
    "Total Proteins": {
        "unit": "g/dL",
        "reference_range": {"min": 5.7, "max": 8.3}
    },
    "Albumin": {
        "unit": "g/dL",
        "reference_range": {"min": 3.2, "max": 5.2}
    },
    "Globulin": {
        "unit": "g/dL",
        "reference_range": {"min": 2.3, "max": 3.5}
    },
    "Albumin/Globulin Ratio": {
        "unit": "None",
        "reference_range": {"min": 1.1, "max": 2.20}
    },
    "T3 (Tri-iodothyronine)": {
        "unit": "ng/dL",
        "reference_range": {"min": 86, "max": 192}
    },
    "T4 (Thyroxine)": {
        "unit": "ug/dL",
        "reference_range": {"min": 4.5, "max": 10.9}
    },
    "TSH": {
        "unit": "uIU/mL",
        "reference_range": {"min": 0.48, "max": 4.17}
    },
    "Blood Urea": {
        "unit": "mg/dL",
        "reference_range": {"min": 14.98, "max": 44.9}
    },
    "Blood Urea Nitrogen": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.90, "max": 23.0}
    },
    "Creatinine": {
        "unit": "mg/dL",
        "reference_range": {"min": 0.69, "max": 1.3}
    },
    "Blood Urea Nitrogen/Creatinine Ratio": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.3, "max": 10.6}
    },
    "Calcium": {
        "unit": "mg/dL",
        "reference_range": {"min": 8.3, "max": 10.6}
    },
    "Uric Acid": {
        "unit": "mg/dL",
        "reference_range": {"min": 3.5, "max": 9.2}
    },
    "Volume": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Colour (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Appearance (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Specific Gravity": {
        "unit": "None",
        "reference_range": {"min": 1.003, "max": 1.035}
    },
    "pH (Urine)": {
        "unit": "None",
        "reference_range": {"min": 4.6, "max": 8.0}
    },
    "Protein (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Glucose (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Ketones (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Bilirubin (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Urobilinogen (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Normal"}
    },
    "Bile Salt (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Bile Pigment (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Blood (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Nitrite (Urine)": {
        "unit": "None",
        "reference_range": {"value":"Negative"}
    },
    "Red Blood Cells (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Pus Cells (Urine)": {
        "unit": "/hpf",
        "reference_range": {"min": 0, "max": 5}
    },
    "Epithelial Cells (Urine)": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Casts": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Crystals": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Bacteria": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Yeast Cells": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "Blood Glucose Fasting": {
        "unit": "mg/dL",
        "reference_range": {"min": 70, "max": 105}
    },
    "HbA1c": {
        "unit": "None",
        "reference_range": {
            "min": 0, "max": 6
        }
    },
    "W.B.C. Count": {
        "unit": "/c.mm",
        "reference_range": {"min": 4000, "max": 10000}
    },
    "Neutrophils": {
        "unit": "%",
        "reference_range": {"min": 40, "max": 80}
    },
    "Lymphocytes": {
        "unit": "%",
        "reference_range": {"min": 20, "max": 40}
    },
    "Monocytes": {
        "unit": "%",
        "reference_range": {"min": 2, "max": 10}
    },
    "Eosinophils": {
        "unit": "%",
        "reference_range": {"min": 1, "max": 6}
    },
    "Basophils": {
        "unit": "%",
        "reference_range": {"min": 0, "max": 2}
    },
    "Absolute Neutrophil Count": {
        "unit": "cells/cu.mm",
        "reference_range": {"min": 2000, "max": 7000}
    },
    "Absolute Lymphocyte Count": {
        "unit": "cells/cu.mm",
        "reference_range": {"min": 1000, "max": 3000}
    },
    "Absolute Monocyte Count": {
        "unit": "cells/c.mm",
        "reference_range": {"min": 200, "max": 1000}
    },
    "Absolute Eosinophil Count": {
        "unit": "cells/c.mm",
        "reference_range": {"min": 20, "max": 500}
    },
    "R.B.C. Count": {
        "unit": "mill/c.mm",
        "reference_range": {"min": 4.5, "max": 5.5}
    },
    "Haemoglobin": {
        "unit": "gm%",
        "reference_range": {"min": 13.0, "max": 17.0}
    },
    "PCV": {
        "unit": "%",
        "reference_range": {"min": 40, "max": 50}
    },
    "MCV": {
        "unit": "fL",
        "reference_range": {"min": 83, "max": 101}
    },
    "MCH": {
        "unit": "pg",
        "reference_range": {"min": 27, "max": 32}
    },
    "MCHC": {
        "unit": "g/dL",
        "reference_range": {"min": 31.5, "max": 34.5}
    },
    "Mean Platelet Volume": {
        "unit": "fL",
        "reference_range": {"min": 9.0, "max": 13.0}
    },
    "Platelet Count": {
        "unit": "*10^3/c.mm",
        "reference_range": {"min": 150, "max": 410}
    },
    "Phosphorus": {
        "unit": "mg/dL",
        "reference_range": {"min": 2.3, "max": 5.1}
    },
    "Estimated Average Glucose (eAG)": {
        "unit": "mg/dL",
        "reference_range": {"value":"None"}
    },
    "Deposit (Urine)": {
        "unit": "None",
        "reference_range": {"value": "Absent"} 
    },
    "Amorphous Materials (Urine)": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "CPK (Total)": {
        "unit": "U/L",
        "reference_range": {"min": 30, "max": 171}
    },
    "LDH": {
        "unit": "U/L",
        "reference_range": {"min": 120, "max": 246}
    },
    "Bicarbonate": {
        "unit": "mmol/L",
        "reference_range": {"min": 20.0, "max": 31.0}
    },
    "Microcytes": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "Macrocytes": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "Anisocytosis": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Poikilocytosis": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Hypochromia": {
        "unit": "%",
        "reference_range": {"value":"None"}
    },
    "RDW": {
        "unit": "%",
        "reference_range": {"min": 11.6, "max": 14.0}
    },
    "Magnesium": {
        "unit": "None",
        "reference_range": {"min": 1.6, "max": 2.6}
    },
    "Trichomonas Vaginalis": {
        "unit": "None",
        "reference_range": {"value": "Absent"}
    },
    "G6-PDH Activity": {
        "unit": "U/g Hb",
        "reference_range": {"min": 4.6, "max": 13.5}
    },
    "Absorbance": {
        "unit": "None",
        "reference_range": {"value":"None"}
    },
    "Hepatitis C": {
        "unit": "None",
        "reference_range": {"min": 0, "max": 0.9}
    },
    "Hepatitis B": {
        "unit": "S/CO",
        "reference_range": {"min": 0, "max": 0.9}
    },
    "TB-Gold": {
        "unit": "IU/mL",
        "reference_range": {"min": 0.0, "max": 0.35}
    },
    "Mucus": {
        "unit": "None",
        "reference_range": {"value": "None"}
    }
}
    return nm_medical_test_data
