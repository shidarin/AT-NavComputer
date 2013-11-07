#!/usr/bin/kivy
# AT-NavComputer
# A Star Wars galactic map and hyperdrive transit calculator
# By Sean Wallitsch, 2013/09/01


# ==============================================================================
# IMPORTS
# ==============================================================================


# Python Imports

import cPickle as pickle # For reading systemsList, to be replaced by XML reader
import math # For calculating positions and distances
import random
from sys import path

# Kivy Imports

from kivy.app import App # Base App Class
from kivy.core.image import Image
from kivy.graphics import \
    Canvas, Color, Rectangle, Line, Point, Rotate, PushMatrix, PopMatrix
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics.transformation import Matrix
from kivy.core.text import Label as CoreLabel


# ==============================================================================
# VARIABLES
# ==============================================================================


# Images

STAR01 = path[0] + '/stars/star_' + '01' + '.png'
STAR02 = path[0] + '/stars/star_' + '02' + '.png'
STAR03 = path[0] + '/stars/star_' + '03' + '.png'
STAR04 = path[0] + '/stars/star_' + '04' + '.png'
STAR05 = path[0] + '/stars/star_' + '05' + '.png'
STAR06 = path[0] + '/stars/star_' + '06' + '.png'
STAR07 = path[0] + '/stars/star_' + '07' + '.png'
STAR08 = path[0] + '/stars/star_' + '08' + '.png'
STAR09 = path[0] + '/stars/star_' + '09' + '.png'
STAR10 = path[0] + '/stars/star_' + '10' + '.png'
STAR11 = path[0] + '/stars/star_' + '11' + '.png'
STAR12 = path[0] + '/stars/star_' + '12' + '.png'
STAR13 = path[0] + '/stars/star_' + '13' + '.png'
STAR14 = path[0] + '/stars/star_' + '14' + '.png'

STARS = [
    STAR01,
    STAR02,
    STAR03,
    STAR04,
    STAR05,
    STAR06,
    STAR07,
    STAR08,
    STAR09,
    STAR10,
    STAR11,
    STAR12,
    STAR13,
    STAR14
    ]

# Coordinate Translations

ALPHA = {
    'A': -55000,
    'B': -50000,
    'C': -45000,
    'D': -40000,
    'E': -35000,
    'F': -30000,
    'G': -25000,
    'H': -20000,
    'I': -15000,
    'J': -10000,
    'K': -5000,
    'L': 0,
    'M': 5000,
    'N': 10000,
    'O': 15000,
    'P': 20000,
    'Q': 25000,
    'R': 30000,
    'S': 35000,
    'T': 40000,
    'U': 45000,
    'V': 50000,
    'W': 55000,
    'X': 60000,
    'Y': 65000,
    'Z': 70000
    }

NUMERIC = {
    '0': 45000,
    '1': 40000,
    '2': 35000,
    '3': 30000,
    '4': 25000,
    '5': 20000,
    '6': 15000,
    '7': 10000,
    '8': 5000,
    '9': 0,
    '10': -5000,
    '11': -10000,
    '12': -15000,
    '13': -20000,
    '14': -25000,
    '15': -30000,
    '16': -35000,
    '17': -40000,
    '18': -45000,
    '19': -50000,
    '20': -55000,
    '21': -60000,
    '22': -65000,
    '23': -70000,
    '24': -75000,
    '25': -80000
    }

# System Paths

Path_up = path[0].split('/')
Path_up = '/'.join(Path_up[:-1])

# Star Systems

SYSTEMS_LIST = pickle.load(open(
    Path_up + '/StarSystems/' + 'StarSystems.pk',
    'rb'
    ))

# Quick Systems fixes below, need to be written back into pickled list.
for system in SYSTEMS_LIST:
    if system[0] == 'Junction' and system[1] == 'Thesme':
        system[0] = 'Feriae Junction'
SYSTEMS_LIST.append(['Bandomeer','Meerian','Outer Rim Territories', 'O-6'])
SYSTEMS_LIST.append(['Joiol','Orus','Inner Rim', 'M-8'])
SYSTEMS_LIST.append(['Estaria','Indrexu','Outer Rim Territories', 'S-5'])
SYSTEMS_LIST.append(['Doldur','Doldur','Mid Rim', 'P-15'])
SYSTEMS_LIST.append(['Mechis', None,'Inner Rim', 'L-14'])
SYSTEMS_LIST.append(["Yag'Dhul", None,'Inner Rim', 'L-14'])
SYSTEMS_LIST.append(['Tauber','Jaso','Inner Rim', 'L-14'])
SYSTEMS_LIST.append(['Sullust','Brema','Outer Rim Territories', 'M-17'])
SYSTEMS_LIST.append(['Galand','Torranix','Core Worlds', 'K-10'])
SYSTEMS_LIST.append(['Ywllandr','Prefsbelt','Outer Rim Territories', 'K-5'])
SYSTEMS_LIST.append(['Enarc','Alui','Mid Rim', 'O-17'])
SYSTEMS_LIST.append(['Aikhibba','Fei Hu','Mid Rim', 'P-13'])
SYSTEMS_LIST.append(['Dravian Starport','Tamarin','Outer Rim Territories', 'N-18'])
SYSTEMS_LIST.append(['Foerost', None, 'Core Worlds', 'L-10'])
SYSTEMS_LIST.append(['Teyr', None, 'Colonies', 'L-13'])
SYSTEMS_LIST.append(['Vasha','Zuma (Moddell)','Outer Rim Territories', 'H-16'])
SYSTEMS_LIST.append(['Trindello','Zuma (Moddell)','Outer Rim Territories', 'H-16'])
SYSTEMS_LIST.append(['Ninn','Corporate Sector','Outer Rim Territories', 'R-3'])
SYSTEMS_LIST.append(['Duroon','Corporate Sector','Outer Rim Territories', 'S-4'])
SYSTEMS_LIST.append(['Ton-Falk','Pakuuni','Outer Rim Territories', 'T-5'])
SYSTEMS_LIST.append(['Anstares','Juvex','Mid Rim', 'L-17'])
SYSTEMS_LIST.append(["Milvayne", None,'Inner Rim', 'L-8'])

# Major Trade Routes

CORELLIAN_RUN = [
    'Corellian Run',
    [
        'Coruscant',
        'Ixtlar',
        'Wukkar',
        'Kailor',
        'Xorth',
        'Vuma',
        'Leria Kerlsil',
        'Perma',
        'Lolnar',
        'Rehemsa',
        'Sedratis',
        'Rydonni Prime',
        'Corellia',
        'Nubia',
        'Tinnel',
        'Loronar',
        'Byblos',
        'Pencael',
        'Havricus',
        'Iseno',
        'Denon',
        'Spirana',
        'Rhommamool',
        'Tlactehon',
        'Allanteen',
        'Gamor',
        'Milagro',
        'Thaere',
        'New Cov',
        'Doldur',
        'Druckenwell',
        'Kabray',
        'Algara',
        'Andosha',
        'Mon Gazza',
        'Herdessa',
        'Radnor',
        'Christophsis',
        'Arkanis',
        'Sirpar',
        'Gorno',
        'Dalchon',
        'Ryloth',
        'Wrea'
        ]
    ]
CORELLIAN_TRADE_SPINE = [
    'Corellian Trade Spine',
    [
        'Corellia',
        'Duro',
        'Chasin',
        'Condular',
        'Gandeal',
        'Belazura',
        'Bryexx',
        'Enisca',
        'Kelada',
        'Foless',
        'Bestine',
        'Mechis',
        'Renillis',
        "Yag'Dhul",
        'Harrin',
        'Moorja',
        'Calus',
        'Epica',
        'Roona',
        'Borkyne',
        'Kinyen',
        'Pendari',
        'Tar Morden',
        'Calonica',
        'Bomis Koori',
        'Kriselist',
        'Chibias',
        'Kaal',
        'Dalisor',
        'Jiroch',
        'Quamar',
        'Cargamalis',
        'Mugaar',
        'Javin',
        'Aztubek',
        'Kumru',
        'High Chunah',
        'Kirtarkin',
        'Mexeluine',
        'Gerrenthum',
        'Indellian',
        'Bendeluum',
        'Zhanox',
        'Ione',
        'Mataou',
        'Anantapar',
        'Shuxl',
        'Ertegas',
        'Darlyn Boda',
        'Orn Kios',
        'Ozu',
        'Isde Naha',
        'Togominda',
        "Berrol's Donn",
        "Sil'Lume",
        'Manpha',
        'Terminus'
        ]
    ]
