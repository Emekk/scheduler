from typing import Sized
from interval import Interval
from task import Task
from schedvis import SchedVis


class Schedule:
    """A Schedule consists of Tasks and provides visualizations such as gantt chart."""
    def __init__(self, planning_horizon: Interval, planning_days: int) -> None:
        self.planning_horizon: Interval = planning_horizon  # an interval representing a planning day in the schedule
        self.planning_days: int = planning_days
        self._schedule: list[list] = [[] for i in range(self.planning_days)]
        self._vis: SchedVis = SchedVis()  # visualization utility
        self.task_enum: dict = {}  # enumerate tasks with unique names
        self.__nunique: int = 0  # number of tasks with unique names
    
    def add_task(self, task: Task) -> bool:
        """Schedule a task maintaining the chronological order of the schedule."""
        # Check if the task is compatible
        if task.day < 0 or task.day >= self.planning_days:
            raise IncompatibleTask(f"Day of the Task {task.id} is not between 0 and {self.planning_days - 1}!")
        if not task.interval.is_in(self.planning_horizon):
            raise IncompatibleTask(f"Task {task.id} is not in the planning horizon!")    
        # Schedule the task
        j = len(self._schedule[task.day]) - 1
        while j >= 0:
            left_task = self._schedule[task.day][j]
            if left_task.interval.overlaps(task.interval):
                raise IncompatibleTask(f"Task {task.id} overlaps with Task {left_task.id}!")
            if left_task.interval.left > task.interval.left:
                j -= 1
            else:
                break
        if task.name not in self.task_enum:
            self.task_enum[task.name] = self.__nunique
            self.__nunique += 1
        self._schedule[task.day].insert(j + 1, task)
        return True

    def __str__(self) -> str:
        result: list = []
        for day in self._schedule:
            result.append('[')
            for task in day:
                result.extend(list(task.name))
                result.append(', ')
            if result[-1] == ', ':
                result[-1] = ']'
            else:
                result.append(']')
            result.append('\n')
        return "".join(result)
    
    @property
    def task_names(self) -> list[list]:
        """Returns each task's name in a 2D list."""
        return [[task.name for task in day] for day in self._schedule]
    
    @property
    def task_ranges(self) -> list[list[tuple]]:
        """Return each task's start time and duration in a 2D list."""
        return [[(task.interval.left, task.interval.width) for task in day] for day in self._schedule]
    
    @property
    def task_ids(self) -> list[list]:
        """Return each task's name in scheduled position."""
        return [[task.id for task in day] for day in self._schedule]
    
    @property
    def color_keys(self) -> list[list]:
        return [[self.task_enum[task.name] / self.__nunique for task in day] for day in self._schedule]

    @property
    def time_allocation(self) -> dict[str, int]:
        """Return a dict of tasks and the weekly time (in minutes) allocated to them."""
        alloc = {}
        for day in self._schedule:
            for task in day:
                if task.name not in alloc:
                    alloc[task.name] = 0
                alloc[task.name] += task.interval.width
        return alloc

    def display(self,
        day_labels: Sized = None,
        time_labels: Sized = None,
        day_height: float = 14,
        day_spacing: float = 2,
        task_colors: list[list[tuple]] = None,
        line_color: tuple = (0, 0, 0, 1),
        line_width: float = 0,
        day_color: tuple = (1, 1, 1, 1),
        tasklabel_color: tuple = (1, 1, 1),
        tasklabel_fontsize: float | None = None,
        xlabel: str = "",
        ylabel: str = "",
        xtickrotation: float = 0,
        ytickrotation: float = 0,
        grid: bool = False,
        figure_size: tuple = None,
        font_size: float = 12,
        xmargin: float = 0,
        padding: float = 1,
        background_color: tuple = (0.90, 0.90, 0.90),
        show: bool = True,
        save_file: str = "",
        dpi: int = 300,
    ) -> None:
        """Displays the schedule as a gantt chart."""
        if day_labels is None:
            day_labels = range(self.planning_days)
        else:
            if len(day_labels) != self.planning_days:
                raise ValueError(f"Length of day_labels must be consistent with planning_days ({self.planning_days})!")
        # set time labels automatically if not provided by user
        if time_labels is None:
            time_labels = range(0, self.planning_horizon.width + 1, 30)
        # set task colors automatically if not provided by user
        if task_colors is None:
            task_colors = [[self._vis.CMAP(key) for key in day] for day in self.color_keys]
        # set figure size automatically if not provided by user
        if figure_size is None:
            figure_size = min(16, self.planning_days * 3.2), min(9, self.planning_days * 1.8)
        # plot gantt_chart
        self._vis.gantt_chart(yticklabels=day_labels, xticklabels=time_labels, xranges=self.task_ranges, bar_height=day_height,
                              bar_spacing=day_spacing, facecolors=task_colors, line_color=line_color, line_width=line_width,
                              horizon_facecolor=day_color, horizon_width=self.planning_horizon.width, bar_labels=self.task_names,
                              bar_label_color=tasklabel_color, bar_label_fontsize=tasklabel_fontsize, xlabel=xlabel, ylabel=ylabel,
                              xtickrotation=xtickrotation, ytickrotation=ytickrotation, grid=grid, figure_size=figure_size,
                              font_size=font_size, xmargin=xmargin, padding=padding, bgcolor=background_color, show=show, 
                              save_file=save_file, dpi=dpi)

class IncompatibleTask(Exception):
    pass
