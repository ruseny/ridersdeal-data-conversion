#######################
### Convert HV Polo ###
#######################

# Dependencies
# import pandas as pd
# import numpy as np
import re
import fasttext
from huggingface_hub import hf_hub_download
import joblib

fasttext.FastText.eprint = lambda x: None # Disable fasttext warnings

# The following 2 dicts will probably be in the main file (they are not vendor specific)

# color_mapper_df = pd.read_excel("../../data/raw/color_dict.xlsx", sheet_name = 0)
# color_mapper_df["Hersteller"] = color_mapper_df["Hersteller"].str.lower().str.strip()
# colors_dict = color_mapper_df.set_index("Hersteller").to_dict()["Grundfarbe"]

Optionen_dict= {
    'Decken' : 'rueckenlaenge', 
    'Hosen': 'hosen_groesse',
    'Oberbekleidung' : 'oberbekleidung_groesse',
    'Schuhe, Stiefel und Socken' : 'schuhgroesse',
    'Sporen' : 'sporen_laenge',
    'Sporenriemen' : 'sporenriemen_laenge',
    'Reithelme' : 'kopfgroesse',
    'Schutzwesten' : 'schutzwesten_groesse',
    'Gerten und Peitschen' : 'gerten_groesse',
    'Trensen, Kandaren und Halfter' : 'pferdegroesse',
    'Hilfszuegel' : 'pferdegroesse',
    'Stricke' : 'strick_laenge',
    'Gebisse' : 'gebiss_groesse',
    'Sattelgurte' : 'sattelgurt_laenge',
    'Beinschutz' : 'beinschutz_groesse', # could also be 'pferdegroesse'
    'Handschuhe' : 'handschuh_groesse',
    'Saettel' : 'sitzgroesse', # could also be 'kammerweite'
    'Schabracken' : 'schabracken_groesse', 
    'Fliegenhauben' : 'pferdegroesse',
    'Steigbügel' : 'trittflaeche', 
    'Steigbuegelriemen' : 'riemen_laenge', 
    'Pferdezubehoer' : 'zubehoer_groesse',   
    'Accessoires': 'accessoires_groesse', 
    'Halsbänder' : 'halsband_groesse', # could also be 'halsband_laenge' 
    'Hundedecken' : 'rueckenlaenge', 
    'Leinen und Geschirre' : 'leinen_laenge',
    'Heimtierzubehoer' : 'zubehoer_groesse',
    'Elektronikzubehoer' : 'zubehoer_groesse',
}

# Dicts for attributset to be checked before predicting from model

dict_att_gr = {
    "Bandagen und Gamaschen (Beinschutz)" : "Beinschutz", 
    "Decken" : "Decken", 
    "Fleece" : "Oberbekleidung", 
    "Fliegenmütze" : "Fliegenhauben", 
    "Handschuhe" : "Handschuhe",
    "Home" : "Accessoires",
    "Oberbekleidung" : "Oberbekleidung",
    "Polo Shirts" : "Oberbekleidung",
    "Putzzeug" : "Pferdezubehoer",
    "Reithosen" : "Hosen", 
    "Satteldecken": "Schabracken", 
    "Schuhe" : "Schuhe, Stiefel und Socken", 
    "Socken" : "Schuhe, Stiefel und Socken", 
    "Sporen und Zubehör" : "Sporenriemen", 
    "Stallzubehör" : "Pferdezubehoer", 
    "Stiefel" : "Schuhe, Stiefel und Socken", 
    "Strickwaren" : "Oberbekleidung", 
    "Sweat" : "Oberbekleidung", 
    "Tech Shell" : "Oberbekleidung", 
    "Tops" : "Oberbekleidung", 
    "Turnier Jackets" : "Oberbekleidung", 
    "Turnier Shirts" : "Oberbekleidung",
    "Westen" : "Oberbekleidung"
}

