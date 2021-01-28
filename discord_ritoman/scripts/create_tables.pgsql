CREATE TABLE IF NOT EXISTS discord_users (
    discord_username varchar(255) PRIMARY KEY,
    riot_puuid varchar(78),
    discord_id bigint
);

CREATE TABLE IF NOT EXISTS lol_data (
    discord_username varchar(255) PRIMARY KEY,
    last_game_recorded bigint,
    FOREIGN KEY (discord_username) REFERENCES discord_users (discord_username)
);

CREATE TABLE IF NOT EXISTS prefixes (
    prefix text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS stat_prefixes_01 (
    stat_prefix text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS suffixes (
    suffix text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS lol_winrate (
    discord_username varchar(255) PRIMARY KEY,
    win_count int,
    loss_count int,
    FOREIGN KEY (discord_username) REFERENCES discord_users (discord_username)
)
