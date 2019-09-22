/* 
 * Prof. Michele Maffucci 
 * 01.05.2017 
 * accensione/spegnimento LED da pagina web 
 * per maggiori informazioni: 
 * https://www.arduino.cc/en/Reference/WiFi 
 * https://github.com/esp8266 

wemos D1 R2 & mini
cose da aggiungere

reset via pin (collegare una uscita digitale al reset
\\ip statico
pagina per chiamata periodica, resetta se non arriva nulla

14apr18 | reset hw
        | wdog https://techtutorialsx.com/2017/01/21/esp8266-watchdog-functions/
        | https://github.com/esp8266/Arduino/blob/4897e0006b5b0123a2fa31f67b14a3fff65ce561/doc/faq/a02-my-esp-crashes.md

per gestire rst collego D0 a RST con il circuito sotto

3v3 ---\/\/------D0---|<-----RST

--|<--- diodo



 */  
  
#include <WiFiUdp.h>  
#include <ESP8266WiFi.h>  
#include <ESP8266mDNS.h>  


#define TEMPO_CHIUSURA   30000
#define TEMPO_HEARTBEAT  120000
#define TEMPO_LAMP       500
  
// La connessione di WeMos D1 mini al un network WiFi viene  
// realizzata usando un personal encryption WEP e WPA2  
// Per poter sapere a quale rete connettersi bisogna  
// effettuare un broadcast dell'SSID (nome del network)   
  
// definizione di due array di caratteri  
// in cui memorizzare nome della rete WiFi e password  
  
const char ssid[] = "";       // inserire l'ssid della rete  
const char pass[] = "";   // password della rete  

// the IP address for the shield:
IPAddress ip      (192,168,1,200);   
IPAddress gateway (192,168,1,254);   
IPAddress subnet  (255,255,255,0);   

// Creazione di un server web in ascolto sulla porta 80  
// attende contenuti (pagine html, immagini, css, ecc...)  
WiFiServer server(80);  
  
//    int pinLed = LED_BUILTIN;//D4;    // LED connesso tra pin D4 e ground  
int pinLed   = LED_BUILTIN;//D4;    // LED connesso tra pin D4 e ground  
int pinRele0 = D1; 
int pinRrst  = D0; 

char chiudi;
long lastTime, tempoChiusura, lampTime;


 
void setup() {  
    Serial.begin(115200);           // inizializzazione Serial Monitor  
    delay(10);  
    
    Serial.println("\nC:\\Users\\giorgio.rancilio\\Dropbox\\MakersPgo\\iot\\wemos\\webServer");
    Serial.println("09apr18");
    
    pinMode(  pinLed, OUTPUT);    
    pinMode(pinRele0, OUTPUT);    
    pinMode(pinRrst, OUTPUT);    

    
    digitalWrite(pinRrst,  HIGH);     // rst alto  
    digitalWrite(pinLed,   LOW);      // LED inizialmente spento  
    digitalWrite(pinRele0, LOW);      // LED inizialmente spento  
    
    // Connessione alla rete WiFi  
    
    Serial.println();  
    Serial.println();  
    Serial.println("------------- Avvio connessione ------------");  
    Serial.print("Tentativo di connessione alla rete: ");  
    Serial.println(ssid);  
    
    /*  
    *  Viene impostata l'impostazione station (differente da AP o AP_STA) 
    * La modalità STA consente all'ESP8266 di connettersi a una rete Wi-Fi 
    * (ad esempio quella creata dal router wireless), mentre la modalità AP  
    * consente di creare una propria rete e di collegarsi 
    * ad altri dispositivi (ad esempio il telefono). 
    */  
    
    WiFi.mode(WIFI_STA);  
    
    /*  
    *  Inizializza le impostazioni di rete della libreria WiFi e fornisce lo stato corrente della rete, 
    *  nel caso in esempio ha come parametri ha il nome della rete e la password. 
    *  Restituisce come valori: 
    *   
    *  WL_CONNECTED quando connesso al network 
    *  WL_IDLE_STATUS quando non connesso al network, ma il dispositivo è alimentato 
    */  
    WiFi.config(ip, gateway, subnet);
    
    WiFi.begin(ssid, pass);  
    
    /*  
    *  fino a quando lo non si è connessi alla WiFi 
    *  compariranno a distanza di 250 ms dei puntini che 
    *  evidenziano lo stato di avanzamento della connessione 
    */    
    while (WiFi.status() != WL_CONNECTED) {  
        delay(250);  
        Serial.print(".");  
    }  
    
    // se connesso alla WiFi stampa sulla serial monitor  
    // nome della rete e stato di connessione  
    Serial.println("");  
    Serial.print  ("Sei connesso ora alla rete: ");  
    Serial.println(ssid);  
    Serial.println("WiFi connessa");  
    
    // Avvia il server  
    server.begin();  
    Serial.println("Server avviato");  
    
    // Stampa l'indirizzo IP  
    Serial.print("Usa questo URL : ");  
    Serial.print("http://");  
    Serial.print(WiFi.localIP()); // Restituisce i'IP della scheda  
    Serial.println("/");  

    ESP.wdtDisable();
    lastTime = millis();
}  
  
