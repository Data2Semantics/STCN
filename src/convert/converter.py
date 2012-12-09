#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2012

@author: hoekstra
'''
import argparse
import re
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS

class Converter(object):
    '''
    classdocs
    '''

    TYPOGRAFISCHE_KENMERKEN = {
                                'x' : 'typografische titelpagina',
                                'y' : 'geen titelpagina',
                                'a' : 'illustratie op de titelpagina',
                                'w' : 'gegraveerde titelpagina',
                                'z' : 'meerkleurig',
                                'h' : 'drukkersmerk',
                                'v' : 'bedrukte omslag',
                                'i' : 'romein',
                                'j' : 'gotisch',
                                'k' : 'cursief',
                                'l' : 'civilité',
                                'm' : 'Grieks',
                                'n' : 'Hebreeuws',
                                'o' : 'Arabisch',
                                'p' : 'Armeens',
                                'r' : 'cyrillisch',
                                'q' : 'muzieknoten',
                                's' : 'overige',
                                'a' : 'illustratie op de titelpagina',
                                'b' : 'illustraties buiten collatie',
                                'c' : 'andere illustraties binnen collatie',
                                'd' : 'van auteur',
                                'e' : 'fondslijst',
                                'f' : 'assortimentslijst',
                                'g' : 'diversen',
                                '3' : 'lijst van intekenaren',
                                '4' : 'prijsopgave',
                                '8' : 'boekverkoperslijst'}
    
    TALEN = {
            'abk': 'Abchazisch',
            'ace': 'Acehs, Atjehs',
            'aco': 'Acoli',
            'ada': 'Adangme',
            'ady': 'Adyghe, Adygei',
            'aar': 'Afar',
            'ari': 'Afrihili',
            'afr': 'Afrikaans',
            'afa': 'Afro-aziatische talen (overige)',
            'ain': 'Ainu',
            'aka': 'Akan',
            'akk': 'Akkadisch',
            'alb': 'Albanees',
            'ale': 'Aleut',
            'alg': 'Algonkium',
            'ajm': 'Aljamia',
            'alu': 'Aluku, Boni',
            'amh': 'Amharisch',
            'ang': 'Angelsaksisch',
            'anp': 'Angika',
            'apa': 'Apache',
            'ara': 'Arabisch',
            'arg': 'Aragonees',
            'ars': 'Aramees',
            'arp': 'Arapahoe',
            'arn': 'Araukaans',
            'arw': 'Arawak',
            'arm': 'Armeens',
            'rup': 'Aromaans',
            'asm': 'Assameens',
            'ath': 'Athapaskische talen',
            'aus': 'Australische talen',
            'ave': 'Avestisch',
            'awa': 'Awaars',
            'aad': 'Awadhi',
            'aym': 'Aymara',
            'aze': 'Azerbajdjaans',
            'ast': 'Bable (Asturisch)',
            'bli': 'Balinees',
            'bal': 'Baloetsji',
            'bat': 'Baltische talen (overige)',
            'bam': 'Bambara',
            'bai': 'Bamileketalen',
            'bad': 'Banda',
            'bnt': 'Bantoetalen (overige)',
            'baa': 'Basa',
            'bak': 'Basjkiers',
            'bas': 'Baskisch',
            'btk': 'Bataktalen',
            'bej': 'Beja',
            'bem': 'Bemba',
            'ben': 'Bengaals',
            'ber': 'Berbertalen',
            'bho': 'Bhoipuri',
            'bih': 'Bihari',
            'bik': 'Bikol',
            'byn': 'Bilin',
            'bin': 'Bini',
            'bis': 'Bislama',
            'bla': 'Blackfoot',
            'zbl': 'Blissymbolics',
            'bor': 'Borneotalen, Kalimantantalen',
            'bos': 'Bosnisch',
            'bra': 'Braj',
            'bre': 'Bretons',
            'bug': 'Buginees',
            'bul': 'Bulgaars',
            'bua': 'Buriat',
            'bur': 'Burmees',
            'cad': 'Caddo',
            'cam': 'Cambodjaans',
            'car': 'Caribisch',
            'cat': 'Catalaans',
            'ceb': 'Cebuano',
            'cel': 'Celebestalen, Sulawesitalen',
            'chg': 'Chagatai',
            'cmc': 'Chamictalen',
            'cha': 'Chamorro',
            'chr': 'Cherokee',
            'chy': 'Cheyenne',
            'chb': 'Chibcha',
            'chi': 'Chinees',
            'chn': 'Chinook',
            'chp': 'Chipewyan',
            'cho': 'Choctaw',
            'cor': 'Cornisch',
            'cos': 'Corsicaans',
            'cre': 'Cree',
            'crp': 'Creools en Pidgin',
            'cpf': 'Creools en Pidgin Frans (overige)',
            'cpp': 'Creools en Pidgin Portugees (overige)',
            'hat': 'Creools, Haïtiaans Frans',
            'cru': 'Cru',
            'dak': 'Dakota',
            'dar': 'Dargva',
            'day': 'Dayak',
            'dee': 'Deens',
            'del': 'Delaware',
            'din': 'Dinka',
            'div': 'Divehi',
            'dog': 'Dogri',
            'dgr': 'Dogrib',
            'dra': 'Dravidische talen (overige)',
            'dua': 'Duala',
            'dui': 'Duits',
            'dmh': 'Duits, Middelhoog',
            'ndu': 'Duits, Neder',
            'doh': 'Duits, Oudhoog',
            'gsw': 'Duits, Zwitsers-',
            'dyu': 'Dyula',
            'dzo': 'Dzongkha',
            'efi': 'Efik',
            'egy': 'Egyptisch',
            'eka': 'Ekajuk',
            'ela': 'Elamitisch',
            'eng': 'Engels',
            'enm': 'Engels, Middel',
            'myv': 'Erzja',
            'esk': 'Eskimotaal',
            'esp': 'Esperanto',
            'est': 'Estisch',
            'eth': 'Ethiopisch',
            'ewe': 'Ewe',
            'ewo': 'Ewondo',
            'far': 'Faeroer',
            'fan': 'Fang',
            'fat': 'Fanti',
            'phn': 'Fenicisch',
            'fij': 'Fidji',
            'fil': 'Filipino',
            'phi': 'Filippijnse talen (overige)',
            'fin': 'Fins',
            'fio': 'Fins-Oegrische talen',
            'fon': 'Fon',
            'fra': 'Frans',
            'frm': 'Frans, Middel',
            'fro': 'Frans, Oud',
            'fri': 'Fries',
            'fur': 'Friulaans',
            'ful': 'Fula',
            'gaa': 'Ga',
            'gae': 'Gaelisch',
            'gag': 'Galicisch',
            'gal': 'Galla',
            'gay': 'Gayo',
            'gba': 'Gbaya',
            'sgn': 'Gebarentaal',
            'zxx': 'Geen taalkundige inhoud',
            'geo': 'Georgisch',
            'ger': 'Germaanse talen (overige)',
            'gil': 'Gilbertees',
            'gon': 'Gondi',
            'gor': 'Gorontalo',
            'got': 'Gotisch',
            'grb': 'Grebo',
            'grk': 'Grieks, klassiek',
            'grn': 'Grieks, modern',
            'gua': 'Guarani',
            'guj': 'Gujarati',
            'gwi': 'Gwich\'in',
            'hai': 'Haida',
            'hal': 'Halmaheratalen',
            'hau': 'Hausa',
            'haw': 'Hawaïïtaal',
            'heb': 'Hebreews',
            'her': 'Herero',
            'hil': 'Hiligaynon',
            'him': 'Himachali',
            'hin': 'Hindi',
            'hmo': 'Hiri Motu',
            'hmn': 'Hmong',
            'hon': 'Hongaars',
            'hup': 'Hupa',
            'iba': 'Iban',
            'ibo': 'Ibo',
            'ido': 'Ido',
            'ier': 'Iers',
            'mga': 'Iers, Middel (ca. 1100-1500)',
            'sga': 'Iers, Oud (tot 1100)',
            'ijo': 'Ijo',
            'ijs': 'IJslands',
            'ilo': 'Ilocano',
            'smn': 'Inari-Samisch',
            'ica': 'Indianentalen (Centraal-Amerika)',
            'ina': 'Indianentalen (Noord-Amerika)',
            'iza': 'Indianentalen (Zuid-Amerika)',
            'inc': 'Indische talen (overige)',
            'ine': 'Indo-Europese talen (overige)',
            'ind': 'Indonesisch',
            'inh': 'Ingoesjetisch (Ingoesj)',
            'int': 'Interlingua',
            'ile': 'Interlingue',
            'iku': 'Inuktitut',
            'ipk': 'Inupiaq',
            'ira': 'Iraans (overige)',
            'iro': 'Irokees',
            'ita': 'Italiaans',
            'jao': 'Jao',
            'jap': 'Japans',
            'jav': 'Javaans',
            'jid': 'Jiddisch',
            'jor': 'Joruba',
            'jrb': 'Judeo-Arabisch',
            'jpr': 'Judeo-Perzisch',
            'jus': 'Judeo-Spaans',
            'kbd': 'Kabardisch',
            'kac': 'Kachin',
            'kal': 'Kalatdlissut',
            'xal': 'Kalmuks',
            'kam': 'Kamba',
            'kan': 'Kanarees',
            'kau': 'Kanuri',
            'kaa': 'Karakalpaks',
            'krc': 'Karatsjai-Balkarisch',
            'krl': 'Karelisch',
            'kar': 'Karen',
            'kas': 'Kasjmiri',
            'csb': 'Kasjoebisch',
            'kak': 'Kaukasisch',
            'kaw': 'Kawi',
            'kaz': 'Kazaks',
            'kel': 'Keltische talen (overige)',
            'slk': 'Kerkslavisch',
            'kha': 'Khasi',
            'khi': 'Khoisan talen (overige)',
            'kho': 'Khotanees',
            'kik': 'Kikuyu',
            'kmb': 'Kimbundu',
            'kin': 'Kinyarwanda',
            'kir': 'Kirgizisch',
            'ksu': 'Kleine Sunda Eilanden m.u.v. Balinees',
            'tlh': 'Klingon',
            'kur': 'Koerdisch',
            'koe': 'Koesjitische talen (overige)',
            'kom': 'Komi',
            'kon': 'Kongo',
            'kok': 'Konkani',
            'kop': 'Koptisch',
            'kor': 'Koreaans',
            'kpe': 'Kpelle',
            'crh': 'Krim-Tataars',
            'kro': 'Kroatisch, zie ook: Servo-Kroatisch (Latijns)',
            'kua': 'Kuanyama',
            'kum': 'Kumyk',
            'art': 'Kunstmatige talen (overige)',
            'kru': 'Kurukh',
            'kus': 'Kusaie',
            'kut': 'Kutenai',
            'kwi': 'Kwinti',
            'lah': 'Lahnda',
            'lam': 'Lamba',
            'lan': 'Langue d\'Oc',
            'lao': 'Laotiaans',
            'lap': 'Laps',
            'lat': 'Latijn',
            'let': 'Lets',
            'lez': 'Lezgian',
            'lim': 'Limburgs',
            'lin': 'Lingala',
            'lit': 'Litouws',
            'jbo': 'Lojban',
            'lol': 'Lolo',
            'loz': 'Lozi',
            'lub': 'Luba',
            'lua': 'Luba-Luala',
            'lug': 'Luganda',
            'lui': 'Luisend',
            'smj': 'Lule-Samisch',
            'lun': 'Lunda',
            'luo': 'Luo',
            'lus': 'Lushai',
            'ltz': 'Luxemburgs',
            'mac': 'Macedonisch',
            'mad': 'Malagasi (gesproken op Madagascar)',
            'mdu': 'Madurees',
            'mag': 'Magahi',
            'mai': 'Maithili',
            'mak': 'Makasar',
            'mly': 'Malayalam',
            'mal': 'Maleis',
            'map': 'Maleis-Polynesische talen (overige)',
            'mlk': 'Malinke',
            'mlt': 'Maltees',
            'mnc': 'Manchu',
            'mdr': 'Mandar',
            'mni': 'Manipuri',
            'mno': 'Manobo',
            'man': 'Manx',
            'mao': 'Maori',
            'mar': 'Marathi',
            'chm': 'Mari',
            'mah': 'Marshall',
            'mwr': 'Marwari',
            'mas': 'Massai',
            'myn': 'Mayan',
            'mis': 'Verschillende teksten in verschillende talen', 
            'men': 'Mende',
            'mic': 'Micmac',
            'min': 'Minangkabau',
            'mwl': 'Mirandees',
            'moh': 'Mohawk',
            'mdf': 'Moksha',
            'mol': 'Moldavisch',
            'muk': 'Molukse talen',
            'mon': 'Mongools',
            'mkh': 'Mon-Khmertalen (m.u.v. Cambodjaans)',
            'mos': 'Mossi',
            'mun': 'Munda talen',
            'mus': 'Muskogee',
            'nqo': 'N\'Ko',
            'nah': 'Nahuatl',
            'nap': 'Napolitaans (Italiaans)',
            'nau': 'Nauru',
            'nav': 'Navaho',
            'nde': 'Ndebele',
            'nbl': 'Ndebele (Zuid-Afrika)',
            'ndo': 'Ndonga',
            'dsb': 'Nedersorbisch',
            'ned': 'Nederlands',
            'mnd': 'Nederlands, Middel',
            'nep': 'Nepalees',
            'new': 'Newari',
            'nwc': 'Newari, Oud',
            'nia': 'Nias',
            'nic': 'Niger-Kongo talen (overige)',
            'niu': 'Niuean',
            'nog': 'Nogais',
            'frr': 'Noord-Fries',
            'nso': 'Noord-Sotho',
            'noo': 'Noors',
            'nob': 'Noors, Bokmål',
            'nno': 'Noors, Nynorsk',
            'non': 'Noors, Oud',
            'nub': 'Nuba',
            'nym': 'Nyamwesi',
            'nya': 'Nyanja, Chewa',
            'nyn': 'Nyankole',
            'nyo': 'Nyoro',
            'nzi': 'Nzima',
            'oei': 'Oeigoers',
            'oek': 'Oekraïens',
            'oes': 'Oesbeeks',
            'oji': 'Ojibwa',
            'onb': 'Onbepaald/onbekend',
            'frs': 'Oost-Fries',
            'hsb': 'Oppersorbisch',
            'ori': 'Oriya',
            'osa': 'Osage',
            'ota': 'Osmaans-Turks',
            'oss': 'Ossetisch',
            'oto': 'Otomi',
            'pac': 'Pacifictalen',
            'pah': 'Pahari',
            'pal': 'Pahlavi',
            'pau': 'Palauan',
            'pli': 'Pali',
            'pam': 'Pampanga',
            'pag': 'Pangasinan',
            'pan': 'Panjabi',
            'pap': 'Papiamento',
            'ppa': 'Papoea',
            'pas': 'Pashto',
            'per': 'Perzisch, modern',
            'peo': 'Perzisch, Oud',
            'pon': 'Ponape',
            'poo': 'Pools',
            'por': 'Portugees',
            'pra': 'Prakrit',
            'pro': 'Provencaals',
            'que': 'Quechua',
            'raj': 'Rajasthani',
            'rap': 'Rapanui',
            'rar': 'Rarotongan',
            'rho': 'Rhaeto-Romaans',
            'roe': 'Roemeens',
            'roa': 'Romaanse talen (overige)',
            'run': 'Rundi',
            'rus': 'Russisch',
            'sal': 'Salishan talen',
            'sam': 'Samaritaans',
            'sme': 'Sami, noord',
            'smn': 'Samisch, Inari-',
            'smj': 'Samisch, Lule-',
            'sms': 'Samisch, Skolt-',
            'sma': 'Samisch, Zuid-',
            'sao': 'Samoaans',
            'sad': 'Sandawe',
            'sag': 'Sango',
            'san': 'Sanskrit',
            'sat': 'Santali',
            'sac': 'Saramaccaans',
            'srd': 'Sardisch',
            'sar': 'Sarnami Hindustani',
            'sas': 'Sasak',
            'sco': 'Schots (Lallans)',
            'sel': 'Selkup',
            'sem': 'Semitische talen (overige)',
            'srr': 'Serer',
            'ser': 'Servisch, zie ook: Servo-Kroatisch (Cyrillisch)',
            'scc': 'Servo-Kroatisch (Cyrillisch)',
            'scr': 'Servo-Kroatisch (Latijns)',
            'shn': 'Shan',
            'sho': 'Shona',
            'iii': 'Sichuan Yi',
            'sid': 'Sidamo',
            'snd': 'Sindhi',
            'snh': 'Singalees',
            'sit': 'Sino-Tibetaanse talen (overige)',
            'sio': 'Siouan talen',
            'sms': 'Skolt-Samisch',
            'den': 'Slave',
            'sla': 'Slavische talen (overige)',
            'slo': 'Slovaaks',
            'slw': 'Sloveens',
            'soe': 'Soemerisch',
            'sog': 'Sogdisch',
            'som': 'Somalisch',
            'son': 'Songhai',
            'snk': 'Soninke',
            'sor': 'Sorbisch',
            'spa': 'Spaans',
            'sra': 'Sranan',
            'ssa': 'Sub-Sahara Afrikaanse talen (overige)',
            'suk': 'Sukuma',
            'sum': 'Sumatraanse talen m.u.v. Acehs, Bataks, Minangkabau',
            'sun': 'Sundanees',
            'suj': 'Surinaams-Javaans',
            'sne': 'Surinaams-Nederlands',
            'sus': 'Susu',
            'swa': 'Swahili',
            'swz': 'Swazi',
            'syr': 'Syrisch',
            'syc': 'Syrisch, Oud',
            'tad': 'Tadjik',
            'tag': 'Tagalog',
            'tah': 'Tahitisch',
            'tai': 'Tai talen (overige)',
            'tmh': 'Tamashek',
            'tam': 'Tamil',
            'tat': 'Tataars',
            'tel': 'Telugu',
            'tem': 'Temne',
            'ter': 'Tereno',
            'tet': 'Tetum',
            'tha': 'Thai',
            'tib': 'Tibetaans',
            'tig': 'Tigre',
            'tir': 'Tigrina',
            'tiv': 'Tiv',
            'tli': 'Tlingit',
            'tpi': 'Tok Pisin',
            'tkl': 'Tokelau',
            'ton': 'Tonga',
            'tog': 'Tonga (Nyassa)',
            'tri': 'Trio',
            'tru': 'Truk',
            'tsi': 'Tsimshian',
            'tse': 'Tsjechisch',
            'che': 'Tsjetsjeens',
            'tsj': 'Tsjoevasjisch',
            'tso': 'Tsonga',
            'tsw': 'Tswana',
            'tum': 'Tumbuka',
            'tup': 'Tupi talen',
            'tuk': 'Turkmeens',
            'tur': 'Turks',
            'tut': 'Turks-Tataarse talen (overige)',
            'tvl': 'Tuvalu',
            'tyv': 'Tuviniaans',
            'twi': 'Twi',
            'udm': 'Udmurts',
            'uga': 'Ugaritisch',
            'umb': 'Umbundu',
            'urd': 'Urdu',
            'vai': 'Vai',
            'mul': 'Zelfde tekst in verschillende talen',
            'ven': 'Venda',
            'vie': 'Vietnamees',
            'vol': 'Volapük',
            'wln': 'Waals',
            'wak': 'Wakashan talen',
            'wal': 'Walamo',
            'wap': 'Waphisana',
            'war': 'Waray',
            'was': 'Washo',
            'way': 'Wayana',
            'wel': 'Welsh',
            'wit': 'Wit-Russisch',
            'wol': 'Wolof',
            'wot': 'Wotisch',
            'xho': 'Xhosa',
            'sah': 'Yakut',
            'yar': 'Yar',
            'ypk': 'Yupik',
            'znd': 'Zande',
            'zap': 'Zapotec',
            'zza': 'Zazaki',
            'mul': 'Zelfde tekst in verschillende talen',
            'zen': 'Zenega',
            'zha': 'Zhuang',
            'zig': 'Zigeunertalen',
            'alt': 'Zuid-Altajs',
            'sma': 'Zuid-Samisch',
            'sso': 'Zuid-Sotho',
            'zul': 'Zulu',
            'zun': 'Zuni',
            'zwe': 'Zweeds',
            'gsw': 'Zwitsers-Duits'
            }
    
    LANDEN = {
            'af': 'Afganistan',
            'al': 'Albanië',
            'dz': 'Algerije',
            'ad': 'Andorra',
            'ao': 'Angola',
            'aq': 'Antarctica',
            'bq': 'Antarctica (Brits)',
            'fq': 'Antarctica (Frans)',
            'ag': 'Antigua en Baruda',
            'ar': 'Argentinië',
            'am': 'Armenië',
            'aw': 'Aruba',
            'ac': 'Ashmore en Cartier Eilanden',
            'au': 'Australië',
            'az': 'Azerbeidjan',
            'bs': 'Bahama Eilanden',
            'bh': 'Bahrein',
            'bd': 'Bangladesh',
            'bb': 'Barbados',
            'be': 'België',
            'bz': 'Belize',
            'bj': 'Benin',
            'bm': 'Bermuda',
            'bt': 'Bhoetan',
            'bu': 'Birma',
            'bi': 'Boeroendi',
            'bo': 'Bolivia',
            'ba': 'Bosnië-Herzogowina',
            'bw': 'Botswana',
            'bv': 'Bouvet Eilanden',
            'br': 'Brazilië',
            'bn': 'Brunei',
            'bg': 'Bulgarije',
            'hv': 'Burkina Fasso',
            'ca': 'Canada',
            'ct': 'Canton en Enderbury Eilanden',
            'ky': 'Cayman Eilanden',
            'cf': 'Centraal Afrikaanse Republiek',
            'ln': 'Central en Southern Line Eilanden',
            'cl': 'Chili',
            'cn': 'Chincx     Christmas Eiland',
            'cc': 'Cocos (Keeling) Eilanden',
            'co': 'Colombia',
            'km': 'Comoren',
            'cg': 'Congo (Brazzaville)',
            'ck': 'Cook Eilanden',
            'cr': 'Costa Rica',
            'cu': 'Cuba',
            'cy': 'Cyprus',
            'dk': 'Denemarken',
            'dj': 'Djibouti',
            'dm': 'Dominica',
            'do': 'Dominicaanse Republiek',
            'nq': 'Dronning Maud Land',
            'de': 'Duitslandd     Duitslanec     Ecuador',
            'eg': 'Egypte en Verenigde Arabische Republiek (1958-1961)',
            'sv': 'El Salvador',
            'gq': 'Equatorial Guinea',
            'er': 'Eritrea',
            'ee': 'Estland',
            'et': 'Ethiopië',
            'fo': 'Faeröer',
            'fk': 'Falkland Eilanden',
            'fj': 'Fiji Eilanden',
            'ph': 'Filippijnen',
            'fi': 'Finland',
            'fr': 'Frankrijk',
            'ga': 'Gabon',
            'gm': 'Gambia',
            'go': 'Georgië',
            'gh': 'Ghana',
            'gi': 'Gibraltar',
            'ge': 'Gilbert en Ellice Eilanden tot 1978 - na 1978 gebruik Kiribati of Tuvalu',
            'gd': 'Grenada',
            'gr': 'Griekenland',
            'gl': 'Groenland',
            'gp': 'Guadeloupe',
            'gu': 'Guam',
            'gt': 'Guatemala',
            'gf': 'Guyana (Frans)',
            'gn': 'Guinee',
            'gw': 'Guinee-Bissau',
            'gy': 'Guyana',
            'ht': 'Haïti',
            'hm': 'Heard en McDonald Eilanden',
            'hn': 'Honduras',
            'hk': 'Hong Kong',
            'hu': 'Hongarije',
            'ie': 'Ierland',
            'is': 'IJsland',
            'in': 'India',
            'io': 'Indische Oceaangebied (Brits)',
            'id': 'Indonesie',
            'iq': 'Irak',
            'nt': 'Irak-Saoedi-Arabië Neutrale Zone',
            'ir': 'Iran',
            'il': 'Israël',
            'it': 'Italië',
            'ci': 'Ivoorkust',
            'jm': 'Jamaica',
            'jp': 'Japan',
            'ye': 'Jemeyd     Jemeyu     Joegoslavië tot oktober 1992. Na oktober 1992 tot maart 2006 code yu gebruiken voor Servië en Montenegro',
            'jt': 'Johnston Eiland',
            'jo': 'Jordanië',
            'cv': 'Kaapverdische Eilanden',
            'cm': 'Kameroen',
            'kh': 'Kampuchea',
            'qa': 'Katar',
            'kz': 'Kazachstan',
            'ke': 'Kenia',
            'ki': 'Kiribati',
            'kw': 'Koeweit',
            'kr': 'Korekp     Korehr     Kroatië',
            'kg': 'Kyrgyzstan',
            'la': 'Laos',
            'ls': 'Lesotho',
            'lv': 'Letland',
            'lb': 'Libanon',
            'lr': 'Liberia',
            'ly': 'Libië',
            'li': 'Liechtenstein',
            'lt': 'Litouwen',
            'lu': 'Luxemburg',
            'vi': 'Maagden Eilanden (Amerikaans)',
            'vg': 'Maagden Eilanden (Brits)',
            'mo': 'Macao',
            'mk': 'Macedonië',
            'mg': 'Madagascar',
            'mw': 'Malawi',
            'mv': 'Maldiven',
            'my': 'Maleisië',
            'ml': 'Mali',
            'mt': 'Malta',
            'ma': 'Marokko',
            'mh': 'Marshall Eilanden',
            'mq': 'Martinique',
            'mr': 'Mauretanië',
            'mu': 'Mauritius',
            'me': 'Mayotte',
            'mx': 'Mexico',
            'fm': 'Micronesië',
            'mi': 'Midway Eilanden',
            'md': 'Moldavië',
            'mc': 'Monaco',
            'mn': 'Mongolië',
            'mb': 'Montenegro (vanaf maart 2006); zie ook: Servië en Montenegro',
            'ms': 'Montserrat',
            'mz': 'Mozambique',
            'na': 'Namibië',
            'nr': 'Nauru',
            'nl': 'Nederland',
            'an': 'Nederlandse Antillen',
            'np': 'Nepal',
            'ni': 'Nicaragua',
            'nc': 'Nieuw-Caledonië',
            'nz': 'Nieuw-Zeeland',
            'ne': 'Niger',
            'ng': 'Nigeria',
            'nu': 'Niue',
            'mp': 'Noordelijke Mariana Eilanden',
            'no': 'Noorwegen',
            'nf': 'Norfolk',
            'ug': 'Oeganda',
            'ua': 'Oekraïne',
            'uz': 'Oezbekistan',
            'om': 'Oman',
            'xx': 'Onbekend',
            'at': 'Oostenrijk',
            'pu': 'Pacific Eilanden (Amerikaans)',
            'pc': 'Pacific Eilanden (Trust Territory)',
            'pk': 'Pakistan',
            'pw': 'Palau Eilanden',
            'pa': 'Panama',
            'pz': 'Panama-kanaalzone',
            'pg': 'Papoea-Nieuw-Guinea',
            'py': 'Paraguay',
            'pe': 'Peru',
            'pn': 'Pitcairn Eiland',
            'pl': 'Polen',
            'pf': 'Polynesië (Frans)',
            'pt': 'Portugal',
            'pr': 'Puerto Rico',
            'qa': 'Quatar',
            're': 'Réunion',
            'rh': 'Rhodesië tot 1979 - na 1979 gebruik Zimbabwe',
            'ro': 'Roemenië',
            'ru': 'Russische Federatie',
            'rw': 'Rwanda',
            'sh': 'St. Helena',
            'kn': 'St. Kitts-Neville-Anguilla',
            'lc': 'St. Lucia',
            'pm': 'St. Pierre en Miguelon',
            'vc': 'St. Vincent',
            'as': 'Samoa (Amerikaans)',
            'ws': 'Samoa (West)',
            'sm': 'San Marino',
            'st': 'Sao Tome en Principe',
            'sa': 'Saoedi-Arabië',
            'sn': 'Senegal',
            'sq': 'Servië; vanaf maart 2006',
            'yu': 'Servië en Montenegro; periode oktober 1992 tot maart 2006',
            'sc': 'Seychellen',
            'sl': 'Sierra Leone',
            'sg': 'Singapore',
            'sk': 'Slovakije (na 1-1-1993)',
            'si': 'Slovenië',
            'sd': 'Soedan',
            'sb': 'Solomon Eilanden',
            'so': 'Somalië',
            'es': 'Spanje',
            'sj': 'Spitsbergen en Jan Mayen',
            'lk': 'Sri Lanka',
            'sr': 'Suriname',
            'sz': 'Swaziland',
            'sy': 'Syrië',
            'tj': 'Tadzjikistan',
            'tw': 'Taiwan',
            'tz': 'Tanzania',
            'th': 'Thailand',
            'tp': 'Timor (Oost- of Portugees) Tot 20 mei 2002 gebruik Indonesië',
            'tm': 'Toerkmenistan',
            'tg': 'Togo',
            'tk': 'Tokelan Eilanden',
            'to': 'Tonga',
            'tt': 'Trinidad en Tobago',
            'td': 'Tsjaad',
            'cz': 'Tsjechië (na 1-1-1993)',
            'cs': 'Tsjechoslowakije (1918 t/m 31-12-1992)',
            'tn': 'Tunesië',
            'tr': 'Turkije',
            'tc': 'Turks en Caicos Eilanden',
            'tm': 'Turkmenistan',
            'tv': 'Tuvalu',
            'ug': 'Uganda',
            'uy': 'Uruguay',
            'su': 'USSR',
            'vu': 'Vanuatu',
            'va': 'Vaticaan',
            've': 'Venezuela',
            'gb': 'Verenigd Koninkrijk',
            'ae': 'Verenigde Arabische Emiraten',
            'us': 'Verenigde Staten',
            'vn': 'Vietnam na 1978',
            'wk': 'Wake',
            'wf': 'Wallis en Futuna Eilanden',
            'de': 'West-Berlijn (1948-1990)',
            'eh': 'Westelijke Sahara',
            'by': 'Witrusland',
            'xx': 'Onbekend',
            'zr': 'Zaïre',
            'zm': 'Zambia',
            'zw': 'Zimbabwe',
            'za': 'Zuid Afrika',
            'se': 'Zweden',
            'ch': 'Zwitserland'
            }

    def __init__(self, redactiebladen):
        '''
        Constructor
        '''
        self.rb = redactiebladen
        self.rb_pos = 0
        self.last = []
        self.prev_line = ""
        
        self.STCN = Namespace('http://stcn.data2semantics.org/resource/')
        self.STCNV = Namespace('http://stcn.data2semantics.org/resource/vocab/')
        self.SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
        self.FOAF = Namespace('http://xmlns.com/foaf/0.1/')
        
    def __iter__(self):
        return self
        
    def next(self):
        pub_lines = []
        
        started = False
        count = self.rb_pos
        
        if count != 0 :
            pub_lines.append(self.prev_line)
            started = True
        
        for line in self.rb:
            count = count + 1
            if line.startswith('SET') and not started :
                started = True
            elif line.startswith('SET') and started :
                self.prev_line = line.strip('\n')
                started = False
                break
            elif line == '\n' :
                continue
            elif line.endswith('-\n') :
                self.prev_line = line.strip("\n")
                continue
            
            pub_lines.append(self.prev_line + line.strip("\n"))
            self.prev_line = ""
        
        print pub_lines
        self.rb_pos = count
        
        """Make sure that all lines start with a KMC"""
        checked_pub_lines = pub_lines[:2]
        for line in pub_lines[2:] :
            if line[:3].isdigit() :
                checked_pub_lines.append(line)
            else :
                checked_pub_lines[-1] += line
        
        if len(pub_lines) > 1:
            self.current = checked_pub_lines
            return checked_pub_lines
        else :
            raise StopIteration
    
    def init_graph(self):
        g = Graph()
        g.bind('stcn',self.STCN)
        g.bind('stcnv',self.STCNV)
        g.bind('rdfs',RDFS)
        g.bind('rdf',RDF)
        g.bind('foaf',self.FOAF)
        g.bind('skos',self.SKOS)
        
        return g
    
    def get_ppn(self, g):
        r = r'SET\:\s(?P<set>\w+\s.+?)\sTTL\:\s(?P<ttl>\d+)\sPPN\:\s(?P<ppn>\d{9})\sPAG\:\s(?P<pag>\d+)\s\.\n'
        m = re.search(r,self.current_text)
        print self.current_text
        
        if m :
            set_value = m.group('set')
            ttl_value = m.group('ttl')
            pag_value = m.group('pag')
            ppn_value = m.group('ppn')
            
            uri = self.STCN['werk/{}'.format(ppn_value)]
            
            g.add((uri,RDF.type,self.STCNV['Werk']))
            g.add((uri,self.STCNV['set'],Literal(set_value)))
            g.add((uri,self.STCNV['ttl'],Literal(ttl_value)))
            g.add((uri,self.STCNV['pag'],Literal(pag_value)))
            g.add((uri,self.STCNV['ppn'],Literal(ppn_value)))
        
            return g, uri
        else:
            raise Exception('No match for PPN regex!')
        
    def get_meta(self, g, uri):
        r = r'Ingevoerd\:\s(?P<ingevoerd>\d{4}\:\d\d-\d\d-\d\d)\sGewijzigd\:\s(?P<gewijzigd>\d{4}\:\d\d-\d\d-\d\d\s\d\d\:\d\d:\d\d)\sStatus:\s(?P<status>\d{4}\:\d\d-\d\d-\d\d)\n'
        m = re.search(r,self.current_text)
        
        if m:
            ingevoerd = m.group('ingevoerd')
            gewijzigd = m.group('gewijzigd')
            status = m.group('status')
            
            g.add((uri,self.STCNV['ingevoerd_meta'],Literal(ingevoerd)))
            g.add((uri,self.STCNV['gewijzigd_meta'],Literal(gewijzigd)))
            g.add((uri,self.STCNV['status_meta'],Literal(status)))
            
            return g
        else:
            raise Exception('No match for metadata regex!')
    
    def get_0500(self, g, uri):
        """Status, or type of work"""
        
        r = r'0500\s(?P<status>\w{3})\n'
        m = re.search(r, self.current_text)
        
        if m:
            status = m.group('status')
           
            g.add((uri,self.STCNV['status'],self.STCN['status/{}'.format(status)]))
            
            g.add((self.STCN['status/{}'.format(status)],RDF.type,self.SKOS['Concept']))    
            g.add((self.STCN['status/{}'.format(status)],RDF.type,self.STCNV['Status']))    
            g.add((self.STCN['status/{}'.format(status)],self.SKOS['inScheme'],self.STCN['STCN']))
           
            if status == 'Aav':
                g.add((uri,RDF.type,self.STCNV['Monografie']))
                g.add((self.STCN['status/{}'.format(status)],RDFS.label,Literal('Monografie','nl')))
            elif status == 'Abv':
                g.add((uri,RDF.type,self.STCNV['MeerdeligWerk']))
                g.add((self.STCN['status/{}'.format(status)],RDFS.label,Literal('Meerdelig werk','nl')))
            elif status == 'Acv':
                g.add((uri,RDF.type,self.STCNV['Tijdschrift']))
                g.add((self.STCN['status/{}'.format(status)],RDFS.label,Literal('Tijdschrift','nl')))
        
            return g
        else :
            raise Exception('No KMC 0500/Status found (obligatory)')
        
    def get_1100(self, g, uri):
        """Year in which the work was published"""
        
        r = r'1100\s(?P<jaar>(\w|\d){4})\n'
        m = re.search(r, self.current_text)
        
        if m:
            jaar = m.group('jaar')
            
            if jaar.endswith('XX') :
                g.add((uri,self.STCNV['eeuw'],self.STCN['eeuw/{}'.format(jaar)]))
            elif jaar.endswith('X') :
                g.add((uri,self.STCNV['eeuw'],self.STCN['eeuw/{}XX'.format(jaar[:2])]))
                g.add((uri,self.STCNV['decennium'],self.STCN['decennium/{}'.format(jaar)]))
            else:
                g.add((uri,self.STCNV['eeuw'],self.STCN['eeuw/{}XX'.format(jaar[:2])]))
                g.add((uri,self.STCNV['decennium'],self.STCN['decennium/{}X'.format(jaar[:3])]))
                g.add((uri,self.STCNV['jaar'],self.STCN['jaar/{}'.format(jaar)]))
            
            return g
        else :
            raise Exception('No KMC 1100/Year found (obligatory)')
            
    def get_1200(self, g, uri):
        """Typographical characteristics"""
        
        r = r'1200\s(?P<typokenmerk>.+?)\n'
        m = re.search(r, self.current_text)
        
        if m:
            kenmerken = re.split('|',m.group('typokenmerk'))
            
            for k in kenmerken:
                label = self.TYPOGRAFISCHE_KENMERKEN[k]
                
                g.add((uri,self.STCNV['typografisch_kenmerk'],self.STCN['kenmerk/{}'.format(k)]))
                
                g.add((self.STCN['kenmerk/{}'.format(k)],RDF.type,self.SKOS['Concept']))    
                g.add((self.STCN['kenmerk/{}'.format(k)],RDF.type,self.STCNV['TypografischKenmerk']))    
                g.add((self.STCN['kenmerk/{}'.format(k)],self.SKOS['inScheme'],self.STCN['STCN']))
                g.add((self.STCN['kenmerk/{}'.format(k)],RDFS.label,Literal(label,'nl')))
            
            return g
        else :
            raise Exception("No KMC 1200/Typographical characteristics found (obligatory)")
        
    def get_1500(self, g, uri):
        """Language code"""
        
        r = r'1500\s(?P<talen>.+?)\n'
        m = re.search(r, self.current_text)
        
        if m :
            talen = re.split('/',m.group('talen'))
            
            for t in talen:
                rt = r'(?P<soort>\d)(?P<taal>\w{3})'
                mt = re.search(rt, t)
                
                if mt:
                    soort = mt.group('soort')
                    taal = mt.group('taal')
                    
                    if soort == '1':
                        g.add((uri,self.STCNV['taal'],self.STCN['taal/{}'.format(taal)]))
                    elif soort == '2':
                        g.add((uri,self.STCNV['tussentaal'],self.STCN['taal/{}'.format(taal)]))
                    elif soort == '3':
                        g.add((uri,self.STCNV['oorspronkelijke_taal'],self.STCN['taal/{}'.format(taal)]))
                        
                    g.add((self.STCN['taal/{}'.format(taal)],RDF.type,self.SKOS['Concept']))    
                    g.add((self.STCN['taal/{}'.format(taal)],RDF.type,self.STCNV['Taal']))    
                    g.add((self.STCN['taal/{}'.format(taal)],self.SKOS['inScheme'],self.STCN['STCN']))
                    g.add((self.STCN['taal/{}'.format(taal)],RDFS.label,Literal(self.TALEN[taal],'nl')))
            
            return g
        else :
            raise Exception("No KMC 1500/Language found (obligatory)")
            
    def get_1700(self, g, uri):
        """Country code"""
        
        r = r'1700\s(?P<landen>.+?)\n'
        m = re.search(r, self.current_text)
        
        if m :
            landen = re.split('/',m.group('landen'))
            
            for l in landen:
                rl = r'(?P<soort>\d)(?P<land>\w{2})'
                ml = re.search(rl, l)
                
                if ml:
                    soort = ml.group('soort')
                    land = ml.group('land')
                    
                    if soort == '1':
                        g.add((uri,self.STCNV['land'],self.STCN['land/{}'.format(land)]))
                    elif soort == '2':
                        g.add((uri,self.STCNV['gecorrigeerd_land'],self.STCN['land/{}'.format(land)]))

                    g.add((self.STCN['land/{}'.format(land)],RDF.type,self.SKOS['Concept']))    
                    g.add((self.STCN['land/{}'.format(land)],RDF.type,self.STCNV['Land']))    
                    g.add((self.STCN['land/{}'.format(land)],self.SKOS['inScheme'],self.STCN['STCN']))
                    g.add((self.STCN['land/{}'.format(land)],RDFS.label,Literal(self.LANDEN[land],'nl')))
            
            return g
        else :
            raise Exception("No KMC 1700/Country found (obligatory)")
    
    
    def get_2275(self, g, uri):
        """Fingerprint"""
        
        r = r'2275\s(?P<vingerafdruk>.+?)\n'
        m = re.search(r, self.current_text)
        
        if m :
            vingerafdruk = m.group('vingerafdruk')
            
            g.add((uri,self.STCNV['vingerafruk'],Literal(vingerafdruk)))
            
            return g    
        else :
            raise Exception('No KMC 2275/Fingerprint found (obligatory)')
    
    def get_30XX(self, g, uri):
        """Authors"""
        UNITS = ["eerste", "tweede", "derde", "vierde", "vijfde", "zesde", "zevende", "achtste", "negende"]
        
        # The 0 or 1 in the third position of KMC 3000/301X or beyond is irrelevant, as the count starts with 0 
        r = r'30\d(?P<volgorde>\d)\s(?P<auteur>.+?)\n'
        i = re.finditer(r, self.current_text)
        
        first_author = None
        if i :
            for m in i:
                pos_int = int(m.group('volgorde'))
                author_property_name = UNITS[pos_int] + "_auteur"
                
                author_string = m.group('auteur')
                print author_string
                
                ra = r'(?P<voornaam>.+?)(/(?P<tussenvoegsel>.+?))?\@(?P<achternaam>.+?)\!(?P<ppn>\d{9})\!(?P<uitgeschreven>.+?)'
                rm = re.search(ra,author_string)
                
                if rm :
                    voornaam = rm.group('voornaam')
                    tussenvoegsel = rm.group('tussenvoegsel')
                    achternaam = rm.group('achternaam')
                    ppn = rm.group('ppn')
                    print voornaam, tussenvoegsel, achternaam, ppn
                
                g.add((uri,self.STCNV[author_property_name],Literal(author_string)))
                
            return g, first_author
        else :
            return g, first_author
                
    def parse(self):
        g = self.init_graph()
        
        self.current_text = '\n'.join(self.current)
        
        g, uri = self.get_ppn(g)
        g = self.get_meta(g, uri)
        g = self.get_0500(g, uri)
        g = self.get_1100(g, uri)
        g = self.get_1200(g, uri)
        g = self.get_1500(g, uri)
        g = self.get_1700(g, uri)
        g = self.get_2275(g, uri)
        g, first_author = self.get_30XX(g, uri)
        
        print g.serialize(format='n3')
        
#        for l in self.current[2:]:
#            print l
        
        
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # ../../STCN/data/redactiebladen/alleredacs.checked.1.txt
    parser.add_argument("redactiebladen",nargs="?", type=str, help="Filename of the STCN redactiebladen dump",default='test.txt')
    
    args = parser.parse_args()
    
    redactiebladen = open(args.redactiebladen,"r")
    
    c = Converter(redactiebladen)
    
    c.next()
    c.next()
    c.next()
    c.next()
    c.next()
    c.next()
    c.parse()