HYDIAN_WAY = [
    'Hydian Way',
    [
        'Bonadan',
        'Cadomai',
        'Ruuria',
        'Listehol',
        'Tantive',
        'Doniphon',
        'Telos',
        'Praadost',
        "Pho Ph'eah",
        'Serenno',
        'Toprawa',
        'Simpla',
        'Sorrus',
        'Feriae Junction',
        'Tierell',
        'Celanon',
        'Hijado',
        'Botajef',
        'Harloen',
        'Bandomeer',
        'Taris',
        'Skorrupon',
        'Corsin',
        'Leafar',
        'Chennis',
        'Adin',
        'Draria',
        'Viga',
        'Kidriff',
        'Nessem',
        'Bogden',
        'Paqualis',
        'Per Lupelo',
        'Drearia',
        'Champala',
        'Nierport',
        'Uviuy Exen',
        'Wakeelmui',
        'Brentaal',
        'Skako',
        'Aldraig',
        'Demophon',
        'Glithnos',
        'Fedalle',
        'Talravin',
        'Ruul',
        'Trellen',
        'Mawan',
        'Loretto',
        'Baraboo',
        'Bellassa',
        'Jaciprus',
        'Voktunma',
        'Exodeen',
        'Boudolayz',
        'Herzob',
        'Besnia',
        'Koensayr',
        'Aquilae',
        'Denon',
        'Sagar',
        'Ronyards',
        'Chardaan',
        'Babbadod',
        'Nordra',
        'Perithal',
        'Shibric',
        'Baroli',
        'Gacerian',
        'Ragith',
        'Majoor',
        'Ramordia',
        'Arrgaw',
        'Pax',
        'ZeHeth',
        'Malastare',
        'Chryya',
        'Darkknell',
        'Cmaoli Di',
        'Eriadu',
        'Averam',
        'Shumavar',
        'Atravis',
        'Rutan',
        'Fwatna',
        'Terminus',
        'Imynusoph'
        ]
    ]
PERLEMIAN_TRADE_ROUTE = [
    'Perlemian Trade Route',
    [
        'Coruscant',
        'Alsakan',
        'Grizmallt',
        'Anaxes',
        'Corulag',
        'Chandrila',
        'Brentaal',
        'Esseles',
        'Rhinnal',
        'Ralltiir',
        'Delle',
        'Yabol Opa',
        'Ifmix',
        'Shulstine',
        'Castell',
        'Raithal',
        'Vurdon Ka',
        'Joiol',
        'Chazwa',
        'Relatta',
        'Tirahnn',
        'Dalcretti',
        'Taanab',
        'Sermeria',
        'Carcel',
        'Pirin',
        'Gizer',
        'Lantillies',
        'Rearqu Cluster',
        'Jeyell',
        'Roche',
        'Orleon',
        'Talcene',
        'Salvara',
        'Euceron',
        'Abhean',
        'Wheel, The',
        'Centares',
        'Antemeridias',
        'Budpock',
        'Columex',
        'Arcan',
        'Lianna',
        'Barseg',
        'Lorrad',
        'Desevro',
        'Kanaver',
        'Janodral Mizar',
        "Ank Ki'Shor",
        'Estaria',
        'Makem Te',
        'Quermia'
        ]
    ]
RIMMA_TRADE_ROUTE = [
    'Rimma Trade Route',
    [
        'Abregado',
        'Dentaal',
        'Giju',
        'Ghorman',
        'Vanik',
        'Thyferra',
        'Tauber',
        "Yag'Dhul",
        'Sukkult',
        'Wroona',
        'Tregillis',
        'Vandelhelm',
        'Woostri',
        'Daemen',
        'Alakatha',
        'Lanthe',
        'Vondarc',
        'Medth',
        'Starlyte Station',
        'Sullust',
        'Eriadu',
        "Clak'dor",
        'Triton',
        'Sluis Van',
        'Denab',
        'Tarabba Prime',
        'Adarlon',
        'Karideph'
        ]
    ]

MAJOR_TRADE_ROUTES = [
    CORELLIAN_RUN,
    CORELLIAN_TRADE_SPINE,
    HYDIAN_WAY,
    PERLEMIAN_TRADE_ROUTE,
    RIMMA_TRADE_ROUTE
    ]

# Minor Trade Routes

ACFREN_SPUR = [
    "Ac'fren Spur",
    [
        'Sriluur',
        'Ques',
        'Tas-La',
        ]
    ]
AGARIX_TRADE_ROUTE = [
    'Agarix Trade Route',
    [
        'Pieldi',
        'Dramassia',
        'Umthyg',
        'Dasoor',
        ]
    ]
AGRICULTURAL_CIRCUIT = [
    'Agricultural Circuit',
    [
        'Cal-Seti',
        'Fresia',
        'Galand',
        "Worru'du",
        'Salliche',
        'Stassia',
        'Ruan',
        'Yulant',
        'Aargau',
        'Broest',
        'Xorth'
        ]
    ]
ADO_SPINE = [
    'Ado Spine',
    [
        'Medth',
        'Indupar',
        'StarForge Nebula',
        'Eiattu',
        ]
    ]
AMADOR_DREARIA_HYPERLANE = [
    'Amador-Drearia Hyperlane',
    [
        'Mayvitch',
        'Ord Lithone',
        'Milvayne',
        'Drearia',
        ]
    ]
ANNAJ_HOUCHE_RUN = [
    'Annaj-Houche Run',
    [
        'Annaj',
        'Ovise',
        'Thonner',
        'Maya Kovel',
        'Vasha',
        'Houche',
        ]
    ]
ANTURI_REACH = [
    'Anturi Reach',
    [
        'Karfeddion',
        'Atron',
        'Port Evokk',
        "Tekurr'k",
        'Yetoom',
        'Dolla',
        ]
    ]
ARDAN_CROSS = [
    'Ardan Cross',
    [
        'Troos',
        'Atorra',
        'Chenowei',
        "B'trilla",
        'Feena',
        'Kalishik',
        'Arda',
        'Feldwes',
        'Pygorix',
        'Spintir',
        ]
    ]
ARLEEN_LOOP = [
    'Arleen Loop',
    [
        'Arleen',
        'Rafa',
        'Dela',
        'Lekua',
        ]
    ]
AUTHORITY_ARC = [
    'Authority Arc',
    [
        'Ammuud',
        'Urdur',
        'Oslumpex',
        'Matra',
        'Orron',
        ]
    ]
AUTHORITY_GUARDIAN_CORRIDOR = [
    'Authority Guardian Corridor',
    [
        'Lafra',
        'Dra',
        'Craci',
        'Drog',
        "Mall'ordian",
        'Ninn',
        'Hiit',
        'Atchorb',
        'Tothis',
        'Kir',
        ]
    ]
AXXILA_TANGRENE_HYPERLANE = [
    'Axxila-Tangrene Hyperlane',
    [
        'Axxila',
        'Vandyne',
        'Camden',
        'Edusa',
        'Tangrene',
        ]
    ]
BAKURA_TRACE = [
    'Bakura Trace',
    [
        'Endor',
        'Sanyassa',
        'Ast Kikorie',
        'Bakura',
        ]
    ]
BELSAVIS_RUN = [
    'Belsavis Run',
    [
        "Tekurr'k",
        'Belsavis',
        ]
    ]
BOTHAN_RUN = [
    'Bothan Run',
    [
        'Bothawui',
        'Moonus Mandel',
        'Lannik',
        'Daalang',
        ]
    ]
BRAXANT_RUN = [
    'Braxant Run',
        [
        'Bandomeer',
        "Er'Kit",
        'Borgo Prime',
        'Agamar',
        "Harrod's Planet",
        'Ketaris',
        'Fedje',
        'Vuchelle',
        'Isiring',
        'New Bakstre',
        'Cassander',
        'Garqi',
        'Minashee',
        'Mygeeto',
        'Aris',
        'Ord Trasi',
        'Gwori',
        'Kwevron',
        'Venestria',
        'Muunilinst',
        'Jaemus',
        'Bescane',
        'Bastion',
        'Qonto',
        'Xerton',
        ]
    ]
BRENTAAL_DENON_ROUTE = [
    'Brentaal-Denon Route',
    [
        'Brentaal',
        'Skako',
        'Fedalle',
        'Bellassa',
        'Exodeen',
        'Denon',
        ]
    ]
BYSS_RUN = [
    'Byss Run',
    [
        'Empress Teta',
        'Keeara Major',
        'Prakith',
        'Byss',
        ]
    ]
CADINTH_RUN = [
    'Cadinth Run',
    [
        'Lianna',
        'Spinax',
        'Cadinth',
        'Embaril',
        'Voss',
        'Jaminere',
        'Dravione',
        ]
    ]
CADMA_CONDUIT = [
    'Cadma Conduit',
    [
        'Junkfort Station',
        'Dagelin Minor',
        'Oseon',
        'Scillal',
        'Lekua',
        'Cadma',
        'Zebitrope',
        ]
    ]
