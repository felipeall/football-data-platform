from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Type

import pandas as pd
from loguru import logger
from sqlalchemy import Table, create_engine
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.engine import Engine, Inspector
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.base import Base, BaseMixin
from app.settings import settings


@dataclass
class Database:
    engine: Engine = field(init=False)
    session: sessionmaker = field(init=False)

    def __post_init__(self):
        self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def __build_upsert_stmt(self, sql_table: Table, values_to_insert) -> Insert:
        """Build an upsert statement for a given table."""
        insert_stmt = insert(sql_table).values(values_to_insert)
        update_stmt = {
            c.name: c for c in insert_stmt.excluded if not c.primary_key and c.name not in ["created_at", "updated_at"]
        }
        return insert_stmt.on_conflict_do_update(
            constraint=self.__get_constraint_name(sql_table),
            set_=update_stmt,
        )

    def __get_constraint_name(self, sql_table: Table):
        """Get the constraint name for a given table."""
        unique_constraints = self.__inspector.get_unique_constraints(sql_table.name, schema=sql_table.schema)

        if unique_constraints:
            return f"uq_{sql_table.name}"
        return f"pk_{sql_table.name}"

    def get_dataframe(self, model: Type[Base]) -> pd.DataFrame:
        """Download the model data from the database as a DataFrame."""
        return pd.read_sql(self.session().query(model.__table__).statement, self.engine)

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table: str,
        schema: str = "public",
        if_exists: Literal["fail", "replace", "append"] = "replace",
    ):
        """Load the data from a DataFrame to the database."""
        df.to_sql(
            table,
            con=self.engine,
            if_exists=if_exists,
            index=False,
            schema=schema,
        )
        logger.info(f"Loaded {len(df)} records to {schema}.{table} (mode: {if_exists})")

    def upsert_from_model(self, model: BaseMixin):
        """Upsert the data from a model to the database."""
        table, schema, sql_table = self.__get_model_info(model)
        upsert_stmt = self.__build_upsert_stmt(sql_table, [model.to_dict()])

        with self.engine.begin() as conn:
            try:
                conn.execute(upsert_stmt)
            except IntegrityError as e:
                logger.debug(f"Failed loading to {schema}.{table}: {str(e.orig).replace(chr(10), '. ')}")

    @property
    def __inspector(self):
        """Return the database inspector."""
        return Inspector.from_engine(self.engine)

    @staticmethod
    def __get_model_info(model: BaseMixin) -> tuple[str, str, Table]:
        """Return the table name and schema for a given model."""
        table = model.__tablename__
        schema = next((arg.get("schema") for arg in model.__table_args__ if isinstance(arg, dict)), None)
        sql_table = Table(table, Base.metadata, schema=schema)
        return table, schema, sql_table

    def get_latest_scrapped_at(self, model: BaseMixin) -> datetime:
        """Return the latest scrapped_at timestamp from the database."""
        table, schema, _ = self.__get_model_info(model)
        with self.engine.connect() as conn:
            return conn.execute(f"SELECT MAX(scrapped_at) FROM {schema}.{table}").scalar()
