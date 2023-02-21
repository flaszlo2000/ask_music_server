from typing import Callable, Final, Iterable, List

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from db.main import DbHandler
from db.models import *  # asterisk is fine here this is only for assure metadata is complete
from db.models.base import Base, IDBModel
from scripts.shared.db_saver import fast_records, slow_records
from scripts.shared.dotenv_data import (AllowedEnvKey, get_env_data,
                                        get_env_file_path)

# I make this selectable via env variable
DATA_BACKUP_STRATEGIES: Final[List[Callable[[Session, Table], Iterable[IDBModel]]]] = [
    slow_records,
    fast_records
]

def get_registered_tables(metadata: MetaData = Base.metadata) -> Iterable[Table]:
    return metadata.sorted_tables

def get_data_backup_strategy_index() -> int:
    env_strategy_index: str = get_env_data(AllowedEnvKey.DB_BACKUP_STRATEGY)
    db_backup_strategy_env_name = AllowedEnvKey.DB_BACKUP_STRATEGY.value

    if env_strategy_index is None:
        raise ValueError(f"Missing {db_backup_strategy_env_name} env variable!")

    if not env_strategy_index.isnumeric():
        raise ValueError(f"Incorrectly typed {db_backup_strategy_env_name} env variable!")

    strategy_index = int(env_strategy_index)
    if strategy_index >= len(DATA_BACKUP_STRATEGIES) or strategy_index < 0:
        raise ValueError(f"{db_backup_strategy_env_name} env variable incorrect number")

    return strategy_index

def main() -> None:
    load_dotenv(get_env_file_path())
    strat_index = get_data_backup_strategy_index()

    postgres_db_handler = DbHandler(AllowedEnvKey.DATABASE_URL)
    sqlite_db_handler = DbHandler(AllowedEnvKey.DATABASE_BACKUP)

    with postgres_db_handler.session() as pg_session, sqlite_db_handler.session() as sqlite_session:
        for table in get_registered_tables():
            for record in DATA_BACKUP_STRATEGIES[strat_index](pg_session, table):
                insertion_obj = table.insert().values(record)
                sqlite_session.execute(insertion_obj)

        sqlite_session.commit()

if __name__ == "__main__":
    main()