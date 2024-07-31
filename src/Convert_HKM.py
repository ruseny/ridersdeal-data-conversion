###################
### Convert HKM ###
###################

# Dependencies
import pandas as pd
import numpy as np
import re
import string
import fasttext
import os
#load env file
from dotenv import load_dotenv
load_dotenv()

fasttext.FastText.eprint = lambda x: None # Disable fasttext warnings

# Dict for mapping to base_color. Should later be moved to the main file.
# color_mapper_df = pd.read_excel("../../data/raw/color_dict.xlsx", sheet_name = 0)
# color_mapper_df["Hersteller"] = color_mapper_df["Hersteller"].str.lower().str.strip()
# color_mapper = color_mapper_df.set_index("Hersteller").to_dict()["Grundfarbe"]

# Dict for mapping attributset to option column names
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
dict_att_ug = {
    "Funktionsshirts & Sweatshirts" : "Oberbekleidung", 
    "Gamaschen & Hufglocken"        : "Beinschutz",  
    "Gürtel"                        : "Accessoires", 
    "Hundebetten"                   : "Heimtierzubehoer", 
    "Hundefressnäpfe"               : "Heimtierzubehoer", 
    "Hundegeschirre"                : "Leinen und Geschirre", 
    "Hundehalsbänder"               : "Halsbänder", 
    "Hundeleinen"                   : "Leinen und Geschirre", 
    "Hundemäntel"                   : "Hundedecken", 
    "Mützen & Stirnbänder"          : "Accessoires", 
    "Pferde-Putzzeug"               : "Pferdezubehoer", 
    "Pflegemittel"                  : "Pflegeprodukte", 
    "Poloshirts & T-Shirts"         : "Oberbekleidung", 
    "Reitblusen & Reithemden"       : "Oberbekleidung", 
    "Reitchaps & Stiefelschäfte"    : "Schuhe, Stiefel und Socken", 
    "Reithandschuhe"                : "Handschuhe", 
    "Reithosen Damen & Kinder"      : "Hosen", 
    "Reithosen Herren"              : "Hosen", 
    "Reitjacken"                    : "Oberbekleidung", 
    "Reitsocken"                    : "Schuhe, Stiefel und Socken", 
    "Reitwesten"                    : "Oberbekleidung", 
    "Sattelgurte"                   : "Sattelgurte", 
    "Schals & Tücher"               : "Accessoires", 
    "Schmuck"                       : "Accessoires", 
    "Steigbügelriemen"              : "Steigbuegelriemen", 
    "Strick-/Fleecejacken"          : "Oberbekleidung", 
    "Turnierjacket Damen"           : "Oberbekleidung"   
}
dict_att_sp = {
    'Abschwitzdecken': 'Decken',
    'Ausbindezügel': 'Hilfszuegel',
    'Bandagen': 'Beinschutz',
    'Doppelt gebrochen': 'Gebisse',
    'Dreieckszügel': 'Hilfszuegel',
    'Einfach gebrochen': 'Gebisse',
    'Fliegendecken': 'Decken',
    'Fliegenfransen': 'Pferdezubehoer',
    'Führanlagendecken': 'Decken',
    'Gebiss-Zubehör': 'Pferdezubehoer',
    'Gummi-Reitstiefel & Gummistiefel': 'Schuhe, Stiefel und Socken',
    'Halfter': 'Trensen, Kandaren und Halfter',
    'Halfter + Strick Set': 'Trensen, Kandaren und Halfter',
    'Kandaren': 'Gebisse',
    'Lederhalfter': 'Trensen, Kandaren und Halfter',
    'Lederreitstiefel': 'Schuhe, Stiefel und Socken',
    'Martingal': 'Hilfszuegel',
    'Mexikanische Reithalfter': 'Trensen, Kandaren und Halfter',
    'Modische Schuhe & Stiefel': 'Schuhe, Stiefel und Socken',
    'Nierendecken': 'Decken',
    'Pelham': 'Gebisse',
    'Reithelme': 'Reithelme',
    'Reitstiefeletten': 'Schuhe, Stiefel und Socken',
    'Sattelgurtschoner': 'Sattelgurte',
    'Sattelpads': 'Schabracken',
    'Schabracken': 'Schabracken',
    'Schwedische Reithalfter': 'Trensen, Kandaren und Halfter',
    'Sicherheitswesten': 'Schutzwesten',
    'Sonstige Hilfszügel': 'Hilfszuegel',
    'Stalldecken': 'Decken',
    'Stallschuhe': 'Schuhe, Stiefel und Socken',
    'Stoffschuhe': 'Schuhe, Stiefel und Socken',
    'Stricke': 'Stricke',
    'Trensen-Zubehör': 'Pferdezubehoer',
    'Trensenhalter': 'Pferdezubehoer',
    'Turnierjacket Kinder': 'Oberbekleidung',
    'Unterlagen': 'Beinschutz',
    'Unterleggebisse': 'Gebisse',
    'Weidedecken': 'Decken',
    'Westerngebisse': 'Gebisse',
    'Westernpads': 'Schabracken',
    'Westernsattelgurte & Steigbügel': 'Sattelgurte',
    'Winter-Reitstiefel': 'Schuhe, Stiefel und Socken',
    'Zubehör': 'Accessoires'
 }

