import os
from typing import List, Optional, Union

import pyspark.sql.functions as F
from pyspark import SparkConf
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType

from .base import DataNode


class SparkDFNode(DataNode):
    def _default_spark_config(self, **configs):
        scfg = SparkConf()

        user = os.environ.get("USER", "")
        scfg.set(
            "spark.sql.warehouse.dir", os.path.join(f"/tmp/{user}", "spark-warehouse")
        )

        for k, v in configs.items():
            scfg.set(k, v)

        return scfg

    def load(
        self,
        fullpaths: Union[str, List[str]] = None,
        ss: Optional[SparkSession] = None,
        scfg: Optional[SparkConf] = None,
        **read_options,
    ) -> DataFrame:

        if ss is None:
            cfg = dict(scfg.getAll()) if isinstance(scfg, SparkConf) else {}
            scfg = self._default_spark_config(**cfg)

            ss = SparkSession.builder.config(conf=scfg).getOrCreate()

        if "format" not in read_options:
            read_options["format"] = self.data.format
        if "schema" not in read_options:
            read_options["schema"] = self.data.schema

        return ss.read.load(fullpaths or self.data.source.fullpath, **read_options)

    def dump(self, sdf: DataFrame, destination=None, **write_options) -> None:
        """"""

        if "mode" not in write_options:
            write_options["mode"] = "overwrite"
        if "format" not in write_options:
            write_options["format"] = self.data.format

        sdf.write.save(destination or self.data.source.fullpath, **write_options)


def udfy(fn=None, return_type=StringType()):
    """A wrapper to provide additional spark udf interface to regular python function object.

    For example:
    in python context, invoke function call by `my_function(a, b)`,
    then in spark pipeline, invoke udf by `my_function.udf('col-a', 'col-b')`,
    additionally, keyword arguments can be overrided by "dynamic udf interface",
    i.e., invoke `my_function.dudf(**override_kwargs)('col-a', 'col-b')`

    """

    def wrap_before_runtime(f):
        def dynamic_wrap(**kwargs):
            return F.udf(lambda *args: f(*args, **kwargs), returnType=return_type)

        f.udf = F.udf(f, returnType=return_type)
        f.dudf = dynamic_wrap

        return f

    if fn is None:
        return wrap_before_runtime
    else:
        return wrap_before_runtime(fn)
