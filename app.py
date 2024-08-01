#################################################
### Streamlit app for product data conversion ###
#################################################

#Dependencies
import streamlit as st
import pandas as pd
import numpy as np
import inspect
import joblib
import csv
import os
# import importlib
from huggingface_hub import hf_hub_download

#load env file
# from dotenv import load_dotenv
# load_dotenv()

### Streamlit design and inputs

st.title("Product Data Conversion")

st.header("Vendor")
producer = st.selectbox("Please select the vendor", ["", "BUSSE", "Kerbl", "Waldhausen", "HV_Polo", "HKM"])

# Load module relevant for the vendor
with st.spinner(f"Loading the module for {producer} ..."):
    if producer == 'BUSSE' :
        from src import Convert_BUSSE
    elif producer == 'Kerbl':
        from src import Convert_Kerbl
    elif producer == 'Waldhausen':
        from src import Convert_Waldhausen
    elif producer == 'HV_Polo':
        from src import Convert_HV_Polo
    elif producer == 'HKM':
        from src import Convert_HKM

st.header("Product type: shop or stock item")
product_type = st.selectbox("Please select the product type", ["", "is_shop", "is_stock_item"])
if product_type == 'is_shop':
    is_shop = 1
    is_stock_item = 0
elif product_type == 'is_stock_item':
    is_shop = 0
    is_stock_item = 1
else:
    is_shop = 0
    is_stock_item = 0

st.header("Discount and Margin")
discount = st.slider("Discount", min_value=0, max_value=100, value=0)
target_margin = st.slider("Target margin", min_value=0, max_value=100, value=0)
margin_factor = 1 / (1 - target_margin / 100)
discount_factor = 1 - discount / 100

st.header("Colour conversion")
color_choice = st.radio("Do you want to upload a new dictionary?", ["No: use the existing dictioanry", "Yes: upload a new dictionary"])
if color_choice == "Yes: upload a new dictionary":
    color_file = st.file_uploader("Upload a color dictinoary", type=["xlsx", "xls", "xlsm"])
    if color_file:
        colors_dict_file = pd.read_excel(color_file, sheet_name = 0)
        colors_dict = {}
        for i in range(len(colors_dict_file)):
            colors_dict[colors_dict_file.iloc[i]['Hersteller'].lower()] = colors_dict_file.iloc[i]['Grundfarbe']
    else: 
        colors_dict_path = "data/color_dict.xlsx"
        colors_dict_file = pd.read_excel(colors_dict_path, sheet_name = 0)
        colors_dict = {}
        for i in range(len(colors_dict_file)):
            colors_dict[colors_dict_file.iloc[i]['Hersteller'].lower()] = colors_dict_file.iloc[i]['Grundfarbe']
else:
    colors_dict_path = "data/color_dict.xlsx"
    colors_dict_file = pd.read_excel(colors_dict_path, sheet_name = 0)
    colors_dict = {}
    for i in range(len(colors_dict_file)):
        colors_dict[colors_dict_file.iloc[i]['Hersteller'].lower()] = colors_dict_file.iloc[i]['Grundfarbe']

st.header("Product data")
if producer == "" :
    st.write("Please select a vendor before uploading the product data")
else:
    with st.spinner('Loading file...'):
        data_raw = st.file_uploader("Please upload a file", type=["xlsx", "xls", "xlsm"])
    if data_raw:
        if producer == 'BUSSE' :
            data = pd.read_excel(data_raw, sheet_name = 2)
            pic_idx = pd.read_excel(data_raw, sheet_name = 0)
            list_pic_idx = []
            for i in range(len(data)):
                list_pic_idx.append(list(pic_idx[pic_idx['ArtNr'] == data['Artikelnummer'].iloc[i]].sort_values(by='Ranking')['Bilddatei'].values))
            data['picture_ids'] = list_pic_idx
        else:
            data = pd.read_excel(data_raw)


# # Downloading models
# loaded_models = []
# # these lists are just for not loading the same model twice / not displaying the same message that a model wasnt found multiple times
# loaded_models_names = []

# loaded_models.append(joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_breite_model.pkl")
# ))
# loaded_models_names.append('pack_breite')

