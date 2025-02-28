#!/usr/bin/env python
# -- encoding: UTF-8 --

import qi
import sys
import httplib
import json
import time

def main():
    session = qi.Session()
    session.connect("tcp://192.168.0.101:9559")

    animated_speech_service = session.service("ALAnimatedSpeech")

    while True:
        try:
            text_to_say = None
            while text_to_say is None:
                conn = httplib.HTTPConnection("192.168.0.115", 9559)
                try:
                    conn.request('GET', '/send-to-pepper') 
                    response = conn.getresponse()
                    response_data = response.read().decode('utf-8')
                    #response_data = response.read()

                    if response.status == 200:
                        response_json = json.loads(response_data)
                        text_to_say = response_json.get('response', None)

                        if text_to_say:
                            print(text_to_say)
                            animated_speech_service.say(text_to_say)
      
                            notify_server()
                            time.sleep(4)
                        else:
                            print("No hay respuesta disponible, esperando...")

                    else:
                        print("Error en la respuesta del servidor, código de estado:", response.status)

                except Exception as e:
                    print("Error en la conexión o procesamiento de la respuesta:", e)
                finally:
                    conn.close()

                time.sleep(5)
        
        except Exception as e:
            print("Error en el bucle principal:", e)

def notify_server():
    try:
        conn = httplib.HTTPConnection("192.168.0.115", 9559)
        conn.request('POST', '/pepper-done')  # Ruta para notificar que Pepper ha terminado de hablar
        response = conn.getresponse()
        response_data = response.read()

        if response.status == 200:
            print("Notificación enviada al servidor.")
        else:
            print("Error en la notificación al servidor, código de estado:", response.status)

    except Exception as e:
        print("Error de conexión en notify_server:", e)

    finally:
        conn.close()

if __name__ == "__main__":
    main()