CALIPSA_RUN = [
    'Calipsa Run',
    [
        'Aleron',
        'Nista',
        'Gilliana',
        'Pelagon',
        'Bethal',
        'Kamper',
        'Calipsa',
        'New Javis',
        'Lorenz',
        'Dampher',
        'Grella',
        'Nella',
        'Estaph',
        ]
    ]
CALORIA_RUN = [
    'Caloria Run',
    [
        'Canti',
        'Caloria',
        'Tanger',
        'Reena',
        'Tillo',
        'Tavitz',
        ]
    ]
CARBONITE_RUN = [
    'Carbonite Run',
    [
        'Empress Teta',
        'Goluud Prime',
        'Vulpter',
        ]
    ]
CELANON_SPUR = [
    'Celanon Spur',
    [
        'Dorin',
        'Myomar',
        'Vicondor',
        'Station 88',
        'Vortex',
        'Nentan',
        "T'olan",
        'Dohu',
        'Ord Mantell',
        'Dor Nameth',
        'Korvaii',
        'Alderath',
        'Orocco',
        'Ithor',
        'Noonar',
        'Cademimu',
        'Paarin Minor',
        'Kebolar',
        'Agamar',
        'Shaum Hii',
        'New Holgha',
        'Vinsoth',
        'Axxila',
        'Ord Cestus',
        'Pedd',
        'Celanon',
        ]
    ]
CEREAN_REACH = [
    'Cerean Reach',
    [
        'Cerea',
        'Cheelit',
        'Koba',
        'Riflor',
        'Hirsi',
        'Elbara',
        'Quaensan Prime',
        'Lorta',
        ]
    ]
COMMENOR_RUN = [
    'Commenor Run',
    [
        'Brentaal',
        'Tepasi',
        'Korfo',
        'Caamas',
        'Alderaan',
        'Tyed Kant',
        'Parkis',
        'Kattada',
        'Commenor',
        ]
    ]
COR_LANE = [
    'Cor Lane',
    [
        'Cor III',
        'Cor II',
        'Cor I',
        'Crella',
        'Barnaba',
        ]
    ]
CORSIN_RUN = [
    'Corsin Run',
    [
        'Brentaal',
        'Uviuy Exen',
        'Champala',
        'Drearia',
        'Paqualis',
        'Bogden',
        'Corsin',
        ]
    ]
COTH_FUURAS_NESSEM_HYPERLANE = [
    'Coth Fuuras-Nessem Hyperlane',
    [
        'Coth Fuuras',
        'Aramal',
        'Doshan',
        'Muzara',
        'Vorian',
        'Anduvia',
        'Immalia',
        'Mayvitch',
        'Yinchorr',
        'Golden Nyss',
        'Shili',
        'Kiros',
        'Sljee',
        'Nessem',
        ]
    ]
COYN_ROUTE = [
    'Coyn Route',
    [
        'Coyn',
        'Tantra',
        ]
    ]
DAELGOTH_TRADE_ROUTE = [
    "D'Aelgoth Trade Route",
    [
        'Kassido',
        'Selenius',
        'Ogem',
        'Cyphar',
        'Feenix',
        'Miztoc',
        'Kriselist',
        ]
    ]
DAUNTLESS_RUN = [
    'Dauntless Run',
    [
        'Ota',
        'Rorgam',
        'Pizilis',
        ]
    ]
DEAD_ROAD = [
    'Dead Road, The',
    [
        'Nimia',
        'Kafane',
        'Ulmatra',
        'Zisia',
        'Elgit',
        'Usk',
        'Saqqar',
        'Tisht',
        "M'Hanna",
        'Varl',
        ]
    ]
DESEVRAN_TRACE = [
    'Desevran Trace',
    [
        'Desevro',
        'Folende',
        'Omman',
        'Amarin',
        'Corlax',
        'Dravione',
        ]
    ]
DURKTEEL_LOOP = [
    'Durkteel Loop',
    [
        'Kashyyyk',
        'Kwookrrr',
        'Sneeve',
        'Durkteel',
        'Yitabo',
        ]
    ]
DUROS_SPACE_RUN = [
    'Duros Space Run',
    [
        'New Cov',
        'Kalarba',
        'Triffis',
        'Bannistar Station',
        'Enarc',
        'Alui',
        'Verdanth',
        'Sanrafsix',
        'Heptooine',
        'Jutrand',
        'Darkknell',
        ]
    ]
ENARC_RUN = [
    'Enarc Run',
    [
        'Enarc',
        'Naboo',
        'Alassa Major',
        'Kalinda',
        'Nigel',
        'Roldalna',
        'Ropagi',
        'Pax',
        'Krann',
        'Vogel',
        'Vondarc',
        ]
    ]
ENTRALLA_ROUTE = [
    'Entralla Route',
        [
        'Ord Mantell',
        'Qiilura',
        'Yout',
        'Ord Tessebok',
        'Gonmore',
        'Obredaan',
        'Lonnaw',
        'Orinda',
        'Wistril',
        'JanFathal',
        'Domgrin',
        'Ywllandr',
        'Borosk',
        'Prefsbelt',
        'Ompersan',
        'Yaga Minor',
        'Capza',
        'Entralla',
        'Endoraan',
        'Bisellia',
        'Muunilinst',
        ]
    ]
ETTI_ROUTE_MAJOR = [
    'Etti Route Major',
    [
        'Kail',
        'Davirien',
        'Drog',
        'Etti',
        ]
    ]
FALKO_RUN = [
    'Falko Run',
    [
        'Oseon',
        'Arleen',
        'Dilonexa',
        'Uaua',
        'Falko',
        'Antipose',
        'Paulking',
        'Douglas',
        ]
    ]
FEENA_RUN = [
    'Feena Run',
    [
        'Feena',
        'Barison',
        'Usta',
        'Cometwash, The',
        'Korphir',
        ]
    ]
FIVE_VEILS_ROUTE = [
    'Five Viels Route',
    [
        'Farstine',
        'Ninzam',
        'Stend',
        'Lybeya',
        'Bajic',
        'Vohai',
        'Elshandruu Pica',
        'Skynara',
        ]
    ]
GAMOR_RUN = [
    'Gamor Run',
    [
        'Gamor',
        'Merren',
        'Aridus',
        'Charra',
        'Aikhibba',
        'Hoylin',
        'Beris',
        'Deneba',
        'Chokan',
        'Shador',
        'Thokosia',
        'Daalang',
        'Circumtore',
        'Rorak',
        ]
    ]
GANDEAL_FONDOR_HYPERLANE = [
    'Gandeal-Fondor Hyperlane',
    [
        'Gandeal',
        'Scarl',
        'Fondor',
        ]
    ]
GELVARNO_LOOP = [
    'Gelvarno Loop',
    [
        "Ch'manss",
        'Gevarno Cluster',
        'Haruun Kal',
        'Jutrand',
        'Opari',
        ]
    ]
GIBLIM_ROUTE = [
    'Giblim Route',
    [
        'Caluula',
        'Dellalt',
        'Minntooine',
        'Mon Calamari',
        ]
    ]
GIJU_RUN = [
    'Giju Run',
    [
        'Tallaan',
        'Giju',
        'Omar',
        'Illodia',
        'Dahrtag',
        'Hjaff',
        'Kitel Phard',
        ]
    ]
GREAT_GRAN_RUN = [
    'Great Gran Run',
    [
        'Kinyen',
        'New Balosar',
        "Noe'ha'on",
        'Natalon',
        'Har Binande',
        'Halm',
        'Petabys Station',
        'Tashtor Seneca',
        'Chalcedon',
        'Cerea',
        ]
    ]
GREAT_KASHYYYK_BRANCH = [
    'Great Kashyyyk Branch',
    [
        'Zeltros',
        'Virujansi',
        'Umbara',
        'Quas Killam',
        'Torn Station',
        'Kashyyyk',
        'Balamak',
        'Charros',
        ]
    ]
GREATER_CRONESE_ARC = [
    'Greater Cronese Arc',
    [
        'Arcan',
        'Janilis',
        'Chandaar',
        'Oor',
        'Barancar',
        'Soruus',
        'Pasmin',
        'Arramanx',
        'Duinarbulon',
        'Derellium',
        ]
    ]
HARRIN_TRADE_CORRIDOR = [
    'Harrin Trade Corridor',
    [
        'Harrin',
        'Wroona',
        'Droecil',
        'Lohopa',
        'Jurzan',
        'Arrgaw',
        'Lazerian',
        'Cerenia',
        'Brevost',
        'Momansi',
        'Krann',
        'Coonee',
        'Sika',
        'Milagro',
        'Merren',
        ]
    ]
HOLLASTIN_RUN = [
    'Hollastin Run',
    [
        'Circumtore',
        'Affavan',
        'Hollastin',
        'Aylayl',
        'Tsyk',
        'Unagin',
        'Syvris',
        ]
    ]
