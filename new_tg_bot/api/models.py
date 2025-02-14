from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramUser:
    tg_user_id: str
    tg_username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
