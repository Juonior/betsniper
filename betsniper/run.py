from datetime import datetime

from betsniper.fonbet.scanner import main as fonbet_scanner
from betsniper.olimp.scanner import main as olimp_scanner

from betsniper_web.app import app
from betsniper_web.app.views import UpdateEvents

from difflib import SequenceMatcher

import time
sports = ["basketball"]
first_appearance_times = {}
# if __name__ == "__main__":
def main():
    while True:
        events = []
        s = fonbet_scanner(requested_sports = sports)
        g = olimp_scanner(requested_sports = sports)
        for event in s:
            check = False
            eventg = ''
            for event2 in g:
                similarity = SequenceMatcher(None, event, event2).ratio()
                if similarity > 0.70:
                    # print(event2, similarity)
                    eventg = event2
                    check = True
            if check == False:
                continue
            if len(s[event]["bets"]) != 0 and len(g[eventg]["bets"]) != 0:
                print(event)
                # print(s[event]["bets"])
                # print(list(s[event]["bets"].keys())[0])
                # print(g[eventg]["bets"])
                k2 = ''
                for k1 in list(s[event]["bets"].keys()):
                    if 'ТБ' in k1:
                        k2 = k1.replace('Б', 'М')
                    if 'ТМ' in k1:
                        k2 = k1.replace('М', 'Б')
                    if 'П1' in k1:
                        k2 = k1.replace('1', '2')
                    if 'П2' in k1:
                        k2 = k1.replace('2', '1')
                    if 'Ф1 (+' in k1:
                        k2 = k1.replace('+', '-')
                    if 'Ф2 (+' in k1:
                        k2 = k1.replace('+', '-')
                    if 'Ф1 (-' in k1:
                        k2 = k1.replace('-', '+')
                    if 'Ф2 (-' in k1:
                        k2 = k1.replace('-', '+')
                    if k2 in list(g[eventg]["bets"].keys()):
                        # print(k1, k2)
                        kf1 = float(s[event]["bets"][k1])
                        kf2 = float(g[eventg]["bets"][k2])
                        # print("kf: ",kf1, kf2)
                        # 100 * (СТАВКА1 / (1 + СТАВКА1 / ПРОТИВОПОЛОЖНАЯСТАВКА1) - 1)
                        pr1 = (100 * (kf1 / (1 + kf1/kf2) - 1))
                        pr2 = 0
                        kf3 = 0
                        kf4 = 0
                        if k2 in s[event]["bets"] and k1 in g[eventg]["bets"]:
                            kf3 = float(s[event]["bets"][k2])
                            kf4 = float(g[eventg]["bets"][k1])
                            # print("kf: ", kf3, kf4)
                            pr2 = (100 * (kf3 / (1 + kf3 / kf4) - 1))
                        if -1000 < pr1 < 1000:
                            print(pr1, kf1, kf2, event, k1, k2, )
                            print(s[event]["url"].replace('tennis', 'basketball'))
                            print(g[eventg]["url"])
                            print('------------------------------')
                            if not "".join([event, str(kf1), str(kf2)]) in first_appearance_times:
                                first_appearance_times["".join([event, str(kf1), str(kf2)])] = datetime.now()
                            events.append({
                                'site1': "Fonbet",
                                'type1': k1,
                                'link1': s[event]["url"].replace('tennis', 'basketball'),
                                'coefficient1': kf1,
                                'matchName1': event,
                                'site2': "Olimp",
                                'type2': k2,
                                'link2': g[eventg]["url"],
                                'coefficient2': kf2,
                                'matchName2': eventg,
                                'profit': round(pr1, 2),
                                'time': first_appearance_times[
                                    "".join([event, str(kf1), str(kf2)])].isoformat()
                            })
                        if -1000 < pr2 < 1000:
                            print(pr2, kf3, kf4, event, k1, k2)
                            print(s[event]["url"].replace('tennis', 'basketball'))
                            print(g[eventg]["url"])
                            print('------------------------------')
                            if not "".join([event, str(kf3), str(kf4)]) in first_appearance_times:
                                first_appearance_times["".join([event, str(kf3), str(kf4)])] = datetime.now()
                            events.append({
                                'site1': "Fonbet",
                                'type1': k2,
                                'link1': s[event]["url"].replace('tennis', 'basketball'),
                                'coefficient1': kf3,
                                'matchName1': event,
                                'site2': "Olimp",
                                'type2': k1,
                                'link2': g[eventg]["url"],
                                'coefficient2': kf4,
                                'matchName2': eventg,
                                'profit': round(pr2, 2),
                                'time': first_appearance_times[
                                    "".join([event, str(kf3), str(kf4)])].isoformat()
                            })

        with app.app_context():
            UpdateEvents(events)