HYABB_TWITH_CORRIDOR = [
    'Hyabb-Twith Corridor',
    [
        'Hyabb',
        'Voon',
        'Twith'
        ]
    ]
ILOSIAN_SPUR = [
    'Ilosian Spur',
    [
        'Bimmisaari',
        'Xoman',
        'Boz Pity',
        'Alee',
        'Tal Nami',
        'Ilos Minor',
        ]
    ]
INDREXU_ROUTE = [
    'Indrexu Route',
    [
        'Dravione',
        'Argai',
        'Corlass',
        'Panna',
        'Derellium',
        ]
    ]
INTRA_SECTOR_SPUR = [
    'Intra-Sector Spur',
    [
        'Reltooine',
        'Knolstee',
        'Kail',
        'Craci',
        'Jerrist',
        'Biewa',
        ]
    ]
ISON_CORRIDOR = [
    'Ison Corridor',
    [
        'Indellian',
        'Varonat',
        'Bespin',
        'Anoat',
        'Hoth',
        'Ison',
        'Mataou',
        ]
    ]
JUNCTION_TIERELL_LOOP = [
    'Junction-Tierell Loop',
    [
        'Feriae Junction',
        'Tertiary Feswe',
        'Selitan',
        'Pinoora',
        'Torque',
        'Jovan',
        'Vallusk Cluster',
        'Arkuda',
        'Gulvitch',
        'Bronsoon',
        'Povanaria',
        "Durgen's Star",
        'Trinovat',
        'Near Indosa',
        'Presbalin',
        'Tierell',
        ]
    ]
KAAGA_RUN = [
    'Kaaga Run',
    [
        'Circumtore',
        'Carnovia',
        'Nar Kaaga',
        'Dohlban',
        'Void Station',
        'Bothawui',
        ]
    ]
KASSIDO_BYPASS = [
    'Kassido Bypass',
    [
        'Kassido',
        'Yhifar',
        'Kardura',
        'Dioll',
        'Thermon',
        'Malador',
        ]
    ]
KESSEL_RUN = [
    'Kessel Run',
    [
        'Formos',
        'Rion',
        'Kessel',
        ]
    ]
KESSEL_TRADE_CORRIDOR = [
    'Kessel Trade Corridor',
    [
        'Kessel',
        'Zerm',
        ]
    ]
KIRA_RUN = [
    'Kira Run',
    [
        'Lazerian',
        'Kira',
        'Ropagi',
        ]
    ]
KISMAANO_BYPASS = [
    'Kismaano Bypass',
    [
        'Cadinth',
        'Kismaano',
        'Gadon',
        'Arramanx',
        ]
    ]
KOROS_TRUNK_LINE = [
    'Koros Trunk Line',
    [
        'Coruscant',
        'Foerost',
        'Kaikielius',
        'Ruan',
        'Jerrilek',
        'Empress Teta',
        ]
    ]
KODA_SPUR = [
    'Koda Spur',
    [
        'Lutrillia',
        'Ryoone',
        'Koda Space Station',
        ]
    ]
KORPHIR_TRACE = [
    'Korphir Trace',
    [
        'Korphir',
        'Roil, The',
        'Arkuda',
        ]
    ]
LUCAYA_CROSS = [
    'Lucaya Cross',
    [
        'Media',
        'Ession',
        'Saffalore',
        ]
    ]
LESSOR_CRONESE_ARC = [
    'Lessor Cronese Arc',
    [
        'Derellium',
        'Eibon',
        'Algor',
        'Saheelindeel',
        'Caluula',
        ]
    ]
LESSOR_LANTILLIAN_ROUTE = [
    'Lesser Lantillian Route',
    [
        'Zeltros',
        'Merson',
        'Taboon',
        'Ambria',
        'Onderon',
        'Porus Vida',
        'Vena',
        'Nazzri',
        'Avenelle',
        'Uyter',
        'Togoria',
        'Charros',
        'Bimmisaari',
        'Peg Shar',
        'Pusat Station',
        'Boonta',
        'Junkfort Station',
        ]
    ]
LEOZI_ROUTE = [
    'Leozi Route',
    [
        'Tanda',
        'Pozzi',
        'Tanzis',
        'Tanya',
        'Javis',
        ]
    ]
LIPSEC_RUN = [
    'Lipsec Run',
    [
        'Lipsec',
        'Virgillia',
        'Sump',
        'Keskin',
        'Abridon',
        'Isde Naha',
        'Bettel',
        'Mev',
        'Kelrodo-Ai',
        'Dorvalla',
        'Eriadu',
        ]
    ]
LISTEHOL_RUN = [
    'Listehol Run',
    [
        'Listehol',
        'Mirial',
        'Sagma',
        'Sikurd',
        'Gigor',
        'Zygerria',
        ]
    ]
LLANIC_SPICE_RUN = [
    'Llanic Spide Run',
    [
        'Troos',
        'Atorra',
        'Chenowei',
        "B'trilla",
        'Feena',
        'Kalishik',
        'Arda',
        'Feldwes',
        'Pygorix',
        'Spintir',
        ]
    ]
LUTRILLIAN_CROSS = [
    'Lutrillian Cross',
    [
        'Lutrillia',
        'Shuldene',
        'Mijos',
        'Gerrenthum',
        ]
    ]
MANDA_MERCHANT_ROUTE = [
    'Manda Merchant Route',
    [
        'Bothawui',
        'Kothlis',
        'Thoran',
        'Zygia',
        'Holess',
        'Boranda',
        'Manda',
        'Dennaskar',
        'Hishyim',
        'Rishi',
        'Ukio',
        'Molavar',
        ]
    ]
MANDALORIAN_ROAD = [
    'Mandalorian Road',
    [
        'Corsin',
        'Ploo',
        'Vulta',
        'Jebble',
        'Taris',
        'Vanquo',
        'Flashpoint',
        'Ordo',
        'Mandalore',
        ]
    ]
MENTELLOS_TRADE_ROUTE = [
    'Mentellos Trade Route',
    [
        'Coruscant',
        'Metellos',
        'Norkronia',
        'Alland',
        'Cal-Seti',
        'Galantos',
        'Orooturoo'
        ]
    ]
MURGO_CHOKE = [
    'Murgo Choke',
    [
        'Rago',
        'Murgo',
        'Utegetu Nebula',
        ]
    ]
MYTOS_ARROW = [
    "Myto's Arrow",
    [
        'Dantooine',
        'Angor',
        'Gabredor',
        'Jaemus',
        ]
    ]
NAMADII_CORRIDOR = [
    'Namadii Corridor',
    [
        'Coruscant',
        'Tanjay',
        'Weerden',
        'Galvoni',
        'Twith',
        'Pantolomin',
        'Borleias',
        'Mirit',
        'Palanhi',
        'Carratos',
        'Voltare',
        'Meastrinnar',
        'Aphran',
        'Bengat',
        'Bilbringi',
        'Rondai',
        'Coth Fuuras',
        'Dorin',
        'Carvandir',
        'Vaced',
        'Glee Anselm',
        'Belshar Othacuu',
        'Ord Varee',
        'Kalaan',
        'Masgen',
        'Ansion',
        'Namadii'
        ]
    ]
NANTHRI_ROUTE = [
    "Nanth'ri Route",
    [
        'Exodeen',
        'Quellor',
        'Antar',
        'Gyndine',
        'Fabrin',
        'Circarpous',
        'Zaloriis',
        'Attahox',
        "Nanth'ri",
        ]
    ]
NIGHTROAD = [
    'Nightroad',
    [
        'Kashyyyk',
        'Tholatin',
        'Mytaranor',
        'Pizilis',
        "Terr'skiar",
        ]
    ]
NOTHOIIN_CORRIDOR = [
    'Nothoiin Corridor',
    [
        'Shuldene',
        'Mijos',
        'Gerrenthum',
        'Council',
        'Nothoiin',
        'Saila Na',
        'Bavva',
        'Dolla',
        'Eriadu',
        ]
    ]
OKTOS_ROUTE = [
    'Oktos Route',
    [
        'Nal Hutta',
        'Kleeva',
        'Toydaria',
        'Tol Amn',
        ]
    ]
OOTMIAN_PABOL = [
    'Ootmian Pabol',
    [
        'Gyndine',
        'Reytha',
        'Chanosant',
        'Trammen',
        'Belasco',
        'Zirulast',
        'New Apsolon',
        'Coachelle',
        'Ota',
        'Randon',
        'Blimph',
        'Ubrikkia',
        'Kwenn Space Station',
        'Keldooine',
        'Nar Bo Sholla',
        'Irith',
        'Du Hutta',
        'Nal Hutta',
        ]
    ]
