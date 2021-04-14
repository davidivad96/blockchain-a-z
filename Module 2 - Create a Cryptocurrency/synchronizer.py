import requests
import time


def synchronize_all_nodes():
    print('Synchronizing nodes...')
    network = {'localhost:5001', 'localhost:5002', 'localhost:5003'}
    for node in network:
        requests.get(f'http://{node}/synchronize')


start_time = time.time()
while True:
    synchronize_all_nodes()
    time.sleep(5.0 - ((time.time() - start_time) % 5.0))
