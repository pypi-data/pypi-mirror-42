# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import threading
from ._adb_run_experiment import adb_run_experiment


class _AdbDriverNode(threading.Thread):
    """This code initiates the experiments to be run on worker nodes by calling adb map and collect."""

    def __init__(self, name, input_data, spark_context, partition_count):
        """
        Initialize the _AdbDriverNode class.

        :param name: Name of the experiment run.
        :type name: string
        :param input_data: Input context data for the worker node run.
        :type input_data: Array of tuple [(worker_id, context_dictionary),(worker_id, context_dictionary)]
        :param spark_context: Spark context.
        :type spark_context: spark context.
        :param partition_count: Partition count.
        :type patition_count: int
        """
        super(_AdbDriverNode, self).__init__()
        self.name = name
        self.input_data = input_data
        self.spark_context = spark_context
        self.partition_count = partition_count

    def run(self):
        automlRDD = self.spark_context.parallelize(
            self.input_data, self.partition_count)
        automlRDD.map(adb_run_experiment).collect()