OVERIC_GRIPLINK = [
    'Overic Gripline',
    [
        'Quermia',
        'Toola',
        'Florn',
        'Ton-Falk',
        'Pakuuni',
        'Shaylin',
        'Turkana',
        'Munto Codru',
        'Reginard',
        'Ruisto',
        'Mon Calamari',
        'Pammant',
        'Mantan',
        ]
    ]
OVISE_REACH = [
    'Ovise Reach',
    [
        'Ovise',
        'Trindello',
        'Zorbia',
        'Endor',
        ]
    ]
PABOL_HUTTA = [
    'Pabol Hutta',
    [
        'Nal Hutta',
        'Hosko',
        'Varl',
        'Gos Hutta',
        'Mulatan',
        'Sleheyron',
        'Sespe',
        ]
    ]
PABOL_KREETA = [
    'Pabol Kreeta',
    [
        'Nar Kreeta',
        'Nar Bo Sholla',
        ]
    ]
PABOL_SLEHEYRON = [
    'Pabol Sleheyron',
    [
        'Formos',
        'Prishella',
        'Little Kessel',
        'Aeneid',
        'Zerm',
        'Randa',
        'Ulmatra',
        'Sleheyron',
        'Nimban',
        'Nar Kreeta',
        'Ilos Minor',
        'Ilos',
        'Chalacta',
        'Yitabo',
        'Randon',
        ]
    ]
PAKUUNI_DRIFT = [
    'Pakuuni Drift',
    [
        'Pakuuni',
        'Gbu',
        'Mullan',
        'Brigia',
        ]
    ]
PANDO_SPUR = [
    'Pando Spur',
    [
        'Hollastin',
        'Xolu',
        'Far Pando',
        'Near Pando',
        ]
    ]
PINOORAN_SPUR = [
    'Pinooran Spur',
    [
        'Kushibah',
        'Mogoshyn',
        'Betshish',
        "Kli'aar",
        'Marrovia',
        'Ladarra',
        'Krylon',
        'Pinoora',
        ]
    ]
PROCOPIAN_SHIPPING_LANE = [
    'Percopian Shipping Lane',
    [
        'Tallaan',
        'Tavya',
        'Neona',
        'Reyna',
        'Procopia',
        'Lastelle',
        'Estaph',
        'Obulette',
        'Javis',
        'Tumus',
        'Bianas',
        'Reena',
        ]
    ]
PROUSLYS_RIM_RUN = [
    "Prously's Rim Run",
    [
        'Mon Calamari',
        'Pammant',
        'Mantan',
        'New Heurkea',
        'Sanctuary',
        'Kamdon',
        'Dornea',
        'Baros',
        ]
    ]
QUELLOR_RUN = [
    'Quellor Run',
    [
        'Commenor',
        'Damoria',
        'Chorax',
        'Rachuk',
        'Cato Neimoidia',
        'Hensara',
        'Talasea',
        'Lankashiir',
        'Quellor',
        ]
    ]
RAGO_RUN = [
    'Rago Run',
    [
        'Rago',
        'Sinton',
        'Gilatter',
        'Ansion',
        'Keitum',
        ]
    ]
RANDON_RUN = [
    'Randon Run',
    [
        'Lantillies',
        'Phaseera',
        'Uyter',
        'Kashyyyk',
        'Rakhuuun',
        'Chamble',
        'Messert',
        'Randon',
        ]
    ]
REENA_TRADE_ROUTE = [
    'Reena Trade Route',
    [
        'Druckenwell',
        'Haseria',
        'Monastery',
        'Spirador',
        'Bothawui',
        ]
    ]
RELGIM_RUN = [
    'Relgim Run',
    [
        'Fedje',
        'Fest',
        'Devon',
        'Generis',
        "Markbee's Star",
        "Nam'ta",
        'Horuz',
        'Mantooine',
        'Vykos',
        'Aris',
        'Marmoth',
        'Cezith',
        'Endoraan',
        'Gelda',
        'Delephr',
        'Ord Thoden',
        ]
    ]
SALIN_CORRIDOR = [
    'Salin Corridor',
    [
        'Salin',
        'Vinsoth',
        'Drackmar',
        'Botajef',
        'Phindar',
        'Gala',
        'Vjun',
        'Lucazec',
        'Columex',
        'Belderone',
        'Trogan',
        'Sy Myrth',
        'Kile',
        'Komnor',
        'Boonta',
        'Novor',
        'Nwarcol',
        ]
    ]
SANCTUARY_PIPELINE = [
    'Sanctuary Pipeline',
    [
        'Sullust',
        'Endor',
        'Murk',
        ]
    ]
SANRAFSIX_CORRIDOR = [
    'Sanrafsix Corridor',
    [
        'Sanrafsix',
        'Fostin',
        'Syned',
        'Omwat',
        'Kabal',
        'Dravian Starport',
        'Sevarcos',
        'Kirdo',
        "Ma'ar Shaddam",
        'Cotellier',
        ]
    ]
SENEX_JUVEX_LOOP = [
    'Senex-Juvex Loop',
    [
        'Juvex',
        'Kimm Aurek',
        'Kimm Besh',
        'Kimm Cresh',
        'Tinallis',
        'Loovria',
        'Velga',
        'Pieldi',
        'Pirralor',
        'Resti Kel',
        'Malador',
        'Zaria',
        'Anstares',
        'Deminol',
        'Ossiathora',
        'Kassido',
        'Manforgon',
        'Mussubir',
        'Cyimarra',
        'Veron',
        'Presteen',
        'Caltinia',
        'Nepoy',
        'Hutlar',
        'Karfeddion',
        'Anturus',
        'Denebia',
        'Kalgo',
        ]
    ]
SENEX_TRACE = [
    'Senex Trace',
    [
        'Karfeddion',
        'Fengrine',
        'Neelanon',
        'Senex',
        'Rindao',
        'Parada',
        'Bortras',
        'Eriadu',
        ]
    ]
SHAG_PABOL = [
    'Shag Pabol',
    [
        'Nal Hutta',
        'Rorak',
        'Diyu',
        'Ylesia',
        'Ziugen',
        'Outland Transit Station',
        'Lirra',
        'Teth',
        ]
    ]
SHALTIN_TUNNELS = [
    'Shaltin Tunnels',
    [
        'Ulicia',
        'Atchorb',
        "D'ian",
        'Etti',
        'Ession',
        'Kalla',
        'Pondut Station',
        'Oslumpex',
        'Zygerria',
        'Tervissis',
        'Syngia',
        'Lianna',
        ]
    ]
SHAPANI_BYPASS = [
    'Shapani Bypass',
    [
        'Thyferra',
        'Mrlsst',
        'Alisandor',
        'Lamuir',
        'Tamber',
        'Tallaan',
        'Aleron',
        'Achillea',
        'Vindalia',
        'Diamal',
        'Abregado',
        ]
    ]
SHIPWRIGHTS_TRACE = [
    "Shipwrights' Trace",
    [
        'Fondor',
        'Bassadro',
        'Teyr',
        'Foless',
        'Las Lagon',
        'Affa',
        'Atzerri',
        'Chardaan',
        'Tynna',
        'Allanteen',
        ]
    ]
SHIRITOKU_WAY = [
    'Shiritoku Way',
    [
        'Endor',
        'Timora',
        'Bakura',
        ]
    ]
SHWUY_EXCHANGE = [
    'Shwuy Exchange',
    [
        'Uviuy Exen',
        'Dankayo',
        'Ord Antalaha',
        'Noquivzor',
        'Palanhi',
        'Vakkar',
        ]
    ]
SISAR_RUN = [
    'Sisar Run',
    [
        'Nwarcol',
        'Sriluur',
        'Terman',
        'Sespe',
        'Dirha',
        'Cyborrea',
        'Sionia',
        'Nimban',
        ]
    ]
SOLENBARAN_MERCHANT_ROUTE = [
    'Solenbaran Merchant Route',
    [
        'Kir',
        "R'alla",
        'Bonadan',
        'Etti',
        'Tirsa',
        'Jerrist',
        'Saclas',
        ]
    ]
SOLTERIOS_TRADE_ROUTE = [
    'Solterios Trade Route',
    [
        'Procopia',
        'Shindra',
        'Rianon',
        'Shella',
        'Bilios',
        'Soterios',
        'Barnaba',
        'Garobi',
        'Hellios',
        'Mrlsst',
        ]
    ]
SPAR_TRADE_ROUTE = [
    'Spar Trade Route',
    [
        'Cerea',
        'Abbaji',
        'Annaj',
        "Kuna's Tooth",
        ]
    ]
TALCENE_TRANSIT = [
    'Talcene Transit',
    [
        'Talcene',
        'Saleucami',
        'Kuthic',
        ]
    ]
TERRSKIAR_PASS = [
    "Terr'skiar Pass",
    [
        "Terr'skiar",
        'Bissillirus',
        'Deysum',
        ]
    ]
