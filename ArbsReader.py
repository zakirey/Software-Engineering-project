import random
import time

# american football 10
# basketball 2
# volleyball 9
# table tennis 13
# football 7
# tennis 8
# hockey 6

# favbet 22
# williamhill 13
# betathome 23
# pinnacle 1
# marathon 4
# tippico 29
# lion 30
# 37 GGBET
# 17 Parimatch

# fora 1 17
# fora 2 18
#
# total bigger 19
# total smaller 20
#
# winner 1 1
# winner 2 2
#
# 1x 14
# 2 13
# x2 15
# 1 11

sports = {2: "Basketball", 6: "Hockey", 7: "Football", 8: "Tennis", 9: "Volleyball", 10: "American football",
          13: "Table tennis "}
bookmakers = {1: "Pinnacle", 4: "Marathon", 13: "William hill", 17: "Parimatch", 22: "Favbet", 23: "Bet-at-home",
              29: "Tipico", 30: "Lion", 37: "GGBet"}
bet_types = {0: "?", 1: "Win 1", 2: "Win 2", 11: "1", 13: "2", 14: "1X", 15: "X2", 17: "H1", 18: "H2", 19: "TB",
             20: "TS", 131: "SETS H1", 132: "SETS H2"}


def link_maker(bet_id, token):
    link = "https://www.allbestbets.com/bets/" + bet_id + "?access_token=" + token + "&is_live=0"
    return link


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


def arbs(x, token):
    DATA = []
    for event in x["arbs"]:

        bet1_id = str(event["bet1_id"])
        bet2_id = str(event["bet2_id"])
        team1 = str(event["team1_name"])
        team2 = str(event["team2_name"])
        sport_id = event['sport_id']
        percent = str(event["percent"])
        bet1_type = None
        bet2_type = None
        bet1_koef = None
        bet2_koef = None
        book1 = None
        book2 = None
        link1 = None
        link2 = None

        first = True

        for bet in x["bets"]:
            if (bet["id"] == bet1_id) or (bet["id"] == bet2_id):
                if first:
                    book = bookmakers[bet["bookmaker_id"]]
                    book1 = book
                    bet_koef = bet["koef"]
                    bet1_koef = bet_koef
                    try:
                        bet_type = bet_types[bet["market_and_bet_type"]]
                    except KeyError:
                        bet_type = bet_types[0]
                    if bet["market_and_bet_type"] == 1 or bet["market_and_bet_type"] == 2 or bet[
                        "market_and_bet_type"] == 11 or bet["market_and_bet_type"] == 13 or bet[
                        "market_and_bet_type"] == 14 or bet["market_and_bet_type"] == 15:
                        bet1_type = bet_type
                    else:
                        bet_param = bet["market_and_bet_type_param"]
                        bet1_type = bet_type + "(" + str(bet_param) + ")"

                    link1 = link_maker(bet1_id, token)
                    first = False
                else:
                    book = bookmakers[bet["bookmaker_id"]]
                    book2 = book
                    bet_koef = bet["koef"]
                    bet2_koef = bet_koef
                    try:
                        bet_type = bet_types[bet["market_and_bet_type"]]
                    except KeyError:
                        bet_type = bet_types[0]
                    if bet["market_and_bet_type"] == 1 or bet["market_and_bet_type"] == 2 or bet[
                        "market_and_bet_type"] == 11 or bet["market_and_bet_type"] == 13 or bet[
                        "market_and_bet_type"] == 14 or bet["market_and_bet_type"] == 15:
                        bet2_type = bet_type
                    else:
                        bet_param = bet["market_and_bet_type_param"]
                        bet2_type = bet_type + "(" + str(bet_param) + ")"
                    link2 = link_maker(bet2_id, token)
        timestamp = str(random_date("1/29/2021 3:30 PM", "1/30/2021 3:30 PM", random.random()))
        date = timestamp.split(" ")[0]
        time = timestamp.split(" ")[1]

        event_dict = {"team1": team1,
                      "team2": team2,
                      "sport": sports[sport_id],
                      "percent": percent,
                      "bet1_type": bet1_type,
                      "bet2_type": bet2_type,
                      "bet1_koef": bet1_koef,
                      "bet2_koef": bet2_koef,
                      "book1": book1,
                      "book2": book2,
                      "link1": link1,
                      "link2": link2,
                      "date": date,
                      "time": time
                      }
        DATA.append(event_dict)
    return DATA

# 'https://www.bet365.com/dl/sportsbookredirect?bs=95198485-1165361414~1.65&bet=1#/AC/B1/C1/D8'
# '/E95198485/F3/'

# https://affiliates.bet-at-home.com/processing/clickthrgh.asp?btag=a_74417b_23447&lang=EN&oddid=


# Bet365
# https://www.bet365.com/dl/sportsbookredirect?bs=94985302-1149248377~2.63&bet=1#/AC/B91/C20717648/D19/E10564558/F19/
# https://www.bet365.com/dl/sportsbookredirect?bs=95198485-1165361414~1.65&bet=1#/AC/B1/C1/D8/E95198485/F3/


# pr.oddsrabbit.org/bets/MTIzNjkzNDgyfDEsMC4wLDMsMCwwLDA?access_token=c89c03b97123f2cc470d311589475cba&is_live=0
