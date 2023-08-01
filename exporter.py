import os
from typing import List, Optional, Any

import prometheus_client
from prometheus_client import start_http_server, Summary, Gauge, Counter
from prometheus_client.core import REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily, CounterMetricFamily

REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


import time
import json
import logging
from pathlib import Path


class GraftorioMPCollector(object):
    def __init__(self, directory: Path):
        assert isinstance(directory, Path)
        self.directory = directory.expanduser().absolute()
        return

    def _get_stats(self) -> Optional[Any]:
        filepath = Path(self.directory / "graftoriomp_stats.json").expanduser().absolute()

        if not filepath.exists():
            return None

        with open(filepath, 'r') as fh:
            stats = json.load(fh)

        return stats

    def _filter_string(self, s: str) -> str:
        return s.replace('-', '_')

    def _make_item_metric(self, metric_name: str, item_name: str, amount: int):
        item_name = self._filter_string(item_name)
        # print(f"[{time.time()}][debug] making metric {metric_name} for {item_name} = {amount}")
        metric_family = CounterMetricFamily(f"factorio_{metric_name}", "", labels=["item_name"])
        metric_family.add_metric([item_name], amount)
        return metric_family


    def collect(self):
        print(f"[{time.time()}][debug] collection called")

        stats = self._get_stats()

        if stats is None:
            print(f"[{time.time()}][warning] no stats file found")
            return

        player_stats = stats["player"]

        for item, amount in player_stats["item_production"].items():
            yield self._make_item_metric("item_production", item, amount)

        for item, amount in player_stats["item_consumption"].items():
            yield self._make_item_metric("item_consumption", item, amount)

        for fluid, amount in player_stats["fluid_production"].items():
            yield self._make_item_metric("fluid_production", item, amount)

        for fluid, amount in player_stats["fluid_consumption"].items():
            yield self._make_item_metric("fluid_consumption", item, amount)

        return


if __name__ == "__main__":
    port = int(os.environ["GFMP_PORT"])

    REGISTRY.register(GraftorioMPCollector(Path("/factorio/script-output")))

    start_http_server(port)

    while True:
        time.sleep(5)
