# import pandas as pd
import re
# import csv
import joblib
import nltk
import contractions
# import tqdm
from huggingface_hub import hf_hub_download


### Setting up all of the dictionarys needed for BUSSE

### getting the dictionary for the different Warengruppen-IDs
Warengruppen_dict = {
    'BEF': 'Sattelgurte',
    'BGD': 'Schabracken',
    'BHZ': 'Trensen, Kandaren und Halfter',
    'BHM': 'Trensen, Kandaren und Halfter',
    'BHG': 'Trensen, Kandaren und Halfter',
    'BMG': 'Pferdezubehoer',
    'BML': 'Pferdezubehoer',
    'BJH': 'Gebisse',
    'BJG': 'Gebisse',
    'BJK': 'Gebisse',
    'BJE': 'Gebisse',
    'BJS': 'Gebisse',
    'BJR': 'Gebisse',
    'BJP': 'Gebisse',
    'BHX': 'Pferdezubehoer',
    'BDZ': 'Pferdezubehoer',
    'BMP': 'Stricke',
    'BQG': 'Trensen, Kandaren und Halfter',
    'BQS': 'Stricke',
    'BOC': 'Decken',
    'BOF': 'Decken',
    'BOL': 'Decken',
    'BOI': 'Decken',
    'BOY': 'Decken',
    'BOJ': 'Decken',
    'BIG': 'Beinschutz',
    'BIL': 'Beinschutz',
    'BX': 'Fliegenhauben',
    'EDG': 'Handschuhe',
    'EDW': 'Handschuhe',
    'EFUG': 'Schuhe, Stiefel und Socken',
    'EFUW': 'Schuhe, Stiefel und Socken',
    'EN': 'Pferdezubehoer',
    'EFZ': 'Schuhe, Stiefel und Socken',
    'EBS': 'Schuhe, Stiefel und Socken',
    'EBL': 'Oberbekleidung',
    'BMT': 'Trensen, Kandaren und Halfter'
}

from src.stopwords_de import stopwords
nltk.data.load("../data/german.pickle")
nltk.data.load("../data/german")

def normalize_document(doc):
    # fix contractions
    doc = contractions.fix(doc)
    # remove special characters and digits
    doc = re.sub(r'[^a-zA-z0-9\s]','',doc, flags = re.I|re.A)
    # lower case
    doc = doc.lower()
    # strip whitespaces
    doc = doc.strip()
    doc = re.sub(r' +',' ', doc)
    # tokenize document
    tokens = nltk.word_tokenize(text = doc, language = 'german')
    #filter stopwords out of document
    filtered_tokens = [token.strip() for token in tokens if token.strip() not in stopwords]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc


zielgruppen_model = joblib.load(
    hf_hub_download("Adriperse/RD-CA2", "BUSSE_zielgruppe_model.pkl")
)


### creating the dictionary for the different o_Optionen depending on the value of Attributmenge
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

### creating a dictionary for the different possible values for the Größe in the product data and the corresponding Pferdegroesse
# in the csv-File
dict_pferdegroesse = {'STANDARD': 'Einheitsgröße',
'WB (44 cm)': 'WB',
'MSH (31 cm)': 'Mini Shetty',
'WB': 'WB',
'Zügelmaß 1.5x145': '1,5x145',
'Zügelmaß 1.9x135': '1,9x135',
'Zügelmaß 1.5x155': '1,5x155',
'SH': 'Shetty',
'P': 'Pony',
'VB': 'VB',
'XWB': 'WB-XL'}

### creating a dictionary for the different values for the zubehoergroesse
# this dict probably will need to be replaced by some ML model / updated when theres more data
dict_zubehoergroesse = {'WB': 'WB',
'14': '14m',
'P': 'Pony',
'VB': 'VB',
'STANDARD': 'Einheitsgröße',
'28.5x20.5x3': 'Einheitsgröße',
'45x20x55': '45x20x55cm',
'40x25x25': '40x25x25cm'}


