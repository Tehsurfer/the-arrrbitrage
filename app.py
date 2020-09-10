from flask import Flask, render_template, make_response
import threading
import time
import sys
from settings import PATH as Path
import settings
import ArbitrageMain
app = Flask(__name__, static_url_path='')
test_result = 'failed'
arb_main = ArbitrageMain.ArbMain()


@app.route('/')
def index():
    return arb_main.html

@app.route('/margins')
def margins():
    return arb_main.margin_table

@app.route('/margins-depth')
def margins_depth():
    return arb_main.margin_table_depth

@app.route('/thread-test')
def thread_test():
    global test_result
    return test_result

@app.route('/api/margins-with-depth')
def api_with_depth():
    r = make_response(arb_main.json_export_with_depth)
    r.mimetype = 'application/json'
    return r

@app.route('/api/margins-no-depth')
def api_no_depth():
    r = make_response(arb_main.json_export_no_depth)
    r.mimetype = 'application/json'
    return r

def thread_testy():
    time.sleep(10)
    print('Thread is printing to console')
    sys.stdout.flush()
    global test_result
    test_result = 'passed'
    return

def start_app():
    threading.Thread(target=app.run).start()

# Time in seconds
DOWNTIME = settings.RUNTIME + 1
Path = settings.PATH

def run_arb_if_down():
    global arb_main
    for i in range(0, 1000000):
        filename = 'check.txt'
        f = open(Path / filename, "r")
        line = f.readline()
        print(line)
        f.close()
        if (time.time() - float(line)) > DOWNTIME:
            print('REBOOTING THE ARBITRAGE')
            try:
                arb_main.start()
            except Exception as e:
                print(f'ARBITRAGE hit an error: {e}')
                pass
        else:
            print('ARBITRAGE IS STILL RUNNING')
            print('waiting the following seconds:')
            print(DOWNTIME)
        print('program was checked if running at' + time.strftime('%X %x %Z'))
        time.sleep(DOWNTIME)

threading.Thread(target=thread_testy).start()
threading.Thread(target=run_arb_if_down).start()

if __name__ == "__main__":
    start_app()


