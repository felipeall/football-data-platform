import argparse
import sys

from loguru import logger

from app.processing.sofascore import matches, matches_events, players, teams
from app.processing.transfermarkt import market_value

parser = argparse.ArgumentParser(description="Football Data Platform - Processing CLI")
parser.add_argument(
    "source",
    nargs="?",
    type=str,
    help="Source to process data from.",
    choices=["sofascore", "transfermarkt"],
)
parser.add_argument(
    "--file",
    type=str,
    help="Ingest only a single file.",
)
parser.add_argument(
    "--full-load",
    action="store_true",
    help="Process and load all data from the source.",
)
parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
args = parser.parse_args()

logger.remove()
if args.debug:
    logger.add(sys.stderr, level="DEBUG")
else:
    logger.add(sys.stderr, level="INFO")

logger.debug(f"{args=}")

if args.source == "sofascore":
    logger.info("Started Sofascore processing")
    sofascore_matches = matches.SofascoreMatches(file_path=args.file, full_load=args.full_load)
    sofascore_teams = teams.SofascoreTeams(file_path=args.file, full_load=args.full_load)
    sofascore_players = players.SofascorePlayers(file_path=args.file, full_load=args.full_load)
    sofascore_matches_events = matches_events.SofascoreMatchesEvents(file_path=args.file, full_load=args.full_load)

    logger.info("Running Sofascore Teams")
    sofascore_teams.run()

    logger.info("Running Sofascore Matches")
    sofascore_matches.run()

    logger.info("Running Sofascore Players")
    sofascore_players.run()

    logger.info("Running Sofascore Matches Events")
    sofascore_matches_events.run()

    logger.info("Finished Sofascore processing")

if args.source == "transfermarkt":
    logger.info("Started Transfermarkt processing")
    transfermarkt_market_value = market_value.TransfermarktMarketValue()

    logger.info("Running Transfermarkt Market Value")
    transfermarkt_market_value.run()

    logger.info("Finished Transfermarkt processing")
