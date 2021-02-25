import json


def get_mock_match_data():
    """"""
    with open("./tests/mock/matches_by-matchid.json", "r") as fp:
        return json.load(fp)


def get_mock_match_timeline():
    """"""
    with open("./tests/mock/timelines_by-match-matchid.json", "r") as fp:
        return json.load(fp)


def get_mock_match_data_account_id():
    """"""
    return "htdKMW6n5_HaAo6YxT4Yba47-9PatMVgjR2JeXgCOZkQWE0"
