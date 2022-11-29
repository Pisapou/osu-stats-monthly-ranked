"""
Made by Pisapou, "It is trash, but it works."

Program that use osu!'s apiv1 AND apiv2 to generate stats about maps ranked the last month.
Some functions are not used because they seem useless, feel free to look anyway.
"""

import requests
import copy
import time


API_URL = 'https://osu.ppy.sh/api'
API_URL_V2 = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

"""
IGNORE THIS - INTERN FUNCTION

API V1
"""
    
def main(date):
    k = 'a long string'   # ADD YOU PERSONNAL KEY (osu!api v1)
    since = date
    m = 0

    response = requests.get(f'{API_URL}/get_beatmaps?k={k}&since={since}&m={m}')
    
    liste = []
    while response.json() != []:
        for dico in response.json():
            new_id = dico["beatmapset_id"]
            statut = dico["approved"]
            if statut == "1":
                liste.append({"id":new_id, "favourite_count": int(dico["favourite_count"]), "playcount": int(dico["playcount"]), "genre_id": dico["genre_id"], "language_id": dico["language_id"], "creator": dico["creator"], "difficultyrating": float(dico["difficultyrating"]), "total_length": int(dico["total_length"])})
        since = response.json()[-1]["approved_date"]
        response = requests.get(f'{API_URL}/get_beatmaps?k={k}&since={since}&m={m}')
    return liste

def key_in_list(new_id, liste):
    for dico in liste:
        if dico["id"] == new_id:
            return False
    return True

def get_indice(set_id, l):
    for i in range(0,len(l)):
        if l[i]["id"] == set_id:
            return i

def combine_set(ld):
    ls = []
    for dico in ld:
        if key_in_list(dico["id"], ls):
            ls.append({"id":dico["id"], "favourite_count": int(dico["favourite_count"]), "playcount": int(dico["playcount"]), "genre_id": dico["genre_id"], "language_id": dico["language_id"], "creator": dico["creator"]})
        else:
            ls[get_indice(dico["id"], ls)]["playcount"] += int(dico["playcount"])
    return ls

date = '2022-11-01'           # CHANGE HERE TO THE START OF THE ACTUAL MONTH

ld = main(date)               # LIST OF ALL DIFFS
ld_copy = copy.deepcopy(ld)
ls = combine_set(ld_copy)     # LIST OF ALL SETS

"""
IGNORE THIS - INTERN FUNCTION

API V2
"""

def get_token():
    data = {
        'client_id': 0,                   # ADD YOU PERSONNAL CLIENT ID (osu!api v2)
        'client_secret': 'a long string', # ADD YOU PERSONNAL CLIENT SECRET (osu!api v2)
        'grant_type': 'client_credentials',
        'scope': 'public'
    }

    response = requests.post(TOKEN_URL, data=data)

    return response.json().get('access_token')

def nb_ranked(user_id):
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        'mode': 'osu',
    }

    response = requests.get(f'{API_URL_V2}/users/{user_id}', params=params, headers=headers)
    
    number_ranked = response.json().get('ranked_beatmapset_count')
    
    return number_ranked



"""
USE FUNCTIONS BELOW
"""

def nb(l):
    """
    Number of ranked Set/Diff (ls/ld)
    """
    cpt=0
    for dico in l:
        cpt+=1
    return cpt

def favorite(l):
    """
    Set (ls) with the most favorites
    """
    maxi = 0
    beatmapset = None
    for dico in l:
        if int(dico["favourite_count"]) > maxi:
            beatmapset = dico
            maxi = int(dico["favourite_count"])
    return beatmapset

def play(l):
    """
    Set/Diff (ls/ld) with most plays
    """
    maxi = 0
    beatmapset = None
    for dico in l:
        if int(dico["playcount"]) > maxi:
            beatmapset = dico
            maxi = int(dico["playcount"])
    return beatmapset

