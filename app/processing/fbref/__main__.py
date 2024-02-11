from app.processing.fbref import players, scouting_reports, teams
from loguru import logger

logger.info("Started FBref processing")
fbref_players = players.FBrefPlayers()
fbref_teams = teams.FBrefTeams()
fbref_scouting_reports = scouting_reports.FBrefScoutingReports()

logger.info("Running FBref Teams")
fbref_teams.run()


logger.info("Running FBref Players")
fbref_players.run()

logger.info("Running FBref Scouting Reports")
fbref_scouting_reports.run()

logger.info("Finished FBref processing")