# Lists and dicts for season to be checked before predicting from model
list_sn_gj_gr = ["Accessoires", "Geschenkartikel", "Hund", "Stall & Weide"]
list_sn_gj_ugr = [
    'Bandagen & Bandagierunterlagen',
    'Funktionsshirts & Sweatshirts',
    'Gebisse',
    'Gürtel',
    'Halfter & Stricke',
    'Hilfszügel & Vorderzeug',
    'Lammfellprodukte',
    'Longierbedarf',
    'Pferde-Putzzeug',
    'Pflegemittel',
    'Reitblusen & Reithemden',
    'Reitchaps & Stiefelschäfte',
    'Reithelme & Sicherheitswesten',
    'Reithosen Herren',
    'Reitsocken',
    'Reitunterwäsche',
    'Reitwesten',
    'Sattelgurte',
    'Sattelunterlagen',
    'Schals & Tücher',
    'Shettyzubehör',
    'Sporen',
    'Steigbügel',
    'Steigbügelriemen',
    'Stollen',
    'Strick-/Fleecejacken',
    'Sättel',
    'Trensen',
    'Turnierbedarf',
    'Westernpferde',
    'Westernreiter'
]
dict_sn_sp = {
    '3/4-Besatz': 'Ganzjahres',
    'Fliegenfransen': 'Ganzjahres',
    'Fliegenhauben': 'Ganzjahres',
    'Ganzjahresjacken': 'Ganzjahres',
    'Hufglocken': 'Ganzjahres',
    'Jodhpur Reithose': 'Ganzjahres',
    'Kniebesatz': 'Ganzjahres',
    'Regenjacken & Mäntel': 'Ganzjahres',
    'Reitmäntel': 'Ganzjahres',
    'Silikon-Kniebesatz': 'Ganzjahres',
    'Stalldecken': 'Winter',
    'Stoffschuhe': 'Ganzjahres',
    'Sweatjacken': 'Ganzjahres',
    'Tops': 'Sommer',
    'Vollbesatz': 'Ganzjahres',
    'Winter-Reitstiefel': 'Winter'
 }

#Size conversion
size_mapper = {
    "St" : "Einheitsgroesse", 
    "Warmblut" : "WB", 
    "Vollblut" : "VB", 
    "Vielseitigkeit" : "VS",
    "Dressur" : "DR",
    "Pony Dressur" : "Pony-DR",
    "PonyViels." : "Pony-VS", 
    "Vollblut/Warmblut" : "VB-WB",
    "Kaltblut" : "KB", 
    "Mini Shetty" : "Mini-Shetty", 
    "Stück" : "Einheitsgroesse", 
    "Universalgröße" : "Einheitsgroesse",
    "Pony Viels." : "Pony-VS",
    "Pony Vielseitigkeit/Pony" : "Pony-VS",
    "Pony Dressur/Pony" : "Pony-DR",
    "Ant. VS" : "VS", 
    "Ant. Dressur" : "DR",
    "Mini Shetty " : "Mini-Shetty", 
    "Pony Vielseitigkeit" : "Pony-VS"
}