TERTIARY_SOLENBARAN = [
    'Tertiary Solenbaran',
    [
        'Saclas',
        'Duroon',
        'Biewa',
        'Kalla',
        'Issagra',
        'Deltooine',
        ]
    ]
THREE_ELLAS_RUN = [
    'Three Ellas Run',
    [
        'Tavya',
        'Sorella',
        'Dorella',
        'Pernella',
        ]
    ]
TIDAL_CIRCUIT = [
    'Tidal Circuit',
    [
        'Mon Calamari',
        'Pinperu',
        'Damendine',
        'Krinemonen',
        'Hinakuu',
        'Sanctuary',
        ]
    ]
TINGEL_ROUTE = [
    'Tingel Route',
    [
        'Bonadan',
        'Erysthes',
        'Issagra',
        'Ban-Satir',
        'Gaurick',
        'Joodrudda',
        ]
    ]
TION_TRADE_ROUTE = [
    'Tion Trade Route',
    [
        'Estaria',
        'Endregaad',
        'Raxus Prime',
        'Tion',
        'Argoon',
        'Rudrig',
        'Clariv',
        'Eredenn',
        'Stalimur',
        'Brigia',
        'Caluula',
        'Dellalt',
        ]
    ]
TRAX_TUBE = [
    'Trax Tube',
    [
        'Randon',
        'Deysum',
        'Lexrul',
        "Uogo'cor",
        "Nanth'ri",
        'Nixor',
        'Daalang',
        ]
    ]
TRELLEN_TRADE_ROUTE = [
    'Trellen Trade Route',
    [
        'Trellen',
        'Humbarine',
        'Commenor',
        'Rasterous',
        'Zeltros',
        ]
    ]
TRIANII_SHUNT = [
    'Trianii Shunt',
    [
        'Etti',
        'Lythos',
        'Hiit',
        'Fibuli',
        'Brochiib',
        ]
    ]
TRIELLUS_TRADE_ROUTE = [
    'Triellus Trade Route',
    [
        'Centares',
        'Sy Myrth',
        'Handooine',
        'Jabiim',
        'Taskeed',
        'Dennogra',
        'Junkfort Station',
        'Nimat',
        'Tammar',
        'Kegan',
        'Gestrex',
        'Norval',
        'Kubindi',
        'Drualkiin',
        'Formos',
        'Bheriz',
        'Aduba',
        'Glottal',
        'Teth',
        'Rampa',
        'Dilbana',
        'Clantaano',
        'Barab',
        'Dubrava',
        'Syvris',
        'Arami',
        'Gamorr',
        'Lyran',
        'Molavar',
        'Koiogra',
        'Piroket',
        'A-Foroon',
        'B-Foroon',
        'C-Foroon',
        'Ooo-temiuk',
        'Tatooine',
        'Andooweel',
        'Kemal Station',
        'New Ator',
        'Issor',
        'Arkanis',
        'Nelvaan',
        'Tythe',
        'Llanic',
        'Gall',
        'Farstine',
        'Ryndellia',
        'Enarc',
        ]
    ]
TRINDELLO_ENDOR_ROUTE = [
    'Trindello-Endor Route',
    [
        'Trindello',
        'Din Pulsar',
        'Endor',
        ]
    ]
TRITON_TRADE_ROUTE = [
    'Trition Trade Route',
    [
        'Karideph',
        'Pergitor',
        "Kal'Shebbol",
        'Torize',
        'Kolatill',
        'Charis',
        'Gandle Ott',
        ]
    ]
VAATHKREE_TRADE_CORRIDOR = [
    'Vaathkree Trade Corridor',
    [
        'Corsin',
        'Comkin',
        'Telerath',
        'Kroctar',
        'Levian',
        'Obroa-skai',
        'Paonid',
        'Gravan',
        'Von-Alai',
        'Contruum',
        'Gizer',
        ]
    ]
VERAGI_TRADE_ROUTE = [
    'Veragi Trade Route',
    [
        'Salin',
        'Ciutric',
        'Corvis Minor',
        'Argazda',
        'Bimmiel',
        'Birgis',
        'Seline',
        'Sernpidal',
        'Veragi',
        'Trassitan',
        'Dubrillion',
        'Ahakista',
        'Dantooine',
        'Sinsang',
        'Anx Minor',
        'Ord Trasi',
        ]
    ]
WETYINS_WAY = [
    "Wetyin's Way",
    [
        'Jovan',
        'Vaal',
        'Glade',
        "Wetyin's Colony",
        ]
    ]
WIDEK_BYPASS = [
    'Widek Bypass',
    [
        'Orooturoo',
        'Wehttam',
        'Thobek',
        'Galantos',
        'Widek'
        ]
    ]
YAVIN_BYPASS = [
    'Yavin Bypass',
    [
        'Krylon',
        'Yavin',
        'Vaal',
        ]
    ]

MINOR_TRADE_ROUTES = [
    ACFREN_SPUR,
    AGARIX_TRADE_ROUTE,
    AGRICULTURAL_CIRCUIT,
    ADO_SPINE,
    AMADOR_DREARIA_HYPERLANE,
    ANNAJ_HOUCHE_RUN,
    ANTURI_REACH,
    ARDAN_CROSS,
    ARLEEN_LOOP,
    AUTHORITY_ARC,
    AUTHORITY_GUARDIAN_CORRIDOR,
    AXXILA_TANGRENE_HYPERLANE,
    BAKURA_TRACE,
    BELSAVIS_RUN,
    BOTHAN_RUN,
    BRAXANT_RUN,
    BRENTAAL_DENON_ROUTE,
    BYSS_RUN,
    CADINTH_RUN,
    CADMA_CONDUIT,
    CALIPSA_RUN,
    CALORIA_RUN,
    CARBONITE_RUN,
    CELANON_SPUR,
    CEREAN_REACH,
    COMMENOR_RUN,
    COR_LANE,
    CORSIN_RUN,
    COTH_FUURAS_NESSEM_HYPERLANE,
    COYN_ROUTE,
    DAELGOTH_TRADE_ROUTE,
    DAUNTLESS_RUN,
    DEAD_ROAD,
    DESEVRAN_TRACE,
    DURKTEEL_LOOP,
    DUROS_SPACE_RUN,
    ENARC_RUN,
    ENTRALLA_ROUTE,
    ETTI_ROUTE_MAJOR,
    FALKO_RUN,
    FEENA_RUN,
    FIVE_VEILS_ROUTE,
    GAMOR_RUN,
    GANDEAL_FONDOR_HYPERLANE,
    GELVARNO_LOOP,
    GIBLIM_ROUTE,
    GIJU_RUN,
    GREAT_GRAN_RUN,
    GREAT_KASHYYYK_BRANCH,
    GREATER_CRONESE_ARC,
    HARRIN_TRADE_CORRIDOR,
    HOLLASTIN_RUN,
    HYABB_TWITH_CORRIDOR,
    ILOSIAN_SPUR,
    INDREXU_ROUTE,
    INTRA_SECTOR_SPUR,
    ISON_CORRIDOR,
    JUNCTION_TIERELL_LOOP,
    KAAGA_RUN,
    KASSIDO_BYPASS,
    KESSEL_RUN,
    KESSEL_TRADE_CORRIDOR,
    KIRA_RUN,
    KISMAANO_BYPASS,
    KOROS_TRUNK_LINE,
    KODA_SPUR,
    KORPHIR_TRACE,
    LUCAYA_CROSS,
    LESSOR_CRONESE_ARC,
    LESSOR_LANTILLIAN_ROUTE,
    LEOZI_ROUTE,
    LIPSEC_RUN,
    LISTEHOL_RUN,
    LLANIC_SPICE_RUN,
    LUTRILLIAN_CROSS,
    MANDA_MERCHANT_ROUTE,
    MANDALORIAN_ROAD,
    MENTELLOS_TRADE_ROUTE,
    MURGO_CHOKE,
    MYTOS_ARROW,
    NAMADII_CORRIDOR,
    NANTHRI_ROUTE,
    NIGHTROAD,
    NOTHOIIN_CORRIDOR,
    OKTOS_ROUTE,
    OOTMIAN_PABOL,
    OVERIC_GRIPLINK,
    OVISE_REACH,
    PABOL_HUTTA,
    PABOL_KREETA,
    PABOL_SLEHEYRON,
    PAKUUNI_DRIFT,
    PANDO_SPUR,
    PINOORAN_SPUR,
    PROCOPIAN_SHIPPING_LANE,
    PROUSLYS_RIM_RUN,
    QUELLOR_RUN,
    RAGO_RUN,
    RANDON_RUN,
    REENA_TRADE_ROUTE,
    RELGIM_RUN,
    SALIN_CORRIDOR,
    SANCTUARY_PIPELINE,
    SANRAFSIX_CORRIDOR,
    SENEX_JUVEX_LOOP,
    SENEX_TRACE,
    SHAG_PABOL,
    SHALTIN_TUNNELS,
    SHAPANI_BYPASS,
    SHIPWRIGHTS_TRACE,
    SHIRITOKU_WAY,
    SHWUY_EXCHANGE,
    SISAR_RUN,
    SOLENBARAN_MERCHANT_ROUTE,
    SOLTERIOS_TRADE_ROUTE,
    SPAR_TRADE_ROUTE,
    TALCENE_TRANSIT,
    TERRSKIAR_PASS,
    TERTIARY_SOLENBARAN,
    THREE_ELLAS_RUN,
    TIDAL_CIRCUIT,
    TINGEL_ROUTE,
    TION_TRADE_ROUTE,
    TRAX_TUBE,
    TRELLEN_TRADE_ROUTE,
    TRIANII_SHUNT,
    TRIELLUS_TRADE_ROUTE,
    TRINDELLO_ENDOR_ROUTE,
    TRITON_TRADE_ROUTE,
    VAATHKREE_TRADE_CORRIDOR,
    VERAGI_TRADE_ROUTE,
    WETYINS_WAY,
    WIDEK_BYPASS,
    YAVIN_BYPASS,
    ]

