from betsniper.fonbet.config import bet_types, variants_sports
import requests
import time


def main(requested_sports: list):
    # Обнуляем все масссивы событий
    events = {}
    events_name_by_id = {}
    childs_event_by_id = {}
    sports = {}

    response = requests.get("https://line54w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600").json()

    # Получаем ID спортивных дисциплин, которые нам нужны
    parent_sport_ids = []
    sport_ids = []
    for requested_sport in requested_sports:
        variants = variants_sports.get(requested_sport, [])
        for sport in response['sports']:
            if sport['name'].lower() in variants:
                parent_sport_ids.append(sport['id'])

            if 'parentId' in list(sport.keys()):
                if sport['parentId'] in parent_sport_ids:
                    # print(sport)
                    # print(sport['id'], sport['name'], sport['parentId'], sport['parentIds'])
                    sport_ids.append(sport['id'])
    # print(sport_ids)
    # print(response['sports'])
    # Получаем все необходимые нам события
    for event in response["events"]:
        if event["sportId"] in sport_ids:
            # print(event['sportId'])
            if event['place'] == 'live':
                sport_type = next((key for key, value in sports.items() if event["sportId"] in value), None)
                if "team1" in event and "team2" in event:
                    event_name = event["team1"]+" - "+event["team2"]
                    events[event_name] = {"id": event["id"],"bets": {}, "type": sport_type}
                    events_name_by_id[event["id"]] = {"name": event_name, "sportid": event["sportId"]}
                # print(events_name_by_id)
                if "parentId" in event:
                    if event["parentId"] in events_name_by_id.keys():
                        childs_event_by_id[event["id"]] = {"parent": event["parentId"], "name": event["name"],"type": sport_type}
                        # print(event['parentId'], event['sportId'], childs_event_by_id)

    # Получаем все котировки ставок
    outcomes_response = requests.get("https://line06w.bk6bba-resources.com/events/list?lang=ru&version=21257564342&scopeMarket=1600").json()
    for event in outcomes_response["customFactors"]:
        # Основные события (Исход матча, фора и т.д.)
        if event["e"] in events_name_by_id.keys():
            event_name = events_name_by_id[event["e"]]["name"]
            sport_id = events_name_by_id[event["e"]]["sportid"]
            event_id = event["e"]
            events[event_name]["url"] = f"https://www.fon.bet/live/tennis/{sport_id}/{event_id}/"
            for factor in event["factors"]:
                if factor['f'] in bet_types.keys():
                    bet_name = bet_types[factor['f']] if not 'pt' in factor else bet_types[factor['f']] + " ("+factor["pt"]+")"
                    events[event_name]["bets"][bet_name] = factor["v"]

        # Дополнительные события (Исход сета, четверти и т.д.)
        elif event["e"] in childs_event_by_id.keys():
            event_name =  events_name_by_id[childs_event_by_id[event["e"]]["parent"]]["name"]
            child_name = childs_event_by_id[event["e"]]["name"]
            # print(event_name, child_name)
            for factor in event["factors"]:
                # print(factor['f'], factor)
                if factor['f'] in bet_types.keys():
                    bet_name = bet_types[factor['f']] + " (" + child_name + ")" if ('pt' not in factor or float(factor['pt']) == 0) else bet_types[factor['f']] + " (" + str(factor["pt"]) + ")" + " (" + child_name + ")"
                    if "четверть" in bet_name or "сет" in bet_name:
                        events[event_name]["bets"][bet_name] = factor["v"]

    return events


print(main(['tennis']), '\n', len(main(['tennis'])))
