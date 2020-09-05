from flask import Flask, render_template
import threading
import time
import sys
import RunArbIfDown
app = Flask(__name__, static_url_path='')
test_result = 'failed'

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
def return_thread_test():
    global test_result
    return test_result

def thread_test():
    time.sleep(10)
    print('Thread is printing to console')
    sys.stdout.flush()
    global test_result
    test_result = 'passed'
    return




if __name__ == "__main__":
    print('Logging is working')
    sys.stdout.flush()

    threading.Thread(target=app.run).start()
    threading.Thread(target=thread_test).start()
    threading.Thread(target=RunArbIfDown.start).start()