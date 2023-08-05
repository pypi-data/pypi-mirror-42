# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
from pathlib import Path
import yaml
import sys

from release_bot.version import __version__


class Configuration:
    # note that required items need to reference strings as their length is checked
    REQUIRED_ITEMS = {"conf": ['repository_name', 'repository_owner', 'github_token'],
                      "release-conf": ['python_versions']}

    def __init__(self):
        self.version = __version__
        self.repository_name = ''
        self.repository_owner = ''
        self.github_token = ''
        self.github_username = ''
        self.refresh_interval = 3 * 60
        self.debug = False
        self.configuration = ''
        self.keytab = ''
        self.fas_username = ''
        self.logger = None
        self.set_logging()
        # configuration when bot is deployed as github app
        self.github_app_installation_id = ''
        self.github_app_id = ''
        self.github_app_cert_path = ''

    def set_logging(self,
                    logger_name="release-bot",
                    level=logging.INFO,
                    handler_class=logging.StreamHandler,
                    handler_kwargs=None,
                    msg_format='%(asctime)s.%(msecs).03d %(filename)-17s %(levelname)-6s %(message)s',
                    date_format='%H:%M:%S'):
        """
        Set personal logger for this library.
        :param logger_name: str, name of the logger
        :param level: int, see logging.{DEBUG,INFO,ERROR,...}: level of logger and handler
        :param handler_class: logging.Handler instance, default is StreamHandler (/dev/stderr)
        :param handler_kwargs: dict, keyword arguments to handler's constructor
        :param msg_format: str, formatting style
        :param date_format: str, date style in the logs
        :return: logger instance
        """
        logger = logging.getLogger(logger_name)
        # do we want to propagate to root logger?
        # logger.propagate = False
        logger.setLevel(level)

        if not [x for x in logger.handlers if isinstance(x, handler_class)]:
            handler_kwargs = handler_kwargs or {}
            handler = handler_class(**handler_kwargs)

            formatter = logging.Formatter(msg_format, date_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger

    def load_configuration(self):
        """Load bot configuration from .yaml file"""
        if not self.configuration:
            # configuration not supplied, look for conf.yaml in cwd
            path = Path.cwd() / 'conf.yaml'
            if path.is_file():
                self.configuration = path
            else:
                self.logger.error("Cannot find valid configuration")
                sys.exit(1)
        with self.configuration.open() as ymlfile:
            file = yaml.safe_load(ymlfile)
        for key, value in file.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # check if required items are present
        for item in self.REQUIRED_ITEMS['conf']:
            if item not in file:
                self.logger.error(f"Item {item!r} is required in configuration!")
                sys.exit(1)
        self.logger.debug(f"Loaded configuration for {self.repository_owner}/{self.repository_name}")

    def load_release_conf(self, conf):
        """
        Load items from release-conf.yaml

        :param conf: contents of release-conf.yaml
        :return dict with configuration
        """
        if not conf:
            self.logger.error("No release-conf.yaml found in "
                              f"{self.repository_owner}/{self.repository_name} repository root!\n"
                              "You have to add one for releasing to PyPi/Fedora")
            if self.REQUIRED_ITEMS['release-conf']:
                sys.exit(1)

        parsed_conf = yaml.safe_load(conf) or {}
        parsed_conf = {k: v for (k, v) in parsed_conf.items() if v}
        for item in self.REQUIRED_ITEMS['release-conf']:
            if item not in parsed_conf:
                self.logger.error(f"Item {item!r} is required in release-conf!")
                sys.exit(1)
        for index, version in enumerate(parsed_conf.get('python_versions', [])):
            parsed_conf['python_versions'][index] = int(version)
        for index, branch in enumerate(parsed_conf.get('fedora_branches', [])):
            parsed_conf['fedora_branches'][index] = str(branch)
        for index, label in enumerate(parsed_conf.get('labels', [])):
            parsed_conf['labels'][index] = str(label)
        if parsed_conf.get('fedora') and not self.fas_username:
            self.logger.warning("Can't release to fedora if there is no FAS username, disabling")
            parsed_conf['fedora'] = False
        if parsed_conf.get('trigger_on_issue') and not self.github_username:
            msg = "Can't trigger on issue if 'github_username' is not known, disabling"
            self.logger.warning(msg)
            parsed_conf['trigger_on_issue'] = False

        return parsed_conf


configuration = Configuration()