# fastText models, and needed dicts
model_at_path = os.getenv("HKM_ATT_FT_MODEL")
model_zg_path = os.getenv("HKM_ZG_FT_MODEL")
model_sn_path = os.getenv("HKM_SN_FT_MODEL")
model_at = fasttext.load_model(model_at_path)
model_zg = fasttext.load_model(model_zg_path)
model_sn = fasttext.load_model(model_sn_path)
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
    '__label__Steigbuegel': 'Steigbügel',
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
label_mapper_sn = {
    "__label__Ganzjahres" : "Ganzjahres",
    "__label__Sommer" : "Sommer",
    "__label__Winter" : "Winter"
}

### Functions ###

# Functions for main columns

def get_type(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return 'simple'
    else:
        return 'configurable'

def get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):

    if current_row["Untergruppe"] in dict_att_ug.keys():
        return dict_att_ug[current_row["Untergruppe"]]
    elif current_row["Spezifikation"] in dict_att_sp.keys():
        return dict_att_sp[current_row["Spezifikation"]]
    else:

        input_string = str(current_row["Beschreibung"]) + " " + \
            str(current_row["Beschreibung 2"]) + " " + str(current_row["Beschreibung 3"]) + " " + \
            str(current_row["Obergruppe"]) + " " + str(current_row["Gruppe"]) + " " + \
            str(current_row["Untergruppe"]) + " " + str(current_row["Spezifikation"]) + " " + \
            str(current_row["Themenname"])
        
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
    
    if current_row["Beschreibung 3"] in size_mapper.keys():
        size = size_mapper[current_row["Beschreibung 3"]]
    else:
        size = current_row["Beschreibung 3"]

    if "Damen" in current_row["Beschreibung"] or "Herren" in current_row["Beschreibung"] or "Kinder" in current_row["Beschreibung"]:
        target = ""
    elif zielgruppe in ["Damen", "Kinder", "Herren"]:
        target = " für " + zielgruppe
    else:
        target = ""
    
    if not use_configurable:
        return current_row["Beschreibung"] + target
    elif row_is_simple:
        return current_row["Beschreibung"] + target + ", " + str(size)
    else:
        return current_row["Beschreibung"] + target

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
    return "HKM"

def get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Obergruppe"]

