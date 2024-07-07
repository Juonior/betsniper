import requests, threading
from betsniper.olimp.config import variants_sports, get_bet_name

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36",
}

def get_info(event_id,sport_name, team_1):

    global events

    # Получение сведений о событии
    response = requests.get("https://www.olimp.bet/api/v4/0/live/events?vids[]="+str(event_id)+":&main=false",headers=headers).json()
    event = response[0]["payload"]

    event_name = event["names"]["0"].replace('.', '')
    sport_name = next((key for key, value in variants_sports.items() if value == sport_name), None)

    events[event_name] = {"type": sport_name, "bets": {}, "url": "https://www.olimp.bet/live/"+str(event["sportId"])+"/"+str(event["competitionId"])+"/"+str(event['id'])}

    # Получение ставок на события и конвертация их в словарь
    for outcome in event["outcomes"]:
        bet_name = get_bet_name(outcome, team_1)
        events[event_name]["bets"][bet_name] = outcome["probability"]

def main(requested_sports: list):

    # Обнуление переменных
    global events
    threads = []
    events = {}

    # Получения списка всех матчей
    response = requests.get("https://www.olimp.bet/api/v4/0/live/broadcast/sports-with-competitions-with-events", headers=headers).json()
    sports = [variants_sports[requested_sport] for requested_sport in requested_sports]
    i = 0
    # Просмотр всех котировок на нужном матче
    for sport in response:
        sport_name = sport["payload"]["sport"]["name"]
        if sport_name in sports:
            for competition in sport["payload"]["competitionsWithEvents"]:
                for event in competition["events"]:
                    thread = threading.Thread(target=get_info, args=(event["id"], sport_name, event["team1Name"]))
                    thread.start()
                    threads.append(thread)
                    # break
                # break
    
    # Дожидаемся получения всех котировок
    for thread in threads:
        thread.join()

    return events