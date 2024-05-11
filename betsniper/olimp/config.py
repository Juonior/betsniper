def get_bet_name(outcome):
    if outcome['tableType'] == 'HANDICAP' and outcome["groupName"] in "Основные Победа с учетом форы":
        handicap_number = outcome['shortName'].split()[-1]
        return f"Ф{handicap_number} ({float(outcome['param']):+g})"
    elif outcome['tableType'] == 'TOTAL' and outcome["groupName"].lower() in "основные доп. тоталы":
        total_value = float(outcome['param'])
        total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
        return f"{total_type} ({total_value})"
    elif outcome["groupName"] == "Основные":
        if outcome['shortName'] in "П1 П2":
            return outcome['shortName']
    elif outcome["groupName"] == "Ставки по сетам":
        words = outcome["shortName"].split("_")
        if 'Тотал' in outcome['unprocessedName']:
            total_value = float(outcome['param'])
            total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
            set_number = outcome['shortName'][1]
            return f"{total_type} ({total_value}) ({set_number}-й сет)"
        elif len(words) == 3:
            words = outcome["shortName"].split("_")
            param = words[2] if "-" in words[2] else "+"+words[2]
            return f"{words[1]} ({param}) ({words[0][1]}-й сет)"
        else:
            custom_name = outcome['unprocessedName'].split(' в ')
            set_type = custom_name[1].replace('м', 'й')
            return f"{custom_name[0]} ({set_type[:-1]})"
    elif outcome["groupName"] == "Исходы по четвертям":
        if ("П1" in outcome["shortName"] or "П2" in outcome["shortName"]) and not "Ф0" in outcome["shortName"]:
            return f"{outcome['shortName'][2:]} ({outcome['shortName'][1]}-я четверть)"
        elif "Ф" in outcome["shortName"] and not "Ф0" in outcome["shortName"]:
            param = outcome["param"][:-1] if "-" in outcome["param"] else "+"+outcome["param"][:-1]
            return f"{outcome['shortName'][2:4]} ({param}) ({outcome['shortName'][1]}-я четверть)"
        elif "Тот"  in outcome["shortName"]:
            param = float(outcome['param'])
            total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
            return f"{total_type} ({param}) ({outcome['shortName'][1]}-я четверть)"
    else:
        return "None"
variants_sports = {
    'tennis': "Теннис",
    'basketball': "Баскетбол"
}
groupNames = [
    "Основные",
    "Ставки по сетам",
    "Доп.тотал",
    "Победа с учетом форы",
]