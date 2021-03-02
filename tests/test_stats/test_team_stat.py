from unittest import mock
from discord_ritoman.lol.stats.team import TeamStat
import discord_ritoman.lol.stats.team


def team_stat(team_id: int = 100, participant_id: int = 1):
    def decorator(func):
        @mock.patch.object(discord_ritoman.lol.stats.team, "get_stat")
        def wrapper(mock_get_stat):
            stat_table = {
                "participant_ids": {
                    "A1": participant_id,
                    "user": participant_id,
                }
            }

            mock_get_stat.side_effect = lambda x: stat_table[x]

            data = {
                "participants": [
                    {"participantId": participant_id, "teamId": team_id}
                ]
            }
            response = TeamStat.obj.process(data, {}, "A1")
            func(response)

        return wrapper

    return decorator


@team_stat()
def test_team_stat(response):
    """"""
    assert response == 100
