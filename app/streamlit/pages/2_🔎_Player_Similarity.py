import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from app.services.db import Database

st.set_page_config(page_title="Player Similarity", page_icon="️🔎", layout="wide", initial_sidebar_state="expanded")

QUERY_MATCHES_EVENTS = """
SELECT
    matches_events.*
FROM sofascore.matches_events
JOIN sofascore.matches
ON matches.id = matches_events.match_id AND date >= CURRENT_DATE - INTERVAL '{last_n_years} year'
JOIN sofascore.players
ON players.id = matches_events.player_id
JOIN sofascore.tournaments
ON matches.tournament_id = tournaments.id
WHERE players.retired IS NOT TRUE
AND (date_part('year', age(players.dob)) BETWEEN {age_min} AND {age_max} OR players.id = '{player_id}')
"""

QUERY_PLAYERS = """
SELECT
    players.id,
    players.name,
    date_part('year', age(dob))::int AS age,
    teams.name AS team_name,
    teams.league_name,
    players.position,
    players.height,
    players.preferred_foot,
    players.country_name
    --CASE WHEN tournaments.id IS NOT NULL THEN true ELSE false END AS player_flag
FROM sofascore.players
JOIN sofascore.teams
ON teams.id = players.team_id
--LEFT JOIN sofascore.tournaments
JOIN sofascore.tournaments
ON teams.league_id = tournaments.id
WHERE retired IS NOT TRUE
--AND tournaments.id IS NOT NULL
ORDER BY players.name
"""

db = Database()
df_players = pd.read_sql(QUERY_PLAYERS, db.engine)


def preprocess_match_data(
    player_id: str, last_n_years: int, age_range: tuple[int], minutes_played_min: int,
) -> pd.DataFrame:
    """Preprocess match data."""
    df = pd.read_sql(
        QUERY_MATCHES_EVENTS.format(
            player_id=player_id,
            last_n_years=last_n_years,
            age_min=age_range[0],
            age_max=age_range[1],
        ),
        db.engine,
    )
    df = df.drop(
        columns=["id", "match_id", "team_id", "has_statistics", "scrapped_at", "created_at", "updated_at"],
        errors="ignore",
    )
    df = df.groupby(["player_id"]).sum()
    df = df[df["minutes_played"] > minutes_played_min]
    return df.reset_index()


def calculate_per_90_metrics(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Calculate per 90 minutes metrics."""
    cols_stats = [
        col
        for col in df.columns
        if col
        not in ["player_id", "minutes_played", "rating", "rating_versions_alternative", "rating_versions_original"]
    ]

    df[cols_stats] = df[cols_stats].div(df["minutes_played"], axis=0)
    df_per_90 = df.drop(
        columns=["minutes_played", "rating", "rating_versions_alternative", "rating_versions_original"],
    )
    return df_per_90, cols_stats


def scale_data(df_per_90: pd.DataFrame, cols_stats: list[str]) -> pd.DataFrame:
    """Scale the data."""
    scaler = StandardScaler()
    df_scaled = df_per_90.copy()
    df_scaled[cols_stats] = scaler.fit_transform(df_scaled[cols_stats])
    return df_scaled


def find_similar_players(df: pd.DataFrame, player_id: str, cols_stats: list[str]) -> list[tuple[int, float]]:
    """Find similar players based on cosine similarity."""
    player_index = df[df["player_id"] == player_id].index.values[0]
    similarity = cosine_similarity(df[cols_stats])
    similarity_scores = list(enumerate(similarity[player_index]))
    return sorted(similarity_scores, key=lambda x: x[1], reverse=True)


def get_top_similar_players(
    df_players: pd.DataFrame, df_scaled: pd.DataFrame, similarity_scores: list[tuple[int, float]], top_n: int,
) -> pd.DataFrame:
    """Get the top N similar players."""
    similarity_players = {df_scaled.iloc[index]['player_id']: score for index, score in similarity_scores[1 : top_n + 1]}  # {player_id: similarity_score}
    df_similar_players = df_players[df_players["id"].isin(similarity_players.keys())].copy()
    df_similar_players['similarity_score'] = df_similar_players['id'].map(similarity_players)
    return df_similar_players.sort_values(by="similarity_score", ascending=False)


def main(input_player_id: str) -> pd.DataFrame:
    df_processed_matches = preprocess_match_data(input_player_id, last_n_years, age_range, minutes_played_min)
    df_per_90, cols_stats = calculate_per_90_metrics(df_processed_matches)
    df_scaled = scale_data(df_per_90, cols_stats)
    similarity_scores = find_similar_players(df_scaled, input_player_id, cols_stats)
    print(f"{similarity_scores=}")
    df_similar_players = get_top_similar_players(
        df_players,
        df_scaled,
        similarity_scores,
        top_n_similar_players,
    )
    df_similar_players["url"] = df_similar_players["id"].apply(
        lambda x: f"/Player_Profile?player_id={x}",
    )
    df_similar_players.drop(columns=["id"], inplace=True)
    return df_similar_players


with st.sidebar:
    players_ids = df_players["id"].tolist()
    players_names = df_players["name"].tolist()
    players_id2name = dict(zip(players_ids, players_names))

    input_player_id = st.selectbox("Select player", players_ids, format_func=lambda x: players_id2name[x], index=None)
    input_player_name = players_id2name.get(input_player_id)

    players_age_min = int(df_players["age"].min())
    players_age_max = int(df_players["age"].max())
    age_range = st.sidebar.slider(
        "Age range:",
        min_value=players_age_min,
        max_value=players_age_max,
        value=(players_age_min, players_age_max),
    )
    minutes_played_min = st.sidebar.number_input("Minimum minutes played:", min_value=0, value=450, step=100)
    last_n_years = st.sidebar.number_input("Number of years to consider:", min_value=1, value=1, step=1)
    top_n_similar_players = st.sidebar.number_input(
        "Number of similar players to display:",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
    )


if input_player_id:
    st.write(f"Top {top_n_similar_players} players similar to {input_player_name}:")
    df_similar_players = main(input_player_id)
    st.dataframe(
        df_similar_players, hide_index=True, column_config={"url": st.column_config.LinkColumn(display_text="🔗")},
    )
else:
    st.write("Please select a player name.")
