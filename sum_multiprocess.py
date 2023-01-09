from multiprocessing import Process, Queue
import queue
from random import shuffle
import random
from copy import deepcopy
from functools import update_wrapper
import time

class return_decorator_instance:
    def __init__(self, target):
        '''
        prevent using decorator to raise a "unpickled" exception
        '''
        self.target = target
        try:
            update_wrapper(self, target)
        except:
            pass

    def __call__(self, queue, *args):
        queue.put(False)
        self.target(*args)
        queue.put(True)

class MultiProcess:
    process_set = []
    inter_process_queue = Queue()
    @staticmethod
    def create_process(callback, *args):
        instance = MultiProcess.get_callback_decorator(callback)
        child_process = Process(target=instance, args=(MultiProcess.inter_process_queue, *args,))
        child_process.start()
        MultiProcess.process_set.append(child_process)

    @staticmethod
    def kill_all_child_processes():
        for i in MultiProcess.process_set:
            i.terminate()
            MultiProcess.process_set.remove(i)

    @staticmethod
    def try_get_compute_result():
        for i in MultiProcess.process_set:
            try:
                if MultiProcess().inter_process_queue.empty() == False:
                    if MultiProcess.inter_process_queue.get(block=False) != True:
                        pass
                    else:
                        return True
                else:
                    pass
            except queue.Empty:
                print("inter-process queue is empty")
        return False

    @staticmethod
    def all_child_process_join():
        for i in MultiProcess.process_set:
            i.join()

    @staticmethod
    def get_callback_decorator(func):
        return return_decorator_instance(func)

def get_random_list(data_set, split_range = None):
    '''
    data_set: list
    split_range: list, example: [0, 10]
    '''
    if split_range == None:
        shuffle(data_set)
        return data_set
    else:
        choose_num = random.randint(split_range[0], split_range[1])
        item = data_set[choose_num]
        copy_data_set = deepcopy(data_set)
        create_data_set = []
        create_data_set.append(item)
        copy_data_set.pop(choose_num)
        shuffle(copy_data_set)
        create_data_set.extend(copy_data_set)
        return create_data_set

def compose_num(sum_num, data_set, specify_num = 0):
    temp_total_check_num = 0.0
    fulfilled_num_set = []

    for i in data_set:
        temp_total_check_num += i
        if (temp_total_check_num + specify_num) == sum_num:
            print("congratulation, get a number set fulfilled the requirement!!!")
            fulfilled_num_set.append(i)
            fulfilled_num_set.append(specify_num)
            print(f"{fulfilled_num_set}")
            return fulfilled_num_set
        elif (temp_total_check_num + specify_num) < sum_num:
            fulfilled_num_set.append(i)
        elif (temp_total_check_num + specify_num) > sum_num:
            fulfilled_num_set.clear()
            temp_total_check_num = 0.0
    return None

def create_compose_number(range_index_list, total_data_set, sum_num, specify_num = 0):
    while 1:
        shuffled_data_set = get_random_list(total_data_set, range_index_list)
        result = compose_num(sum_num, shuffled_data_set, specify_num)
        if result != None:
            return result

def start_multiprocessing_compose_num(sum_num, total_data_set, process_num = 1, specify_num = 0):
    span_size = int(len(total_data_set) / process_num)
    for i in range(process_num):
        if i != process_num - 1 :
            range_index_list = [i * span_size, (i + 1) * span_size - 1]
        else:
            range_index_list = [i * span_size, len(total_data_set) - 1]
        MultiProcess.create_process(create_compose_number, range_index_list, total_data_set, sum_num, specify_num)
