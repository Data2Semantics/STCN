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
        
        for line in self.rb:
#            print count
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
        
        if len(pub_lines) > 1:
            self.current = pub_lines
            return pub_lines
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
           
            if status == 'Aav':
                g.add((uri,RDF.type,self.STCNV['Monografie']))
            elif status == 'Abv':
                g.add((uri,RDF.type,self.STCNV['Meerdelig_Werk']))
            elif status == 'Acv':
                g.add((uri,RDF.type,self.STCNV['Tijdschrift']))
        
            return g
        else :
            raise Exception('No KMC 0500/Status found (obligatory)')
        
    def get_1100(self, g, uri):
        """Year in which the work was published"""
        
        r = r'1100\s(?P<jaar>(\w|\d){4})\n'
        m = re.search(r, self.current_text)
        
        if m:
            jaar = m.group('jaar')
            
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
                
                g.add((uri,self.STCNV['typografisch_kenmerk'],self.STCNV[k]))
                g.add((self.STCNV[k],RDFS.label,Literal(label,'nl')))
            
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
                        g.add((uri,self.STCNV['taal'],self.STCNV[taal]))
                    elif soort == '2':
                        g.add((uri,self.STCNV['tussentaal'],self.STCNV[taal]))
                    elif soort == '3':
                        g.add((uri,self.STCNV['oorspronkelijke_taal'],self.STCNV[taal]))
                        
                    g.add((self.STCNV[taal],RDFS.label,Literal(self.TALEN[taal],'nl')))
            
            return g
        else :
            raise Exception("No KMC 1500/Language found (obligatory)")
            
        
    def parse(self):
        g = self.init_graph()
        
        self.current_text = '\n'.join(self.current)
        
        g, uri = self.get_ppn(g)
        g = self.get_meta(g, uri)
        g = self.get_0500(g, uri)
        g = self.get_1100(g, uri)
        g = self.get_1200(g, uri)
        g = self.get_1500(g, uri)
        
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
    c.parse()
