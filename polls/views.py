from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import requests

def index(request):
    r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes')
    bb = []
    bcs = []
    actual = 0
    actual2 = 0
    for elem in r.json():
        if elem["series"] == "Breaking Bad":
            if elem["season"] != actual:
                bb.append(elem["season"])
            actual = elem["season"]
        else:
            if elem["season"] != actual2:
                bcs.append(elem["season"])
            actual2 = elem["season"]
    return render(request, 'polls/index.html', {'bb': bb, 'bcs':bcs})

def episodios(request, serie, num_temporada):
    if serie == "BreakingBad":
        r1 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad')
    else:
        r1 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul')     

    lista_de_episodios = []
    for elem in r1.json(): 
        if elem["season"] == str(num_temporada):
            lista_de_episodios.append([elem["title"], elem["episode_id"]])
    return render(request, 'polls/episodios.html', {"lista_de_episodios": lista_de_episodios, "serie": serie, "num_temporada": num_temporada})


def detalles_episodio(request, episode_id):
    r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes/'+str(episode_id))
    try:
        title = r.json()[0]["title"]
        season = r.json()[0]["season"]
        characters = r.json()[0]["characters"]
        episode = r.json()[0]["episode"]
        air_date = r.json()[0]["air_date"]
        series = r.json()[0]["series"]
        
        return render(request, 'polls/detalles_episodio.html', {"title": title, "season": season, "episode": episode, "air_date": air_date, "series":series, "episode_id": episode_id, "characters": characters})
    except IndexError:
        return HttpResponse("Este episodio no existe")

def personajes(request, personaje):
    try: 
        r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+str(personaje))
        id_p = r.json()[0]["char_id"]
        occupation = r.json()[0]["occupation"]
        img = r.json()[0]["img"]
        status = r.json()[0]["status"]
        nickname = r.json()[0]["nickname"]
        appearance = r.json()[0]["appearance"]
        better_call_saul_appearance = r.json()[0]["better_call_saul_appearance"]
        portrayed = r.json()[0]["portrayed"]
        category = r.json()[0]["category"]
        r2 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/quote?author='+str(personaje))
        quotes = [] 
        
        for elem in r2.json():
            quotes.append([elem["quote_id"],elem["quote"]])
            
        return render(request, 'polls/personaje.html', {"id": id_p, "occupation": occupation, "img": img, "status": status, "nickname":nickname, "appearance": appearance, "better_call_saul_appearance": better_call_saul_appearance, "portrayed": portrayed, "category": category, "name": personaje, "quotes": quotes})
    except IndexError:
        return HttpResponse("Este personaje no existe")

def personajes2(request):
    searchWord = request.POST.get('search','')
    print(searchWord)
    offset = 0
    dict_personajes = {}
    contador = 0
    lista_de_personajes = []
    while True:
        r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+str(searchWord)+'&limit=10&offset='+str(offset))
        if len(r.json()) == 10:
            offset += 10
            dict_personajes[contador] = r.json()
            contador += 1
        else:
            dict_personajes[contador] = r.json()
            break
    
    for personajes in dict_personajes.values():
        for perso in personajes:
            for nombre in perso:
                if nombre == "name":
                    lista_de_personajes.append(perso["name"])
                
    return render(request, 'polls/personajes.html', {'lista': lista_de_personajes})
