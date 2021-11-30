"""Main project class."""
"""
   Copyright 2021 Deutsche Telekom AG

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import argparse
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import List

from onapsdk.onap_service import OnapService  # type: ignore

from onap_data_provider.config_parser import ConfigParser


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "odp": {
                "class": "logging.Formatter",
                "format": "%(asctime)s [%(levelname)s] %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": os.getenv("LOGGING_LEVEL", "INFO").upper(),
                "formatter": "odp",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "filename": "odp.log",
                "mode": "w",
                "formatter": "odp",
            },
        },
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["console", "file"]},
        },
    }
)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="ONAP data provider"
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=Path,
        action="append",
        dest="infra_files",
        required=True,
        help="Path to the infra file which describes resources to create. Can be directory as well",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Doesn't create any resources - checks only if data in infra file has valid format",
    )
    parser.add_argument(
        "--proxy",
        nargs="*",
        help="Setup proxy connection with given url. Provide full URL with protocol, eg. http://localhost:8080",
    )
    return parser


def run() -> None:
    """Project main function."""
    parser: argparse.ArgumentParser = create_parser()
    args: argparse.Namespace = parser.parse_args()
    if args.proxy:
        OnapService.set_proxy(
            {url.split("://")[0]: url.split("://")[1] for url in args.proxy}
        )
    conf_parser = ConfigParser(args.infra_files)
    conf_parser.validate()
    if args.validate_only:
        print("Input data is valid!")
        sys.exit(0)
    for x in conf_parser.parse():
        x.create()


if __name__ == "__main__":
    run()
