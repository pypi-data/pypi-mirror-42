"""
Loads Rook into pyspark workers
Usage: spark-submit --conf spark.python.daemon.module=rook.pyspark_daemon
"""

import pyspark.daemon
import functools
import six
import sys

original_worker_main = pyspark.daemon.worker_main


def worker_main(*args, **kwargs):
    try:
        import rook
        rook.start(log_file="", log_to_stderr=True)
        from rook.logger import logger
        from rook.interface import _rook as singleton
        from rook.services import ImportService
        import_service = singleton.get_trigger_services().get_service(ImportService.NAME)

        def pickle_load_hook(orig_func, *args, **kwargs):
            obj = orig_func(*args, **kwargs)
            try:
                import_service.evaluate_module_list()
            except:
                logger.exception("Silenced exception during module list evaluation")
                pass
            return obj

        # we may end up missing pickle module imports if we rely on the sys.modules polling thread
        import pyspark.serializers
        pyspark.serializers.pickle.loads = functools.partial(pickle_load_hook, pyspark.serializers.pickle.loads)
        pyspark.serializers.pickle.load = functools.partial(pickle_load_hook, pyspark.serializers.pickle.load)
    except:
        six.print_("Starting Rook in worker_main failed", file=sys.stderr)

    result = original_worker_main(*args, **kwargs)
    return result


pyspark.daemon.worker_main = worker_main

if __name__ == '__main__':
    pyspark.daemon.manager()
