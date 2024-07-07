import re


first_team = None

# функция для удаления цифр из названия ставки
def remove_digits(s):
    return re.sub(r'\d', '', s)


def format_handicap(outcome):
    handicap_number = outcome['shortName'].split()[-1]
    return f"Ф{handicap_number} ({float(outcome['param']):+g})"


def format_total(outcome):
    if outcome['groupName'] == 'Индивидуальное количество выигранных геймов':
        total_value = float(outcome['param'])
        total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
        bet_team = outcome['shortName'][:2]
        return f"{bet_team} {total_type} ({total_value})"
    total_value = float(outcome['param'])
    total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
    return f"{total_type} ({total_value})"


def format_main_outcome(outcome):
    return outcome['shortName']


def format_set_bet(outcome):
    words = outcome["shortName"].split("_")
    if 'Тотал' in outcome['unprocessedName']:
        total_value = float(outcome['param'])
        total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
        set_number = outcome['shortName'][1]
        return f"{total_type} ({total_value}) ({set_number}-й сет)"
    elif len(words) == 3:
        param = words[2] if "-" in words[2] else "+" + words[2]
        return f"{words[1]} ({param}) ({words[0][1]}-й сет)"
    else:
        custom_name = outcome['unprocessedName'].split(' в ')
        set_type = custom_name[1].replace('м', 'й')
        return f"{custom_name[0]} ({set_type[:-1]})"


def format_quarter_bet(outcome):
    if ("П1" in outcome["shortName"] or "П2" in outcome["shortName"]) and "Ф0" not in outcome["shortName"]:
        return f"{outcome['shortName'][2:]} ({outcome['shortName'][1]}-я четверть)"
    elif "Ф" in outcome["shortName"] and "Ф0" not in outcome["shortName"]:
        param = outcome["param"][:-1] if "-" in outcome["param"] else "+" + outcome["param"][:-1]
        return f"{outcome['shortName'][2:4]} ({param}) ({outcome['shortName'][1]}-я четверть)"
    elif "Тот" in outcome["shortName"]:
        param = float(outcome['param'])
        total_type = 'ТМ' if 'мен' in outcome['unprocessedName'] else 'ТБ'
        return f"{total_type} ({param}) ({outcome['shortName'][1]}-я четверть)"


def format_set_game(outcome):
    winner = outcome['shortName'][-2:]
    num_set = outcome['shortName'][0]
    game = outcome['shortName'][2]
    return f"{winner} ({num_set}-й сет) ({game}-й гейм)"


def format_set_score(outcome):
    if "ровно" in outcome["groupName"]:
        num_set = outcome['unprocessedName'][21] if outcome['unprocessedName'][21].isdigit() \
            else outcome['unprocessedName'][22]
        game = outcome['unprocessedName'][11]
        result = 1 if outcome['unprocessedName'][-2:] == 'да' else 0
        return f"{result} 40:40 счет ({num_set}-й сет) ({game}-й гейм)"
    num_set = outcome['shortName'][0]
    game = outcome['shortName'][1]
    winner = outcome['shortName'][3]
    result = outcome['shortName'][4:]
    return f"П{winner} счет {result} ({num_set}-й сет) ({game}-й гейм)"


def format_race_set(outcome):
    num_set = outcome['shortName'][0]
    count_game = outcome['shortName'][2]
    team = outcome['shortName'][-1]
    return f"К{team} до {count_game} геймов ({num_set}-й сет)"


def format_win_total(outcome):
    param = float(outcome['param'])
    winner = outcome['shortName'][1]
    if "ТотМ" in outcome['shortName']:
        return f"П{winner} ТМ ({param})"
    return f"П{winner} ТБ ({param})"


def format_total_set(outcome):
    num_set = outcome['shortName'][0]
    bet = "нечет" if outcome['shortName'][-3:] == "НеЧ" else "чет"
    return f"{num_set}-й сет {bet}"


def format_scorefull_set(outcome):
    num_set = outcome['shortName'][1]
    score = outcome['shortName'][-2]+":"+outcome['shortName'][-1]
    return f"{num_set}-й сет {score}"


def format_at_least_set(outcome):
    global first_team
    result = 1 if outcome['unprocessedName'][-2:] == "да" else 0
    num_team = 1 if outcome['unprocessedName'].split(":")[0] == first_team else 2
    return f"К{num_team} хотя бы в одном сете: {result}"


def format_tiebreak(outcome):
    result = 1 if outcome['unprocessedName'][-2:] == "да" else 0
    num_set = outcome['unprocessedName'].split("-")[-2][-1]
    return f"Тай-брейк: {result} ({num_set}-й сет)"


def format_count_sets(outcome):
    return f"{outcome['unprocessedName']} из 3-х сетов"


def get_bet_name(outcome, team_1):

    global first_team
    first_team = team_1

    # набор тегов и названий для определения функции форматирования названия ставки
    formatters = {
        ('HANDICAP', "основные победа с учетом форы"): format_handicap,
        ('TOTAL', "основные доп. тоталы индивидуальное количество выигранных геймов"): format_total,
        ('RESULT', None): format_main_outcome,
        ('SCORE_FULL', None): format_main_outcome,
        ("OTHER", 'ставки по сетам'): format_set_bet,
        ("OTHER", 'й сет й гейм'): format_set_game,
        ("OTHER", 'счёт \"ровно\" (:) счет в гейме: -й сет'): format_set_score,
        ("OTHER", "гонка по геймам"): format_race_set,
        ("OTHER", "победа и тотал"): format_win_total,
        ("OTHER", "тотал по сетам"): format_total_set,
        ("OTHER", "счет сета"): format_scorefull_set,
        ("OTHER", "победа хотя бы в одном сете"): format_at_least_set,
        ("OTHER", "тай-брейк в матче"): format_tiebreak,
        ("OTHER", "кол-во сетов в матче (из -х)"): format_count_sets,
        ('Исходы по четвертям', None): format_quarter_bet
    }

    for (table_type, group_names), formatter in formatters.items():
        if outcome['tableType'] == table_type:
            if group_names is None or remove_digits(outcome["groupName"]).lower() in group_names:
                return formatter(outcome)
            if "счет" in outcome["groupName"].lower() and "сета" in outcome["groupName"]:
                return format_scorefull_set(outcome)

    return "None"


variants_sports = {
    'tennis': "Теннис",
    'basketball': "Баскетбол"
}


