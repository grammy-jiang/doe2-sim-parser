import os
from itertools import chain
from unittest import TestCase

import gspread

from doe2_sim_parser.update_google_spreadsheet import (get_credentials,
                                                       update_report)
from doe2_sim_parser.utils.data_types import Report


class TestUpdateGoogleSpreadsheet(TestCase):
    maxDiff = None

    def setUp(self):
        self.spreadsheet_id = os.environ["SPREADSHEET_ID"]

        self.gc = gspread.authorize(get_credentials())
        self.ss = self.gc.open_by_key(self.spreadsheet_id)

        self.reports = [
            # Report(
            #     type_="normal_report",
            #     code="BEPS",
            #     name="Building Energy Performance",
            #     report=[
            #         [
            #             "sample", "DOE-2.2-48z", "2/03/2019", "13:58:04",
            #             "BDL RUN", "1"
            #         ],
            #         [
            #             "REPORT",
            #             "BEPS",
            #             "Building Energy Performance",
            #             "WEATHER FILE",
            #             "CHICAGO, IL",
            #         ],
            #         [
            #             "METER",
            #             "TYPE",
            #             "UNIT",
            #             "LIGHTS",
            #             "TASK\nLIGHTS",
            #             "MISC\nEQUIP",
            #             "SPACE\nHEATING",
            #             "SPACE\nCOOLING",
            #             "HEAT\nREJECT",
            #             "PUMPS\n& AUX",
            #             "VENT\nFANS",
            #             "REFRIG\nDISPLAY",
            #             "HT PUMP\nSUPPLEN",
            #             "DOMEST\nHOT WTR",
            #             "EXT\nUSAGE",
            #             "TOTAL",
            #         ],
            #         [
            #             "EM1",
            #             "ELECTRICITY",
            #             "MBTU",
            #             "236.0",
            #             "0.0",
            #             "315.4",
            #             "0.0",
            #             "87.4",
            #             "0.0",
            #             "7.2",
            #             "76.7",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "722.8",
            #         ],
            #         [
            #             "FM1",
            #             "NATURAL-GAS",
            #             "MBTU",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "341.7",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "0.0",
            #             "41.0",
            #             "0.0",
            #             "382.7",
            #         ],
            #         [
            #             "",
            #             "",
            #             "MBTU",
            #             "236.0",
            #             "0.0",
            #             "315.4",
            #             "341.7",
            #             "87.4",
            #             "0.0",
            #             "7.2",
            #             "76.7",
            #             "0.0",
            #             "0.0",
            #             "41.0",
            #             "0.0",
            #             "1105.5",
            #         ],
            #         [
            #             "TOTAL SITE ENERGY",
            #             "1105.48",
            #             "MBTU",
            #             "44.2",
            #             "KBTU/SQFT-YR GROSS-AREA",
            #             "44.2",
            #             "KBTU/SQFT-YR NET-AREA",
            #         ],
            #         [
            #             "TOTAL SOURCE ENERGY",
            #             "2551.00",
            #             "MBTU",
            #             "102.0",
            #             "KBTU/SQFT-YR GROSS-AREA",
            #             "102.0",
            #             "KBTU/SQFT-YR NET-AREA",
            #         ],
            #         [
            #             "PERCENT OF HOURS ANY SYSTEM ZONE OUTSIDE OF THROTTLING RANGE",
            #             "2.35",
            #         ],
            #         ["PERCENT OF HOURS ANY PLANT LOAD NOT SATISFIED", "0.00"],
            #         ["HOURS ANY ZONE ABOVE COOLING THROTTLING RANGE", "59"],
            #         ["HOURS ANY ZONE BELOW HEATING THROTTLING RANGE", "6"],
            #         [
            #             "NOTE:  ENERGY IS APPORTIONED HOURLY TO ALL END-USE CATEGORIES."
            #         ],
            #     ],
            # ),
            # Report(
            #     type_="normal_report",
            #     code="BEPU",
            #     name="Building Utility Performance",
            #     report=[
            #         [
            #             "sample", "DOE-2.2-48z", "2/03/2019", "13:58:04",
            #             "BDL RUN", "1"
            #         ],
            #         [
            #             "REPORT",
            #             "BEPU",
            #             "Building Utility Performance",
            #             "WEATHER FILE",
            #             "CHICAGO, IL",
            #         ],
            #         [
            #             "METER",
            #             "TYPE",
            #             "UNIT",
            #             "LIGHTS",
            #             "TASK\nLIGHTS",
            #             "MISC\nEQUIP",
            #             "SPACE\nHEATING",
            #             "SPACE\nCOOLING",
            #             "HEAT\nREJECT",
            #             "PUMPS\n& AUX",
            #             "VENT\nFANS",
            #             "REFRIG\nDISPLAY",
            #             "HT PUMP\nSUPPLEN",
            #             "DOMEST\nHOT WTR",
            #             "EXT\nUSAGE",
            #             "TOTAL",
            #         ],
            #         [
            #             "EM1",
            #             "ELECTRICITY",
            #             "KWH",
            #             "69156.",
            #             "0.",
            #             "92425.",
            #             "0.",
            #             "25606.",
            #             "0.",
            #             "2116.",
            #             "22465.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "211768.",
            #         ],
            #         [
            #             "FM1",
            #             "NATURAL-GAS",
            #             "THERM",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "3417.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "0.",
            #             "410.",
            #             "0.",
            #             "3827.",
            #         ],
            #         [
            #             "TOTAL ELECTRICITY",
            #             "ELECTRICITY",
            #             "211768.",
            #             "KWH",
            #             "8.471",
            #             "KWH",
            #             "/SQFT-YR GROSS-AREA",
            #             "8.471",
            #             "KWH",
            #             "/SQFT-YR NET-AREA",
            #         ],
            #         [
            #             "TOTAL NATURAL-GAS",
            #             "NATURAL-GAS",
            #             "3827.",
            #             "THERM",
            #             "0.153",
            #             "THERM",
            #             "/SQFT-YR GROSS-AREA",
            #             "0.153",
            #             "THERM",
            #             "/SQFT-YR NET-AREA",
            #         ],
            #         [
            #             "PERCENT OF HOURS ANY SYSTEM ZONE OUTSIDE OF THROTTLING RANGE",
            #             "2.35",
            #         ],
            #         ["PERCENT OF HOURS ANY PLANT LOAD NOT SATISFIED", "0.00"],
            #         ["HOURS ANY ZONE ABOVE COOLING THROTTLING RANGE", "59"],
            #         ["HOURS ANY ZONE BELOW HEATING THROTTLING RANGE", "6"],
            #         [
            #             "NOTE:  ENERGY IS APPORTIONED HOURLY TO ALL END-USE CATEGORIES."
            #         ],
            #     ],
            # ),
            Report(
                type_="normal_report",
                code="ES-D",
                name="Energy Cost Summary",
                report=[
                    [
                        "sample", "DOE-2.2-48z", "2/03/2019", "13:58:04",
                        "BDL RUN", "1"
                    ],
                    [
                        "REPORT",
                        "ES-D",
                        "Energy Cost Summary",
                        "WEATHER FILE",
                        "CHICAGO, IL",
                    ],
                    [
                        "UTILITY-RATE",
                        "RESOURCE",
                        "METERS",
                        "METERED\nENERGY\nUNITS/YR",
                        "",
                        "TOTAL\nCHARGE\n($)",
                        "VIRTUAL\nRATE\n($/UNIT)",
                        "RATE USED\nALL YEAR?",
                    ],
                    [
                        "SCE GS-2 Elec Rate",
                        "ELECTRICITY",
                        "EM1",
                        "211768.",
                        "KWH",
                        "35072.",
                        "0.1656",
                        "YES",
                    ],
                    [
                        "SoCalGas GN-10 Gas Rate",
                        "NATURAL-GAS",
                        "FM1",
                        "3827.",
                        "THERM",
                        "2617.",
                        "0.6837",
                        "YES",
                    ],
                    ["", "", "", "", "", "37689."],
                    ["", "", "", "", "ENERGY COST/GROSS BLDG AREA", "1.51"],
                    ["", "", "", "", "ENERGY COST/NET BLDG AREA", "1.51"],
                ],
            ),
        ]

    def tearDown(self):
        for sheet in self.ss.worksheets():
            if sheet.title != 'homepage':
                self.ss.del_worksheet(sheet)

    def test_update_report(self):
        for report in self.reports:
            with self.subTest(report.name):
                result = update_report(
                    spreadsheet_id=self.spreadsheet_id, report=report)

                sheet = self.ss.worksheet(
                    "{} - {}".format(report.code, report.name)
                )
                cell_list = sheet.range(1, 1, sheet.col_count, sheet.row_count)

                for cell in cell_list:
                    try:
                        cell.value = float(cell.value)
                    except ValueError as err:
                        pass

                list_report = list()

                for line in report.report:
                    for i, element in enumerate(line):
                        try:
                            line[i] = float(element)
                        except ValueError as err:
                            pass
                    list_report.append(line)

                self.assertSequenceEqual(
                    list(filter(lambda x: x != "", chain(*list_report))),
                    list(filter(
                        lambda x: x != "", map(lambda x: x.value, cell_list)
                    )),
                )
