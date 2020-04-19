from datetime import datetime

def updateOrcreateCardInList(card,cardListid,data,listData,cardData):
    n = 0   # Numero de lista
    flagEncontrado=False
    flagUpdate=False
    flagReordenar=False
    campos = []

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
        listData.extend(data['list'])
        cardData.append(None)

def moveCardInList(data,listData, cardData):
    card2move = None
    cardDataBefore = []
    flagEncontradoOld=False
    flagcreateCardInNew=False
    #"listBefore":{"id":"5e7e4e3e1b2ffc59c21438a3","name":"Done"},"listAfter":{"id":

    n = 0
    for list in listData:
        if list['id'] == data['listBefore']['id']:
            for cardItem in cardData[n]: #localizar la card
                if cardItem['id'] == data['card']['id']:
                    card2move = cardItem
                else:
                    cardDataBefore.append(cardItem)
            flagEncontradoOld=True
            cardData[n] = cardDataBefore
        n += 1

    if flagEncontradoOld:
        n = 0
        flagcreateCardInNew=True
        for list in listData:
            if list['id'] == data['listAfter']['id']:
                if cardData[n] == None:
                    cardData[n] = [card2move]
                else:
                    cardData[n].extend([card2move])
                flagcreateCardInNew=False
            n += 1

    if flagcreateCardInNew:
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

def convertDate(d):
    if d.endswith('Z'):
        d = d[:-1] + '+00:00'
    return datetime.fromisoformat(d)