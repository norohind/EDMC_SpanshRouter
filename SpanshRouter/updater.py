import os
import requests
import zipfile
import sys
import traceback
import json

import logging
from config import appname

# We need a name of plugin dir, not SpanshRouter.py dir
plugin_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
logger = logging.getLogger(f'{appname}.{plugin_name}')


class SpanshUpdater():
    def __init__(self, version, plugin_dir):
        self.version = version
        self.zip_name = "EDMC_SpanshRouter_" + version.replace('.', '') + ".zip"
        self.plugin_dir = plugin_dir
        self.zip_path = os.path.join(self.plugin_dir, self.zip_name)
        self.zip_downloaded = False
        self.changelogs = self.get_changelog()

    def download_zip(self):
        url = 'https://github.com/CMDR-Kiel42/EDMC_SpanshRouter/releases/download/v' + self.version + '/' + self.zip_name

        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(self.zip_path, 'wb') as f:
                    logger.info(f"Downloading SpanshRouter to {self.zip_path}")
                    f.write(os.path.join(r.content))
                self.zip_downloaded = True
            else:
                logger.warning("Failed to fetch SpanchRouter update. Status code: " + str(r.status_code))
                self.zip_downloaded = False
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.warning(''.join('!! ' + line for line in lines))
            self.zip_downloaded = False
        finally:
            return self.zip_downloaded

    def install(self):
        if self.download_zip():
            try:
                with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.plugin_dir)

                os.remove(self.zip_path)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                logger.warning(''.join('!! ' + line for line in lines))
        else:
            logger.warning("Error when downloading the latest SpanshRouter update")

    def get_changelog(self):
        url = "https://api.github.com/repos/CMDR-Kiel42/EDMC_SpanshRouter/releases/latest"
        try:
            r = requests.get(url, timeout=2)
            
            if r.status_code == 200:
                # Get the changelog and replace all breaklines with simple ones
                changelogs = json.loads(r.content)["body"]
                changelogs = "\n".join(changelogs.splitlines())
                return changelogs

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.warning(''.join('!! ' + line for line in lines))
