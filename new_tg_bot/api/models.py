from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramUser:
    tg_username: str
    tg_user_id: Optional[str] = None
    name: str
    lastname: Optional[str] = None