# loaded_models.append(joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_hoehe_model.pkl")
# ))
# loaded_models_names.append('pack_hoehe')
# loaded_models.append(joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_laenge_model.pkl")
# ))
# loaded_models_names.append('pack_laenge')
# loaded_models.append(joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "season_model.pkl")
# ))
# loaded_models_names.append('season')

# not_loaded_models = ['tax_class_id']


# The main function

def create_csv():
    needed_columns = [
        'type','Attributmenge','o_Optionen','Orphan','Hat_Optionen','vendor','brand','visibility','cost','price','special price','tax_class_id',
        'Beschreibung','Menge','Gewicht','Bild','Weitere Bilder','ean','herstellerbezeichnung','grundpreis_menge','grundpreis_einheit',
        'destatis_warennummer','country_of_manufacture','manufacturer_nr','material','passform','simples_skus','LiNr','base_color',
        'pack_laenge','pack_breite','pack_hoehe','is_shop','is_stock_item','season','pvs_verpackungstyp','gefahrgut','VPE','cost Discount'
    ]
    
    # the columns that wont be filled in Step 3 with some function in the Convert_***.py file / some model
    given_columns = ['is_shop','is_stock_item','cost Discount','Attributmenge','zielgruppe','special price']
    
    needed_columns_dict = {
        'Decken' : ['name','rueckenlaenge','halsteil','fuellung','denier','color','zielgruppe','materialeigenschaft','produktmerkmale','pflegehinweis'],
        'Hosen' : ['name','hosen_groesse','color','besatz','zielgruppe','pflegehinweis'],
        'Oberbekleidung' : ['oberbekleidung_groesse','color','zielgruppe','pflegehinweis'],
        'Schuhe, Stiefel und Socken' : ['schuhgroesse','verschlussart','color','zielgruppe','wadenweite','schafthoehe','pflegehinweis'],
        'Sporen' : ['sporen_laenge','color','zielgruppe'],
        'Sporenriemen' : ['sporenriemen_laenge','color','sporenriemen_material','zielgruppe'],
        'Reithelme' : ['kopfgroesse','farbe','zielgruppe','pflegehinweis'],
        'Schutzwesten' : ['schutzwesten_groesse','color','zielgruppe'],
        'Gerten und Peitschen' : ['gerten_laenge','color','zielgruppe'],
        'Trensen, Kandaren und Halfter' : ['pferdegroesse','color','ausfuehrung_halfter','zielgruppe'],
        'Hilfszuegel' : ['pferdegroesse','hilfszuegel_laenge','color','zielgruppe'],
        'Stricke' : ['strick_laenge','color','verschlussart','zielgruppe'],
        'Gebisse' : ['gebiss_staerke','gebiss_groesse','gebissart','gebissmaterial','zielgruppe'],
        'Sattelgurte' : ['art_des_sattelgurtes','color','sattelgurt_laenge','zielgruppe'],
        'Beinschutz' : ['pferdegroesse','color','zielgruppe'],
        'Pflegeprodukte' : ['inhalt','zielgruppe'],
        'Futter' : ['pferdefutter_art','inhalt','zielgruppe'],
        'Handschuhe' : ['handschuh_groesse','color','zielgruppe','pflegehinweis'],
        'Saettel' : ['kammerweite','sitzgroesse','color','zielgruppe'],
        'Schabracken' : ['name','schabraken_groesse','color','pflegehinweis'],
        'Fliegenhauben' : ['pferdegroesse','color','zielgruppe'],
        'Steigbügel' : ['trittflaeche','color','zielgruppe'],
        'Steigbuegelriemen' : ['riemen_laenge','color','zielgruppe'],
        'Pferdezubehoer' : ['zubehoer_groesse','color','zielgruppe'],
        'Accessoires' : ['accesoires_groesse','color','zielgruppe'],
        'Halsbänder' : ['halsband_laenge','halsband_groesse','color','zielgruppe'],
        'Hundedecken' : ['rueckenlaenge','color','pflegehinweis','zielgruppe'],
        'Heimtierfutter' : ['heimtierfutter_art','inhalt','zielgruppe'],
        'Leinen und Geschirre' : ['leinen_laenge','color'],
        'Heimtierzubehoer' : ['zubehoer_groesse','color','zielgruppe'],
        'Sonstiges' : ['color','pflegehinweis','zielgruppe'],
        'Elektronik' : ['kabel','leistung','color','zielgruppe'],
        'Elektronikzubehoer' : ['zubehoer_groesse','zielgruppe'],
        'Unknown' : []
    }
    
    for key in needed_columns_dict.keys():
        needed_columns_dict[key] = needed_columns_dict[key] + needed_columns
    
    
    ### Step 1: read the data and all the other needed data values (are there any other things needed to be read?)
    
    # i placed a file with the color-dictionary in this folder, it doesnt need to be there but it needs to be somewhere
    # colors_dict_path = os.getenv("COLOR_DICT_FILE")
    # colors_dict_file = pd.read_excel(colors_dict_path, sheet_name = 0)
    # colors_dict = {}
    # for i in range(len(colors_dict_file)):
    #     colors_dict[colors_dict_file.iloc[i]['Hersteller'].lower()] = colors_dict_file.iloc[i]['Grundfarbe']
    
    ### THESE VALUES WILL BE READ IN FROM THE EXCEL FILE
    # user_input_path = os.getenv("USER_INPUT_FILE")
    # main_excel_file = pd.read_excel(user_input_path)
    # # producer = main_excel_file['Unnamed: 2'].iloc[4]
    # check_stock_shop = main_excel_file['Unnamed: 2'].iloc[5]
    # if check_stock_shop == 'is_shop':
    #     is_shop = 1
    #     is_stock_item = 0
    # elif check_stock_shop == 'is_stock_item':
    #     is_shop = 0
    #     is_stock_item = 1
    # else:
    #     is_shop = 0
    #     is_stock_item = 0
    # discount = main_excel_file['Unnamed: 2'].iloc[6]
    # target_margin = main_excel_file['Unnamed: 2'].iloc[7]

    # values for the calculation of the special price
    # margin_factor = 1 / (1 - target_margin / 100)
    # discount_factor = 1 - discount / 100
    
    grouping_columns_dict = {
        "BUSSE" : ['Bezeichnung','Farbe'],
        "Kerbl" : ['ERP_BEZEICHNUNG_1_STR','FARBE_MARKETING_SLA_SEL'],
        "Waldhausen" : ['Modellname','Farbe'], 
        "HV_Polo" : ["Name","Colour"], 
        "HKM" : ["Beschreibung","Beschreibung 2"]
    }

    # product_data_dir = os.getenv("PRODUCT_DATA_PATH")
    
    # if producer == 'BUSSE' :
    #     data = pd.read_excel(product_data_dir + "BUSSE_product-data.xlsx", sheet_name = 2)
    #     pic_idx = pd.read_excel(product_data_dir + "BUSSE_product-data.xlsx", sheet_name = 0)
    #     list_pic_idx = []
    #     for i in range(len(data)):
    #         list_pic_idx.append(list(pic_idx[pic_idx['ArtNr'] == data['Artikelnummer'].iloc[i]].sort_values(by='Ranking')['Bilddatei'].values))
    #     data['picture_ids'] = list_pic_idx
    # else:
    #     data = pd.read_excel(product_data_dir + producer + '_product-data.xlsx')
    #     # -> get the data file / path as an input or let the user place the follow in the ordner the program is in?
    
    # ### Step 2: predict Attributmenge / Zielgruppe if its not given by the data already or read them from the data if possible
    
    # get a list of all functions in the Convert_producer module
    functions_list = inspect.getmembers(eval('Convert_'+producer), inspect.isfunction)
    functions_list = [func[0] for func in functions_list]
    
    # check if theres a function for the Attributmenge (if no -> prediction needed)
    if 'get_Attributmenge' in functions_list:
        list_Attributmenge = []
        for i in range(len(data)):
            list_Attributmenge.append(eval('Convert_'+producer+'.get_Attributmenge')(0,data.iloc[i],0,0,0,0,0,0))
    data['Attributmenge'] = list_Attributmenge
    
    # Check if the zielgruppe is needed (not always needed, only for certain values of Attributmenge) and read / predict that if needed
    zielgruppe_needed = False
    for attr in list(set(list_Attributmenge)):
        if 'zielgruppe' in needed_columns_dict[attr]:
            zielgruppe_needed = True
    if zielgruppe_needed:
        if 'get_zielgruppe' in functions_list:
            list_zielgruppe = []
            for i in range(len(data)):
                list_zielgruppe.append(eval('Convert_'+producer+'.get_zielgruppe')(0,data.iloc[i],0,0,0,0,0,list_Attributmenge[i]))
        data['zielgruppe'] = list_zielgruppe
    
    list_beschreibung = []
    list_color = []
    col1 = grouping_columns_dict[producer][0]
    col2 = grouping_columns_dict[producer][1]
    for i in range(len(data)):
        list_beschreibung.append(data[col1].iloc[i])
        list_color.append(data[col2].iloc[i])
    
    if zielgruppe_needed:
        df = pd.DataFrame([list_Attributmenge,list_zielgruppe,list_beschreibung,list_color]).T
        df.rename(columns={0: "Attributmenge", 1: "zielgruppe", 2: "Beschreibung", 3: "Farbe"}, inplace = True)
        grouped_df = df[['Attributmenge','zielgruppe','Beschreibung','Farbe']].groupby(['Attributmenge','zielgruppe','Beschreibung','Farbe'], sort = False).size().reset_index(name='Count')
    else:
        df = pd.DataFrame([list_Attributmenge,list_beschreibung,list_color]).T
        df.rename(columns={0: "Attributmenge", 1: "Beschreibung", 2: "Farbe"}, inplace = True)
        grouped_df = df[['Attributmenge','Beschreibung','Farbe']].groupby(['Attributmenge','Beschreibung','Farbe'], sort = False).size().reset_index(name='Count')
    

    ### Step 3: get all the columns that can be read directly from the data
    
    # get the columns needed for the whole document via the needed_columns_dict
    for attr in df['Attributmenge'].unique():
        for col in needed_columns_dict[attr]:
            if col not in needed_columns:
                needed_columns.append(col)
    
    loaded_models = []
    # these lists are just for not loading the same model twice / not displaying the same message that a model wasnt found multiple times
    loaded_models_names = []
    not_loaded_models = []
    
    ### filling the data
    # this is mostly the same code as in the Convert_*** notebook
    current_row_nr = 0
    total_row_nr = 1
    all_rows_data = []
    for i in range(len(grouped_df)):
        current_LiNr = []
        current_attr = grouped_df.iloc[i]['Attributmenge']
        if zielgruppe_needed:
            j = len(data[(data[col1] == grouped_df.iloc[i]['Beschreibung']) & (data[col2] == grouped_df.iloc[i]['Farbe']) & (data['zielgruppe'] == grouped_df.iloc[i]['zielgruppe']) & (data['Attributmenge'] == grouped_df.iloc[i]['Attributmenge'])])
        else:
            j = len(data[(data[col1] == grouped_df.iloc[i]['Beschreibung']) & (data[col2] == grouped_df.iloc[i]['Farbe']) &  (data['Attributmenge'] == grouped_df.iloc[i]['Attributmenge'])])
        ### if j>1 then we add a row with type = configurable
        if j > 1:
            use_configurable = True
        else:
            use_configurable = False
        for _ in range(j):
            current_row_data = []
            if current_row_nr >= len(data):
                print(f'DEBUG MESSAGE: i={i}, j={j}, current_row_nr = {current_row_nr}')
                print(len(data))
            current_row = data.iloc[current_row_nr]
            current_row_nr += 1
            total_row_nr += 1
            row_is_simple = True
            ### go through the current rows where Bezeichnung and Farbe are given by grouped_df and create a row with the different data values for each
            ### of the rows
            for column in needed_columns:
                if column == 'Weitere Bilder':
                    column = 'Weitere_Bilder'
                if column in given_columns:
                    if column == 'is_shop':
                        current_row_data.append(is_shop)
                    elif column == 'is_stock_item': 
                        current_row_data.append(is_stock_item)
                    elif column == 'cost Discount':
                        current_row_data.append(discount)
                    elif column == 'Attributmenge':
                        current_row_data.append(df['Attributmenge'].iloc[current_row_nr-1])
                    elif column == 'zielgruppe':
                        current_row_data.append(df['zielgruppe'].iloc[current_row_nr-1])
                    elif column == 'special price':
                        if 'get_price' in functions_list:
                            try:
                                price = float(str(eval('Convert_'+producer+'.get_price')(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)).replace(',','.'))
                            except ValueError:
                                price = np.nan
                            if 'get_tax_class_id' in functions_list:
                                tax_id = eval('Convert_'+producer+'.get_tax_class_id')(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
                            else:
                                input = df['Beschreibung'].iloc[current_row_nr-1] + ' ' + df['Attributmenge'].iloc[current_row_nr-1]
                                if 'tax_class_id' not in loaded_models_names:
                                    try:
                                        loaded_models.append(joblib.load('../models/'+'tax_class_id_model.pkl'))
                                        loaded_models_names.append(column)
                                    except FileNotFoundError:
                                        if column not in not_loaded_models:
                                            print(f'The model {column}_model.pkl was not found')
                                            not_loaded_models.append(column)
                                        current_row_data.append('')
                                        tax_id = 'not_found'
                                if 'tax_class_id' in loaded_models_names:
                                    tax_id = loaded_models[loaded_models_names.index('tax_class_id')].predict([input])[0]
                            if tax_id != 'not_found':
                                # i dont know how the value of of tax.compute_all is calculated
                                if tax_id == '1':
                                    tax_factor = 1
                                else:
                                    tax_factor = 1
                                price = price * tax_factor * margin_factor * discount_factor
                                if price < 10:
                                    digits = 1
                                    offset = 0.025
                                else:
                                    digits = 0
                                    offset = 0.25
                                special_price = round(round(price + offset,digits)-0.01,2)
                                current_row_data.append(special_price)
                            else:
                                current_row_data.append('')
                                
                        else:
                            # if there is no function for the price, then we dont try to predict the price / special_price and only append an empty string
                            current_row_data.append('')

                    else:
                        print('Failed on trying to append column ' + column)
                else:
                    if 'get_' + str(column) in functions_list:
                        current_row_data.append(eval('Convert_'+producer+'.get_'+column)(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr))
                    else:
                        if column in needed_columns_dict[grouped_df['Attributmenge'].iloc[i]]:
                            if column not in loaded_models_names:
                                try:
                                    loaded_models.append(joblib.load('../models/'+str(column)+'_model.pkl'))
                                    loaded_models_names.append(column)
                                except FileNotFoundError:
                                    if column not in not_loaded_models:
                                        print(f'The model {column}_model.pkl was not found')
                                        not_loaded_models.append(column)
                                    current_row_data.append('')
                            if column in loaded_models_names:
                                input = df['Beschreibung'].iloc[current_row_nr-1] + ' ' + df['Attributmenge'].iloc[current_row_nr-1]
                                current_row_data.append(loaded_models[loaded_models_names.index(column)].predict([input])[0])
                        else:
                            current_row_data.append('')
            current_LiNr.append(eval('Convert_'+producer+'.get_LiNr')(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr))
            all_rows_data.append(current_row_data)
        if use_configurable:
            ### create a row with type = configurable
            # the variable current_row at that point is the last row with the Artikelbezeichnung and Farbe.
            # For each value that is calculated in this row, the values in current_row can be used.
            current_row_data = []
            row_is_simple = False
            total_row_nr +=1
            for column in needed_columns:
                if column == 'Weitere Bilder':
                    column = 'Weitere_Bilder'
                if column in given_columns:
                    if column == 'is_shop':
                        current_row_data.append(is_shop)
                    elif column == 'is_stock_item': 
                        current_row_data.append(is_stock_item)
                    elif column == 'cost Discount':
                        current_row_data.append(discount)
                    elif column == 'Attributmenge':
                        current_row_data.append(df['Attributmenge'].iloc[current_row_nr-1])
                    elif column == 'zielgruppe':
                        current_row_data.append(df['zielgruppe'].iloc[current_row_nr-1])
                    elif column == 'special price':
                        if 'get_price' in functions_list:
                            try:
                                price = float(str(eval('Convert_'+producer+'.get_price')(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)).replace(',','.'))
                            except ValueError:
                                price = np.nan
                            if 'get_tax_class_id' in functions_list:
                                tax_id = eval('Convert_'+producer+'.get_tax_class_id')(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
                            else:
                                input = df['Beschreibung'].iloc[current_row_nr-1] + ' ' + df['Attributmenge'].iloc[current_row_nr-1]
                                if 'tax_class_id' not in loaded_models_names:
                                    try:
                                        loaded_models.append(joblib.load('../models/'+'tax_class_id_model.pkl'))
                                        loaded_models_names.append(column)
                                    except FileNotFoundError:
                                        if column not in not_loaded_models:
                                            print(f'The model {column}_model.pkl was not found')
                                            not_loaded_models.append(column)
                                        current_row_data.append('')
                                        tax_id = 'not_found'
                                if 'tax_class_id' in loaded_models_names:
                                    tax_id = loaded_models[loaded_models_names.index('tax_class_id')].predict([input])[0]
                            if tax_id != 'not_found':
                                # i dont know how the value of of tax.compute_all is calculated
                                if tax_id == '1':
                                    tax_factor = 1
                                else:
                                    tax_factor = 1
                                price = price * tax_factor * margin_factor * discount_factor
                                if price < 10:
                                    digits = 1
                                    offset = 0.025
                                else:
                                    digits = 0
                                    offset = 0.25
                                special_price = round(round(price + offset,digits)-0.01,2)
                                current_row_data.append(special_price)
                            else:
                                current_row_data.append('')
                                
                        else:
                            # if there is no function for the price, then we dont try to predict the price / special_price and only append an empty string
                            current_row_data.append('')
                    else:
                        print('Failed on trying to append column ' + column)
                else:
                    if 'get_' + str(column) in functions_list:
                        current_row_data.append(eval('Convert_'+producer+'.get_'+column)(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr))
                    else:
                        if column in needed_columns_dict[grouped_df['Attributmenge'].iloc[i]]:
                            if column not in loaded_models_names:
                                try:
                                    loaded_models.append(joblib.load('../models/'+str(column)+'_model.pkl'))
                                    loaded_models_names.append(column)
                                except FileNotFoundError:
                                    if column not in not_loaded_models:
                                        print(f'The model {column}_model.pkl was not found')
                                        not_loaded_models.append(column)
                                    current_row_data.append('')
                            if column in loaded_models_names:
                                input = df['Beschreibung'].iloc[current_row_nr-1] + ' ' + df['Attributmenge'].iloc[current_row_nr-1]
                                current_row_data.append(loaded_models[loaded_models_names.index(column)].predict([input])[0])
                        else:
                            current_row_data.append('')
            all_rows_data.append(current_row_data)
    
    # for each needed column col check if a function with the name get_col exists in the notebook for the specific vendor
    # if yes -> call that 
    # if no -> use ML model
    
    ### Step 4: get the rest of the columns where a ML model is used
    
    # go through the list of columns and call the corresponding model for each of them
    # this is already done before
    
    ### Step 5: save the results in a csv-file   
    result = pd.DataFrame(all_rows_data, columns = needed_columns)
    for i in range(len(result)):
        row = result.iloc[i]
        unknown_columns = row[row == 'Unknown'].index.tolist()
        if len(unknown_columns) > 0:
            print(f'In the row {i+2} the value of the column {unknown_columns} is unknown')
    print('successfully finished')
    # output_data_path = os.getenv("OUTPUT_DATA_PATH")
    # result.to_csv(output_data_path + producer + '_upload.csv',sep=',', quoting=csv.QUOTE_ALL, index = False)
    return result

if "data" in locals():
    with st.spinner('Processing data...'):
        result_data = create_csv()

if "result_data" in locals():
    st.subheader("Converted data")
    st.dataframe(result_data)

# if __name__ == "__main__":
#     create_csv()