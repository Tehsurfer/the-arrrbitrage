#save_files.py is used to copy files form data to templates to show on flask server
import base64
import settings
from shutil import copyfile
import os

Path = settings.PATH


class save_files:
    def __init__(self):
        pass

    def update_templates(self):
        file_list = [
            (Path / 'index.html'),
            (Path / 'margin_table.html'),
            (Path / 'margin_table_with_depth.html'),
        ]

        file_names = [
            (Path / '../templates/index.html'),
            (Path / '../templates/margin_table.html'),
            (Path / '../templates/margin_table_with_depth.html'),
        ]

        for i, source_file in enumerate(file_list):
            copyfile(source_file, file_names[i])


    def update_data(self, fileStr, html='', html2=''):
        # Update files
        g = open(Path / "index.html", "w")
        html_text = '<pre>' + fileStr + '</pre>'
        g.write(html_text)

        f = open(Path / 'margin_table_with_depth.html', 'w')
        f.write(html)
        f.close()

        h = open(Path / 'margin_table.html', 'w')
        h.write(html2)
        h.close()