# ==============================================================================
# FUNCTIONS
# ==============================================================================


def translate_coords(instance):
    """Takes a Letter-Numeric map lookup and creates an (x,y) tuple"""
    coords = instance.coords.split('-')
    x = ALPHA[coords[0]] + random.randrange(5000)
    try:
        y = NUMERIC[coords[1]] + random.randrange(5000)
    except:
        coords_sublist = coords[1].split('/')
        y1 = NUMERIC[coords_sublist[0]] + random.randrange(5000)
        y2 = NUMERIC[coords_sublist[1]] + random.randrange(5000)
        y = (y1 + y2)/2
    return (x,y)

def true_center(pos, size):
    """Gets the correct center of an object"""
    center_x = pos[0]-size[0]/2
    center_y = pos[1]-size[1]/2
    return (center_x, center_y)

def true_scale(size, size_mult):
    """Aspect locked size scaling"""
    size_x = size[0] * size_mult
    return (size_x, size_x)

def random_pos():
    """Will return a totally random galactic coordinate"""
    distance = 500
    while distance > 300:
        distance = random.expovariate(.45)*50
    distance += random.expovariate(.6)*30
    angle_deg = random.random()*360
    angle_rad = math.radians(angle_deg)
    x = math.cos(angle_rad) * distance
    y = math.sin(angle_rad) * distance
    return x,y


# ==============================================================================
# GENERAL CLASSES
# ==============================================================================


class TradeRoutes(object):
    """Master Trade Route Controller, inits and contains all Trade Routes"""
    def __init__(self):
    
        self.major_routes = MAJOR_TRADE_ROUTES
        self.major_routes.extend(MINOR_TRADE_ROUTES)
        
        for i in range(len(self.major_routes)):
            
            # Assign a random color
            color = (random.random(), random.random(), random.random(), .5)
            
            # Initiate object and replace simple string with object
            self.major_routes[i] = TradeRoute(
                self.major_routes[i][0],
                self.major_routes[i][1],
                color
                )

    def register_system(self, instance):
        """Passes registration through to all trade routes"""
        for route in self.major_routes:
            route.register_system(instance)

class TradeRoute(object):
    """Singular Trade Route, converts text list to object list"""
    def __init__(self, route_name, route_list, route_color):
        self.name = route_name
        self.route = route_list
        self.color = route_color
        self.activated = False
        self.indicators = []
        self.system_labels = []
        self.route_points = []
        self.built = False
        
        self.register_system()
    
    def register_system(self):
        """Checks calling instance for inclusion in Trade Route"""
        for i in range(len(self.route)):
            self.route[i] = StarSystem.allSystems[self.route[i]]
    
    def draw_route(self, caller):
        """Draws route line, adds widgets and circles"""
        self.activated = True
        
        for instance in self.route:
            try:
                # If system has no other trade routes, add widget to scatter
    #             if not instance.route_membership and not instance.selected:
    #                 caller.add_widget(instance)
        
                # Register route membership with system
                instance.route_membership.append(self.name)
            
                if not self.built:
    
                    # Create the points for the line
                    self.route_points.extend(instance.pos)
    
                    # Create a circle around system
                    systemCircle = Line(
                        circle = (instance.pos[0], instance.pos[1], 100),
                        width = 20
                        )
                    systemLabel = Rectangle(
                        texture = instance.texture,
                        size = instance.texture.size,
                        pos = (
                            instance.pos[0]-(instance.texture.size[0]/2), 
                            instance.pos[1]-400
                            )
                        )
                    self.indicators.append(systemCircle)
                    self.system_labels.append(systemLabel)
            except:
                print self.name, self.route
        
        if not self.built:
            self.line = Line(
                bezier = self.route_points,
                width = len(self.route)
                )
        
        # Add the line to the scatter
        with caller.canvas.before:
            Color(self.color[0],self.color[1],self.color[2],self.color[3])
        caller.canvas.before.add(self.line)
        # Add each circle to scatter
        for circle in self.indicators:
            caller.canvas.before.add(circle)
        with caller.canvas.before:
            Color(1,1,1,1)
        for label in self.system_labels:
            caller.canvas.before.add(label)
        
        self.built = True
    
    def remove_route(self, caller):
        """Removes route line, circles and widgets"""
        self.activated = False
        
        # Remove each circle
        for circle in self.indicators:
            caller.canvas.before.remove(circle)
        # Remove the line
        caller.canvas.before.remove(self.line)
        
        for label in self.system_labels:
            caller.canvas.before.remove(label)
        
        # Remove route membership from each system
        for instance in self.route:
            instance.route_membership.remove(self.name)
            
            # If no more routes remain AND not selected, remove widget
#             if not instance.route_membership and not instance.selected:
#                 caller.remove_widget(instance)

class StarSystem(Label):
    """Basic Star System"""
    
    # Class variable allSystems contains all instances
    allSystems = {}
    starChart = {}
    
    def __init__(self, name, sector, region, coords, **kwargs):
        super(StarSystem, self).__init__(**kwargs)
        
        self.name = name
        self.sector = sector
        self.region = region
        self.coords = coords # These are the 'dumb' coords
        
        # Image representation
        self.star = STARS[random.randrange(len(STARS))]
        
        # For now, if the widget is assigned, name will be visible
        self.text = '[size=240][b]' + self.name + '[/b][/size]'
        self.markup = True
#         self.mipmap = True

        # Actual coordinates
        self.pos = translate_coords(self)
        
        StarSystem.allSystems[self.name] = self # Add to class dictionary
        
#         try:
#             StarSystem.starChartX[(self.pos[0]/10)].append(self)
#         except KeyError:
#             StarSystem.starChartX[(self.pos[0]/10)] = [self]
#         
#         try:
#             StarSystem.starChartY[(self.pos[1]/10)].append(self)
#         except KeyError:
#             StarSystem.starChartY[(self.pos[1]/10)] = [self]
        
        # Not sure what this is accomplishing for now
        self.size_hint_x = 1
        self.size_hint_y = 1
        
        # Routes currently activated
        self.route_membership = []
        
        # Will turn True with manual selection
        self.selected = False


# ==============================================================================
# KIVY GUI CLASSES
# ==============================================================================


class GalSlider(Slider):
    """Slider to control GalScatter"""
    def __init__(self, type, **kwargs):
        super(GalSlider, self).__init__(**kwargs)
        
        self.type = type
        
        if self.orientation == 'vertical':
            if self.type == 'pos':
                self.min = -85000
                self.max = 25000
            else:
                self.min = 0.01
                self.max = 1
        else:
            self.min = -50000
            self.max = 25000
        
        if self.type == 'pos':
            self.value = 0
            self.old_value = 0
            self.bind(
                value_pos = self._drive_scatter_pos
                )
        else:
            self.value = .5
            self.old_value = 1
            self.bind(
                value_pos = self._drive_scatter_scale
                )
    
    def _drive_scatter_pos(self, ignore='', ignore2=''):
        """Updates scatter object with difference between old and new value"""
        difference = (self.value - self.old_value)
        
        if self.orientation == 'vertical':
            self.parent.y = difference*-1
        else:
            self.parent.x = difference*-1
        
        self.old_value = self.value
        self.parent.move_scatter()
    
    def _drive_scatter_scale(self, ignore='', ignore2=''):
#         pow_value = .5 + (math.pow(self.value, 2))
        difference = self.value/self.old_value
        
        scale_matrix = Matrix()
        scale_matrix.scale(difference, difference, 1)
