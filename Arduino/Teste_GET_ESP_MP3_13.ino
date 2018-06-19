#include <ESP8266WiFi.h>
#include "Arduino.h"
#include "DFRobotDFPlayerMini.h"

#define SERIAL_BAUD_RATE 9600
#define BUFFER_SISE 100

const char* ssid     = "autofalante";
const char* password = "autofalante";
String url = "/autofalante/esp/comandos/";
String url_command = "/autofalante/esp/comandos/";
String url_playlist = "/autofalante/esp/fila/";
const char* host = "10.42.0.1"; //Server IP
const int httpPort = 8000; //Server port
String response; //String recieved from server
int volume = 6; //Default volume
int wait = 500; //Wait time required by mp3 module to work properly
int busy = 0; //True if MP3 is idle
int playlist[BUFFER_SISE]; //Stores songs queue
int song_count = 0; //Stores number os songs on playlist vetor
int current_song = 0; //Current song index
int pause = 0; //True only if user sends pause command
int read_playlist_ok = 0; //True when URL playlist was read
int end_of_playlist = 0; //Index of the last song on playlist
int read_playlist_again = 0; //True when playlist URL needs to be read again
int song = 0; //Current song value

WiFiClient client;
DFRobotDFPlayerMini myDFPlayer;


void setup() {
  //Set ESP8266 pin_2 as input to read mp3 busy I/O
  pinMode(2, INPUT);
  delay(10);

  //Set baud rate
  Serial.begin(SERIAL_BAUD_RATE);
  delay(10);

  //First, set up MP3
  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

  if (!myDFPlayer.begin(Serial)) {
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    //while(true);
  }
  Serial.println(F("DFPlayer Mini online."));

  myDFPlayer.volume(volume);  //Set volume value. From 0 to 30. Is needed for proper setup
  myDFPlayer.disableLoopAll(); //Plays one mp3 file and stops.
  myDFPlayer.volume(volume);  //Ocasionaly the first volume set fails and needs to be resent
  myDFPlayer.enableDAC();  //Enable On-chip DAC. L, R, G.
  myDFPlayer.outputSetting(true, 15); //Output setting, enable the output and set the gain to 15
  delay(wait);
  myDFPlayer.play(1); //Start to play from first MP3 file
  delay(wait);

  //Second, connectto WiFi network
  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  delay(wait);
}


void loop() {
  //Use WiFiClient class to create TCP connections
  if (!client.connect(host, httpPort)) {
    return;
  }
  //Send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }

  //Read all the responses of the reply from server
  while (client.available()) {
    response = client.readStringUntil('$'); //Character "$" acts as a divider
    response = response.substring(0, response.indexOf("</ul>")); //Cleans the response

    if (response != "xxxx" && response.length() <= 4) { //True if acommand was recieved

      if (url == url_command) { //Commands URL

        switch (response.toInt()) { //Commands cases

          case 9992: //Read queue and append to current
            if (song_count == 0) { //Set next url to read playlist if buffer ins empty
              url = url_playlist;
            }
            else { //Asks to read playlist URL when buffer is empty
              Serial.println("bota em 1");
              read_playlist_again = 1;
            }
            delay(wait);
            break;

          case 9993: //Dump queue and read new 
            url = url_playlist; //Set next url to read playlist
            read_playlist_again = 0; //Dump current playlist
            read_playlist_ok = 0;
            playlist[0] = song;
            end_of_playlist = 1;
            current_song = 0;
            song_count = 0;
            delay(wait);
            break;

          case 9994: //Start the mp3 from the pause
            myDFPlayer.start();
            pause = 0;
            delay(wait);
            break;

          case 9995: //Pause the mp3
            myDFPlayer.pause();
            pause = 1;
            delay(wait);
            break;

          case 9996: //Volume Down
            volume = volume - 3;
            myDFPlayer.volume(volume);
            delay(wait);
            break;

          case 9997: //Volume Up
            volume = volume + 3;
            myDFPlayer.volume(volume);
            delay(wait);
            break;

          case 9998: //Play previous mp3
            if (song_count == 0) { //Queue empty
              myDFPlayer.previous(); //Plays direct previous song
              delay(wait);
            }
            else {
              myDFPlayer.play(playlist[current_song - 1]); //Plays previuos song on queue
              current_song --;
              song_count ++;
            }
            break;

          case 9999: //Play next mp3
            if (song_count == 0) { //Queue empty
              myDFPlayer.next(); //Plays direct next song
              delay(wait);
            }
            else {
              myDFPlayer.play(playlist[current_song +1]); //Plays next song on queue
              current_song ++;
              song_count --;
            }
            break;

          default: //Case "response" is a song
            song = response.toInt();
            myDFPlayer.play(song); //Play MP3 given by "response"
            delay(wait);
            break;
        } //End switch
      } //End if url_command

      else { //Playlist URL
        playlist[end_of_playlist] = response.toInt(); //Add songs to queue
        read_playlist_ok = 1;
        end_of_playlist ++;
        song_count ++;
        if (song_count == BUFFER_SISE) { //Read playlist URL when buffer is empty
          Serial.println("bota em 1");
          read_playlist_again = 1;
        }
      }
    } //End if command recieved

    else if (response == "xxxx" && digitalRead(2) == 1 && pause == 0) { //No command, nothing is beeing played and not on pause
      if (song_count == 0) { //Queue empty
        myDFPlayer.next(); //Plays direct next song
        delay(wait);
      }
      else {
        myDFPlayer.play(playlist[current_song +1]); //Plays next song on queue
        current_song ++;
        song_count --;
      }
    }
  }//End while
  if (url == url_playlist && read_playlist_ok == 1) {
    url = url_command; //Set next url to read commands
    read_playlist_ok = 0;
  }
  if (url == url_playlist && read_playlist_ok == 0) { //Necesseray for playlists whith one song
    read_playlist_ok = 1;
  }
  if (read_playlist_again == 1 && song_count == 0) { //Set URL to playlist when buffer is empty and playlist URL needs to be read again
    read_playlist_again = 0; //Dump current playlist
    read_playlist_ok = 0;
    end_of_playlist = 1;
    current_song = 0;
    song_count = 0;
    url = url_playlist;
  }
}//End loop
