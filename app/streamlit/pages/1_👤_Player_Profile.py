import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.models.sofascore import SofascoreSeasons, SofascoreTeams
from app.services.db import Database

st.set_page_config(page_title="Player Profile", page_icon="️👤", layout="wide", initial_sidebar_state="expanded")

hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""
st.markdown(hide_img_fs, unsafe_allow_html=True)

QUERY_PLAYERS = """
SELECT 
    players.*
FROM sofascore.players
JOIN sofascore.teams
ON players.team_id = teams.id
JOIN sofascore.tournaments
ON teams.league_id = tournaments.id
WHERE retired IS NOT TRUE
ORDER BY players.name
"""

db = Database()
data_sofascore_players = pd.read_sql(QUERY_PLAYERS, db.engine)
data_sofascore_seasons = db.get_dataframe(SofascoreSeasons)
data_sofascore_teams = db.get_dataframe(SofascoreTeams)
col = st.columns((2, 7), gap="small")


def main():
    df_player = pd.read_sql(
        "SELECT tournaments.*, seasons.*, matches.*, players.name AS player_name, matches_events.* FROM"
        " sofascore.matches_events JOIN sofascore.matches ON matches_events.match_id = matches.id JOIN"
        " sofascore.seasons ON matches.season_id = seasons.id JOIN sofascore.tournaments ON seasons.tournament_id ="
        " tournaments.id JOIN sofascore.players ON matches_events.player_id = players.id WHERE player_id ="
        f" '{input_player_id}' ORDER BY date DESC",
        db.engine,
    )
    season_id = df_player[df_player["country_code"].notnull()]["season_id"].values[0]
    team_name = data_sofascore_teams[data_sofascore_teams["id"] == df_player["team_id"].values[0]]["name"].values[0]
    season_name = data_sofascore_seasons[data_sofascore_seasons["id"] == season_id]["name"].values[0]
    df_player_plot = (
        df_player[df_player["season_id"] == season_id]
        .groupby(["player_id", "player_name"])
        .agg({"expected_goals": "sum", "goals": "sum"})
        .reset_index()
    )
    df_season = pd.read_sql(
        "SELECT players.name AS player_name, matches_events.* FROM sofascore.matches_events JOIN sofascore.matches ON"
        " matches_events.match_id = matches.id JOIN sofascore.players ON matches_events.player_id = players.id WHERE"
        f" matches.season_id = '{season_id}' AND players.id <> '{input_player_id}'",
        db.engine,
    )
    df_season_plot = (
        df_season.groupby(["player_id", "player_name"]).agg({"expected_goals": "sum", "goals": "sum"}).reset_index()
    )

    with col[0]:
        st.text(input_player_name)
        st.text(team_name)
        st.image(f"https://api.sofascore.com/api/v1/player/{input_player_id}/image")

    with col[1]:
        st.text(season_name)
        max_number = max(
            df_player_plot[["expected_goals", "goals"]].max().max(),
            df_season_plot[["expected_goals", "goals"]].max().max(),
        )
        max_axis = 5 * math.ceil(max_number / 5)
        fig_player = px.scatter(
            df_player_plot,
            y="goals",
            x="expected_goals",
            hover_data=["player_name"],
            range_x=[0, max_axis],
            range_y=[0, max_axis],
            color_discrete_sequence=["red"],
        )
        fig_season = px.scatter(
            df_season_plot,
            y="goals",
            x="expected_goals",
            hover_data=["player_name"],
            range_x=[0, max_axis],
            range_y=[0, max_axis],
        )

        fig = go.Figure(data=fig_player.data + fig_season.data)
        fig.update_layout(
            shapes=[
                {
                    "type": "line",
                    "yref": "paper",
                    "xref": "paper",
                    "y0": 0,
                    "y1": 1,
                    "x0": 0,
                    "x1": 1,
                    "layer": "below",
                },
            ],
        )
        fig.update_layout(
            yaxis_range=[0, max_axis],
            xaxis_range=[0, max_axis],
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig, config={"displayModeBar": False})


with st.sidebar:
    print(data_sofascore_players[data_sofascore_players['id'] == '1190933'] )
    players_ids = data_sofascore_players["id"].tolist()
    players_names = data_sofascore_players["name"].tolist()
    players_id2name = dict(zip(players_ids, players_names))

    param_player_id = st.query_params.get("player_id")
    player_index = None
    if param_player_id in players_ids:
        player_index = players_ids.index(param_player_id)

    input_player_id = st.selectbox(
        "Select player", players_ids, format_func=lambda x: players_id2name[x], index=player_index,
    )
    input_player_name = players_id2name.get(input_player_id)

if input_player_id:
    main()
