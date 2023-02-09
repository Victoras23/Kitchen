import time
import queue
import threading

import requests
from flask import Flask, request

from settings import KITCHEN_PORT, DINNING_HALL_PORT, Task

flask_app = Flask(__name__)
shared_resource = queue.Queue()
OKBLUE = '\033[94m'
ENDC = '\033[0m'
NR_OF_WORKERS = 6

@flask_app.route('/Kitchen', methods=['POST'])
def Kitchen():
    destination = request.get_json()
    task = Task.dict2task(destination)
    print(f'{OKBLUE}Kitchen: Received {task} from Dinning Hall{ENDC}')
    shared_resource.put(task)
    return {'status_code': 200}

class Worker(threading.Thread):
    def run(self):
        while True:
            task: Task = shared_resource.get()
            task.destination = 'DinningHall'
            requests.post(f'http://localhost:{DINNING_HALL_PORT}/DinningHall', json=task.task2dict())

def run():
    threads: list[threading.Thread] = []

    server_thread = threading.Thread(target=lambda: flask_app.run(
        port=KITCHEN_PORT, debug=False, use_reloader=False))
    threads.append(server_thread)

    for _ in range(NR_OF_WORKERS):
        threads.append(Worker())

    for thread in threads:
        thread.start()

run()