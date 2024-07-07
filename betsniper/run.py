import threading
from datetime import datetime
from flask import jsonify
import requests, re

from betsniper.fonbet.scanner import main as fonbet_scanner
from betsniper.olimp.scanner import main as olimp_scanner

from betsniper_web.app import app
from betsniper_web.app.views import UpdateEvents

from difflib import SequenceMatcher

import time

sports = ["tennis"]
first_appearance_times = {}

fonbet_events = []
olimp_events = []


def get_fonbet():
    global fonbet_events
    fonbet_events = fonbet_scanner(sports)


def get_olimp():
    global olimp_events
    olimp_events = olimp_scanner(sports)


# получение всех событий из олимпа и фонбета
def get_all_events():
    fonbet_thread = threading.Thread(target=get_fonbet, args=())
    olimp_thread = threading.Thread(target=get_olimp, args=())

    fonbet_thread.start()
    olimp_thread.start()

    fonbet_thread.join()
    olimp_thread.join()


types = {
    "ТБ": ["ТМ"],
    "ТМ": ["ТБ"],
    "П1": ["П2"],
    "П2": ["П1"],
    "Ф2": ["Ф1"],
    "Ф1": ["Ф2"]
}


# функция для извлечения числа из строчки
def extract_value(value):
    match = re.search(r"[-+]?\d*\.\d+|\d+", value)
    if match:
        return float(match.group())
    return 0


# функция для нахождения противоположных ставок в 2 букмекерах
def find_opposite_bets(array1, array2):
    opposite_bets = []
    for bet1 in array1:
        split_bet1 = bet1.split()
        if len(split_bet1) > 1:
            type1, value1 = split_bet1[0], extract_value(split_bet1[1])
        else:
            type1, value1 = split_bet1[0], 0

        for bet2 in array2:
            split_bet2 = bet2.split()
            if len(split_bet2) > 1:
                type2, value2 = split_bet2[0], extract_value(split_bet2[1])
            else:
                type2, value2 = split_bet2[0], 0

            if types.get(type1) == [type2] and abs(value1) == abs(value2) and value1 * value2 < 0:
                if split_bet2[2:] == split_bet1[2:]:
                    opposite_bets.append([bet1, bet2])

            elif types.get(type1) == [type2] and split_bet1[1:] == split_bet2[1:]:
                opposite_bets.append([bet1, bet2])

    return opposite_bets


def main():
    while True:

        current_keys = set()
        events = []
        get_all_events()

        for event_fonbet in fonbet_events:

            current_event_olimp = ''
            flag = True

            for event_olimp in olimp_events:

                similarity = SequenceMatcher(None, event_fonbet, event_olimp).ratio()

                # проверяем чтобы названия события совпадали более чем на 70%
                if similarity > 0.70:
                    # print(event_olimp, similarity)
                    flag = False
                    current_event_olimp = event_olimp
                    break

            if flag:
                continue

            count_bets_fonbet = len(fonbet_events[event_fonbet]['bets'])
            count_bets_olimp = len(olimp_events[current_event_olimp]['bets'])

            if count_bets_olimp != 0 and count_bets_fonbet != 0:

                olimp_bets = olimp_events[current_event_olimp]["bets"]
                fonbet_bets = fonbet_events[event_fonbet]["bets"]
                opposite_bets = find_opposite_bets(fonbet_bets.keys(), olimp_bets.keys())

                for fork in opposite_bets:

                    kf1 = fonbet_bets[fork[0]]
                    kf2 = float(olimp_bets[fork[1]])
                    # print("kf: ",kf1, kf2)
                    # 100 * (СТАВКА1 / (1 + СТАВКА1 / ПРОТИВОПОЛОЖНАЯСТАВКА1) - 1)
                    pr1 = (100 * (kf1 / (1 + kf1 / kf2) - 1))

                    if -1000 < pr1 < 1000:
                        print(pr1, kf1, kf2, event_fonbet, fork[0], fork[1])
                        print(fonbet_events[event_fonbet]["url"])
                        print(olimp_events[current_event_olimp]["url"])
                        print('------------------------------')
                        key = "".join([event_fonbet, str(kf1), str(kf2)])

                        current_keys.add(key)

                        if key not in first_appearance_times:
                            first_appearance_times[key] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                        events.append({
                            'site1': "Fonbet",
                            'type1': fork[0],
                            'link1': fonbet_events[event_fonbet]["url"],
                            'coefficient1': kf1,
                            'matchName1': event_fonbet,
                            'site2': "Olimp",
                            'type2': fork[1],
                            'link2': olimp_events[current_event_olimp]["url"],
                            'coefficient2': kf2,
                            'matchName2': current_event_olimp,
                            'profit': round(pr1, 2),
                            'time': first_appearance_times[key],
                            "sport": "tennis"
                        })

        # если в текущей итерации вилка не повторилась, убираем ее первое появление из словаря
        keys_to_remove = set(first_appearance_times.keys()) - current_keys
        for key in keys_to_remove:
            del first_appearance_times[key]

        # отправляем полученные вилки
        response = requests.post(url="https://87.251.86.97:911/getEvents", json=events, verify=False)
