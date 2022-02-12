import gspread
import pandas as pd


class GoogleSheet:
    def __init__(self):
        self._gs = gspread.service_account()
        self._ws = self._gs.open("Moonland Users").sheet1

        r = len(self._ws.get_all_values())
        self._ws.resize(r, 4)
    
    def write_new_member(self, user):
        for value in self._ws.get_all_values():
            if value[0] == user:
                return
        self._ws.append_row([user,  5, 0, ""])
    
    def link_email(self, user, email):
        values = self._ws.get_all_values()[1:]
        for i, value in enumerate(values):
            if (value[0] == user):
                self._ws.update_cell(i+2, 4, email)
                return True
        else:
            return False
    
    def fetch_wallet(self, user):
        for value in self._ws.get_all_values():
            if value[0] == user:
                return value
        return [None, None, None, None]


gs = GoogleSheet()

