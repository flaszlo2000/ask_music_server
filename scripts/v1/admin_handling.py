from http import HTTPStatus
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Query, Session

from db.models.admins import DBAdmins
from db.singleton_handler import global_db_handler
from pydantic_models.admin import (AdminModel, DetailedAdminModel,
                                   FullAdminModel)
from scripts.shared.check_id_in_db import check_id_in_db
from scripts.shared.security import hash_pwd


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

def add_admin_to_db(admin_credentials: DetailedAdminModel) -> None:
    "Adds an admin to the db with the original password additionally hashed"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        record_with_the_same_name = session \
            .query(DBAdmins) \
            .filter(DBAdmins.username == admin_credentials.username) \
            .first()
        
        #! FIXME: check webhooks!!!!

        if record_with_the_same_name is not None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Username taken")

        session.add(
            DBAdmins.convertFromPydanticObject(
                admin_credentials,
                exclude = set("password"),
                include = {"password": hash_pwd(admin_credentials.password)}
            )
        )

        session.commit()

#region change_admin_in_db checking utils
def __check_admin_unique_values(session: Session, updated_admin_model: FullAdminModel) -> None:
    "Check if a change would violate any unique fields in the admins table"
    base_query = session.query(DBAdmins)
    unique_filters = (
        base_query.filter(DBAdmins.username == updated_admin_model.username),
        base_query.filter(DBAdmins.webhooks_url == updated_admin_model.webhooks_url)
    )

    for unique_filter in unique_filters:
        violating_instance = unique_filter.filter(DBAdmins.id != updated_admin_model.id).first()

        if violating_instance is not None:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Username and webhooks url must be unique!"
            )

def __check_if_at_least_one_maintainer_left(session: Session, maintainer_to_remove_id: int) -> None:
    "Checks if we would proceed with the given change, at least one maintainer would left"
    maintainers_left = session.query(DBAdmins) \
        .filter(DBAdmins.is_maintainer == True) \
        .filter(DBAdmins.id != maintainer_to_remove_id) \
        .count()

    if maintainers_left == 0:
        raise HTTPException(
            HTTPStatus.CONFLICT,
            "Must be at least one maintainer!"
        )

def get_admin_from_db_checked(
    session: Session,
    updated_admin_model: FullAdminModel,
    admin_query: Query[DBAdmins] 
) -> DBAdmins:
    "Gets admin instance from the db for update with all the checks needed"
    admin_in_db = admin_query.first()

    if admin_in_db is None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "The given admin id does not exist in the db"
        )

    __check_admin_unique_values(session, updated_admin_model)
    if not updated_admin_model.is_maintainer:
        __check_if_at_least_one_maintainer_left(session, updated_admin_model.id)

    return admin_in_db
#endregion

def change_admin_in_db(updated_admin_model: FullAdminModel) -> FullAdminModel:
    "Updates admin in db"
    db_hadnler = global_db_handler()

    with db_hadnler.session() as session:
        admin_in_db_query = session.query(DBAdmins).filter(DBAdmins.id == updated_admin_model.id)
        admin_in_db = get_admin_from_db_checked(session, updated_admin_model, admin_in_db_query)

        old_admin_model = FullAdminModel.convertFromOrm(admin_in_db)
        
        admin_in_db_query.update(updated_admin_model.dict())
        session.commit()

    return old_admin_model # return the old model for loggin purposes

def delete_admin_from_db(admin_id: int) -> None:
    # TODO maybe twofactor ?
    db_handler = global_db_handler()

    with db_handler.session() as session:
        admin_in_db = check_id_in_db(session, DBAdmins, admin_id)
        __check_if_at_least_one_maintainer_left(session, admin_id)

        session.delete(admin_in_db)
        session.commit()

def change_webhook_url_for(admin_id: int, new_webhook_url: str) -> bool:
    # TODO: definitely two factor
    # TODO: logs
    ...