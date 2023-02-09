import threading
from dataclasses import dataclass

DINNING_HALL_PORT = 8080
KITCHEN_PORT = 8081

## Definim Structura Datelor Trimise
@dataclass
class Task:
    destination: str
## Atribuim valori (set)
    @staticmethod
    def dict2task(d: dict):
        return Task(
            destination=d['destination']
        )
## Returneaza datele (get)
    def task2dict(self):
        return {
            'destination': self.destination
        }
