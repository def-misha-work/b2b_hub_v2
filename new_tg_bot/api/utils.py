import requests

from abc import ABC, abstractmethod
from typing import List, Optional

from api.models import (
    TelegramUser,
)


class ApiRepository(ABC):
    @abstractmethod
    def get_all_users(self) -> List[TelegramUser]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[TelegramUser]:
        pass

    @abstractmethod
    def create_user(self, user: TelegramUser) -> TelegramUser:
        pass


class ApiRepository(ApiRepository):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_users(self) -> List[TelegramUser]:
        response = requests.get(f"{self.base_url}/api/v1/tg_users/")
        response.raise_for_status()
        return [TelegramUser(**user_data) for user_data in response.json()]

    def get_user_by_id(self, user_id: str) -> Optional[TelegramUser]:
        response = requests.get(f"{self.base_url}/api/v1/tg_users/{user_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return TelegramUser(**response.json())

    def create_user(self, user: TelegramUser) -> TelegramUser:
        response = requests.post(f"{self.base_url}/api/v1/tg_users/", json={
            "tg_username": user.tg_username,
            "tg_user_id": user.tg_user_id,
            "name": user.name,
            "lastname": user.lastname
        })
        response.raise_for_status()
        return TelegramUser(**response.json())

    # Дополнительные методы для update и delete могут быть добавлены по аналогии