dict_att_subgr = {
    "Anbinder und Trailerlines" : "Stricke", 
    "Baseballcaps" : "Accessoires", 
    "Führstricke Panikhaken" : "Stricke", 
    "Haaraccessories" : "Accessoires", 
    "Hand- und Tragetaschen" : "Accessoires",
    "Hilfszügel" : "Hilfszuegel", 
    "Kandarren" : "Trensen, Kandaren und Halfter", 
    "Lederhalfter" : "Trensen, Kandaren und Halfter",
    "Nylonhalfter" : "Trensen, Kandaren und Halfter", 
    "Pferdezubehör" : "Pferdezubehoer", 
    "Portemonnaie" : "Accessoires", 
    "Trensen" : "Trensen, Kandaren und Halfter"
}

# Dict for zielgruppe to check before predicting from model

dict_zg_gr = {
    "Accessories" : "Unisex", 
    "Bandagen und Gamaschen (Beinschutz)": "Pferd", 
    "Decken" : "Pferd", 
    "Fliegenmütze" : "Pferd", 
    "Halfter & Stricke" : "Pferd", 
    "Home" : "Unisex", 
    "Hunde" : "Hund", 
    "Putzzeug" : "Pferd", 
    "Sattel und Zubehör" : "Pferd", 
    "Satteldecken" : "Pferd", 
    "Sporen und Zubehör" : "Pferd", 
    "Stallzubehör" : "Pferd", 
    "Trensen & Zügel" : "Pferd"
}

# Load models for Attirubtset and Zielgruppe, and needed dicts

model_at = fasttext.load_model(
    hf_hub_download("Adriperse/RD-CA", "hvpolo_attributset_model.bin")
)
model_zg = fasttext.load_model(
    hf_hub_download("Adriperse/RD-CA", "hvpolo_zielgruppe_model.bin")
)
# model_pack_breite = joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_breite_model.pkl")
# )
# model_pack_hoehe = joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_hoehe_model.pkl")
# )
# model_pack_laenge = joblib.load(
#     hf_hub_download("Adriperse/RD-CA2", "pack_laenge_model.pkl")
# )

label_mapper_at = {
    '__label__Decken': 'Decken',
    '__label__Hosen': 'Hosen',
    '__label__Oberbekleidung': 'Oberbekleidung',
    '__label__Schuhe_Stiefel_und_Socken': 'Schuhe, Stiefel und Socken',
    '__label__Sporen': 'Sporen',
    '__label__Sporenriemen': 'Sporenriemen',
    '__label__Reithelme': 'Reithelme',
    '__label__Schutzwesten': 'Schutzwesten',
    '__label__Gerten_und_Peitschen': 'Gerten und Peitschen',
    '__label__Trensen_Kandaren_und_Halfter': 'Trensen, Kandaren und Halfter',
    '__label__Hilfszuegel': 'Hilfszuegel',
    '__label__Stricke': 'Stricke',
    '__label__Gebisse': 'Gebisse',
    '__label__Sattelgurte': 'Sattelgurte',
    '__label__Beinschutz': 'Beinschutz',
    '__label__Pflegeprodukte': 'Pflegeprodukte',
    '__label__Futter': 'Futter',
    '__label__Handschuhe': 'Handschuhe',
    '__label__Saettel': 'Saettel',
    '__label__Schabracken': 'Schabracken',
    '__label__Fliegenhauben': 'Fliegenhauben',
    '__label__Steigbügel': 'Steigbügel',
    '__label__Steigbuegelriemen': 'Steigbuegelriemen',
    '__label__Pferdezubehoer': 'Pferdezubehoer',
    '__label__Accessoires': 'Accessoires',
    '__label__Halsbaender': 'Halsbänder',
    '__label__Hundedecken': 'Hundedecken',
    '__label__Heimtierfutter': 'Heimtierfutter',
    '__label__Leinen_und_Geschirre': 'Leinen und Geschirre',
    '__label__Heimtierzubehoer': 'Heimtierzubehoer',
    '__label__Sonstiges': 'Sonstiges',
    '__label__Elektronik': 'Elektronik',
    '__label__Elektronikzubehoer': 'Elektronikzubehoer',
    '__label__Unknown': 'Unknown'
}