void loop() {  

    
    if ((millis() - lastTime) > TEMPO_HEARTBEAT){
        // timeOut
        Serial.println("heartBeta non arrivato, arrivederci!!");  
        delay(1000);
        digitalWrite(pinRrst,  LOW);     // rst alto  
    }

    if ((millis() - lampTime) > TEMPO_LAMP){
        lampTime = millis();
        // blink
        digitalWrite(pinLed,  !digitalRead(pinLed));    
        ESP.wdtFeed(); // https://techtutorialsx.com/2017/01/21/esp8266-watchdog-functions/
    }



    switch (chiudi){

      case 0:
            break;

      case 1:
            if ((millis() - tempoChiusura) > TEMPO_CHIUSURA){
                chiudi = 2;
                Serial.println("rele aperto");  
            }
            rele(HIGH);
            break;
      case 2:
            rele(LOW);
            chiudi = 0;
            break;
    }




    // Verifca se il client e' connesso  
    WiFiClient client = server.available();  
    if (!client) {  
        return;  
    }  
    
    // Aspetta fino a quando il client invia dei dati  
    Serial.println("Nuovo client");  
    while (!client.available()) {  
        delay(1);  
    }  
    
    // Legge la prima richiesta  
      
    /*  
     *  readStringUntil() legge i caratteri dal buffer seriale 
     * all'interno di una stringa fino a quando non riceve il 
     * carattere di terminazione in questo cas \r 
     * oppure si verivica un time out 
     */  
       
    String request = client.readStringUntil('\r');  
    Serial.println(request);  
    client.flush();                               // flush() elimina il buffer una volta che  
                                                  // tutti i caratteri in uscita sono stati inviati.  
    
    // Verifica quale richiesta e' stata fatta  
    
    /* 
     * Individua un carattere o una stringa all'interno di un'altra stringa (nell'esempio la strina è request). 
     * Per impostazione predefinita, ricerche dall'inizio della stringa, 
     * ma è possibile effettuare la ricerca partendo da un dato indice, 
     * permettendo di individuare tutte le istanze del carattere o della stringa. 
     * Se il valore restituito è -1 allora la stringa non è stata trovata. 
     */  
    
    int valore = LOW;  
    if (request.indexOf("/LED=ON") != -1) {  
        valore = HIGH;  
        rele(valore);
    }  
    if (request.indexOf("/LED=OFF") != -1) {  
        valore = LOW;  
        rele(valore);
    }  
    if (request.indexOf("/heartBeat") != -1) {  
        lastTime = millis();
        Serial.println("cmd heartBeat");
        
    }  
    if (request.indexOf("/chiudi") != -1) {  
        lastTime = millis();
        Serial.println("cmd chiudi");
        chiudi = 1;
        tempoChiusura = millis();
    }  
    
    // Restituisce la risposta  
      
    /* 
     * La pagina web dovrà essere formattata con la sua intestazione html 
     * e variando il messaggio che identifica lo stato del LED  
     */  
       
  // intestazione pagina html  
  client.println("HTTP/1.1 200 OK");  
  client.println("Content-Type: text/html");  
  client.println(""); //  non dimenticare questa linea  
  client.println("<!DOCTYPE HTML>");  
  client.println("<html>");  
  
  // titolo della pagina  
  client.println("<h2>Intefaccia di controllo LED mediante WeMos D1 Mini</h2>");  
  
  // includiamo tutto il testo in un div in cui il font è impostato a 20 px  
  // N.B. ricorda che per poter considerare le " come stringa e' necessario farle precedere da uno \  
  client.print("<div style=\"font-size: 20px;\">");  
  client.print("Il LED e': ");  
  
  if (valore == HIGH) {  
    // stampa ON di colore verde  
    client.print("<strong style=\"color:green;\">ON</strong>");  
  } else {  
    // stampa OFF di colore rosso  
    client.print("<strong style=\"color:red;\">OFF</strong>");  
  }  
  // stampa una riga separatrice  
  client.println("<hr>");  
  // lista puntata  
  client.println("<ul>");  
  client.println("<li>Fai click <a href=\"/LED=ON\">QUI</a> per portare ad ON il LED sul pin D4</li>");  
  client.println("<li>Fai click <a href=\"/LED=OFF\">QUI</a> per portare ad OFF il LED sul pin D4</li>");  
  client.println("</ul>");  
  client.print("</div>");  
  client.println("</html>");  
  
// chiusura connessione  
  delay(1);  
  Serial.println("Client disconnesso");  
  Serial.println("");  
}  

void rele(char stato){
    digitalWrite(pinRele0, stato);  
}

