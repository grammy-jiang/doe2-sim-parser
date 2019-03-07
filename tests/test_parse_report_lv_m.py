from unittest import TestCase

from doe2_sim_parser.parser_report_lv_m import parse_lv_m
from tests import SAMPLE_SIM_LV_M


class ParseReportESDTest(TestCase):
    maxDiff = None

    def setUp(self):
        with SAMPLE_SIM_LV_M.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/24/2019", "4:28:19", "1"],
            [
                "REPORT",
                "LV-M",
                "DOE-2.2 Units Conversion Table",
                "WEATHER FILE",
                "CHICAGO, IL",
            ],
            [
                "",
                "ENGLISH",
                "MULTIPLIED BY   GIVES",
                "METRIC",
                "MULTIPLIED BY   GIVES",
                "ENGLISH",
            ],
            ["1", " ", "1.000000", " ", "1.000000", " "],
            ["2", " ", "1.000000", " ", "1.000000", " "],
            ["3", "BTU", "0.293000", "WH", "3.412969", "BTU"],
            ["4", "BTU/HR", "0.293000", "WATT", "3.412969", "BTU/HR"],
            ["5", "BTU/LB-F", "4183.830078", "J/KG-K", "0.000239", "BTU/LB-F"],
            [
                "6", "BTU/HR-SQFT-F", "5.678260", "W/M2-K", "0.176110",
                "BTU/HR-SQFT-F"
            ],
            ["7", "DEGREES", "1.000000", "DEGREES", "1.000000", "DEGREES"],
            ["9", "SQFT", "0.092903", " M2", "10.763915", "SQFT"],
            ["10", "CUFT", "0.028317", " M3", "35.314724", "CUFT"],
            ["11", "LB/HR", "0.453592", "KG/HR", "2.204624", "LB/HR"],
            ["12", "LB/CUFT", "16.018459", "KG/M3", "0.062428", "LB/CUFT"],
            ["13", "MPH", "0.447040", "M/S", "2.236936", "MPH"],
            ["14", "BTU/HR-F", "0.527178", "W/K", "1.896893", "BTU/HR-F"],
            ["15", "FT", "0.304800", " M", "3.280840", "FT"],
            [
                "16", "BTU/HR-FT-F", "1.730735", "W/M-K", "0.577789",
                "BTU/HR-FT-F"
            ],
            [
                "17", "BTU/HR- SQFT", "3.152480", "WATT /M2", "0.317211",
                "BTU/HR- SQFT"
            ],
            ["18", "IN", "2.540000", "CM", "0.393701", "IN"],
            ["19", "UNITS/IN", "0.393700", "UNITS/CM", "2.540005", "UNITS/IN"],
            ["20", "UNITS", "1.000000", "UNITS", "1.000000", "UNITS"],
            ["21", "LB", "0.453592", "KG", "2.204624", "LB"],
            [
                "22",
                "FRAC.OR MULT.",
                "1.000000",
                "FRAC.OR MULT.",
                "1.000000",
                "FRAC.OR MULT.",
            ],
            ["23", "HOURS", "1.000000", "HRS", "1.000000", "HOURS"],
            [
                "24", "PERCENT-RH", "1.000000", "PERCENT-RH", "1.000000",
                "PERCENT-RH"
            ],
            ["25", "CFM", "1.699010", "M3/H", "0.588578", "CFM"],
            [
                "26", "IN-WATER", "25.400000", "MM-WATER", "0.039370",
                "IN-WATER"
            ],
            ["27", "LB/SQFT", "4.882400", "KG/M2", "0.204817", "LB/SQFT"],
            ["28", "KW", "1.000000", "KW", "1.000000", "KW"],
            ["29", "W/SQFT", "10.763920", "W/M2", "0.092903", "W/SQFT"],
            ["30", "THERMS", "25.000000", "THERMIES", "0.040000", "THERMS"],
            ["31", "KNOTS", "0.514440", "M/SEC", "1.943861", "KNOTS"],
            [
                "32",
                "HR-SQFT-F /BTU",
                "0.176228",
                "M2-K /W",
                "5.674467",
                "HR-SQFT-F /BTU",
            ],
            ["33", "$DOLLARS", "1.000000", "$DOLLARS", "1.000000", "$DOLLARS"],
            ["34", "MBTU/HR", "0.293000", "MWATT", "3.412969", "MBTU/HR"],
            ["35", "YEARS", "1.000000", "YEARS", "1.000000", "YEARS"],
            ["36", "$/HR", "1.000000", "$/HR", "1.000000", "$/HR"],
            [
                "37", "HRS/YEARS", "1.000000", "HRS/YEARS", "1.000000",
                "HRS/YEARS"
            ],
            ["38", "PERCENT", "1.000000", "PERCENT", "1.000000", "PERCENT"],
            ["39", "$/MONTH", "1.000000", "$/MONTH", "1.000000", "$/MONTH"],
            [
                "40",
                "GALLONS/MIN/TON",
                "1.078000",
                "LITERS/MIN/KW",
                "0.927644",
                "GALLONS/MIN/TON",
            ],
            ["41", "BTU/LB", "0.645683", "WH/KG", "1.548748", "BTU/LB"],
            [
                "42",
                "LBS/SQIN-GAGE",
                "68.947571",
                "MBAR-GAGE",
                "0.014504",
                "LBS/SQIN-GAGE",
            ],
            ["43", "$/UNIT", "1.000000", "$/UNIT", "1.000000", "$/UNIT"],
            [
                "44",
                "BTU/HR/PERSON",
                "0.293000",
                "W/PERSON",
                "3.412969",
                "BTU/HR/PERSON",
            ],
            ["45", "LBS/LB", "1.000000", "KGS/KG", "1.000000", "LBS/LB"],
            ["46", "BTU/BTU", "1.000000", "KWH/KWH", "1.000000", "BTU/BTU"],
            ["47", "LBS/KW", "0.453590", "KG/KW", "2.204634", "LBS/KW"],
            ["48", "REV/MIN", "1.000000", "REV/MIN", "1.000000", "REV/MIN"],
            ["49", "KW/TON", "1.000000", "KW/TON", "1.000000", "KW/TON"],
            ["50", "MBTU", "0.293000", " MWH", "3.412969", "MBTU"],
            ["51", " GAL", "3.785410", "LITER", "0.264172", " GAL"],
            ["52", "GAL/MIN", "3.785410", "LITERS/MIN", "0.264172", "GAL/MIN"],
            ["53", "BTU/F", "1897.800049", "J/K", "0.000527", "BTU/F"],
            ["54", "KWH", "1.000000", "KWH", "1.000000", "KWH"],
            [
                "55", "$/UNIT-HR", "1.000000", "$/UNIT-HR", "1.000000",
                "$/UNIT-HR"
            ],
            ["56", "KW/CFM", "0.588500", "KW/M3/HR", "1.699235", "KW/CFM"],
            [
                "57", "BTU/SQFT-F", "20428.400391", "J/M2-K", "0.000049",
                "BTU/SQFT-F"
            ],
            ["58", "HR/HR", "1.000000", "HR/HR", "1.000000", "HR/HR"],
            ["59", "BTU/FT-F", "6226.479980", "J/M-K", "0.000161", "BTU/FT-F"],
            ["60", "R", "0.555556", "K", "1.799999", "R"],
            ["61", "INCH MER", "33.863800", "MBAR", "0.029530", "INCH MER"],
            [
                "62",
                "UNITS/GAL/MIN",
                "0.264170",
                "UNITS/LITER/MIN",
                "3.785441",
                "UNITS/GAL/MIN",
            ],
            [
                "63",
                "(HR-SQFT-F/BTU)2",
                "0.031056",
                "(M2-K /W)2",
                "32.199585",
                "(HR-SQFT-F/BTU)2",
            ],
            ["64", "KBTU/HR", "0.293000", "KW", "3.412969", "KBTU/HR"],
            ["65", "KBTU", "0.293000", "KWH", "3.412969", "KBTU"],
            ["66", "CFM", "0.471900", "L/S", "2.119093", "CFM"],
            ["67", "CFM/SQFT", "18.288000", "M3/H-M2", "0.054681", "CFM/SQFT"],
            ["68", " 1/R", "1.799900", " 1/K", "0.555586", " 1/R"],
            ["69", "1/KNOT", "1.943860", "SEC/M", "0.514440", "1/KNOT"],
            [
                "70", "FOOTCANDLES", "10.763910", " LUX", "0.092903",
                "FOOTCANDLES"
            ],
            [
                "71", "FOOTLAMBERT", "3.426259", "CANDELA/M2", "0.291864",
                "FOOTLAMBERT"
            ],
            [
                "72",
                "LUMEN / WATT",
                "1.000000",
                "LUMEN / WATT",
                "1.000000",
                "LUMEN / WATT",
            ],
            [
                "73", "KBTU/SQFT-YR", "3.152480", "KWH/M2-YR", "0.317211",
                "KBTU/SQFT-YR"
            ],
            [
                "74", "F (DELTA)", "0.555556", "C (DELTA)", "1.799999",
                "F (DELTA)"
            ],
            ["75", "BTU/DAY", "0.012202", "WATT", "81.953773", "BTU/DAY"],
            ["76", "$/YEAR", "1.000000", "$/YEAR", "1.000000", "$/YEAR"],
            [
                "77", "BTU/WATT", "0.293000", "WATT/WATT", "3.412969",
                "BTU/WATT"
            ],
            ["78", "RADIANS", "1.000000", "RADIANS", "1.000000", "RADIANS"],
            [
                "79", "WATT/BTU", "3.413000", "WATT/WATT", "0.292997",
                "WATT/BTU"
            ],
            ["80", "BTU", "0.000293", "KWH", "3412.969482", "BTU"],
            ["81", "WATT", "1.000000", "WATT", "1.000000", "WATT"],
            ["82", "LUMENS", "1.000000", "LUMENS", "1.000000", "LUMENS"],
            [
                "83", "BTU/HR-FT-R2", "3.115335", "W/M-K2", "0.320993",
                "BTU/HR-FT-R2"
            ],
            ["84", "LB/FT-S", "1.488163", "KG/M-S", "0.671969", "LB/FT-S"],
            [
                "85", "LB/FT-S-R", "2.678693", "KG/M-S-K", "0.373316",
                "LB/FT-S-R"
            ],
            [
                "86", "LB/CUFT-R", "28.833212", "KG/M3-K", "0.034682",
                "LB/CUFT-R"
            ],
            [
                "87", "BTU/HR-FT-R", "1.730741", "W/M-K", "0.577787",
                "BTU/HR-FT-R"
            ],
            ["88", "THERM", "2.831700", "M3", "0.353145", "THERM"],
            ["89", "THERM/HR", "2.831700", "M3/HR", "0.353145", "THERM/HR"],
            ["90", "TON", "0.907180", "TONNE", "1.102317", "TON"],
            ["91", "TON/HR", "0.907180", "TONNE/HR", "1.102317", "TON/HR"],
            ["92", "BTU/UNIT", "1.000000", "BTU/UNIT", "1.000000", "BTU/UNIT"],
            ["93", "$", "1.000000", "$", "1.000000", "$"],
            [
                "94", "KW/GAL/MIN", "0.264170", "KW/LITER/MIN", "3.785441",
                "KW/GAL/MIN"
            ],
            [
                "95", "CUFT/GAL", "0.448831", "M3-MIN/H-LITERS", "2.228010",
                "CUFT/GAL"
            ],
            ["96", "MINUTES", "1.000000", "MINUTES", "1.000000", "MINUTES"],
            ["97", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["98", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["99", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["100", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["101", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["102", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["103", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["104", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["105", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["106", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["107", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["108", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["109", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["110", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["111", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["112", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            [
                "113", "BTU-F/BTU", "0.555560", "KWH-C/KWH", "1.799986",
                "BTU-F/BTU"
            ],
            ["114", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["115", "VOLTS", "1.000000", "VOLTS", "1.000000", "VOLTS"],
            ["116", "C", "1.000000", "C", "1.000000", "C"],
            ["117", "AMPS", "1.000000", "AMPS", "1.000000", "AMPS"],
            ["118", "VOLTS/C", "1.000000", "VOLTS/C", "1.000000", "VOLTS/C"],
            ["119", "1/C", "1.000000", "1/C", "1.000000", "1/C"],
            ["120", "FT/MIN", "0.005080", "M/S", "196.850388", "FT/MIN"],
            [
                "121", "GAL/MIN", "227.160004", "LITERS/HR", "0.004402",
                "GAL/MIN"
            ],
            ["122", "KW/CFM", "588.500000", "W/M3/HR", "0.001699", "KW/CFM"],
            ["123", "BTU/HR-F", "0.000527", "KW/C", "1896.892578", "BTU/HR-F"],
            ["124", "HP", "0.102000", "kW", "9.803922", "HP"],
            ["125", "CFM/TON", "0.483200", "(M3/H)/KW", "2.069536", "CFM/TON"],
            ["126", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["127", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["128", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["129", "UNUSED", "1.000000", "UNUSED", "1.000000", "UNUSED"],
            ["130", "1/VOLTS", "1.000000", "1/VOLTS", "1.000000", "1/VOLTS"],
            [
                "131", "(C-M2)/W", "1.000000", "(C-M2)/W", "1.000000",
                "(C-M2)/W"
            ],
            [
                "132",
                "(C-M-SEC)/W",
                "1.000000",
                "(C-M-SEC)/W",
                "1.000000",
                "(C-M-SEC)/W",
            ],
            ["133", "W/M2", "1.000000", "W/M2", "1.000000", "W/M2"],
            [
                "134", "TDV-MBTUH", "0.293000", "TDV-MW", "3.412969",
                "TDV-MBTUH"
            ],
            ["135", "TDV-MBTU", "0.293000", "TDV-MWH", "3.412969", "TDV-MBTU"],
            [
                "136",
                "TDV-KBTU/KWH",
                "0.293000",
                "TDV-KWH/KWH",
                "3.412969",
                "TDV-KBTU/KWH",
            ],
            [
                "137",
                "TDV-KBTU/THERM",
                "0.010000",
                "TDV-KWH/KWH",
                "100.000000",
                "TDV-KBTU/THERM",
            ],
            ["138", "FT2/HR", "0.092903", "M2/SEC", "10.763915", "FT2/HR"],
            ["139", "GPM", "0.063100", "L/S", "15.847859", "GPM"],
            ["140", "FT/S", "0.304800", "M/S", "3.280840", "FT/S"],
            [
                "141", "HR-FT-F/BTU", "0.577800", "M-K/W", "1.730703",
                "HR-FT-F/BTU"
            ],
        ]

    def tearDown(self):
        pass

    def test_parse_es_d(self):
        self.assertSequenceEqual(parse_lv_m(self.report), self.report_csv)
