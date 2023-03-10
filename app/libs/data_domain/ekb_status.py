from typing import List, Dict


class EkbStatus:
    def __init__(self, status_text_list: List[Dict[str, str]]):
        self._status_text_list = status_text_list

    def get_status_text(self) -> List[Dict[str, str]]:
        return self._status_text_list
