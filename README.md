# ritardoTreno

la mattina il tempo per prendere il treno va gestito oculatamente. Prendere il telefono, avviare l'APP e verificare il ritardo non funziona per me.
Voglio avere un quadretto dove dei led mi dicono se e di quanto il treno è in ritardo. Gli do un'occhiata e so se ho qualche minuto in più.
Nel mio caso visualizzo due trani per Milano e due per Varese

Un programma python interroga l'API di Trenitalia. Questo gira su un Raspberry che gestisce alcune funzione casalinghe. La visulazzazione è a carico di un ESP8266 che lavora come server Http facendo quello che il Raspberry gli dice.


# ESP server

 avvia un server su indirizzo fisso
 chiama con http://192.168.1.166/...
 
 argomenti:
 valori rgb dei quattro led
 
 

# Riferimenti
https://github.com/bluviolin/TrainMonitor/wiki/API-del-sistema-Viaggiatreno

https://github.com/sabas/trenitalia

