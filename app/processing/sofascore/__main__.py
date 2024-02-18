from loguru import logger

from app.processing.sofascore import matches, matches_events, players, teams

logger.info("Started Sofascore processing")
sofascore_matches = matches.SofascoreMatches()
sofascore_teams = teams.SofascoreTeams()
sofascore_players = players.SofascorePlayers()
sofascore_matches_events = matches_events.SofascoreMatchesEvents()


logger.info("Running Sofascore Teams")
sofascore_teams.run()

logger.info("Running Sofascore Matches")
sofascore_matches.run()

logger.info("Running Sofascore Players")
sofascore_players.run()

logger.info("Running Sofascore Matches Events")
sofascore_matches_events.run()

logger.info("Finished Sofascore processing")
