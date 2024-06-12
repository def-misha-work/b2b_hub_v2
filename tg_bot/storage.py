﻿class UserStorage():

    def __init__(self, tg_id, tg_username, tg_name, tg_surname):
        self.tg_id = tg_id
        self.tg_username = tg_username
        self.tg_name = tg_name
        self.tg_surname = tg_surname

    def to_dict(self):
        return {
            "tg_user_id": self.tg_id,
            "tg_username": self.tg_username,
            "name": self.tg_name,
            "lastname": self.tg_surname
        }


class ApplicationStorage():

    def __init__(
        self,
        tg_id=None,
        application_cost=None,
        target_date=None,
        application_id=None
    ):
        self.tg_id = tg_id
        self.application_cost = application_cost
        self.target_date = target_date
        self.application_id = application_id

    def update_tg_id(self, new_tg_id):
        self.tg_id = new_tg_id

    def update_application_cost(self, new_application_cost):
        self.application_cost = new_application_cost

    def update_target_date(self, new_target_date):
        self.target_date = new_target_date

    def update_application_id(self, new_application_id):
        self.application_id = new_application_id

    def to_dict(self):
        return {
            "tg_user_id": self.tg_id,
            "cost": self.application_cost,
            "target_date": self.target_date,
        }


class CompanyPayerStorage():
    def __init__(self, tg_id=None, company_inn=None, company_name=None):
        self.tg_id = tg_id
        self.company_inn = company_inn
        self.company_name = company_name

    def update_tg_id(self, new_tg_id):
        self.tg_id = new_tg_id

    def update_company_inn(self, new_company_inn):
        self.company_inn = new_company_inn

    def update_company_name(self, new_company_name):
        self.company_name = new_company_name

    def to_dict(self):
        return {
            "tg_user_id": self.tg_id,
            "company_inn": self.company_inn,
            "company_name": self.company_name,
        }


class CompanyPecipientStorage():
    def __init__(self, tg_id=None, company_inn=None, company_name=None):
        self.tg_id = tg_id
        self.company_inn = company_inn
        self.company_name = company_name

    def update_tg_id(self, new_tg_id):
        self.tg_id = new_tg_id

    def update_company_inn(self, new_company_inn):
        self.company_inn = new_company_inn

    def update_company_name(self, new_company_name):
        self.company_name = new_company_name

    def to_dict(self):
        return {
            "tg_user_id": self.tg_id,
            "company_inn": self.company_inn,
            "company_name": self.company_name,
        }
