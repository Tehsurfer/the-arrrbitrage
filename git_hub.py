#git_hub.py is used to update all github file for the git projec: 'hugo-contrarian'
import base64
import settings
from shutil import copyfile
import os

Path = settings.PATH


class git_hub:
    def __init__(self):
        pass

    def update(self):
        file_list = [
            os.path.join(Path, 'index.html'),
            os.path.join(Path,  'margin_table.html'),
            os.path.join(Path,  'margin_table_with_depth.html'),
        ]

        file_names = [
            '/var/www/html/arbs/index.html',
            '/var/www/html/arbs/margin-table/index.html',
            '/var/www/html/arbs/margin-table-depth/index.html',
        ]

        for i, source_file in enumerate(file_list):
            copyfile(source_file, file_names[i])
