import mitreattack.attackToExcel.attackToExcel as attackToExcel
import pandas as pd
import os
 
attackToExcel.export("enterprise-attack", "v14.1", "/Users/example/Documents")
 
# Function to create directories based on the structure
def create_directories(base_path, structure):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    
    for tactic, techniques in structure.items():
        tactic_path = os.path.join(base_path, tactic)
        if not os.path.exists(tactic_path):
            os.mkdir(tactic_path)
        
        for technique, sub_techniques in techniques.items():
            technique_path = os.path.join(tactic_path, technique)
            if not os.path.exists(technique_path):
                os.mkdir(technique_path)
            
            for sub_technique in sub_techniques:
                sub_technique_path = os.path.join(technique_path, sub_technique)
                if not os.path.exists(sub_technique_path):
                    os.mkdir(sub_technique_path)
 
# Load the Excel file
file_path = '/Users/example/Documents/enterprise-attack-v14.1/enterprise-attack-v14.1.xlsx'  # Replace with your actual file path
xlsx = pd.ExcelFile(file_path)
 
# Load the 'techniques' sheet into a DataFrame
techniques_df = pd.read_excel(xlsx, 'techniques')
 
# Extracting necessary columns for directory creation
techniques = techniques_df[['ID', 'name', 'tactics', 'is sub-technique', 'sub-technique of']]
 
# Creating a dictionary to hold the structure
structure = {}
 
for index, row in techniques.iterrows():
    # Splitting tactics as a technique might belong to multiple tactics
    tactic_list = str(row['tactics']).split(", ")
 
    for tactic in tactic_list:
        # Ignoring invalid tactics
        if tactic == 'nan':
            continue
 
        if tactic not in structure:
            structure[tactic] = {}
 
        # Adding main techniques
        if not row['is sub-technique']:
            structure[tactic][row['ID']] = []
 
        # Adding sub-techniques to their respective main technique
        elif row['is sub-technique'] and row['sub-technique of'] in structure[tactic]:
            structure[tactic][row['sub-technique of']].append(row['ID'])
 
# Directory for the structure
top_directory = "MITRE_ATT&CK_Structure"
 
# Create the directory structure
create_directories(top_directory, structure)
 
print("Directories based on the MITRE ATT&CK structure have been created.")