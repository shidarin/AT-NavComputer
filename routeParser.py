import pickle

SYSTEMS_LIST = pickle.load(open('/Users/sean/Desktop/StarWarsPython/AT-NC/StarSystems/StarSystems.pk',
    'rb'
    ))
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

rawroute = "Juvex"

for i in range(10):
    rawroute = rawroute.replace('[' + str(i) + ']', '')
    rawlist = rawroute.split(' - ')

not_found = []

for text_system in rawlist:
    found = False
    for list_system in SYSTEMS_LIST:
        if list_system[0] == text_system:
            found = True
    if found == False:
        not_found.append(text_system)


if not_found:
    for entry in not_found:
        print entry
else:
    print "\n\n["
    for entry in rawlist:
        if "'" in entry:
            print "        " + '"' + entry +'",'
        else:
            print "        " + "'" + entry +"',"
    print "        ]"
    print "    ]"