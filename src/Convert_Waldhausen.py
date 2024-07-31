# import pandas as pd
# import numpy as np

# Every 'Hauptwarengruppe', to be filled
Warengruppen_dict = {
    'BENSE&EICKE': '',
    'AKTON': '',
    'Gebisse':'',
    'BERIS Gebisse':'', 
    'Zubehör':'',
    'BIZZY HORSE':'',
    'COMPOSITI':'',
    'DAVIS Artikel':'',
    'DERBY':'',
    'Chaps & Stiefelschäfte':'',
    'Accessoires':'',
    'Schuhe & Stiefeletten':'',
    'Handschuhe':'',
    'Reitsocken':'',
    'DEKO- & WERBEMATERIAL':'',
    'Kinder':'',
    'Damen':'',
    'Winter-Shirts':'',
    'Mäntel':'',
    'Sommer-Shirts':'',
    'Westen':'',
    'Jacken':'',
    'Shirts':'',
    'Thermo':'',
    'Jackets':'',
    'Herren':'',
    'Reiter':'',
    'Stiefel, Stall & Outdoor':'',
    'Zubehör & Pflege':'',
    'EQUINE FUSION':'',
    'Reithelme':'',
    'HAPPY MOUTH':'',
    'Mähnengummis':'',
    'KERALIT':'',
    'LIKIT':'',
    'LINDA TELLINGTON JONES':'',
    'PHARMAKA':'',
    'Sonstiges':'',
    'Lederhalfter':'',
    'Steigbügelriemen':'', 
    'Gurte':'',
    'STAR':'',
    'Sättel':'',
    'Ausbinder':'',
    'Longen':'',
    'Stirnbänder':'',
    'Geschirre & Zubehör':'',
    'STIEFEL':'',
    'Hufbeschlag':'',
    'STUD MUFFINS':'',
    'SWING Protektoren':'',
    'SWING Reithelme':'',
    'Ponysättel & Reitkissen':'',
    'Zaumzeug & Zubehör':'',
    'Putzzeug':'',
    'Gamaschen':'', 
    'Packtaschen':'',
    'Schabracken & Satteldecken':'',
    'Pferd':'',
    'Sattelgurte':'',
    'Fliegenfransen, -Masken & -Ohren':'Fliegenhauben',  #
    'Sonstige Islandprodukte':'',                 
    'Spezialunterlagen':'',
    'Nylonhalfter':'',
    'Bandagen & Unterlagen':'',
    'Abschwitzdecken':'',
    'Anbindestricke & Zubehör':'',
    'Zaumzeug Zubehör':'',
    'X-Line':'',
    'Bein & Hufe':'',
    'Sonstige':'',
    'Hufglocken':'',
    'Sporen':'',
    'Sporenriemen & Zubehör':'',
    'Gerten':'',
    'Fahrpeitschen':'',
    'Longierpeitschen':'',
    'Stalleinrichtungen':'',
    'Sattelschränke':'',
    'Reitplatz-Zubehör':'',
    'Putzkisten':'', 
    'Putztaschen':'',
    'Staubsauger & Zubehör':'',
    'Inhaliergeräte':'',
    'Pflegeprodukte für das Pferd':'',
    'Pflegeprodukte für Reitzubehör':'',
    'Startnummern':'',
    'Preisschleifen':'',
    'BÜCHER':'',
    'Spielbälle':'',
    'Fressschutz':'',
    'Trensen & Zubehör':'', 
    'Labeling Products':'',
    'Unterlagen':'',
    'Stallapotheke':'',
    'Zusatzfutter':'',
    'Belohnungsfutter':'',
    'Pflegemittel':'',
    'Kopfeisen':'',
    'Massagegeräte':'',
    'Schermaschinen & Zubehör':'',
    'Heunetze':'',
    'Bügel & Einlagen':'',
    'Steigbügel & Einlagen':'',
    'Fahrgebisse':'', 
    'Fliegen- & Ekzemerdecken':'Decken',               #
    'Decken':'Decken',                                 #
    'Stalldecken':'', 
    'GESCHENKARTIKEL':'', 
    'Boxentasche':'',
    'Outdoordecken':'',
    'Hundedecken':'',
    'Transportgamaschen':'',
    'Kappzäume':'',
    'S-Line':'',
    'Div. Ersatzteile u.Materialien':'', 
    'Sattelzubehör':''
}

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

def get_type(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'simple'
    else:
        return 'configurable'

def get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if current_row['Hauptwarengruppe'] in Warengruppen_dict.keys():
        Attributmenge = Warengruppen_dict[current_row['Hauptwarengruppe']]
    else:
        Attributmenge = 'Unknown'
    ### FIR SOME DEBUGGING ONLY
    if Attributmenge == '':
        Attributmenge = 'Decken'
    return Attributmenge

def get_name(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    name = str(current_row["Modellname"]) + ", " + str(current_row["Größe"])
    return name

def get_o_Optionen(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    Attributmenge = get_Attributmenge(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr)
    if Attributmenge in Optionen_dict.keys():
        return Optionen_dict[Attributmenge]
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
    return 'Waldhausen'

def get_brand(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return 'Waldhausen'

def get_cost(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    cost = current_row['WVK']
    if cost.is_integer():
        return int(cost)
    else:
        return str(cost).replace('.',',')

def get_price(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    price = current_row['Empf.Vk']
    if price.is_integer():
        return int(price)
    else:
        return str(price).replace('.',',')

### THIS METHOD NEEDS TO BE REWORKED AT SOME POINT
def get_Beschreibung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    Beschreibung = '<ul><li>' + str(current_row['Beschreibung']) + '</li></ul>'
    return Beschreibung

def get_Gewicht(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    Gewicht = current_row['kg brutto']
    return Gewicht

def get_Bild(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    new_prefix = 'https://images.ridersdeal.com/m2/Waldhausen/2024-03/'
    last_part = str(current_row['Bildlink jpg']).split('/')[-1]
    Bild = new_prefix + last_part
    return Bild

### THERE ARE SOME PICTURE LINKS IN THE CSV-FILE THAT ARE CREATED IN ANOTHER UNKNOWN WAY
def get_Weitere_Bilder(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return '?'

def get_ean(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return current_row['EAN']
    else:
        return ''    

def get_herstellerbezeichnung(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return str(current_row['Artikel Nr.']) + ', ' +  str(current_row['Bezeichnung']) + ', ' +  str(current_row['EAN'])  + ', ' + str(current_row['Größe'])  + ', ' + str(current_row['Farbe'])

def get_LiNr(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    if row_is_simple:
        return 'n'+str(current_row_nr)
    else:
        return 'nM'+str(total_row_nr)
    
def get_zielgruppe(use_configurable,current_row,row_is_simple,current_row_nr, current_LiNr,colors_dict,total_row_nr,current_attr):
    return ''