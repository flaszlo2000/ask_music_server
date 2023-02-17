from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector

from .models.base import Base


def check_tables_on(engine: Engine, metadata: MetaData = Base.metadata) -> None:
    inspector = Inspector(bind = engine)
    tables_were_ok = True

    for table_name, table in metadata.tables.items():
        print(table_name, table)
        if not inspector.has_table(table_name):
            tables_were_ok = False
            table.create(bind = engine)
            print(f"[*] Table has been created: *{table_name}*")

    if tables_were_ok:
        print("[*] Tables has been checked!")
