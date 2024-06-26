"""
@file main_window.py
@author Sherif Adel
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024 - May 11, 2024
"""

from dataclasses import dataclass
from typing_extensions import override
from copy import deepcopy

@dataclass
class Schedule:
    process_name : str
    start : int
    duration : int


@dataclass
class Process:
    name : str
    arrival : int
    burst : int
    priority : int


class ProcessScheduler:
    @staticmethod
    def schedule(processes : list[Process], quantum: int) -> list[Schedule]:
        answer : list[Schedule] = []
        return answer

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def peek(self):
        """Return the item at the front of the queue without removing it."""
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Queue is empty")


class FCFSScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process], quantum: int) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = 0
        while True:
            possible_processes = [process for process in processes if \
                    process.burst > 0]

            if not possible_processes:
                break
            ready_processes = [process for process in possible_processes if \
                    process.arrival <= current_time]            
            if not ready_processes:
                current_time += 1
                continue
            best_process = min(ready_processes, 
                               key=lambda process: process.arrival)
            schedules.append(
                    Schedule(
                        process_name=best_process.name,
                        start=current_time,
                        duration=best_process.burst,
                        )
                    )
            current_time += best_process.burst
            best_process.burst = 0
        return schedules


class LPFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process], quantum: int) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = 0
        while True:
            possible_processes = [process for process in processes if \
                    process.burst > 0]

            if not possible_processes:
                break
            ready_processes = [process for process in possible_processes if \
                    process.arrival <= current_time]            
            if not ready_processes:
                current_time += 1
                continue
            best_process = min(ready_processes, 
                               key=lambda process: process.priority)
            schedules.append(
                    Schedule(
                        process_name=best_process.name,
                        start=current_time,
                        duration=best_process.burst,
                        )
                    )
            current_time += best_process.burst
            best_process.burst = 0
        return schedules


class SRTFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process], quantum: int) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = 0
        while True:
            possible_processes = [process for process in processes if \
                    process.burst > 0]

            if not possible_processes:
                break
            ready_processes = [process for process in possible_processes if \
                    process.arrival <= current_time]            
            if not ready_processes:
                current_time += 1
                continue
            best_process = min(ready_processes, 
                               key=lambda process: process.burst)
            schedules.append(
                    Schedule(
                        process_name=best_process.name,
                        start=current_time,
                        duration=best_process.burst,
                        )
                    )
            current_time += best_process.burst
            best_process.burst = 0
        return schedules


class LPFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process], quantum: int):
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = -1
        while True:
            possible_processes = [process for process in processes if \
                    process.burst > 0]
            if not possible_processes:
                break
            current_time += 1
            ready_processes = [process for process in possible_processes if \
                    process.arrival <= current_time]            
            if not ready_processes:
                continue
            best_process = min(ready_processes, 
                            key=lambda process: process.priority)
            best_process.burst -= 1
            if schedules and schedules[-1].process_name == best_process.name:
                schedules[-1].duration += 1
            else:
                schedules.append(
                        Schedule(
                            process_name=best_process.name,
                            start=current_time,
                            duration=1,
                            )
                        )
        return schedules


class SRTFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process], quantum: int):
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = -1
        while True:
            possible_processes = [process for process in processes if \
                    process.burst > 0]
            if not possible_processes:
                break
            current_time += 1
            ready_processes = [process for process in possible_processes if \
                    process.arrival <= current_time]            
            if not ready_processes:
                continue
            best_process = min(ready_processes, 
                            key=lambda process: process.burst)
            best_process.burst -= 1
            if schedules and schedules[-1].process_name == best_process.name:
                schedules[-1].duration += 1
            else:
                schedules.append(
                        Schedule(
                            process_name=best_process.name,
                            start=current_time,
                            duration=1,
                            )
                        )
        return schedules


class RRScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes: list[Process], quantum: int) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules: list[Schedule] = []
        current_time = 0
        schedule_duration = 0
        process_queue = Queue()
        # Sort the list to make the first elements is the elements nearest 
        # to our current time which start from zero
        processes = sorted(processes, key=lambda process: process.arrival)
        
        while processes or not process_queue.is_empty():
            while processes and processes[0].arrival <= current_time:
                process_queue.enqueue(processes.pop(0))
            
            if not process_queue.is_empty():
                current_process = process_queue.dequeue()
                schedule_duration = min(quantum, current_process.burst)
                if schedules and \
                        schedules[-1].process_name == current_process.name:
                    schedules[-1].duration += schedule_duration
                else:
                    schedules.append(
                            Schedule(
                                process_name=current_process.name,
                                start=current_time,
                                duration=schedule_duration,
                                )
                            )
                current_time += schedule_duration
                current_process.burst -= schedule_duration
                while processes and processes[0].arrival <= current_time:
                    process_queue.enqueue(processes.pop(0))
                # Add back to the queue if burst time is remaining
                if current_process.burst > 0:
                    process_queue.enqueue(current_process)
            else:
                current_time += 1
        return schedules


PROCESS_SCHEDULERS_DICT = {
        'FCFS': FCFSScheduler(),
        'LPF-NP': LPFNonPreemptiveScheduler(),
        'LPF-P': LPFPreemptiveScheduler(),
        'SRTF-NP': SRTFNonPreemptiveScheduler(),
        'SRTF-P': SRTFPreemptiveScheduler(),
        'RR': RRScheduler(),
        }

def get_process_scheduler_key(process_scheduler : ProcessScheduler):
    for key in PROCESS_SCHEDULERS_DICT.keys():
        if process_scheduler == PROCESS_SCHEDULERS_DICT[key]:
            return key
