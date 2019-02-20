import json
import os
import pprint
from pathlib import Path
from typing import Dict, Union

import gspread
from gspread import Cell, Spreadsheet, Worksheet
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

from doe2_sim_parser.exceptions import CredentialsMissingException
from doe2_sim_parser.utils.data_types import Report

pp = pprint.PrettyPrinter(indent=4)

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials(credentials: Union[Dict, str, Path] = None):
    if isinstance(credentials, (str, Path)):
        return ServiceAccountCredentials.from_json_keyfile_name(
            credentials, SCOPES)
    elif isinstance(credentials, dict):
        return ServiceAccountCredentials.from_json_keyfile_dict(
            credentials, SCOPES)
    elif not credentials:
        credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])

        return ServiceAccountCredentials.from_json_keyfile_dict(
            credentials, SCOPES)
    else:
        raise CredentialsMissingException("Credentials for Google is missing")


def get_sheet(spreadsheet: Spreadsheet,
              title: str,
              rows: int = None,
              cols: int = None) -> Worksheet:
    sheet = None
    try:
        sheet = spreadsheet.worksheet(title)
    except WorksheetNotFound as err:
        if rows and cols:
            sheet = spreadsheet.add_worksheet(
                title=title, rows=rows, cols=cols)
        else:
            pass

    return sheet


def update_report(report: Report,
                  spreadsheet_id: str = None,
                  credentials: Union[Dict, str] = None):

    if not spreadsheet_id:
        spreadsheet_id = os.environ["SPREADSHEET_ID"]
    creds = get_credentials(credentials)

    gc = gspread.authorize(creds)

    ss = gc.open_by_key(spreadsheet_id)

    sheet = get_sheet(
        ss, "{} - {}".format(report.code, report.name), rows=2, cols=2)

    total_rows = sheet.row_count
    total_cols = sheet.col_count

    cell_list = sheet.range(1, 1, total_cols, total_rows)

    for cell in cell_list:
        cell.value = ""

    dict_cells = dict(map(lambda x: ((x._row, x._col), x), cell_list))

    for i, row in enumerate(report.report, 1):
        for j, value in enumerate(row, 1):
            try:
                v = float(value)
            except ValueError as err:
                v = value

            try:
                dict_cells[(i, j)].value = v
            except KeyError as err:
                cell = Cell(row=i, col=j, value=v)
                cell_list.append(cell)

    result = sheet.update_cells(cell_list)

    return result
