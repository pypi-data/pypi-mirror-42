from logzero import logger
import pyexcel as p
from zeroinger.time.race_timer import RaceTimer

'''
基于pyexcel实现
http://docs.pyexcel.org/en/latest/quickstart.html
'''
class XLSX:
    def __init__(self):
        pass

    @staticmethod
    def read_dict_sheet(xlsx_path, sheet_id_or_name=0):
        book = p.iget_book(xlsx_path)
        sheet = None
        if type(sheet_id_or_name) == int:
            # 输入的定位标是数字
            if book.number_of_sheets() > sheet_id_or_name:
                name = book.sheet_names()[sheet_id_or_name]
                sheet = book[name]
        if type(sheet_id_or_name) == str:
            # 输入的定位标是文本
            sheet = book[sheet_id_or_name]
        pass

    @staticmethod
    def write_dict_sheet(xlsx_path, sheet_name='sheet1'):


        pass
