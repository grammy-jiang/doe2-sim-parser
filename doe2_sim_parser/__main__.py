import logging
import argparse

from doe2_sim_parser.parse_report_beps import parse_beps
from doe2_sim_parser.parse_report_bepu import parse_bepu
from doe2_sim_parser.parse_report_es_d import parse_es_d
from doe2_sim_parser.split_sim import split_sim
from doe2_sim_parser.update_google_spreadsheet import update_report

logging.basicConfig()
logger = logging.getLogger(__name__)

PARSERS = {"BEPS": parse_beps, "BEPU": parse_bepu, "ES-D": parse_es_d}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse SIM reports, and upload the parsed reports to "
                    "Google Spreadsheet.")
    parser.add_argument("-s", "--sim", help="the path to sim file")

    return parser.parse_args()


def main():
    args = parse_args()

    logger.info('Receive sim: %s', args.sim)

    sim = split_sim(args.sim)

    for report in sim.normal_reports:
        if report.code in PARSERS:
            logger.info('Start parsing the report %s', report.code + ' ' + report.name)
            parsed_report = PARSERS[report.code](report.report)

            logger.info('Start update the report %s on Google Spreadsheet.', report.code + ' ' + report.name)
            update_report(report=report._replace(report=parsed_report))


if __name__ == "__main__":
    main()
