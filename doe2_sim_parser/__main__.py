import argparse
import logging
from collections import defaultdict

from doe2_sim_parser.parse_hourly_report import parse_hourly_report
from doe2_sim_parser.parse_report_beps import parse_beps
from doe2_sim_parser.parse_report_bepu import parse_bepu
from doe2_sim_parser.parse_report_es_d import parse_es_d
from doe2_sim_parser.parse_report_ps_e import parse_ps_e
from doe2_sim_parser.split_sim import split_sim
from doe2_sim_parser.update_google_spreadsheet import update_report
from doe2_sim_parser.utils.data_types import Report
from doe2_sim_parser.write_sim import write_sim

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PARSERS = {
    "BEPS": parse_beps,
    "BEPU": parse_bepu,
    "ES-D": parse_es_d,
    "PS-E": parse_ps_e,
    "Hourly Report": parse_hourly_report,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse SIM reports, and upload the parsed reports to "
                    "Google Spreadsheet."
    )
    parser.add_argument(
        "-s", "--sim",
        help="the path to sim file",
        required=True,
        type=str
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logger.info("Receive sim: %s", args.sim)

    sim = split_sim(args.sim)

    write_sim(sim)

    dict_sim_report = defaultdict(list)
    for report in sim.normal_reports:
        dict_sim_report[report.code].append(report)

    for code, reports in dict_sim_report.items():
        if code in PARSERS:
            logger.info(
                "Start parsing the sim report %s",
                "{code}".format(code=code),
            )
            parsed_report = PARSERS[code](reports)
            logger.info(
                "Start update the parsed sim report %s on Google Spreadsheet.",
                "{code}".format(code=code),
            )
            update_report(
                report=Report(
                    type_=reports[0].type_,
                    code=reports[0].code,
                    name=reports[0].name,
                    report=parsed_report,
                    report_no=None,
                    page_no=None
                )
            )

    try:
        parsed_hourly_report = parse_hourly_report(sim.hourly_reports)
        logger.info(
            "Start update the parsed sim hourly report %s on Google Spreadsheet.",
            "{code}".format(code="Hourly Report"),
        )
        update_report(
            report=Report(
                type_='hourly report',
                code=None,
                name='hourly report',
                report=parsed_hourly_report,
                report_no=0,
                page_no=0
            )
        )
    except Exception as exc:
        logger.exception(exc)


if __name__ == "__main__":
    main()
