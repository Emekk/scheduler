import csv

from schedule import Schedule
from interval import timestamp_to_interval
from task import Task


DAY_START = "06:30"
DAY_END = "23:30"
DAY_LABELS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# set schedule up
planning_horizon = timestamp_to_interval(DAY_START, DAY_END, DAY_START)
minutes = int(DAY_START.split(':')[0]) * 60 + int(DAY_START.split(':')[1])
time_labels = [f"{m//60:02}:{m % 60:02}" for m in range(minutes, minutes + planning_horizon.width + 1, 30)]

sch = Schedule(planning_horizon, 7)
with open("tasks.csv", "r") as file:
    items = csv.DictReader(file)
    for item in items:
        interval = timestamp_to_interval(item["START"], item["END"], DAY_START)
        task = Task(int(item["ID"]), item["NAME"], int(item["DAY"]), interval)
        sch.add_task(task)

# display the weekly time allocation for each task 
allocation = sorted(sch.time_allocation.items(), key=lambda x: x[1], reverse=True)
for alloc in allocation:
    hours = alloc[1] / 60
    print(f"{alloc[0]:<12} {hours:.2f} hours")

# display the schedule as gantt chart
sch.display(day_labels=DAY_LABELS,
            time_labels=time_labels,
            ytickrotation=90,
            xtickrotation=90,
            save_file="schedule.png",
            tasklabel_fontsize=12,
            dpi=300)