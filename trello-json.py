import json

with open('trello.json', encoding='UTF-8') as json_file:
    trello_json = json.load(json_file)

# person_dict = json.loads(person)

# Fase 1: ver cuantas listas hay

listData = []
boardName = trello_json['name']

for list in trello_json['lists']:
    listData.extend([list])     # Guarda toda la info de la lista

cardData = [None] * len(listData)

print("Hay " + str(len(listData)) + " listas")
print("------------")

# Fase 2: conseguir hacer un array de tarjetas

for card in trello_json['cards']:
    n = 0   # Numero de lista
    for list in listData:
        if list['id'] == card['idList']:
            if cardData[n] == None:
                cardData[n] = [card]
            else:
                cardData[n].extend([card])
        n += 1

# Imprime las tarjetas de forma resumida
print("Tarjetas en cada lista:")
for list in cardData:
    temp = []
    if list is not None:
        for card in list:
             temp.extend([card['name']])
    print("     " +str(temp))

# Las descripciones de cada tarjeta se guardan en el propio archivo "card" del array
print("------------")

# Voy a realizar una simulacion para ver las checklist
print("Lista de Checkist que hay:")
for checklist in trello_json['checklists']:
    card_name = None
    for group_cards in cardData:
        if group_cards is not None:
            for card in group_cards:
                if checklist['idCard'] == card['id']:
                    card_name = str(card['name'])
    print("Checklist de nombre " + str(checklist['name']) + " perteneciente a la tarjeta: " + card_name)
    print("Tareas:")
    for checkItems in checklist['checkItems']:
        if checkItems['state'] == "complete":
            print("    [Complete] " + str(checkItems['name']))
        else:
            print("    [Incomplete] " + str(checkItems['name']))
    print("")

print("------------")
print("")
print("")
print("")
print("Exportado de información:")

print("Nombre del tablero: " + str(boardName))
print("Hay " + str(len(listData)) + " listas")

for lista in listData:
    print("Lista: " + str(lista['name']))
    print("Tarjetas:")
    if cardData[listData.index(lista)] is not None:
        for card in cardData[listData.index(lista)]:
            if card is not None:
                print("   " + str(card['name']))
                print("     Descripcion: " + str(card['desc']))
                str(card['idChecklists'])
                idChecklist = str(card['idChecklists'])[2:len(card['idChecklists']) -3]     # Ojo cuidao con la respuesta, que incluye corchetes dentro del string. Además hay que separarlo, puede tener varios checklist.
                if len(idChecklist) > 3:
                    # print(str(card['idChecklists']).split("'"))       # Prueba que permite ver como devuelve el str
                    for checklist in trello_json['checklists']:
                        if checklist['idCard'] == card['id']:
                            print("     Checklist: " + checklist['name'])
                            for checkItems in checklist['checkItems']:
                                if checkItems['state'] == "complete":
                                    print("       [Complete] " + str(checkItems['name']))
                                else:
                                    print("       [Incomplete] " + str(checkItems['name']))
                            print("")


    print("")
