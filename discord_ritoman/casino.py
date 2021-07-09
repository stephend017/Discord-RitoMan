"""
How to get points

- takedowns
- win
- ranked (positive % modifier)
- aram & RGM (negative % modifier )
- kp modifier?
- kda modifier?


bets calculated with amount of points player won

"""

from discord_ritoman.models import GameMode

WIN_MULTIPLIER = 20


class Casino:
    @staticmethod
    def gamemode_multiplier(gamemode: GameMode) -> float:
        """
        returns the multiplier for the given gamemode
        """
        # TODO implement
        return 1

    @staticmethod
    def calculate_player_points(
        takedowns: int, did_win: bool, gamemode: GameMode
    ) -> int:
        """
        returns the points won by the player in the league game
        """
        if not did_win:
            return 0

        return (
            int(takedowns * Casino.gamemode_multiplier(gamemode))
            * WIN_MULTIPLIER
        )

    @staticmethod
    def calculate_better_points(
        bet: int, did_win: bool, prediction: bool, gamemode: GameMode
    ) -> int:
        """
        returns the points won by the better in the league game
        """
        if did_win != prediction:
            return 0

        return int(bet * Casino.gamemode_multiplier(gamemode)) * WIN_MULTIPLIER

    @staticmethod
    def calculate_player_bonus(
        player_points: int, better_points: int
    ) -> float:
        """
        returns the multiplier for the player points based on the player points
        won and the better points won
        """
        if better_points <= 0:
            return player_points
        return 1.0 + (player_points / better_points)

    @staticmethod
    def calculate_better_bonus(
        player_points: int, better_points: int
    ) -> float:
        """
        returns the multiplier for the better points based on the player points
        won and the better points won
        """
        if player_points <= 0:
            return better_points
        return 1.0 + (better_points / player_points)
