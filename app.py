from flask import Flask, render_template
import threading
import time
import sys
import RunArbIfDown
app = Flask(__name__, static_url_path='')
test_result = 'failed'

@app.before_first_request
def execute_this():
    threading.Thread(target=thread_testy).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/margins')
def margins():
    return render_template('margin_table.html')

@app.route('/margins-depth')
def margins_depth():
    return render_template('margin_table_with_depth.html')

@app.route('/thread-test')
def thread_test():
    global test_result
    return test_result

def thread_testy():
    time.sleep(10)
    print('Thread is printing to console')
    sys.stdout.flush()
    global test_result
    test_result = 'passed'
    return

def start_app():
    threading.Thread(target=app.run).start()

if __name__ == "__main__":
    start_app()


