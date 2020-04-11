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
                print("     Descripcion: " + card['desc'])
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


# Proceso de exportación a archivo
# Paso 1: abrir el archivo
f = open("trello-backup.html","w")		# Si no hay archivo lo crea y sino lo reescribe

# Paso 2: cabecera html
html_inicio = "<HTML><HEAD><title>Trello Backup</title></HEAD><BODY>"
html_final = "</BODY></HTML>"

# Paso 3: creamos cuerpo de pagina
html_medio = "<h1>Tablero: " + str(boardName) + "</h1>"
for lista in listData:
    html_medio += "<div style=\"border-style:solid;border-width:medium;background-color: coral;margin:10px;\"><h2>Lista: " + str(lista['name']) + "</h2><p>Tarjetas: </p>"
    if cardData[listData.index(lista)] is not None:
        for card in cardData[listData.index(lista)]:
            if card is not None:
                html_medio += "<div style=\"background-color:white;margin:10px;\"><h3>" + str(card['name']) + "</h3><p>Descripcion:</p><div style=\"background-color:#99ff99;margin:5px;\">" + card['desc'] + "</div>"
                # str(card['idChecklists'])
                idChecklist = str(card['idChecklists'])[2:len(card['idChecklists']) -3]     # Ojo cuidao con la respuesta, que incluye corchetes dentro del string. Además hay que separarlo, puede tener varios checklist.
                if len(idChecklist) > 3:
                    # print(str(card['idChecklists']).split("'"))       # Prueba que permite ver como devuelve el str
                    for checklist in trello_json['checklists']:
                        if checklist['idCard'] == card['id']:
                            html_medio += "<p>Checklist: " + checklist['name'] + "<br>"
                            for checkItems in checklist['checkItems']:
                                if checkItems['state'] == "complete":
                                    html_medio += "<input type=\"checkbox\" checked> <label>" + str(checkItems['name']) + "</label><br>"
                                else:
                                    html_medio += "<input type=\"checkbox\"> <label>" + str(checkItems['name']) + "</label><br>"
                            html_medio += "</p>"
                html_medio += "</div>"
    html_medio += "</div>"

f.write("" + html_inicio + html_medio + html_final)
f.close()
