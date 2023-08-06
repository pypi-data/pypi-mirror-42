name = "amncore"

try:
    import logger
except ImportError:
    from . import logger

if logger.is_log_source_registered(name) == False:
    logger.register_log_source(name, logger.FlatFileSink("{}.log".format(name)), logger.LEV_1)