label_mapper_zg = {
    "__label__Damen" : "Damen",
    "__label__Herren" : "Herren",
    "__label__Kinder" : "Kinder",
    "__label__Unisex" : "Unisex", 
    "__label__Hund" : "Hund", 
    "__label__Pferd" : "Pferd"
}

# Size conversions
size_mapper = {
    # horse sizes
    "Foal" : "Fohlen",
    "SH/S" : "Shetty", 
    "P/S" : "Pony",
    "C/S" : "VB",
    "F/S" : "WB",
    "XF/S" : "WB-XL",
    # single size
    "1SIZE" : "Einheitsgroesse",
}

# To remove html tags
REM_TAGS = re.compile(r'<[^>]+>')

# Functions

# Functions for main columns

def get_type(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return 'simple'
    else:
        return 'configurable'

def get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    
    if current_row["Group"] in dict_att_gr.keys():
        return dict_att_gr[current_row["Group"]]
    elif current_row["SubGroup"] in dict_att_subgr.keys():
        return dict_att_subgr[current_row["SubGroup"]]
    elif current_row["Group"] == "Hunde" and current_row["SubGroup"] == "Decken":
        return "Hundedecken"
    elif current_row["Group"] == "Sattel und Zubehör" and (current_row["SubGroup"] in ["Gurte und Zubehör", "Sattelzubehör"]):
        return "Sattelgurte"
    else:
        
        input_string = current_row["Name"] + " " + current_row["Brand"] + " " + \
            current_row["Group"] + " " + str(current_row["SubGroup"]) + " " + current_row["Season"] + " " + \
            current_row["Colour"] + " " + current_row["Gender"]
        
        def preprocess_str(doc):
            doc = doc.translate(doc.maketrans("\n\t\r", "   "))
            doc = re.sub(r'[^a-zA-Z\s]', ' ', doc, flags=re.I|re.A)
            doc = doc.lower()
            doc = re.sub(r'\s+', ' ', doc).strip()
            return doc
        
        input_string = preprocess_str(input_string)
        pred_label = model_at.predict(input_string)[0][0]
        return label_mapper_at[pred_label]

def get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    
    zielgruppe = get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)

    if current_row["Size"] in size_mapper.keys():
        size = size_mapper[current_row["Size"]]
    else:
        size = current_row["Size"]

    if "Damen" in current_row["Name"] or "Herren" in current_row["Name"] or "Kinder" in current_row["Name"]:
        target = ""
    elif zielgruppe in ["Damen", "Kinder", "Herren"]:
        target = " für " + zielgruppe
    else:
        target = ""
    
    if not use_configurable:
        return current_row["Name"] + target
    elif row_is_simple:
        return current_row["Name"] + target + ", " + str(size)
    else:
        return current_row["Name"] + target

def get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if use_configurable:
        Attributmenge = get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)
        if Attributmenge in Optionen_dict.keys():
            return Optionen_dict[Attributmenge]
        else:
            return ''
    else:
        return ''

