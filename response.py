
from telebot.bot_class import telegram_chatbot
import requests
import csv
import telegram
from telebot.credentials import bot_token, bot_user_name,URL

#insert google sheet url
csv_url="[google sheet url here]"

csv_file=requests.get(url=csv_url)
open("chatbot.csv", "wb").write(csv_file.content)

global bot
global TOKEN
TOKEN = bot_token

def leer_archivo(nombre_archivo):
    rows = []
    with open(nombre_archivo) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        archivo=csv_reader
        for row in archivo:
            rows.append(row)
    return rows

def lista_de_temas():
    temas=[]
    rows = leer_archivo("chatbot.csv")
    for row in rows:
        tema=row[2]
        if tema in temas:
            pass
        else:
            temas.append(tema)
    return temas

def encontrar_preguntas(tema):
    preguntas = []
    rows = leer_archivo("chatbot.csv")
    for row in rows:
            tema_elegido=row[2]
            pregunta=row[0]
            if tema_elegido == tema:
                preguntas.append(pregunta)
    return preguntas

def encontrar_respuesta(pregunta):
    rows = leer_archivo("chatbot.csv")
    for row in rows:
            if pregunta == row[0]:
                respuesta = row[1]
    return respuesta

#Definición de algunas variables que se van a usar después
temas=lista_de_temas()
for tema in temas:
    preguntas=encontrar_preguntas(tema)
    for pregunta in preguntas:
        respuesta=encontrar_respuesta(pregunta)

#Funcion apilar botones
def apilar_opciones(opciones):
    botones = []
    for boton_1, boton_2 in zip(opciones[::2],opciones[1::2]):
        botones_por_linea = [boton_1,boton_2]
        botones.append(botones_por_linea)
    if len(opciones) % 2 != 0:
        botones.append([opciones[-1]])
    return botones

#Función que decide qué responder en función del msj recibido:

def make_reply(message):
    global preguntas
    if message in temas:
        text="¿Te sirve alguna de estas preguntas? Seleccioná una opción de los botones:"
        preguntas=encontrar_preguntas(message)
        print(preguntas)
        opciones=[]
        for pregunta in preguntas:
            opciones.append(pregunta)
        botones=apilar_opciones(opciones)
        keyboard={"keyboard":botones}
        print(keyboard)
        reply_markup=keyboard
        reply=(reply_markup, text)

    elif message in preguntas:
        reply=str(encontrar_respuesta(message))

    else:
        text="¡Hola! En este chat te vamos a ofrecer información sobre salud sexual integral. Para que funcione no tenés que escribir, sino elegir una opción de los botones.¿Sobre qué tema necesitás informarte? Seleccioná una opción:"
        opciones=[]
        for tema in temas:
            opciones.append(tema)
        botones=apilar_opciones(opciones)
        keyboard={"keyboard":botones}
        print(keyboard)
        reply_markup=keyboard
        reply=(reply_markup, text)

    return reply

response_bot=telegram_chatbot(TOKEN)

def get_response(message, chat_id):
    reply=make_reply(message)
    if message in preguntas:
        response_bot.send_message(reply, chat_id)
        reply_final="Si te quedó alguna duda que no hayamos podido contestar acá, podés escribirnos a nuestro instagram @cesac24oficial o a nuestro facebook CeSAC Eva Perón Soldati y unx médicx te va a responder tan pronto como sea posible. Si querés volver al menú de temas del inicio, mandá cualquier mensaje y se reiniciará el chat."
        response_bot.send_message(reply_final, chat_id)
    else:
        response_bot.send_keyboard(reply, chat_id)
