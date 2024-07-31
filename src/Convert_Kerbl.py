# import pandas as pd

### creating a dictionary for the values of the column Attributmenge depending on the values of the column PRODUKTNAME_KOMPLETT_STR
dict_Attributmenge = {
    'Regenmantel': 'Oberbekleidung',
    'Hoody Jacke': 'Oberbekleidung',
    'Blouson': 'Oberbekleidung',
    'Weste': 'Oberbekleidung',
    'Sweater': 'Oberbekleidung',
    'Active Shirt': 'Oberbekleidung',
    'Poloshirt': 'Oberbekleidung',
    'Top': 'Oberbekleidung',
    'Competition Shirt': 'Oberbekleidung',
    'Riding Tights SL': 'Hosen',
    'Riding Tights': 'Hosen',
    'Reithose LS': 'Hosen',
    'Reithose Grip': 'Hosen',
    'Sportsocken': 'Schuhe, Stiefel und Socken',
    'Reitstrümpfe Competition': 'Schuhe, Stiefel und Socken',
    'Reithandschuh': 'Handschuhe',
    'Softgamaschen Mesh': 'Beinschutz',
    'Hufglocken': 'Beinschutz',
    'Halfter': 'Trensen, Kandaren und Halfter',
    'Führstrick': 'Stricke',
    'Schabracke': 'Schabracken',
    'Fliegenhaube': 'Fliegenhauben',
    'Fliegendecke': 'Decken',
    'Gürtel': 'Accessoires'
}

