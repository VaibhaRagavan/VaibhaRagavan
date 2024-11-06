import json
import requests 


def process_meaning(content):
    definition = []
    for i in content:
        for k, v in i.items():
            if k == "definitions":
                for j in v:
                    for a, b in j.items():
                        if a == "definition":
                            definition.append(b)

    return definition


def process_phonetics(content1):
    audio = []
    for a in content1:
        for k1, v1 in a.items():
            if k1 == "audio":
                audio.append(v1)
    res_audio = "\n".join(audio)
    return res_audio


def api_call(res_word):
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + res_word
    response = requests.get(url).content.decode("utf-8")
    response_obj = json.loads(response)
    return response_obj


def text_processor(string):
    word_v = string[0]["word"]
    phonetic_v = string[0]["phonetic"]
    phonetics_v = process_phonetics(string[0]["phonetics"])
    meanings_v = process_meaning(string[0]["meanings"])
    text = {
        "word": word_v,
        "phonetic": phonetic_v,
        "phonetics": phonetics_v,
        "meanings": meanings_v,
    }
    return text