def get_cost(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for cost in the original data file.")
    return current_row["Preis Händler EK (EUR)"]

def get_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for price in the original data file.")
    return current_row["Preis Endkunde (EUR)"]

def get_special_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for special price in the original data file.")
    return ""

def get_tax_class_id(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("1 is entered as the default tax class ID for all products.")
    return 1

def get_Beschreibung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return ""

def get_Menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Menge' in the original data file.")
    return ""

def get_Gewicht(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if row_is_simple:
        return current_row["Gewicht"]
    else:
        return 1

def get_Bild(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return ""

def get_Weitere_Bilder(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return ""
    
def get_ean(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["EANNummer"]

def get_herstellerbezeichnung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return str(current_row["Artikelnr."]).strip() + ", " + \
            str(current_row["Beschreibung"]).strip() + ", " + \
            str(current_row["Beschreibung 2"]).strip() + ", " + \
            str(current_row["Beschreibung 3"]).strip() + ", " + \
            str(current_row["EANNummer"]).strip()

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
    return current_row["Herkunftsland"]

def get_manufacturer_nr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return current_row["Artikelnr."]

def get_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return ""

def get_passform(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    return ""

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
    
def get_pack_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("Information on item length is available. Parcel length needs to be calculated.")
    return ""

def get_pack_breite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("Information on item width is available. Parcel width needs to be calculated.")
    return ""

def get_pack_hoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("Information on item height is available. Parcel height needs to be calculated.")
    return ""

def get_is_shop(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("1 is entered as the default value for 'is_shop'. This should normally be defined by the user.")
    return 1

def get_is_stock_item(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("0 is entered as the default value for 'is_stock_item'. This should normally be defined by the user.")
    return 0

def get_season(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if current_row["Obergruppe"] == "Posten":
        return "Winter"
    elif current_row["Gruppe"] in list_sn_gj_gr:
        return "Ganzjahres"
    elif current_row["Untergruppe"] in list_sn_gj_ugr:
        return "Ganzjahres"
    elif current_row["Untergruppe"] == "Mützen & Stirnbänder":
        return "Winter"
    elif current_row["Spezifikation"] in dict_sn_sp.keys():
        return dict_sn_sp[current_row["Spezifikation"]]
    elif "Winter" in current_row["Beschreibung"]:
        return "Winter"
    elif "Sommer" in current_row["Beschreibung"]:
        return "Sommer"
    elif "Summer" in current_row["Beschreibung"]:
        return "Sommer"
    else:
        
        input_string = str(current_row["Beschreibung"]) + " " + \
            str(current_row["Beschreibung 2"]) + " " + str(current_row["Beschreibung 3"]) + " " + \
            str(current_row["Obergruppe"]) + " " + str(current_row["Gruppe"]) + " " + \
            str(current_row["Untergruppe"]) + " " + str(current_row["Spezifikation"]) + " " + \
            str(current_row["Themenname"])
        
        def preprocess_str(doc):      
            doc = doc.translate(doc.maketrans("\n\t\r", "   "))
            doc = re.sub(r'[^a-zA-Z\s]', ' ', doc, flags=re.I|re.A)
            doc = doc.lower()
            doc = re.sub(r'\s+', ' ', doc).strip()
            return doc
        
        input_string = preprocess_str(input_string)
        pred_label = model_sn.predict(input_string)[0][0]
        return label_mapper_sn[pred_label]     

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

def get_Cost_Discount(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    # print("No information was found for 'Cost Discount' in the original data file.")
    return ""

def get_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    color_info = str(current_row["Beschreibung 2"])
    color_into_list = color_info.split(" ", 1)
    if len(color_into_list) == 2:
        return color_into_list[1]
    else:
        return ""

def get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):

    size_simple_l = str(current_row["Beschreibung 3"])\
        .translate(str.maketrans(string.punctuation, " "*len(string.punctuation)))\
        .split()
    if len(size_simple_l) > 0:
        size_simple = size_simple_l[-1]
    else:
        size_simple = "NA"

    if current_row["Gruppe"] == "Hund":
        return "Hund"
    elif current_row["Gruppe"] in ["Pferd", "Stall & Weide"]:
        return "Pferd"
    elif current_row["Gruppe"] == "Reiter" and current_row["Obergruppe"] in ["Bibi & Tina", "Funny Horses", "HKM Kids", "Little sister"]:
        return "Kinder"
    elif current_row["Gruppe"] == "Reiter" and current_row["Untergruppe"] == "Reithosen Herren":
        return "Herren"
    elif current_row["Gruppe"] == "Reiter" and current_row["Untergruppe"] == "Turnierjacket Damen":
        return "Damen"
    elif current_row["Gruppe"] == "Reiter" and current_row["Untergruppe"] == "Reithose Kinder":
        return "Kinder"
    elif current_row["Gruppe"] == "Reiter" and current_row["Spezifikation"] == "Turnierjacket Kinder":
        return "Kinder"
    elif current_row["Gruppe"] == "Reiter" and current_row["Spezifikation"] == "Reitsocken Herren": 
        return "Herren"
    elif current_row["Gruppe"] == "Reiter" and current_row["Themenname"] in ["Kid's", "Kids HW 22"]:
        return "Kinder"
    elif current_row["Untergruppe"] == "Reithosen Damen & Kinder":
        if size_simple in np.arange(86, 177, 6).astype(str).tolist():
            return "Kinder"
        else:
            return "Damen"
    elif "Women" in current_row["Beschreibung"] or "Damen" in current_row["Beschreibung"]:
        return "Damen"
    elif "Kinder" in current_row["Beschreibung"] or "Kinder" in current_row["Beschreibung"]:
        return "Kinder"
    elif "Men" in current_row["Beschreibung"] or "Herren" in current_row["Beschreibung"]:
        return "Herren"
    elif "Unisex" in current_row["Beschreibung"]:
        return "Unisex"
    else:
    
        input_string = str(current_row["Beschreibung"]) + " " + \
            str(current_row["Beschreibung 2"]) + " " + str(current_row["Beschreibung 3"]) + " " + \
            str(current_row["Obergruppe"]) + " " + str(current_row["Gruppe"]) + " " + \
            str(current_row["Untergruppe"]) + " " + str(current_row["Spezifikation"]) + " " + \
            str(current_row["Themenname"])
        
        def preprocess_alphanum(doc):
            doc = doc.translate(doc.maketrans("\n\t\r", "   "))
            doc = re.sub(r'[^a-zA-Z0-9\s]', ' ', doc, flags=re.I|re.A)
            doc = doc.lower()
            doc = re.sub(r'\s+', ' ', doc).strip()
            return doc
        
        input_string = preprocess_alphanum(input_string)
        pred_label = model_zg.predict(input_string)[0][0]
        return label_mapper_zg[pred_label]
    
# Functions for option columns

def get_rueckenlaenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken', 'Hundedecken']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_halsteil(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_fuellung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken']:
        return "Unknown"
    else:
        return ""
    
def get_denier(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_materialeigenschaft (use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_produktmerkmale (use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Decken']:
        return "Unknown"
    else:
        return ""

def get_pflegehinweis(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
        return ""

def get_hosen_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Hosen']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_besatz(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Hosen']:
        if "besatz" in str(current_row["Spezifikation"]).lower():
            return current_row["Spezifikation"]
        else:
            return "Unknown"
    else:
        return ""

def get_oberbekleidung_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Oberbekleidung']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_schuhgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schuhe, Stiefel und Socken']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_verschlussart_schuhe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schuhe, Stiefel und Socken']:
        return "Unknown"
    else:
        return ""

def get_wadenweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schuhe, Stiefel und Socken']:
        return "Unknown"
    else:
        return ""

def get_schafthoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schuhe, Stiefel und Socken']:
        return "Unknown"
    else:
        return ""

def get_sporen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Sporen']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_sporenriemen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Sporenriemen']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_sporenriemen_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Sporenriemen']:
        return "Unknown"
    else:
        return ""

def get_kopfgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Reithelme']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_schutzwesten_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schutzwesten']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_gerten_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gerten und Peitschen']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_pferdegroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Trensen, Kandaren und Halfter','Fliegenhauben', 'Hilfszuegel', 'Beinschutz']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_ausfuehrung_halfter(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Trensen, Kandaren und Halfter']:
        return "Unknown"
    else:
        return ""

def get_hilfszuegel_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Hilfszuegel']:
        return "Unknown"
    else:
        return ""

def get_strick_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Stricke']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_verschlussart_stricke(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Stricke']:
        return "Unknown"
    else:
        return ""

def get_gebiss_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gebisse']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_gebiss_staerke(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gebisse']:
        return "Unknown" # This is mandatory information
    else:
        return ""

def get_gebissart(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gebisse']:
        return "Unknown"
    else:
        return ""

def get_gebissmaterial(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Gebisse']:
        return "Unknown"
    else:
        return ""

def get_sattelgurt_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Sattelgurte']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_art_des_sattelgurtes(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Sattelgurte']:
        return "Unknown"
    else:
        return ""

def get_beinschutz_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Beinschutz']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_inhalt(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Pflegeprodukte', 'Futter', 'Heimtierfutter']:
        return "Unknown" # This is mandatory information
    else:
        return ""

def get_pferdefutter_art(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Futter']:
        return "Unknown"
    else:
        return ""

def get_handschuh_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Handschuhe']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_sitzgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Saettel']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_kammerweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Saettel']:
        return "Unknown" # This is mandatory information. Also not clear if Size columns refers to this or sitzgroesse.
    else:
        return ""

def get_schabracken_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Schabracken']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_trittflaeche(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Steigbügel']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_riemen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Steigbuegelriemen']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_zubehoer_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Pferdezubehoer', 'Heimtierzubehoer', 'Elektronikzubehoer']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_accessoires_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Accessoires']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_halsband_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Halsbänder']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_halsband_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Halsbänder']:
        return "Unknown" # This is mandatory information. Also not clear if Size columns refers to this or halsband_groesse.
    else:
        return ""

def get_heimtierfutter_art(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Heimtierfutter']:
        return "Unknown"
    else:
        return ""

def get_leinen_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Leinen und Geschirre']:
        if current_row["Beschreibung 3"] in size_mapper.keys():
            size = size_mapper[current_row["Beschreibung 3"]]
        else:
            size = current_row["Beschreibung 3"]
        return size
    else:
        return ""

def get_kabel(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Elektronik']:
        return "Unknown"
    else:
        return ""

def get_leistung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr):
    if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr, current_attr) in ['Elektronik']:
        return "Unknown"
    else:
        return ""

