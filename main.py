import logging.config
import os
from itertools import repeat
from multiprocessing import get_context

from src.app_config import app_config
from src.scanner import make_scan_options, get_hosts, do_scan, write_result, execution_time_logging
from src.slack_logger import SlackLogHandler
from src.util import get_config_from_syspath

if app_config.APP_ENV == 'prod':
    logging.SlackLogHandler = SlackLogHandler
config_path = get_config_from_syspath(f'logging.{app_config.APP_ENV}.conf')
os.makedirs(app_config.OUTPUT_PATH, exist_ok=True)

logging.config.fileConfig(config_path,
                          disable_existing_loggers=True,
                          defaults={
                              'slack_webhook': app_config.SLACK_WEBHOOK,
                              'app_name': app_config.APP_NAME,
                              'log_path': f'{app_config.OUTPUT_PATH}/{app_config.APP_NAME}'
                          })


@execution_time_logging
def main(target, options):
    # Option
    options = make_scan_options(options)
    # IP 대역대 계산
    hosts = get_hosts(target)
    logging.debug(f'Hosts - {len(hosts)}')
    # WITHOUT MULTIPROCESS #####
    if not app_config.IS_MULTI_PROCESS:
        res = []
        for host in hosts:
            res.append(do_scan(host))
        if res:
            write_result(res, path=app_config.OUTPUT_PATH)
    else:
        # Multi PROCESS ############
        pool_size = app_config.DEFAULT_PROCESS_POOL_COUNT if app_config.DEFAULT_PROCESS_POOL_COUNT <= len(hosts) else len(
            hosts)
        with get_context(app_config.MULTI_PROCESS_CONTEXT).Pool(pool_size) as pool:
            logging.debug(f'Start work pool - pool size: {pool_size}')
            col_res = pool.starmap(do_scan, zip(hosts, repeat(options)))
            logging.debug(f'Finish work pool - {len(col_res)} work.')
        logging.debug(f'Result - {col_res}')
        if col_res:
            write_result(col_res)


if __name__ == '__main__':
    main(app_config.TARGET, app_config.OPTIONS)
