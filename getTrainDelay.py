'''
fileName: getTrainDelay.py

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


'''

#from urllib.request import urlopen
import urllib.request
import random
import json



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

    if (tipoTreno == "ST"):
        ritardo = 999
        stazione = "Parabiago"
    else:
        ritardo = fermate[20]["ritardo"]
        stazione= fermate[20]["stazione"]
    '''
    for fer in fermate:
        print("%s: %d" % (fer["stazione"], fer["ritardo"])) 
    '''
    print (stazione)
    print (ritardo)

    return(ritardo)
    

print ("arrivo a Parabiago con %d minuti di ritardo" % (cercaRitardo()))
#print (conversion)