def get_Orphan(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if not use_configurable:
        return 1
    else:
        return 0

def get_Hat_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return 'nein'
    else:
        return 'ja'

def get_visibility(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if use_configurable and row_is_simple:
        return 'Not Visible Individually'
    else:
        return 'Catalog, Search'

def get_vendor(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return "HV Polo"

def get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Brand"]

# def get_cost(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("No information was found for cost in the original data file.")
#     return ""

# def get_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("No information was found for price in the original data file.")
#     return ""

# def get_special_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("No information was found for special price in the original data file.")
#     return ""

def get_tax_class_id(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if current_attr == "Futter":
        return "Futtermittel"
    else:
        return "1"

def get_Beschreibung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if current_row["Description"] == "":
        return ""
    elif type(current_row["Description"]) is not str:
        return ""
    else:
        desc = REM_TAGS.sub('', current_row["Description"])
        return '<ul><li>' + desc.replace('*', '</li><li>') + '</li></ul>'

def get_Menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Menge' in the original data file.")
    return ""

def get_Gewicht(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return current_row["ItemWeight"]
    else:
        return 1

def get_Bild(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    urls = current_row["ImageDownloadlink"]
    if type(urls) is not str:
        return ""
    else: 
        url_list = urls.split("|", 1)
    return url_list[0]

def get_Weitere_Bilder(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    urls = current_row["ImageDownloadlink"]
    if type(urls) is not str:
        return ""
    else:
        first_split = urls.split("|", 1)
    if len(first_split) < 2:
        return ""
    else:
        return first_split[1].replace("|", ";")
    
def get_ean(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["EAN"]

def get_herstellerbezeichnung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return str(current_row["ItemCode"]).strip() + ", " + str(current_row["Name"]).strip() + ", " + str(current_row["Colour"]).strip()

def get_grundpreis_menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Grundpreis Menge' in the original data file.")
    return ""

def get_grundpreis_einheit(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Grundpreis Einheit' in the original data file.")
    return ""

def get_destatis_warennummer(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Destatis warennummer' in the original data file.")
    return ""

def get_country_of_manufacture(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["ItemCountryOfOrigin"]

def get_manufacturer_nr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["ItemCode"]

def get_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Composition"]

def get_passform(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Fit"]

def get_simples_skus(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return ''
    else:
        current_LiNr.reverse()
        return ','.join(current_LiNr)

def get_LiNr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return 'n'+str(current_row_nr)
    else:
        return 'nM'+str(total_row_nr)
    
def get_base_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    color_name = get_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)
    color_name_lower = color_name.lower().strip()
    if color_name_lower in colors_dict.keys():
        return colors_dict[color_name_lower]
    else:
        return ""
    
# def get_pack_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     try: 
#         name = get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)
#         input = name + " " + current_attr
#         pred = model_pack_laenge.predict([input])[0]
#     except:
#         pred = ""
#     return pred

# def get_pack_breite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     try: 
#         name = get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)
#         input = name + " " + current_attr
#         pred = model_pack_breite.predict([input])[0]
#     except:
#         pred = ""
#     return pred

# def get_pack_hoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     try: 
#         name = get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr)
#         input = name + " " + current_attr
#         pred = model_pack_hoehe.predict([input])[0]
#     except:
#         pred = ""
#     return pred

# def get_is_shop(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("1 is entered as the default value for 'is_shop'. This should normally be defined by the user.")
#     return 1

# def get_is_stock_item(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("0 is entered as the default value for 'is_stock_item'. This should normally be defined by the user.")
#     return 0

def get_season(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Season"]

def get_pvs_verpackungstyp(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gebisse','Sattelgurte']:
            return 'Karton'
        else:
            return 'Polybag'
    else:
        return ''

def get_gefahrgut(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("'Nein' or 0 is entered as the default value for 'gefahrgut'.")
    if row_is_simple:
        return 'Nein'
    else:
        return 0

def get_VPE(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("1 is entered as the default value for 'VPE'")
    return 1

# def get_Cost_Discount(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
#     # print("No information was found for 'Cost Discount' in the original data file.")
#     return ""

def get_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    color_info = current_row["Colour"]
    color_into_list = color_info.split(" - ", 1)
    if len(color_into_list) == 2:
        return color_into_list[1]
    else:
        return ""

def get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    
    if current_row["Group"] in dict_zg_gr.keys():
        return dict_zg_gr[current_row["Group"]]
    elif current_row["SubGroup"] in ["Putztaschen", "Putztaschen"]:
        return "Pferd"
    elif current_row["Gender"] == "Kinder":
        return "Kinder"
    elif current_row["Gender"] == "Herren":
        return "Herren"
    else: 
    
        input_string = current_row["Name"] + " " + current_row["Brand"] + " " + \
            current_row["Group"] + " " + str(current_row["SubGroup"]) + " " + current_row["Season"] + " " + \
            current_row["Colour"] + " " + current_row["Gender"]
        
        def preprocess_str(doc):
            doc = doc.translate(doc.maketrans("\n\t\r", "   "))
            doc = re.sub(r'[^a-zA-Z\s]', ' ', doc, flags=re.I|re.A)
            doc = doc.lower()
            doc = re.sub(r'\s+', ' ', doc).strip()
            return doc
        
        input_string = preprocess_str(input_string)
        pred_label = model_zg.predict(input_string)[0][0]
        return label_mapper_zg[pred_label]

# Functions for option columns

def get_rueckenlaenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken', 'Hundedecken']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_halsteil(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_fuellung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken']:
        return "Unknown"
    else:
        return ""
    
def get_denier(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_materialeigenschaft (use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_produktmerkmale (use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_pflegehinweis(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
        return current_row["CareInstructions"]

def get_hosen_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Hosen']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_besatz(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Hosen']:
        return current_row["SubGroup"]
    else:
        return ""

def get_oberbekleidung_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Oberbekleidung']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_schuhgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schuhe, Stiefel und Socken']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_verschlussart_schuhe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schuhe, Stiefel und Socken']:
        return current_row["Closure"]
    else:
        return ""

def get_wadenweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schuhe, Stiefel und Socken']:
        return "Unknown"
    else:
        return ""

def get_schafthoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schuhe, Stiefel und Socken']:
        return "Unknown"
    else:
        return ""

def get_sporen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Sporen']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_sporenriemen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Sporenriemen']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_sporenriemen_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Sporenriemen']:
        return current_row["Composition"]
    else:
        return ""

def get_kopfgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Reithelme']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_schutzwesten_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schutzwesten']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_gerten_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Gerten und Peitschen']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_pferdegroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Trensen, Kandaren und Halfter','Fliegenhauben', 'Hilfszuegel', 'Beinschutz']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_ausfuehrung_halfter(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Trensen, Kandaren und Halfter']:
        return "Unknown"
    else:
        return ""

def get_hilfszuegel_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Hilfszuegel']:
        return "Unknown"
    else:
        return ""

def get_strick_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Stricke']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_verschlussart_stricke(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Stricke']:
        return current_row["Closure"]
    else:
        return ""

def get_gebiss_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Gebisse']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_gebiss_staerke(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Gebisse']:
        return "Unknown" # This is mandatory information
    else:
        return ""

def get_gebissart(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Gebisse']:
        return "Unknown"
    else:
        return ""

def get_gebissmaterial(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Gebisse']:
        return current_row["Composition"]
    else:
        return ""

def get_sattelgurt_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Sattelgurte']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_art_des_sattelgurtes(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Sattelgurte']:
        return "Unknown"
    else:
        return ""
    
def get_beinschutz_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Beinschutz']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_inhalt(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Pflegeprodukte', 'Futter', 'Heimtierfutter']:
        return "Unknown" # This is mandatory information
    else:
        return ""

def get_pferdefutter_art(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Futter']:
        return "Unknown"
    else:
        return ""

def get_handschuh_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Handschuhe']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_sitzgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Saettel']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_kammerweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Saettel']:
        return "Unknown" # This is mandatory information. Also not clear if Size columns refers to this or sitzgroesse.
    else:
        return ""

def get_schabracken_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Schabracken']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_trittflaeche(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Steigbügel']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_riemen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Steigbuegelriemen']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_zubehoer_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Pferdezubehoer', 'Heimtierzubehoer', 'Elektronikzubehoer']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_accessoires_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Accessoires']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_halsband_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Halsbänder']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_halsband_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Halsbänder']:
        return "Unknown" # This is mandatory information. Also not clear if Size columns refers to this or halsband_groesse.
    else:
        return ""

def get_heimtierfutter_art(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Heimtierfutter']:
        return "Unknown"
    else:
        return ""

def get_leinen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Leinen und Geschirre']:
        if current_row["Size"] in size_mapper.keys():
            size = size_mapper[current_row["Size"]]
        else:
            size = current_row["Size"]
        return size
    else:
        return ""

def get_kabel(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Elektronik']:
        return "Unknown"
    else:
        return ""

def get_leistung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple and current_attr in ['Elektronik']:
        return "Unknown"
    else:
        return ""
