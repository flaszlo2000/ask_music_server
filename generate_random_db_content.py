from random import choices
from string import ascii_letters
from uuid import uuid4

from dotenv import load_dotenv

from db.main import DbHandler
from db.models.events import DBEvents
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_file_path


def generate_random_str(size: int = 30) -> str:
    return "".join(choices(ascii_letters, k = size))

def generate_random_data_into_db(generated_amount: int = 10_000) -> None:
    load_dotenv(get_env_file_path())
    db_handler = DbHandler(AllowedEnvKey.DATABASE_URL)

    with db_handler.session() as session:
        for _ in range(generated_amount):
            c = DBEvents(
                uuid4(),
                generate_random_str(),
                generate_random_str(),
                note = "!!GENERATED!!"
            )
            session.add(c)

        session.commit()

if __name__ == "__main__":
    generate_random_data_into_db()