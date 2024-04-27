from loguru import logger

from app.processing.transfermarkt import market_value

logger.info("Started Transfermarkt processing")
transfermarkt_market_value = market_value.TransfermarktMarketValue()

logger.info("Running Transfermarkt Market Value")
transfermarkt_market_value.run()

logger.info("Finished Transfermarkt processing")
