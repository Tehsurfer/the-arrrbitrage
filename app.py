from flask import Flask, render_template
import threading
import time
import RunArbIfDown
app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/margins')
def margins():
    return render_template('margin_table.html')

@app.route('/margins-depth')
def margins_depth():
    return render_template('margin_table_with_depth.html')

def thread_test():
    time.sleep(10)
    print('Thread is printing to console')


if __name__ == "__main__":
    threading.Thread(target=thread_test).start()
    threading.Thread(target=app.run).start()
    threading.Thread(target=RunArbIfDown.start).start()