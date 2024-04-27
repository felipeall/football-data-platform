import io
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup

from app.models import fbref
from app.processing.base import BaseProcessing

COLS_TO_DROP: list = [
    "Shooting",
    "Passing",
    "Statistic",
    "Pass Types",
    "Goal and Shot Creation",
    "Defense",
    "Possession",
    "Miscellaneous Stats",
]


@dataclass
class FBrefScoutingReports(BaseProcessing):
    """Process the scouting reports from FBref."""

    files_path: str = "files/fbref/scouting_reports"
    cols_to_drop: list = field(default_factory=lambda: COLS_TO_DROP)

    def run(self):
        """Run the processing."""

        for data in self.files_data:
            scouting_report = self.process_file(data)
            if scouting_report:
                self.db.upsert_from_model(scouting_report)

    def process_file(self, data: dict) -> Optional[fbref.FBrefScoutingReports]:
        """Process a file."""
        soup = BeautifulSoup(data["data"], "lxml")
        if self.is_goalkeeper(soup=soup):
            return None

        df = (
            pd.read_html(io.StringIO(data["data"]))[-1]
            .dropna()
            .T.pipe(self.set_first_row_as_headers)
            .pipe(self.keep_only_per_90)
            .drop(columns=self.cols_to_drop)
            .pipe(self.drop_duplicated_columns)
            .map(self.convert_col_to_numeric)
            .rename(columns=self.normalize_col_name)
            .assign(player_id=data["id"])
            .assign(minutes_played=self.extract_minutes_played(soup=soup))
            .assign(
                scrapped_at=datetime.fromtimestamp(data["scrapped_at"], tz=timezone.utc),
            )
        )

        return fbref.FBrefScoutingReports(**df.to_dict("records")[0])

    @staticmethod
    def extract_minutes_played(soup: BeautifulSoup) -> int:
        """Extract the minutes played."""
        try:
            return int(
                soup.find("div", {"id": re.compile("tfooter_scout_summary_")})
                .find("strong")
                .get_text()
                .replace(" minutes", ""),
            )
        except AttributeError:
            return 0

    @staticmethod
    def is_goalkeeper(soup: BeautifulSoup) -> bool:
        """Check if the player is a goalkeeper."""
        return any("GK" in p.get_text() for p in soup.find("div", {"id": "meta"}).find_all("p"))

    @staticmethod
    def set_first_row_as_headers(df: pd.DataFrame) -> pd.DataFrame:
        """Set the first row as headers and drop it."""
        return df.rename(columns=df.iloc[0]).drop(df.index[0])

    @staticmethod
    def keep_only_per_90(df: pd.DataFrame) -> pd.DataFrame:
        """Keep only the rows with "Per 90" in the second level of the index."""
        return df[df.index.get_level_values(1).isin(["Per 90"])]

    @staticmethod
    def drop_duplicated_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Drop duplicated columns."""
        return df.loc[:, ~df.columns.duplicated()]

    @staticmethod
    def normalize_col_name(s: str) -> str:
        """Normalize column names."""
        s = s.lower().replace("+", "_plus_").replace("%", "_pct_").replace("/", "_per_").replace("percentage", "pct")
        s = re.sub(r"[\W]+", "_", s)
        s = re.sub("_+", "_", s)
        return s.strip("_")

    @staticmethod
    def convert_col_to_numeric(col: str) -> pd.Series:
        """Convert values to numeric."""
        if "%" in col:
            return pd.to_numeric(col.rstrip("%")) / 100
        return pd.to_numeric(col)


def main():
    fbref_scouting_reports = FBrefScoutingReports()
    fbref_scouting_reports.run()


if __name__ == "__main__":
    main()
