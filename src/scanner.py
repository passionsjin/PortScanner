import json
import logging
import os.path
from ipaddress import ip_network
from time import time

from CustomNmap import CustomNmap


def write_result(results, path='.', file_name=None, up_state_only=True):
    _result = []
    meta_key = ["runtime", "stats", "task_results"]
    if up_state_only:
        for result in results:
            for k in result.keys():
                if k in meta_key:
                    continue
                if result[k]['state']['state'] == 'up':
                    _result.append(result)
    else:
        _result = results
    if file_name is None:
        file_name = f'result_{int(time())}.json'
    with open(os.path.join(path, file_name), 'w', encoding='utf-8') as f:
        json.dump(_result, f)


def execution_time_logging(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        logging.debug(f'{func.__name__} Execute Time: {end_time - start_time} 초')  # logging 코드 추가
        return result

    return wrapper


def do_scan(ip, options=""):
    nmap = CustomNmap()
    logging.debug(f'Do scan - {ip}')
    result = nmap.scan_command(ip, options)
    logging.debug(f'Done scan - {ip}')
    return result


def make_scan_options(options):
    default_options = ["-vv", "-oX -"]
    for o in default_options:
        if o in options:
            continue
        options = f'{o} {options}'
    return options


def get_hosts(ip):
    ip_net = ip_network(ip)
    return [str(hosts) for hosts in ip_net.hosts()]
