from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
from loguru import logger
from pandas.io.sql import SQLTable
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.engine import Connection, Engine, Inspector
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.base import Base, BaseMixin
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

    def build_upsert_stmt(self, sql_table: Table, values_to_insert) -> Insert:
        insert_stmt = insert(sql_table).values(values_to_insert)
        update_stmt = {
            c.name: c for c in insert_stmt.excluded if not c.primary_key and c.name not in ["created_at", "updated_at"]
        }
        return insert_stmt.on_conflict_do_update(
            constraint=self.get_constraint_name(sql_table),
            set_=update_stmt,
        )

    def get_constraint_name(self, sql_table: Table):
        unique_constraints = self.inspector.get_unique_constraints(sql_table.name, schema=sql_table.schema)

        if unique_constraints:
            return f"uq_{sql_table.name}"
        return f"pk_{sql_table.name}"

    def load_dataframe(self, df: pd.DataFrame, table: str, schema: Optional[str] = None):
        df.to_sql(
            table,
            con=self.engine,
            if_exists="append",
            index=False,
            schema=schema,
            method=self.upsert,
        )

    def load_from_model(self, model: BaseMixin):
        table = model.__tablename__
        schema = next((arg.get("schema") for arg in model.__table_args__ if isinstance(arg, dict)), None)
        sql_table = Table(table, Base.metadata, schema=schema)
        upsert_stmt = self.build_upsert_stmt(sql_table, [model.to_dict()])

        with self.engine.begin() as conn:
            try:
                conn.execute(upsert_stmt)
            except IntegrityError as e:
                logger.warning(f"Failed loading to {schema}.{table}: {str(e.orig).replace(chr(10), '. ')}")

    @property
    def upsert(self):
        return self.create_upsert_method(Base.metadata)

    @property
    def inspector(self):
        return Inspector.from_engine(self.engine)
