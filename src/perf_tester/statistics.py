from collections import defaultdict
from math import nan
from typing import Callable, Dict, List, Optional, Tuple

from perf_tester.utils.system_utils import cls
from perf_tester.utils.table_printer import print_table


# --- Metric Functions ---
def default_mean(data: List[float]) -> float:
    n = len(data)
    return nan if n == 0 else sum(data) / n


def default_stddev(data: List[float], ddof: int = 1) -> float:
    n = len(data)
    if n < 2:
        return nan
    mean_val = default_mean(data)
    variance = sum((x - mean_val) ** 2 for x in data) / (n - ddof)
    return variance**0.5


# --- Metric Definition ---
class Metric:
    """
    Defines a single metric with a label, a function to compute it,
    and an optional unit. If a unit is provided, the value is auto-scaled.
    """

    def __init__(
        self,
        label: str,
        func: Callable[[List[float]], float],
        unit: Optional[str] = None,
    ):
        self.label = label
        self.func = func
        self.unit = unit or ""

    def compute(self, data: List[float]) -> float:
        return self.func(data)

    def scale_value(self, value: float) -> Tuple[float, str]:
        if not self.unit:
            return value, ""
        # Define scaling thresholds (for time-based metrics, for example)
        scales = [
            (1e-9, f"n{self.unit}"),
            (1e-6, f"µ{self.unit}"),
            (1e-3, f"m{self.unit}"),
            (1, self.unit),
        ]
        for factor, unit_label in scales:
            if abs(value) < factor * 100:
                return value / factor, unit_label
        return value, self.unit


# --- Stats Container for a Single Data Set ---
class Stats:
    """
    Computes and stores metrics for a given list of data values.
    Both raw and scaled values are kept.
    """

    def __init__(self, data: List[float], metrics: List[Metric]):
        self.data = data
        self.metrics = metrics
        self.results: Dict[str, float] = {}
        self.scaled_results: Dict[str, Tuple[float, str]] = {}
        self.calculate_metrics()

    def calculate_metrics(self) -> None:
        for metric in self.metrics:
            value = metric.compute(self.data)
            self.results[metric.label] = value
            scaled, scale_label = metric.scale_value(value)
            self.scaled_results[metric.label] = (scaled, scale_label)

    def __str__(self) -> str:
        return ", ".join(
            f"{label}: {self.scaled_results[label][0]:.2g} {self.scaled_results[label][1]}"
            for label in self.results
        )

    def table_repr(self) -> List[str]:
        """
        Returns a list of string representations for each metric,
        in the order the metrics were registered.
        """
        return [
            f"{self.scaled_results[metric.label][0]:6.3f} {self.scaled_results[metric.label][1]}"
            for metric in self.metrics
        ]


# --- Collection for Grouped Stats ---
class StatsCollection:
    """
    Manages a collection of Stats objects. Metrics are registered once,
    and each data set is added under a label (optionally grouped).
    The final output is printed using the table printer.
    """

    def __init__(self, default_metrics: bool = True):
        self.metrics: List[Metric] = []
        self.stats: Dict[str, Stats] = {}
        self.groups: Dict[str, set] = defaultdict(set)
        if default_metrics:
            self.register_metrics(
                [
                    Metric("avg", default_mean, "s"),
                    Metric("std", default_stddev, "s"),
                    Metric("min", min, "s"),
                    Metric("max", max, "s"),
                ]
            )

    def register_metric(self, metric: Metric) -> None:
        self.metrics.append(metric)

    def register_metrics(self, metrics: List[Metric]) -> None:
        self.metrics.extend(metrics)

    def add_stats(
        self, label: str, data: List[float], group: Optional[str] = None
    ) -> None:
        stat = Stats(data, self.metrics)
        self.stats[label] = stat
        if group:
            self.groups[group].add(label)
        else:
            self.groups["_"].add(label)

    def clear(self) -> None:
        self.stats.clear()
        self.groups = defaultdict(set)

    def print_all_stats(self) -> None:
        """
        Builds a table configuration list and prints it using the table printer.
        This follows the same style as your provided example.
        """
        header = ["Label"] + [metric.label for metric in self.metrics]
        config = [header, ["__sep"]]

        sorted_groups = sorted(self.groups.items(), key=lambda x: x[0])
        for group_name, labels in sorted_groups:
            for label in sorted(labels):
                stat = self.stats[label]
                row = [label] + stat.table_repr()
                config.append(row)
            if group_name != sorted_groups[-1][0]:
                config.append(["__sep"])
        cls()  # Clear the console
        print_table(config)


# --- Example Usage ---
if __name__ == "__main__":
    stats_collection = StatsCollection()

    # Register metrics (e.g., average, standard deviation, min, and max) with time unit "s"
    stats_collection.register_metrics(
        [
            Metric("avg", default_mean, "s"),
            Metric("std", default_stddev, "s"),
            Metric("min", min, "s"),
            Metric("max", max, "s"),
        ]
    )

    # Add sample stats under groups for demonstration
    stats_collection.add_stats("test_1", [0.001, 0.002, 0.0015], group="Group A")
    stats_collection.add_stats("test_2", [0.003, 0.004, 0.0025], group="Group A")
    stats_collection.add_stats("test_3", [0.005, 0.006, 0.007], group="Group B")

    # Print all stats using the table printer
    stats_collection.print_all_stats()