def get_type(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'simple'
    else:
        return 'configurable'

def get_Menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    ### getting the dictionary for the different Warengruppen-IDs
    Warengruppen_dict = {
        'BEF': 'Sattelgurte',
        'BGD': 'Schabracken',
        'BHZ': 'Trensen, Kandaren und Halfter',
        'BHM': 'Trensen, Kandaren und Halfter',
        'BHG': 'Trensen, Kandaren und Halfter',
        'BMG': 'Pferdezubehoer',
        'BML': 'Pferdezubehoer',
        'BJH': 'Gebisse',
        'BJG': 'Gebisse',
        'BJK': 'Gebisse',
        'BJE': 'Gebisse',
        'BJS': 'Gebisse',
        'BJR': 'Gebisse',
        'BJP': 'Gebisse',
        'BHX': 'Pferdezubehoer',
        'BDZ': 'Pferdezubehoer',
        'BMP': 'Stricke',
        'BQG': 'Trensen, Kandaren und Halfter',
        'BQS': 'Stricke',
        'BOC': 'Decken',
        'BOF': 'Decken',
        'BOL': 'Decken',
        'BOI': 'Decken',
        'BOY': 'Decken',
        'BOJ': 'Decken',
        'BIG': 'Beinschutz',
        'BIL': 'Beinschutz',
        'BX': 'Fliegenhauben',
        'EDG': 'Handschuhe',
        'EDW': 'Handschuhe',
        'EFUG': 'Schuhe, Stiefel und Socken',
        'EFUW': 'Schuhe, Stiefel und Socken',
        'EN': 'Pferdezubehoer',
        'EFZ': 'Schuhe, Stiefel und Socken',
        'EBS': 'Schuhe, Stiefel und Socken',
        'EBL': 'Oberbekleidung',
        'BMT': 'Trensen, Kandaren und Halfter'
    }
    if current_row['Warengruppen-ID'] in Warengruppen_dict.keys():
        attr =  Warengruppen_dict[current_row['Warengruppen-ID']]
    else:
        attr = 'Unknown'
    return attr

### THERE ARE SOME THINGS UNCLEAR ON HOW THE name WORKS, SO THIS FUNCTION ISNT FINISHED YET
def get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ' '.join([word.title() for word in current_row['Bezeichnung'].split() if word != 'BUSSE'])

def get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in Optionen_dict.keys():
        return Optionen_dict[current_attr]
    else:
        return ''

def get_Orphan(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr) == '':
        return 1
    else:
        return 0

def get_Hat_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'nein'
    else:
        return 'ja'

def get_visibility(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if use_configurable:
        if row_is_simple:
            return 'Not Visible Individually'
        else:
            return 'Catalog, Search'
    else:
        return 'Catalog, Search'

def get_vendor(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return 'BUSSE'

def get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return 'BUSSE'

def get_cost(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    cost = current_row['VK-Preis']
    if cost.is_integer():
        return int(cost)
    else:
        return str(cost).replace('.',',')

def get_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    price = current_row['UVP']
    if price.is_integer():
        return int(price)
    else:
        return str(price).replace('.',',')

### THIS METHOD NEEDS TO BE REWORKED AT SOME POINT
def get_tax_class_id(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return 1

### THIS METHOD NEEDS TO BE REWORKED AT SOME POINT
def get_Beschreibung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_Gewicht(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return str(current_row['kg/Einheit']).replace('.',',')

def get_Bild(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if len(current_row['picture_ids'])>0:
        return 'https://images.ridersdeal.com/m2/BUSSE/'+current_row['picture_ids'][0].split('.')[0]+'.jpg'
    else:
        return ''

def get_Weitere_Bilder(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if len(current_row['picture_ids'])>1:
        pic_idx = current_row['picture_ids'][1:]
        pic_links = []
        for i in range(len(pic_idx)):
            pic_links.append('https://images.ridersdeal.com/m2/BUSSE/'+pic_idx[i].split('.')[0]+'.jpg')
        return ';'.join(pic_links)
    else:
        return ''

def get_ean(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return current_row['Barcode']
    else:
        return ''    

def get_herstellerbezeichnung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return str(current_row['Artikelnummer'])+', '+str(current_row['Bezeichnung'])+', '+ str(current_row['Größe']) +', '+str(current_row['Farbe']) + ', '+ str(current_row['Barcode'])

### THIS METHOD NEEDS TO BE REWORKED
def get_grundpreis_menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### THIS METHOD NEEDS TO BE REWORKED
def get_grundpreis_einheit(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_destatis_warennummer(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return current_row['WKN']

def get_country_of_manufacture(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return current_row['Ursprungsland']
    
def get_manufacturer_nr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return current_row['Artikelnummer']
    else:
        return ''

### THIS METHOD IS WRONG BUT MATERIAL ONLY HAS VALUES FOR ONE SPECIFIC ITEM AND I DONT KNOW WHAT THE RULE IS
def get_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### THIS METHOD IS WRONG BUT MATERIAL ONLY HAS VALUES FOR ONE SPECIFIC ITEM AND I DONT KNOW WHAT THE RULE IS
def get_passform(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_simples_skus(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return ''
    else:
        current_LiNr.reverse()
        return ','.join(current_LiNr)

def get_LiNr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'n'+str(current_row_nr)
    else:
        return 'nM'+str(total_row_nr)

def get_base_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_row['Farbtyp'] == 'Farbe':
        if current_row['Farbe'] in colors_dict.keys():
            return colors_dict[current_row['Farbe']]
        else:
            return current_row['Farbe'].split('/')[0].title()
    else:
        return ''



### this is just a guess if this works that way
def get_pvs_verpackungstyp(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        if current_attr in ['Gebisse','Sattelgurte']:
            return 'Karton'
        else:
            return 'Polybag'
    else:
        return ''

### all values in the current data are 0 / Nein, so if we get examples where that isnt the case then this will be adjusted
def get_gefahrgut(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'Nein'
    else:
        return 0

### all values in the current data are 1, so if we get examples where that isnt the case then this will be adjusted
def get_VPE(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return 1

def get_oberbekleidung_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Oberbekleidung':
        return current_row['Größe']
    return ''

def get_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_row['Farbtyp'] == 'Farbe':
        return current_row['Farbe']
    return ''

def get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Schuhe, Stiefel und Socken':
        return ''
    else:
        input = current_row['Bezeichnung'] + ' ' + current_row['Warengruppen-ID']
        return zielgruppen_model.predict([normalize_document(input)])[0]

### I dont know how the pflegehinweis is determined -> probably a ML model
def get_pflegehinweis(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_schuhgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Schuhe, Stiefel und Socken':
        return current_row['Größe']
    return ''

### all data in the example data set is empty
def get_wadenweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### all data in the example data set is empty
def get_schafthoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### this is only non-empty for Attributmenge = Stricke, but i dont know how the values are determined in the Stricke case
def get_verschlussart(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Stricke':
        return 'Unknown'
    return ''

def get_handschuh_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Handschuhe':
        if row_is_simple:
            return str(current_row['Größe']).split('_')[-1]
    return ''

def get_pferdegroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in ['Trensen, Kandaren und Halfter','Fliegenhauben']:
        if current_row['Größe'] in dict_pferdegroesse.keys():
            return dict_pferdegroesse[current_row['Größe']]
        else:
            return 'Unknown'
    return ''

def get_beinschutz_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in ['Beinschutz']:
        return current_row['Größe']
    return ''

def get_rueckenlaenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in ['Decken']:
        if str(current_row['Größe']).isdigit():
            return str(current_row['Größe'])+'cm'
        else:
            return current_row['Größe']
    return ''

### there are only empty values in the current data set
def get_halsteil(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
   return ''

### I dont know how this is determined when its not empty
def get_fuellung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_row['Warengruppen-ID'] == 'BOY':
        if row_is_simple:
            return 'I dont know'
    return ''

### all data in the example data set is empty
def get_denier(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### all data in the example data set is empty
def get_materialeigenschaft(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### all data in the example data set is empty
def get_produktmerkmale(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in ['Sattelgurte','Stricke']:
        if row_is_simple:
            leng = current_row['Größe']
            if leng.replace(".", "").isnumeric():
                if float(leng) >= 10:
                    leng = leng + 'cm'
                else:
                    leng = leng + 'm'
                return leng
            else:
                return 'Unknown'
    return ''

def get_gebiss_staerke(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Gebisse':
        pattern = r'(\d[\d\s,]*)+mm'
        matches = re.findall(pattern, current_row['Bezeichnung'])
        if len(matches)>0:
            return matches[0] + 'mm'
        else:
            return ''
    else:
        return ''

def get_gebiss_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Gebisse':
        if row_is_simple:
            values = str(current_row['Größe']).split('|')
            if len(values) == 2:
                value = values[0]
                value = value.replace(' ','')
                value = value.replace('.',',')
                return value
            else:
                return 'Unknown'
    return ''

### Are there some other possible values than doppelt gebrochen?
def get_gebissart(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Gebisse':
        if 'doppelt gebr' in current_row['Bezeichnung']:
            return 'Doppelt gebrochen'
    return ''

def get_zubehoer_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Pferdezubehoer':
        if row_is_simple:
            if current_row['Größe'] in dict_zubehoergroesse.keys():
                return dict_zubehoergroesse[current_row['Größe']]
            else:
                return 'Unknown'
    return ''

### all data in the example data set is empty
def get_ausfuehrung_halfter(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_schabracken_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Schabracken':
        if row_is_simple: # im not sure if that is needed, there is no data currently with type = configurable and Attributmenge = Schabracken
            return current_row['Größe'][3:]
    return ''

### all data in the example data set is empty
def get_art_des_sattelgurtes(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''