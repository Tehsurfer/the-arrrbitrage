import json
import time

class ExportAPI:

    def __init__(self):
        self.output = {
            'last_run': 0,
            'results': {}
        }

    def update_results(self, coin, margins, names):
        self.output['results'][coin] = {}
        for i, buy_name in enumerate(names):
            self.output['results'][coin][buy_name] = {}
            for j, sell_name in enumerate(names):
                self.output['results'][coin][buy_name][sell_name] = margins[i][j]
        self.output['last_run'] = str(time.time())

    def export(self):
        return json.dumps(self.output)