def star_rating(l):
    """
    Bigger SR (USE LD)
    """
    maxi = 0
    beatmapset = None
    for dico in l:
        if int(dico["difficultyrating"]) > maxi:
            beatmapset = dico
            maxi = int(dico["difficultyrating"])
    return beatmapset

def length(l):
    """
    Longer set (USE LD)
    """
    maxi = 0
    beatmapset = None
    for dico in l:
        if int(dico["total_length"]) > maxi:
            beatmapset = dico
            maxi = int(dico["total_length"])
    return beatmapset

def nb_diff(l):
    """
    Most difficulties (USE LD)
    """
    deja = {}
    for dico in l:
        if dico["id"] in deja:
            deja[dico["id"]] += 1
        else:
            deja[dico["id"]] = 1
    maxi = 0
    beatmapset_id = None
    for key in deja:
        if deja[key] > maxi:
            maxi = deja[key]
            beatmapset_id = key
    return beatmapset_id, maxi

def ratio(l):
    """
    Set with best ratio play/fav (use ls)
    
    Comment: Don't seems interesting stats (basicelly the most recent maps have the best ratio)
    """
    maxi = 0
    beatmapset = None
    for dico in l:
        ratio = int(dico["favourite_count"])/int(dico["playcount"])
        if ratio > maxi:
            beatmapset = dico
            maxi = ratio
    return beatmapset

def genre(l):
    """
    Most genre ranked (USE LS)
    
    0=any, 1=unspecified, 2=video game, 3=anime, 4=rock, 5=pop, 6=other, 7=novelty, 9=hip hop, 10=electronic, 11=metal, 12=classical, 13=folk, 14=jazz
    
    Comment: who care ?
    """
    cpt = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,}
    for dico in l:
        cpt[dico["genre_id"]] += 1
    maxi = 0
    genre = None
    for key in cpt:
        if cpt[key] > maxi:
            maxi = cpt[key]
            genre = key
    return genre, cpt[genre]

def language(l):
    """
    Most language ranked (USE LS)
    
    0=any, 1=unspecified, 2=english, 3=japanese, 4=chinese, 5=instrumental, 6=korean, 7=french, 8=german, 9=swedish, 10=spanish, 11=italian, 12=russian, 13=polish, 14=other
    
    Comment: who care ?
    """
    cpt = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,}
    for dico in l:
        cpt[dico["language_id"]] += 1
    maxi = 0
    language = None
    for key in cpt:
        if cpt[key] > maxi:
            maxi = cpt[key]
            language = key
    return language, cpt[language]


def new_mappers(l):
    """
    Number of new ranked mappers (USE LS)
    """
    res = []
    for dico in l:
        mapper = dico["creator"]
        if nb_ranked(mapper) == 1:
            res.append(mapper)
            print("Y", mapper)
        else:
            print("N", mapper)
        time.sleep(1)
    return res



def all_stats(ls,ld):
    """
    Basicelly using all the function in one (USE LS AND LD)
    (except new_mappers function due to time duration (~2min) / number of requests (1 request per mapper))
    """
    temp = nb(ld)
    print(f'total diffs : {temp}')
    temp = nb(ls)
    print(f'total sets : {temp}')
    temp = favorite(ls)
    print(f'favorite : {temp["id"]} ({temp["favourite_count"]} favs)')
    temp = play(ls)
    print(f'plays (set) : {temp["id"]} ({temp["playcount"]} plays)')
    temp = play(ld)
    print(f'play(diff) : {temp["id"]} ({temp["playcount"]} plays)')
    temp = star_rating(ld)
    print(f'hardest : {temp["id"]} ({temp["difficultyrating"]} stars)')
    temp = length(ld)
    print(f'longest : {temp["id"]} ({temp["total_length"]} secondes)')
    temp = nb_diff(ld)
    print(f'nb_diff : {temp[0]} ({temp[1]} diffs)')
    temp = language(ld)
    print(f'language : {temp[0]} ({temp[1]})')
    temp = genre(ld)
    print(f'genre : {temp[0]} ({temp[1]})')
    
    
all_stats(ls,ld)
