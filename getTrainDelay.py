'''
fileName: getTrainDelay

Grazie a:
https://medium.com/@albigiu/trenitalia-shock-non-crederete-mai-a-queste-api-painful-14433096502c
https://github.com/bluviolin/TrainMonitor/wiki/API-del-sistema-Viaggiatreno



keys
stazione parabiago
id s01035
riardo in minuti


    tipoTreno vale 'PG' e provvedimento vale 0: treno regolare
    tipoTreno vale 'ST' e provvedimento vale 1: treno soppresso (in questo caso l'array fermate ha lunghezza 0)
    tipoTreno vale 'PP' oppure 'SI' oppure 'SF' e provvedimento vale 0 oppure 2: treno parzialmente soppresso (in questo caso uno o più elementi dell'array fermate hanno il campo actualFermataType uguale a 3)
    tipoTreno vale 'DV' e provvedimento vale 3: treno deviato (da approfondire)

    il campo ritardo alla fermata x indica il ritardo che ha avuto il treno, non il ritardo previsto.
    alla fermata x ritardo è sempre a zero sinchè non arriva il treno. non esiste un orario di arrivo previsto.
    
    se arrivoReale !=  null
       ritardoArrivo vale
    
    per conoscere il ritardo:
        leggo per tutte le fermate partenzaReale
           arrivoReale != da zero
           so dove è il treno e tengo questo ritardo come indicatore
    

'''

#from urllib.request import urlopen
import urllib.request
import random
import json

import http.client


'''
server su indirizzo fisso. Chiama con http://192.168.1.166/;2;0;123;123;x

argomenti:
2:           numero di led da accendere (1-4)
0;123;123:   RGB del colore led
x:           ? senza si impalla tutto
'''
def setLed(ritardo):
    stringa = "http://192.168.1.166/;"
    rosso   = "123;0;0"
    verde   = "0;123;0"
    giallo  = "60;60;0"
    terminatore = ";x"

    if ritardo <= 4:
        nLed    = 2
        colore  = verde
    elif ritardo <= 8:
        nLed    = 2
        colore  = giallo
    else:
        nLed    = 2
        colore  = rosso

    
    
    stringa = stringa + str(nLed) + ";" + colore + terminatore
    print(stringa)
    '''
    connection = http.client.HTTPSConnection(stringa)
    connection.request("GET", "/")
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))

    connection.close()
    '''
    req= urllib.request.Request(stringa)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        print(the_page)




def cercaRitardo(trainId = "23008"):
    startStation = "S01708"
      #8:03
    #trainId      = "23010"  #8:33
#    url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01708/23008"
    url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01708/"+ trainId
#    request = urlopen(url)

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    #print (response.read().decode('utf-8'))

    r = response.read().decode('utf-8')

    #print (r)
    
    data = json.loads(r)

    tipoTreno = data["tipoTreno"]
    fermate = data["fermate"]
    '''
    il campo ritardo alla fermata x indica il ritardo che ha avuto il treno, non il ritardo previsto.
    alla fermata x ritardo è sempre a zero sinchè non arriva il treno. non esiste un orario di arrivo previsto.
    
    se arrivoReale !=  null
       ritardoArrivo vale
    
    per conoscere il ritardo:
        leggo per tutte le fermate partenzaReale
           arrivoReale != da zero
           so dove è il treno e tengo questo ritardo come indicatore
    '''

    


    if (tipoTreno == "ST"):
        ritardo = 999
        stazione = "Parabiago"
        ritardoPartenza = 999
        ritardoArrivo = 999
    else:
        # legge tutte le fermate
        # dove ritardo 
        for fer in fermate:
            #print(fer["arrivoReale"])
            if fer["arrivoReale"] != None:
                ritardo         = fer["ritardo"]
                ritardoArrivo   = fer["ritardoArrivo"]
                #ritardoPartenza = fer["ritardoPartenza"] # sempre a zero
                stazione        = fer["stazione"]

    '''
    print (stazione)
    print ("    %s" % (trainId))
    print ("    ritardo       : %d" %(ritardo))
    print ("    ritardoArrivo : %d" %(ritardoArrivo))
    '''
    return(stazione, ritardo)

    
if __name__ == "__main__":
    #treno      = "23008"  #8:03
    #treno      = "23010"  #8:33
    treno      = "23006"  #8:33
    #treni = ["23004", "23006", "23008", "23010"] 
    '''
    treni = ["23034", "23036", "23040"] 
    for treno in treni:
        [s, r] = cercaRitardo(treno)
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % (treno, s, r))
    #print (conversion)
    '''
    [s, r] = cercaRitardo(treno)
    print ("%6s arrivo a %25s con %3d minuti di ritardo" % (treno, s, r))
    setLed(r)


