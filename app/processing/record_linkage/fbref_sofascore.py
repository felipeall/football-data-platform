from dataclasses import dataclass
from typing import Type

import pandas as pd
import recordlinkage
from loguru import logger
from recordlinkage.preprocessing import clean

from app.models.base import Base
from app.models.fbref import FBrefPlayers
from app.models.sofascore import SofascorePlayers
from app.services.db import Database


@dataclass
class FBrefSofascore:
    db: Database = Database()
    SCORE_THRESHOLD: int = 2
    DISTANCE_THRESHOLD: float = 0.85

    def run(self):
        """Run FBref x Sofascore record linkage process."""
        fbref_players = self._load_data(FBrefPlayers)
        sofascore_players = self._load_data(SofascorePlayers)
        features = self._generate_features(fbref_players, sofascore_players)

        self.db.load_dataframe(features, "fbref_sofascore")

    def _load_data(self, model: Type[Base]) -> pd.DataFrame:
        """Load data from database."""
        df = (
            self.db.get_dataframe(model)
            .assign(name=lambda x: clean(x["name"], strip_accents="unicode"))
            .assign(dob=lambda x: pd.to_datetime(x["dob"]))
            .set_index("id")
            .loc[:, ["name", "dob", "country_code"]]
        )

        logger.info(f"Loaded {len(df)} records from {model.__table__.schema}.{model.__tablename__}")

        return df

    def _generate_features(self, fbref_players: pd.DataFrame, sofascore_players: pd.DataFrame) -> pd.DataFrame:
        """Generate features for record linkage."""
        indexer = recordlinkage.Index()
        indexer.sortedneighbourhood("name").block(["dob", "country_code"])
        candidates = indexer.index(fbref_players, sofascore_players)

        compare = recordlinkage.Compare()
        compare.string("name", "name", method="levenshtein", threshold=self.DISTANCE_THRESHOLD, label="name")
        compare.exact("country_code", "country_code", label="country_code")
        compare.date("dob", "dob", label="dob")

        features = (
            compare.compute(candidates, fbref_players, sofascore_players)
            .assign(score=lambda x: x.sum(axis=1))
            .loc[lambda x: x["score"] >= self.SCORE_THRESHOLD, :]
            .reset_index()
            .rename(columns={"id_1": "fbref_id", "id_2": "sofascore_id"})
            .sort_values("score", ascending=False)
            .drop_duplicates("fbref_id")
            .drop_duplicates("sofascore_id")
            .loc[:, ["fbref_id", "sofascore_id"]]
        )

        logger.info(f"Generated {len(features)} features")

        return features


def main():
    fbref_sofascore = FBrefSofascore()
    fbref_sofascore.run()


if __name__ == "__main__":
    main()