#         anchor = self.parent.scatter.to_local(*self.parent.scatter.center)
#         anchor = (anchor[0] + self.parent.horz_slider.value, anchor[1] + self.parent.vert_slider.value)
        anchor = self.parent.scatter.transform_inv.transform_point(450, 495, 0)
        
        self.parent.scatter.apply_transform(
            scale_matrix,
            post_multiply=True,
            anchor=anchor)
        self.old_value = self.value
    
    def update_maxes(self, instance):
        """This SHOULD update the maxes on the slider if the scale changes"""
        if self.orientation == 'vertical':
            self.min = -170000 * instance.scatter.scale * 1.5
            self.max = 50000 * instance.scatter.scale * 1.5
        else:
            self.min = -100000 * instance.scatter.scale * 1.5
            self.max = 53000 * instance.scatter.scale * 1.5

class GalScatter(ScatterLayout):
    """Main galactic map. Contains GUI representation of all systems"""
    def __init__(self, **kwargs):
        super(GalScatter, self).__init__(**kwargs)
        
        # Turn off all GUI interactions until they work
        self.do_rotation = False
        self.do_translation = False
        
        self.activated_system = {}
        
        self.draw_stars()
        self.scale = 1
        
        with self.canvas.before:
            Color(1,0,0,1)
            Rectangle(
                size = (1000000,100),
                pos = (0,0)
                )
            Rectangle(
                size = (100,1000000),
                pos = (0,0)
                )
            Color(0,1,0,1)
            Rectangle(
                size = (100,1000000),
                pos = (20000,0)
                )
            Rectangle(
                size = (1000000,100),
                pos = (0,20000)
                )
    
    def draw_stars(self):
        """Draws a simple point for every star system"""
        star_points = []
        
        for instance in StarSystem.allSystems:
            star_points.extend(StarSystem.allSystems[instance].pos)
            
        with self.canvas.before:
            Color(1,1,1,1)
            Point(
                points = star_points,
                pointsize = 15
                )
    
    def on_touch_down(self, touch):
        """Should add the touched star system"""
        # push the current coordinate, to be able to restore it later
        touch.push()
        
        print "Pre Local Pos:", touch.pos[0], touch.pos[1],
        print self.to_local(*self.center)
        
        # transform the touch coordinate to local space
        touch.apply_transform_2d(self.to_local)
        
        print "Local Touch Pos:",
        print int(round(touch.pos[0])),
        print int(round(touch.pos[1])),
        print "Slider Value:",
        print int(round(self.parent.parent.horz_slider.value)),
        print int(round(self.parent.parent.vert_slider.value)),
        print "Scale Value:",
        print self.scale
        
        # Offset by Scatter Matrix
        rel_touch_x = int(round(touch.pos[0])) \
            + int(round(self.parent.parent.horz_slider.value))
        rel_touch_y = int(round(touch.pos[1])) \
            + int(round(self.parent.parent.vert_slider.value))
        
        # Get matching systems
        for system in StarSystem.allSystems:
            if system.pos[0] in range(rel_touch_x-100, rel_touch_x+300):
                if system.pos[1] in range(rel_touch_y-100, rel_touch_y+300):
                    if not system.selected:
                        print "Adding", system.name, "at", system.pos
                        self._activate_system(system, (.6,.19,.19,1))
                    else:
                        print "Removing", system.name, "at", system.pos
                        self._deactivate_system(system)
                        
        # whatever the result, don't forget to pop your transformation
        # after the call, so the coordinate will be back in parent space
        touch.pop()
    
    def _activate_system(self, instance, color):
        """Activates the system on the map"""
        if not instance.route_membership:
            self.add_widget(instance)
        instance.selected = True
        with self.canvas.before:
            Color(color[0],color[1],color[2],color[3])
            systemCircle = Line(
                circle = (instance.pos[0], instance.pos[1], 7)
                )
            leftLine = Line(
                points = (
                    instance.pos[0]-6, instance.pos[1],
                    instance.pos[0]-10, instance.pos[1]
                    ),
                width = 1.1
                )
            rightLine = Line(
                points = (
                    instance.pos[0]+6, instance.pos[1],
                    instance.pos[0]+10, instance.pos[1]
                    ),
                width = 1.1
                )
            bottomLine = Line(
                points = (
                    instance.pos[0], instance.pos[1]-6,
                    instance.pos[0], instance.pos[1]-10
                    ),
                width = 1.1
                )
            topLine = Line(
                points = (
                    instance.pos[0], instance.pos[1]+6,
                    instance.pos[0], instance.pos[1]+10
                    ),
                width = 1.1
                )
            Graphics = [systemCircle, leftLine, rightLine, topLine, bottomLine]
            self.activated_system[instance.name] = Graphics
    
    def _deactivate_system(self, instance):
        """Removes system widget and removes canvas instructions"""
        if not instance.route_membership:
            self.remove_widget(instance)
        instance.selected = False
        for object in self.activated_system[instance.name]:
            self.canvas.before.remove(object)
        del self.activated_system[instance.name]

class GalaxyMap(GridLayout):
    """Top GUI control layer"""
    def __init__(self, **kwargs):
        super(GalaxyMap, self).__init__(**kwargs)
        
        # These are for the scatter position
        self.x = 0
        self.y = 0
        
        self.cols = 3
        self.spacing = 10
        
        # Scatter must be restrained within another layout
        self.scatter_box = GridLayout(
            rows = 1,
            size_hint_y = .9,
            size_hint_x = .8
            )
        self.scatter = GalScatter(
            )
        
        self.scale_slider = GalSlider(
            orientation = 'vertical',
            type = 'scale',
            size_hint_x = .1,
            size_hint_y = .9,
            padding = 40
            )
        self.vert_slider = GalSlider(
            orientation = 'vertical',
            type = 'pos',
            size_hint_x = .1,
            size_hint_y = .9,
            padding = 40
            )
        self.horz_slider = GalSlider(
            orientation = 'horizontal',
            type = 'pos',
            size_hint_x = .8,
            size_hint_y = .1,
            padding = 40
            )
        
        # What will this button do? WHO KNOWS!
        self.button = Button(
            size_hint_x = .1,
            size_hint_y = .1,
            on_press = self.remove_Hydian
            )
        
        self.add_widget(self.scale_slider)
        
        self.scatter_box.add_widget(self.scatter)
        self.add_widget(self.scatter_box)
        
        self.add_widget(self.vert_slider)
        
        self.add_widget(Button(
            size_hint_x = .1,
            size_hint_y = .1
            ))
        self.add_widget(self.horz_slider)
        
        self.add_widget(self.button)
        
        # This attempts to update the slider values based on scatter scale
        self.vert_slider.update_maxes(self)
        self.horz_slider.update_maxes(self)
        Clock.schedule_once(self.draw_guide, 30)
        
    def draw_guide(self, ignore=''):
        
        print "Map Size", self.size
        print "Scatter_Box Size", self.scatter_box.size
        
        with self.canvas.after:
            Rectangle(
                size = (2,self.scatter_box.size[1]),
                pos = (self.scatter_box.center[0],0)
                )
            Rectangle(
                size = (self.scatter_box.size[0],2),
                pos = (0,self.scatter_box.center[1])
                )
    
    def move_scatter(self, ignore=''):
        """Translates scatter based on x and y values, driven by sliders"""
        self.scatter.transform.translate(self.x*self.scatter.scale, self.y*self.scatter.scale, 0)
        self.x = 0
        self.y = 0
    
    def remove_Hydian(self, instance):
        for route in TradeRoutes.major_routes:
            if route.activated:
                route.remove_route(self.scatter)
            else:
                route.draw_route(self.scatter)

class GalaxyMapApp(App):
    """Main App, sets icon, name, and window size"""
    # These are high level variables
#     icon = 'tex/diceIcon.png' # Set the App Icon
    title = 'Galaxy Map' # Set the Window Title
    
    def __init__(self, **kwargs):
        super(GalaxyMapApp, self).__init__(**kwargs)
        
        self.ui = GalaxyMap()
        
    
    def on_start(self):
        # This is an undocumented way to set the window size on startup
        # Found at github: https://github.com/kivy/kivy/pull/577
        # Seems the Kivy team gave in over Tito's strong objections.
        # Thank God.
        self._app_window.size = 900, 900
    
    def build(self):
        self.ui.bind(
            size = self._update_rect,
            pos = self._update_rect
            )
            
        # Set Canvas BG Color
        with self.ui.canvas.before:
            Color(0,0,0)
            self.rect = Rectangle(
                size = self.ui.size,
                pos = self.ui.pos
                )
        return self.ui
    
    # Updates Canvas BG size and Pos
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# ==============================================================================
# MAIN
# ==============================================================================

# Init all star systems
for system in SYSTEMS_LIST:
    StarSystem(system[0],system[1],system[2],system[3])

TradeRoutes = TradeRoutes()

GalaxyApp = GalaxyMapApp()

if __name__ == "__main__":
    GalaxyApp.run()