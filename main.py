# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import xml.etree.ElementTree as ET
import requests
from Levenshtein._levenshtein import distance
import cyrtranslit


ROOT = None
SWE_RU_FILE = 'swe-ru.json'
SWE_RU_DICT = {}


def download_dict(url, overwrite=False):
    global ROOT
    global SWE_RU_DICT

    if not overwrite:
        with open(SWE_RU_FILE, 'r') as fr:
            for line in fr.readlines():
                if not line: continue
                SWE_RU_DICT = json.loads(line)
                return

    r = requests.get(url)
    res = r.text
    ROOT = ET.fromstring(res)
    for word in ROOT:
        value = word.get('Value')
        for lang in word:
            if lang.tag == 'TargetLang':
                for tran in lang:
                    if tran.tag == 'Translation':
                        SWE_RU_DICT[value] = word.find('TargetLang').find('Translation').text or ''

    with open(SWE_RU_FILE, 'w') as fw:
        fw.write(json.dumps(SWE_RU_DICT))


def compare(a_dict):
    similar_words = []
    for k, v in a_dict.items():
        dist = distance(translate_ru(v), translate_swe(k))
        if dist < 3 and len(k) >= 3:
            similar_words.append((dist, k, v))
    return similar_words


def translate_ru(word_ru):
    return cyrtranslit.to_latin(word_ru, 'ru')


def translate_swe(work_swe):
    return work_swe.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')


if __name__ == '__main__':
    download_dict('http://liljeholmen.sprakochfolkminnen.se/sprakresurser/lexin/ryska/swe_rus.xml')
    print(len(SWE_RU_DICT))
    similar = compare(SWE_RU_DICT)
    print(len(similar))
    with open('result', 'w') as f:
        for w in similar:
            f.write(f'{w[1]} {w[2]}; Distance={w[0]}\n')
