'''
fileName: getTrainDelay

------------------------------------------------------------------------------
05ott19   modificata cercaRitardo(). ora richiesta ritardo treno attuale o a una particolare stazione


Grazie a:
https://medium.com/@albigiu/trenitalia-shock-non-crederete-mai-a-queste-api-painful-14433096502c
https://github.com/bluviolin/TrainMonitor/wiki/API-del-sistema-Viaggiatreno


23005 - VARESE|23005-S01205
        TREVIGLIO    S01708 

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
#def setLed(quale, colore):
def setLed(arrayRitardo):

    
    stringa = "http://192.168.1.166/;"
    blu     = "1;0;123"
    rosso   = "123;0;0"
    verde   = "2;123;0"
    giallo  = "60;60;0"
    spento  = "0;0;0"
    terminatore = ";"

    colore = ["", "", ""]
    
    colore[0] = verde
    colore[1] = giallo
    colore[2] = rosso
    
    led = [0,0,0,0]
    
    for r in range(0, 3):
        ritardo = arrayRitardo[r]
        if ritardo <= 4:
            led[r]  = 0
        elif ritardo <= 8:
            led[r]  = 1
        else:
            led[r]  = 2

    ledMI   = colore[led[3]]
    ledMI2  = colore[led[2]]
    ledVA2  = colore[led[1]]
    ledVA   = colore[led[0]]
    
    stringa = stringa + ledVA + ";" + ledVA2 + ";" + ledMI2 + ";" + ledMI + terminatore
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



# se stazione non data (99) ritorna dato dell'ultima  stazione raggiunta
# else della richiesta
# se non ancora ragginta da ritardo 777
def cercaRitardo(direzione = "VA", trainId = "23008", stazioneRichiesta = 99):
    startStation = "S01708"
      #8:03
    #trainId      = "23010"  #8:33
#    url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01708/23008"
#    request = urlopen(url)

    if direzione == "VA":
        url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01708/"+ trainId
    else:
        url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01205/"+ trainId


    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    if response.getcode() != 200:
        # 204 No Content
        print(response.getcode())
        return("--", 999)

    else:
        # 200

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

        # verifico se il treno è soppresso
        if (tipoTreno == "ST"):
            ritardo = 999
            stazione = "Parabiago"
            ritardoPartenza = 999
            ritardoArrivo = 999
        else:
            if stazioneRichiesta == 99:
                # legge tutte le fermate
                # dove ritardo 
                for fer in fermate:
                    #print(fer["arrivoReale"])
                    if fer["arrivoReale"] != None:
                        ritardo         = fer["ritardo"]
                        ritardoArrivo   = fer["ritardoArrivo"]
                        #ritardoPartenza = fer["ritardoPartenza"] # sempre a zero
                        stazione        = fer["stazione"]
            else:
                if fermate[stazioneRichiesta] != None:
                    ritardo         = fermate[stazioneRichiesta] ["ritardo"]
                    ritardoArrivo   = fermate[stazioneRichiesta] ["ritardoArrivo"]
                    #ritardoPartenza = fer["ritardoPartenza"] # sempre a zero
                    stazione        = fermate[stazioneRichiesta] ["stazione"]
                        
        '''
        for fer in fermate:
            print("%s: %d" % (fer["stazione"], fer["ritardo"])) 
                    ritardoPartenza = fermate[20]["ritardoPartenza"]
                    stazione= fermate[20]["stazione"]
        '''
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


    if True:
#        treni = ["23004", "23006", "23008", "23010"] 
        treni = ["23006", "23008"] 
#        treni = ["23034", "23036", "23040"] 
#        treni = ["23034", "23036", "23040"]
        '''
        for treno in treni:
            [s, r] = cercaRitardo("VA", treno, 20)
            print ("%6s arrivo a %25s con %3d minuti di ritardo" % (treno, s, r))
            [s, r] = cercaRitardo(treno)
            print ("%6s arrivo a %25s con %3d minuti di ritardo" % (treno, s, r))
        '''
        [s, rVA1] = cercaRitardo("VA", "23006", 20)
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % ("23006", s, rVA1))
        [s, rVA2] = cercaRitardo("VA", "23008", 20)
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % ("23008", s, rVA2))

        [s, rMI1] = cercaRitardo("MI", "23015",  9) # 7:57
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % ("23015", s, rMI1))
        [s, rMI2] = cercaRitardo("MI", "23017",  9) # 8:27
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % ("23017", s, rMI2))

        setLed([rVA1, rVA1, rMI1, rMI2])

    if False:
        [s, r] = cercaRitardo(treno)
        print ("%6s arrivo a %25s con %3d minuti di ritardo" % (treno, s, r))

