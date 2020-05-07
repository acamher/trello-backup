import json
import util
import sys
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", help="in mode Actions, process changes in JSON file until the 'date'")
parser.add_argument("-i", "--input", help="JSON file input", default="trello.json")
parser.add_argument("-o", "--output", help="HTML file input", default="trello-backup.html")
parser.add_argument("--dir", help="Directory in batch mode", default=".")
parser.add_argument("-m", "--movedCards", help="Check cards moved in 'date'", action="store_true")
parser.add_argument("-l", "--list", help="List Name to check cards moved")

args = parser.parse_args()

flagDate=False
#if len(sys.argv)>1:
if args.date is not None:
    flagDate=True
    print("Modo filtrado Actions")

with open(args.input, encoding='UTF-8') as json_file:
    trello_json = json.load(json_file)

# Fase 1: ver cuantas listas hay

listData = []
cardData = []
checklistsList = []
boardName = trello_json['name']

actionsReconocidas = ["addMemberToCard", #NO
                      "updateCard",  #Sí; sólo actualizar el campo que aparece en old
                      "createCard",   #Sí; si el tablero se copió de otro, pueden no venir los createList correspondientes
                      "deleteCard", #Sí
                      "moveCardFromBoard", #Sí
                      "moveCardToBoard", #Sí
                      "commentCard", #NO
                      "removeMemberFromCard", #NO
                      "updateCheckItemStateOnCard", #Sí
                      "removeChecklistFromCard", #NO
                      "addChecklistToCard", #Sí
                      "updateChecklist", #Pte ------------------
                      "addMemberToBoard", #NO
                      "updateBoard", #NO
                      "addToOrganizationBoard",#NO
                      "copyBoard", #NO
                      "createList", #Sí
                      "updateList", #Sí; data.list.closed=true es borrado y no hay que imprimirla
                      "enablePlugin", #NO
                      "copyCard", #Pte -----------------------------------------
                      "updateCustomFieldItem"  #NO
                      "createCustomField"] #NO

for action in trello_json['actions']:
    tipo = action['type']
    if action['type'] not in actionsReconocidas:
        print("Action no reconocida: " + action['type'])

if  flagDate:
    #Replay de los actions , sólo hasta la fecha seleccionada
    d_argument=datetime.strftime(datetime.strptime(args.date,"%d%m%Y"),"%Y%m%d")
    for action in reversed(trello_json['actions']):
        d_action=datetime.strftime(util.convertDate(action['date']),"%Y%m%d")
        if d_action<=d_argument:
            if action['type']=="createCard" or action['type']=="updateCard":
                if 'listBefore' in action['data']:
                    util.moveCardInList(action['data'],listData,cardData)
                else:
                    util.updateOrcreateCardInList(action['data']['card'],action['data']['list']['id'],action['data'],listData,cardData)
            elif action['type']=="createList" or action['type']=="updateList":
                util.updateOrcreateList(action['data'],listData,cardData)
            elif action['type']=="addChecklistToCard":
                util.createCheckListInCard(action['data']['card']['id'],action['data']['checklist']['id'],trello_json['checklists'],cardData,checklistsList)
            elif action['type']=="removeChecklistFromCard":
                pass
            elif action['type']=="updateCheckItemStateOnCard":
                util.updateCheckItemState(action['data']['checklist']['id'],action['data']['checkItem'],checklistsList)
            elif action['type']=="moveCardFromBoard":
                util.deleteCard(action['data']['card'],action['data']['list']['id'],listData,cardData)
            elif action['type']=="deleteCard":
                util.deleteCard(action['data']['card'],action['data']['list']['id'],listData,cardData)
            elif action['type']=="moveCardToBoard":
                util.updateOrcreateCardInList(action['data']['card'],action['data']['list']['id'],action['data'],listData,cardData)
            elif action['type']=="copyCard":
                util.updateOrcreateCardInList(action['data']['card'],action['data']['list']['id'],action['data'],listData,cardData)
            else:
                pass


    for listCards in cardData:
        #util.reshortList(listCards)
        listCards.sort(key=lambda card:card['pos'])
else:
    for list in trello_json['lists']:
        listData.extend([list])     # Guarda toda la info de la lista
        cardData.append(None)

    #test
    #cardData = [None] * len(listData)

    print("Hay " + str(len(listData)) + " listas")
    print("------------")

    # Fase 2: conseguir hacer un array de tarjetas

    for card in trello_json['cards']:
        util.updateOrcreateCardInList(card,card['idList'],[],listData,cardData)


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

    checklistsList = trello_json['checklists']

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
                        for checklist in checklistsList:
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
f = open(args.output,"w")		# Si no hay archivo lo crea y sino lo reescribe

# Paso 2: cabecera html
html_inicio = "<HTML><HEAD><title>Trello Backup</title></HEAD><BODY>"
html_final = "</BODY></HTML>"

# Paso 3: creamos cuerpo de pagina
html_medio = "<h1>Tablero: " + str(boardName) + "</h1>"
for lista in listData:
    if "closed" not in lista or lista['closed']!=True:
        html_medio += "<div style=\"border-style:solid;border-width:medium;background-color: coral;margin:10px;\"><h2>Lista: " + str(lista['name']) + "</h2>"
        if cardData[listData.index(lista)] is not None:
            for card in cardData[listData.index(lista)]:
                if card is not None and ("closed" not in card or card['closed']!=True):
                    desc=""
                    if "desc" in card:
                        desc=card['desc']
                    html_medio += "<div style=\"background-color:white;margin:10px;\"><h3>" + str(card['name']) + "</h3><p>Descripcion:</p><div style=\"background-color:#99ff99;margin:5px;\">" + desc.replace('\n','<br>') + "</div>"
                    # str(card['idChecklists'])
                    if "idChecklists" in card and len(card['idChecklists']) > 0:
                        idChecklist = str(card['idChecklists'])[2:len(card['idChecklists']) -3]     # Ojo cuidao con la respuesta, que incluye corchetes dentro del string. Además hay que separarlo, puede tener varios checklist.
                        if len(idChecklist) > 3:
                            # print(str(card['idChecklists']).split("'"))       # Prueba que permite ver como devuelve el str
                            for checklist in checklistsList:
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
