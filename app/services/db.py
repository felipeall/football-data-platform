from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
from pandas.io.sql import SQLTable
from sqlalchemy import Connection, Engine, MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.settings import settings


@dataclass
class Database:
    engine: Engine = field(init=False)
    SessionLocal: sessionmaker = field(init=False)

    def __post_init__(self):
        self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_upsert_method(self, meta: MetaData):
        def method(table: SQLTable, conn: Connection, keys: list[str], data_iter: zip):
            sql_table = Table(table.name, meta, schema=table.schema)
            values_to_insert = [dict(zip(keys, data)) for data in data_iter]
            upsert_stmt = self.build_upsert_stmt(sql_table, values_to_insert)
            conn.execute(upsert_stmt)

        return method

    @staticmethod
    def build_upsert_stmt(sql_table: Table, values_to_insert) -> Insert:
        insert_stmt = insert(sql_table).values(values_to_insert)
        update_stmt = {
            c.name: c for c in insert_stmt.excluded if not c.primary_key and c.name not in ["created_at", "updated_at"]
        }
        return insert_stmt.on_conflict_do_update(
            index_elements=sql_table.primary_key.columns,
            set_=update_stmt,
        )

    @property
    def upsert(self):
        return self.create_upsert_method(Base.metadata)

    def load_dataframe(self, df: pd.DataFrame, table: str, schema: Optional[str] = None):
        df.to_sql(
            table,
            con=self.engine,
            if_exists="append",
            index=False,
            schema=schema,
            method=self.upsert,
        )

    def load_dict(self, data: dict, table: str, schema: Optional[str] = None) -> None:
        sql_table = Table(table, Base.metadata, schema=schema)
        upsert_stmt = self.build_upsert_stmt(sql_table, [data])
        with self.engine.begin() as conn:
            conn.execute(upsert_stmt)
