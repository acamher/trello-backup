from datetime import datetime

def updateOrcreateCardInList(card,cardListid,data,listData,cardData):
    n = 0   # Numero de lista
    flagEncontrado=False
    flagUpdate=False
    flagReordenar=False
    campos = []
    if ( not "name" in data['list']):
        # vendría de un moveCardFromBoard -> no hacemos nada porque también se hace un CreateCard de la misma card
        pass
    else:
        if "idChecklists" not in card: card["idChecklists"]=[]
        if "desc" not in card: card["desc"]=""

        if "old" in data:
            for campo in data['old']:
                flagUpdate=True
                campos.append(campo)
        for list in listData:
            if list['id'] == cardListid:
                if flagUpdate: #updateCard
                    for cardItem in cardData[n]: #localizar la card
                        if cardItem['id'] == card['id']:
                            for campo in campos: #actualizamos todos los campos updates
                                cardItem[campo]=card[campo]
                                if campo == "pos":
                                        flagReordenar=True
                else: #createCard
                    if cardData[n] == None:
                        card["pos"] = 65535
                        cardData[n] = [card]
                    else:
                        ultima_pos = 0
                        if len(cardData[n]) > 0:
                            ultima_pos = cardData[n][-1]['pos']
                        card['pos'] = ultima_pos + 65535 + 1
                        cardData[n].extend([card])
                flagEncontrado=True
            n += 1
        if not flagEncontrado:
            if "list" in data:
                listData.append(data['list'])
                cardData.append(None)
                card["pos"] = 65535
                cardData[n] = [card]
            else:
                pass
    return flagReordenar

def updateOrcreateList(data,listData,cardData):
    n = 0   # Numero de lista
    flagEncontrado=False
    flagUpdate=False
    campos = []
    if "old" in data:
        for campo in data['old']:
            flagUpdate=True
            campos.append(campo)
    for list in listData:
        if list['id'] == data['list']['id']:
            if flagUpdate: #updateList
                for campo in campos: #actualizamos todos los campos updates
                    list[campo]=data['list'][campo]
            else: #createList de una List que ya existe
                list = data['list']
            flagEncontrado=True
        n += 1
    if not flagEncontrado: #createList
        listData.append(data['list'])
        cardData.append(None)
        cardData[n] = []

def moveCardInList(data,listData, cardData):
    card2move = None
    cardDataBefore = []
    flagEncontradoOld=False
    flagcreateCardInNewList=False
    #"listBefore":{"id":"5e7e4e3e1b2ffc59c21438a3","name":"Done"},"listAfter":{"id":

  #Se quita de la lista original
    n = 0
    for list in listData:
        if list['id'] == data['listBefore']['id']:
            for cardItem in cardData[n]: #localizar la card
                if cardItem['id'] == data['card']['id']:
                    card2move = cardItem
                    flagEncontradoOld=True
                else:
                    cardDataBefore.extend([cardItem])
            cardData[n] = cardDataBefore
        n += 1

    if not flagEncontradoOld:
        #la card es nueva
        card2move = data['card']
        card2move["pos"] = 65535
    #Se mete en la lista destino
    n = 0
    flagcreateCardInNewList=True
    for list in listData:
        if list['id'] == data['listAfter']['id']:
            if cardData[n] == None:
                cardData[n] = [card2move]
            else:
                if len(cardData[n]) > 0:
                    ultima_pos = cardData[n][-1]['pos']
                    card2move['pos'] = ultima_pos + 65535 + 1
                cardData[n].extend([card2move])
            flagcreateCardInNewList=False
        n += 1

    # Si no se encuentra es que la la lista destino es nueva
    if flagcreateCardInNewList:
        if "listAfter" in data:
            listData.append(data['listAfter'])
            cardData.append(None)
            cardData[n] = [card2move]
        else:
            pass

def createCheckListInCard(cardId,checklistId,repoCheckLists,cardData,checklistsList):

    for cardDataItem in cardData:
        for cardItem in cardDataItem:
            if cardItem['id'] == cardId:
                if 'idChecklists' in cardItem:
                    cardItem['idChecklists'].append(checklistId)
                else:
                    cardItem['idChecklists']=[checklistId]

                for repocheckList in repoCheckLists:
                    if repocheckList['id'] == checklistId:
                        for item in repocheckList['checkItems']:
                            item['state'] = 'incomplete'
                        checklistsList.append(repocheckList)

                # checklist['idCard'] = cardId
                # checklist['pos'] = 16384 * len(cardItem['idChecklists'])
                # checklist['checkItems'] = []
                # checklistsList.append(checklist)

def updateCheckItemState(checklistId,checkitem,checklistsList):
    for checklist in checklistsList:
        if checklist['id'] == checklistId:
            for item in checklist['checkItems']:
                if item['id'] == checkitem['id']:
                        item['state'] = checkitem['state']

def deleteCard(card,cardListid,listData,cardData):
    n = 0   # Numero de lista
    for list in listData:
        if list['id'] == cardListid:
            element = 0 # numero de card en la lista
            for cardItem in cardData[n]: #localizar la card
                if cardItem['id'] == card['id']:
                    del cardData[n][element]
                element = element +1
        n += 1

def addcommentCard(cardId, cardListid, text, listData, cardData):
    n = 0   # Numero de lista
    for list in listData:
        if list['id'] == cardListid:
            element = 0 # numero de card en la lista
            for cardItem in cardData[n]: #localizar la card
                if cardItem['id'] == cardId:
                    if "comments" not in cardData[n][element]:
                        cardData[n][element]['comments']=[text]
                    else:
                        cardData[n][element]['comments'].insert(0,text)
                element = element +1
        n += 1

def convertDate(d):
    if d.endswith('Z'):
        d = d[:-1] + '+00:00'
    return datetime.fromisoformat(d)