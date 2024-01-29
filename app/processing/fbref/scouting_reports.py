import io
import re
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from app.services.aws import AWS
from app.services.db import Database

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
class FbrefScoutingReports:
    """Process the scouting reports from FBref."""

    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/fbref/scouting_reports"
    cols_to_drop: list = field(default_factory=lambda: COLS_TO_DROP)

    def run(self):
        """Run the processing."""
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            df = self.process_file(data)
            if df is not None:
                self.db.load_dataframe(df=df, table="scouting_reports", schema="fbref")

    def process_file(self, data: dict) -> Optional[pd.DataFrame]:
        """Process a file."""
        soup = BeautifulSoup(data["data"], "lxml")
        if self.is_goalkeeper(soup=soup):
            return None

        return (
            pd.read_html(io.StringIO(data["data"]))[-1]
            .dropna()
            .T.pipe(self.set_first_row_as_headers)
            .pipe(self.keep_only_per_90)
            .drop(columns=self.cols_to_drop)
            .pipe(self.drop_duplicated_columns)
            .map(self.convert_to_numeric)
            .rename(columns=self.normalize_col_name)
            .assign(player_id=data["id"])
            .assign(minutes_played=self.extract_minutes_played(soup=soup))
        )

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
    def convert_to_numeric(val) -> pd.Series:
        """Convert values to numeric."""
        if isinstance(val, str) and "%" in val:
            return pd.to_numeric(val.rstrip("%")) / 100
        return pd.to_numeric(val)


def main():
    fbref = FbrefScoutingReports()
    fbref.run()


if __name__ == "__main__":
    main()
