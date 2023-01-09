# multiprocess_get_sum
Get a number list which sum is euqal to a specifical number from a multiple data set.

# example
```python
test_sum = [1,2,3,4,5,6]
sum_num = 10
specify_num = 3
process_num = 3
start_multiprocessing_compose_num(sum_num, test_sum, process_num, specify_num)
while MultiProcess.try_get_compute_result() != True:
    time.sleep(1)
MultiProcess.kill_all_child_processes()
```