### creating a dictionary to get the values of o_Optionen depending on the value of Attributmenge
dict_o_Optionen = {
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

### creating a dictionary to get the first part of the name column using the value of PRODUKTNAME_KOMPLETT_STR
dict_name = {
    'Regenmantel' : 'Regenmantel FS',
    'Hoody Jacke' : 'Jacke mit Kapuze FS',
    'Blouson' : 'Blouson FS',
    'Weste' : 'Weste FS',
    'Sweater' : 'Sweater FS',
    'Active Shirt' : 'Langarmshirt Active FS',
    'Poloshirt' : 'Poloshirt FS',
    'Top' : 'Mesh-Top FS',
    'Competition Shirt' : 'Turniershirt FS',
    'Riding Tights SL' : 'Silikonvollbesatzreitleggings SL',
    'Riding Tights' : 'Silikonvollbesatzreitleggings FS',
    'Reithose LS' : 'Kunstledervollbesatzreithose FS',
    'Reithose Grip' : 'Silikonvollbesatzreithose Grip FS',
    'Sportsocken' : 'Sportsocken FS',
    'Reitstrümpfe Competition' : 'Turnierreitstrümpfe FS',
    'Reithandschuh' : 'Reithandschuhe FS',
    'Softgamaschen Mesh' : '2er Set Softgamaschen Mesh',
    'Hufglocken' : '2er Set Hufglocken FS',
    'Halfter' : 'Halfter FS',
    'Führstrick' : 'Führstrick FS',
    'Schabracke' : 'Sometimes Vielseitigkeitsschabracke, sometimes Dressurschabracke', # this is the only value where the dict wouldnt work, 
    # will need to be a special case but i dont know the rule when which value appears
    'Fliegenhaube' : 'Fliegenhaube FS',
    'Fliegendecke' : 'Fliegendecke FS',
    'Gürtel' : 'Gürtel FS'
}

### creating a dictionary to get the values of beinschutz_groesse depending on a word appearing in ERP_BEZEICHNUNG_2_STR
dict_beinschutz_groesse = {
    'Pony (S)' : 'Pony',
    'Cob (M)' : 'VB',
    'Full (L)' : 'WB',
    'Full (XL)' : 'WB-XL'
}

### creating a dictionary to get the values of handschuh_groesse depending on a word appearing in ERP_BEZEICHNUNG_2_STR
dict_handschuh_groesse = {
    'Gr. XXS' : 5,
    'Gr. XS' : 6,
    'Gr. S' : 7,
    'Gr. M' : 8,
    'Gr. L' : 9,
    'Gr. XL' : 10
}

### creating a dictionary to get the values of besatz depending on the value of BESATZ_HOSE_SEL
dict_besatz = {
    'Vollbesatz mit Covalliero-Grip' : 'Silikonvollbesatz',
    'Vollbesatz' : 'Kunstledervollbesatz'
}

### creating a dictionary to get the values of pferdegroesse depending on a word in ERP_BEZEICHNUNG_2_STR
dict_pferdegroesse ={
    'Pony' : 'Pony',
    'FULL' : 'WB',
    'COB/WB' : 'WB', # the order here is important, because it checks the keys in order and COB/WB is supposed to map to WB and not VB
    'COB' : 'VB'     # (COB/WB would be mapped to VB if they were swapped because it stops checking after it finds a fitting key)
}

### creating a dictionary to get the values of schabracken_groesse depending on a word in ERP_BEZEICHNUNG_2_STR
dict_schabracken_groesse = {
    'Pony VS' : 'Pony-VS',
    'Pony DS' : 'Pony-DR',
    'VS' : 'WB-VS',
    'DR' : 'WB-DR'
}

dict_schabracken_name = {
    'Pony VS' : 'Vielseitigkeitsschabracke',
    'Pony DS' : 'Dressurschabracke',
    'VS' : 'Vielseitigkeitsschabracke',
    'DR' : 'Dressurschabracke',
}

dict_schabracken_name2 = {
    'Pony VS' : 'Pony-VS',
    'Pony DS' : 'Pony-DR',
    'VS' : 'WV-VS',
    'DR' : 'WB-DR'
}

def get_type(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'simple'
    else:
        return 'configurable'

def get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    produktname = current_row['PRODUKTNAME_KOMPLETT_STR']
    if produktname in dict_Attributmenge.keys():
        return dict_Attributmenge[produktname]
    else:
        return 'Unknown'

def get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Schabracken':
        current_key = ''
        for key in dict_schabracken_name:
            if key in current_row['ERP_BEZEICHNUNG_2_STR'] and len(key) > len(current_key):
                current_key = key
        if current_key == '':
            return 'Unknown'
        name = current_row['ERP_BEZEICHNUNG_1_STR']
        name = name.replace('Schabracke', dict_schabracken_name[current_key])
    else:
        name = dict_name[current_row['PRODUKTNAME_KOMPLETT_STR']]
    zielgruppe = get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
    if zielgruppe in ['Damen','Kinder']:
        name += ' für '+zielgruppe
    if row_is_simple:
        optionen = get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
        if current_attr == 'Schabracken':
            name += ', ' + dict_schabracken_name2[current_key]
        if optionen != '':
            name += ', ' + str(eval('get_'+optionen)(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)).replace(' ','')
    name = name.replace(get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr), '')
    name = name.strip()
    return name

def get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in dict_o_Optionen.keys():
        return dict_o_Optionen[produktname]
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
    return 'Kerbl'

def get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return current_row['KATALOG_BEZEICHNUNG_DICT'].split()[0]

### THIS NEEDS TO BE REWORKED AS SOON AS I FIND OUT WHERE THE COST IS IN THE PRODUCT DATA
def get_cost(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '???'

### THIS NEEDS TO BE REWORKED AS SOON AS I FIND OUT WHERE THE PRICE IS IN THE PRODUCT DATA
def get_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '???'

### THIS NEEDS TO BE REWORKED AS SOON AS THERES DATA WHERE THIS COLUMN ISNT EMPTY
def get_special_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### THIS NEEDS TO BE REWORKED AS SOON AS THERES DATA WHERE THIS COLUMN ISNT 1
def get_tax_class_id(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '1'

def get_Beschreibung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '<ul><li>' + current_row['BESCHREIBUNG_DICT'] + '</li></ul>'

### THIS NEEDS TO BE REWORKED AS SOON AS I FIND OUT WHERE THE WEIGHT IS IN THE PRODUCT DATA
def get_Gewicht(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '???'

def get_Bild(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if isinstance(current_row['Hauptbild'],str):
        hauptbild_nr = current_row['Hauptbild'].split('.')[0]
        bestell_nr = current_row['ERP_BESTELLNUMMER_STR']
        return 'https://images.ridersdeal.com/m2/Kerbl/'+hauptbild_nr+'_Hauptbild_'+str(bestell_nr)+'.jpg'
    else:
        return 'No Picture Data'
        

### RIGHT NOW THIS FUNCTION DOESNT EXACTLY CREATE THE LINKS FROM THE DOCUMENT, SINCE FOR SOME REASON THE bestell_nr USED THERE
# IS FROM THE FIRST ROW IN THE CLASS, NOT THE LAST (LIKE IN BILD).
# MAYBE CHANGE THAT IN GENERAL THAT ALL INFO NEEDED IS IN THE ROW AND NOT THE FIRST / LAST ONE OF THE CLASS?
def get_Weitere_Bilder(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if isinstance(current_row['Zusatzbild'],str):
        pic_idx = current_row['Zusatzbild'].split('|')
        pic_linkx = []
        bestell_nr = current_row['ERP_BESTELLNUMMER_STR']
        for i in range(len(pic_idx)):
            pic_linkx.append('https://images.ridersdeal.com/m2/Kerbl/'+pic_idx[i].split('.')[0]+'_Zusatzbild_'+str(bestell_nr)+'.jpg')
            # in the original theres a space in _Zusatzbild _ , i removed that here
        return ';'.join(pic_linkx)
    else:
        return ''

def get_ean(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return current_row['ERP_BARCODE_EAN13_STR']
        

def get_herstellerbezeichnung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return str(current_row['ERP_BESTELLNUMMER_STR']) + ', ' + current_row['ERP_BEZEICHNUNG_1_STR'] + ', ' + current_row['ERP_BEZEICHNUNG_2_STR'] + ', ' + str(current_row['ERP_BARCODE_EAN13_STR'])

### THIS METHOD NEEDS TO BE REWORKED AS SOON AS SOME NON EMPTY VALUES ARE KNOWN
def get_grundpreis_menge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### THIS METHOD NEEDS TO BE REWORKED AS SOON AS SOME NON EMPTY VALUES ARE KNOWN
def get_grundpreis_einheit(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### THIS NEEDS TO BE REWORKED AS SOON AS I FIND OUT WHERE THE WARENNUMMER IS IN THE PRODUCT DATA
def get_destatis_warennummer(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '???'

### THIS NEEDS TO BE REWORKED AS SOON AS I FIND OUT WHERE THE COUNTRY IS IN THE PRODUCT DATA
def get_country_of_manufacture(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '???'

def get_manufacturer_nr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return current_row['ERP_BESTELLNUMMER_STR']

def get_material(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    columns_to_check = [['P1_TEXTIL_TEXTIL_MENGE_NUM','P1_TEXTIL_TEXTIL_MATERIAL_SEL'],['P2_TEXTIL_TEXTIL_MENGE_NUM','P2_TEXTIL_TEXTIL_MATERIAL_SEL'],['P3_TEXTIL_TEXTIL_MENGE_NUM','P3_TEXTIL_TEXTIL_MATERIAL_SEL']]
    material = ''
    for i in range(len(columns_to_check)):
        if isinstance(current_row[columns_to_check[i][1]],str):
            if i != 0:
                material += ', '
            material += current_row[columns_to_check[i][0]].replace(' ','') + ' ' + current_row[columns_to_check[i][1]]
    return material.replace('Spandex','Elasthan')

def get_passform(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr in ['Handschuhe','Hosen','Oberbekleidung','Schuhe, Stiefel und Socken']:
        return 'Normal'
    else:
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
    if len(current_row['ERP_BEZEICHNUNG_2_STR'].split(',')) >= 2:
        color_namex = current_row['ERP_BEZEICHNUNG_2_STR'].split(',')
        for color_name in color_namex:
            if color_name.strip() in colors_dict.keys():
                return colors_dict[color_name.strip()]
        return 'NO COLOR FOUND'
    else: # sometimes the color name isnt seperated by a comma, in that case we brute-force check all keys if they are contained in the string
        # and choose the longest key to use -- If someone has a better idea feel free to tell me
        current_key = ''
        for key in colors_dict.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR'] and len(key) > len(current_key):
                current_key = key
        if current_key != '':
            return colors_dict[current_key]
        else:
            return 'NO COLOR FOUND'

### this is just a guess if this works that way - for Kerbl there are no products with the Attributmenge Gebisse or Sattelgurte
# so this check isnt needed for the data but maybe thats the general rule
def get_pvs_verpackungstyp(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        if get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr) in ['Gebisse','Sattelgurte']:
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

def get_accessoires_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple and get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr) == 'Accessoires':
        return current_row['LAENGE_ARTIKEL_NUM'].replace(' ','')
    else:
        return ''

def get_color(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if len(current_row['ERP_BEZEICHNUNG_2_STR'].split(',')) >= 2:
        color_namex = current_row['ERP_BEZEICHNUNG_2_STR'].split(',')
        for color_name in color_namex:
            if color_name.strip() in colors_dict.keys():
                return color_name.strip().title()
        return 'NO COLOR FOUND'
    else: # sometimes the color name isnt seperated by a comma, in that case we brute-force check all keys if they are contained in the string
        # and choose the longest key to use -- If someone has a better idea feel free to tell me
        current_key = ''
        for key in colors_dict.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR'] and len(key) > len(current_key):
                current_key = key
        if current_key != '':
            return current_key.strip().title()
        else:
            return 'NO COLOR FOUND'

def get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if 'Damen' in current_row['ERP_BEZEICHNUNG_2_STR']:
        return 'Damen'
    if 'Kinder' in current_row['ERP_BEZEICHNUNG_2_STR']:
        return 'Kinder'
    if current_attr in ['Accessoires','Handschuhe','Hosen','Oberbekleidung','Schuhe, Stiefel und Socken']:
        return 'Unisex'
    return 'Pferd'

def get_rueckenlaenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    current_attr = get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
    if row_is_simple and current_attr == 'Decken':
        return current_row['LAENGE_TIERRUECKEN_MIN_NUM'].replace(' ','')
    else:
        return ''

### ARE THERE ANY OTHER POSSIBLE VALUES HERE?
def get_halsteil(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if 'mit abnehmbarem Halsteil' in current_row['BESCHREIBUNG_DICT']:
        return 'Mit abnehmbaren Halsteil'
    else:
        return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_fuellung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_denier(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_materialeigenschaft(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_produktmerkmale(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_pflegehinweis(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_pferdegroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple and current_attr in ['Trensen, Kandaren und Halfter','Fliegenhauben']:
        for key in dict_pferdegroesse.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR']:
                return dict_pferdegroesse[key]
    return ''

def get_schabracken_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple and current_attr == 'Schabracken':
        for key in dict_schabracken_groesse.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR']:
                return dict_schabracken_groesse[key]
    return ''

### Open question here: 
# right now the unit of the data is converted (200 cm -> 2m, this is the only example value)
# is laenge generally in m / can the original data be in another unit than cm?
# e.g. 250 cm -> 2.5m or 2,5m
def get_laenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Stricke': # and row_is_simple: <- unclear from the example data if that is needed
        laenge = current_row['LAENGE_ARTIKEL_NUM']
        if laenge.endswith('cm'):
            laenge = float(laenge[:-3])
            laenge = laenge/100
            if laenge.is_integer():
                laenge = int(laenge)
        return str(laenge).replace('.',',')+'m' # the replace is in case 2.5m should be written as 2,5m
    return ''

def get_verschlussart(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    current_attr = get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
    if current_attr == 'Stricke':
        return current_row['AUSFUEHRUNG_HAKEN_SEL']
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_ausfuehrung_halfter(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_beinschutz_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Beinschutz' and row_is_simple:
        for key in dict_beinschutz_groesse.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR']:
                return dict_beinschutz_groesse[key]
    return ''

def get_handschuh_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Handschuhe' and row_is_simple:
        for key in dict_handschuh_groesse.keys():
            if key in current_row['ERP_BEZEICHNUNG_2_STR']:
                return dict_handschuh_groesse[key]
    return ''

def get_schuhgroesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Schuhe, Stiefel und Socken' and row_is_simple:
        return current_row['GROESSE_SCHUHE_SLA_SEL']
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_wadenweite(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

### ALL VALUES IN THE EXAMPLE DATA SET ARE EMPTY
def get_schafthoehe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''

def get_hosen_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Hosen' and row_is_simple:
        return current_row['ERP_BEZEICHNUNG_2_STR'].split(',')[-1].strip().replace('/','-')
    return ''

def get_besatz(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Hosen':
        besatz_hose_sel = current_row['BESATZ_HOSE_SEL']
        if besatz_hose_sel in dict_besatz.keys():
            return dict_besatz[besatz_hose_sel]
        return 'Unknown'
    return ''

def get_oberbekleidung_groesse(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_attr == 'Oberbekleidung' and row_is_simple:
        zielgruppe = get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
        if zielgruppe == 'Kinder':
            row_to_look_at = 'GROESSE_BEKLEIDUNG_KINDER_SEL'
        else:
            row_to_look_at = 'GROESSE_BEKLEID_MENSCH_INTL_SLA_SEL'
        return str(current_row[row_to_look_at]).replace('/','-')
    return ''