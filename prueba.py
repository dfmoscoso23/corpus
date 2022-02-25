def ultimasilaba(palabra):
    medidorsilaba=-1
    vocalcerrada=False
    vocalabierta=False
    for pos,letra in enumerate(palabra[::-1]):
        if letra in ["a","e","i","o","u","y","á","é","í","ó","ú"]:
            medidorsilaba -= pos
            break
    if palabra[medidorsilaba] in ["a","e","o","á","é","ó"]:
        vocalabierta=True
    elif palabra[medidorsilaba] in ["i","u","í","ú","y"]:
        vocalcerrada=True
    if len(palabra)+medidorsilaba>0:
        if (palabra[medidorsilaba-1] in ["a","e","o","á","é","ó","í","ú"]) and vocalabierta:
            pass
            #print(palabra[medidorsilaba:])
            #return palabra[medidorsilaba:]
        elif palabra[medidorsilaba-1] in ["a","e","o","á","é","ó","í","ú","i","u","y"]:
            medidorsilaba-=1
            if palabra[medidorsilaba-1] not in ["l","r","a","e","o","á","é","ó","í","ú","i","u","y"]:
                medidorsilaba-=1
            elif palabra[medidorsilaba-1] in ["l","r"]:
                medidorsilaba-=2
            else:
                if (palabra[medidorsilaba] in ["e","i","é","í"]) and (palabra[medidorsilaba-1] == "u") and (palabra[medidorsilaba-2] in ["g","q"]):
                    medidorsilaba-=2
                    #print(palabra[medidorsilaba:])
                else:
                    medidorsilaba-=1
                    if palabra[medidorsilaba-1] not in ["l","r","a","e","o","á","é","ó","í","ú","i","u","y"]:
                        medidorsilaba-=1
                    elif palabra[medidorsilaba-1] in ["l","r"]:
                        medidorsilaba-=2
                    else:
                        print(palabra)
    #             if (palabra[medidorsilaba] in ["e","i","é","í"]) and (palabra[medidorsilaba-1] == "u") and (palabra[medidorsilaba-2] in ["g","q"]):
    #                 medidorsilaba-=2
    #                 #print(palabra[medidorsilaba:])
    #             else:
    #                 print(palabra[medidorsilaba:])
    #                 medidorsilaba-=1
    #                 if palabra[medidorsilaba-1] in ["a","e","o","á","é","ó","í","ú","i","u","y"]:
    #                     pass
    #                     #print(palabra[medidorsilaba:])
    #                 elif palabra[medidorsilaba] not in ["l","r"]:
    #                     pass
    #                     #print(palabra[medidorsilaba:])
    #                 else:
    #                     medidorsilaba-=1
    #                     #print(palabra[medidorsilaba:])
        else:
            medidorsilaba-=1
            if len(palabra)+medidorsilaba>0:
                if palabra[medidorsilaba-1] in ["a","e","o","á","é","ó","í","ú","i","u","y"]:
                    pass
                    #print(palabra[medidorsilaba:])
                elif palabra[medidorsilaba] not in ["l","r"]:
                    pass
                    #print(palabra[medidorsilaba:])
                else:
                    medidorsilaba-=1
                    #print(palabra[medidorsilaba:])
    return palabra[medidorsilaba:]

def silabasplitter(palabra,palabradividida = ["a"]):
    ultimasil = ultimasilaba(palabra)
    if ultimasil == palabra:
        palabradividida.append(ultimasilaba(palabra))
    else:
        palabradividida.append(ultimasilaba(palabra))
        silabasplitter(palabra.rsplit(ultimasilaba(palabra))[0],palabradividida)
    return palabradividida[::-1]

tokens=["extinguió","del","madero","difícil","dificiles","taladro","árbol", "extinguir",'comida',"increible","existió","existía","extinguían","guía","guiar","hidrai","buey"]
for token in tokens:
    print(token,silabasplitter(token))
    silabasplitter()