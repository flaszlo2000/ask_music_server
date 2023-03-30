from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from db.models.admins import DBAdmins
from db.singleton_handler import global_db_handler
from pydantic_models.admin import AdminModel, DetailedAdminConfigModel
from scripts.shared.security import pwd_context


def get_all_admins() -> List[AdminModel]:
    "Gets each admin from db and converts it into safer model to respond with"
    result: List[AdminModel] = list()
    db_handler = global_db_handler()

    with db_handler.session() as session:
        for db_admin in session.query(DBAdmins).all():
            result.append(
                AdminModel.convertFromOrm(db_admin)
            )

    return result


def add_admin_to_db(admin_credentials: DetailedAdminConfigModel) -> None:
    "Adds an admin to the db with the original password additionally hashed"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        record_with_the_same_name = session \
            .query(DBAdmins) \
            .filter(DBAdmins.username == admin_credentials.username) \
            .first()
        
        if record_with_the_same_name is not None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Username taken")

        session.add(
            DBAdmins.convertFromPydanticObject(
                admin_credentials,
                exclude = set("password"),
                include = {"password": pwd_context.hash(admin_credentials.password)}
            )
        )

        session.commit()
