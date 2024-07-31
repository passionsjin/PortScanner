import os


class AppConfig:
    APP_NAME = 'PortScanner'
    APP_ENV = os.getenv('APP_ENV', 'dev')  # dev, prod
    TARGET = os.getenv('TARGET', '')
    OPTIONS = os.getenv('OPTIONS', '')
    IS_MULTI_PROCESS = int(os.getenv('IS_MULTI_PROCESS', 1))
    MULTI_PROCESS_CONTEXT = os.getenv('MULTI_PROCESS_CONTEXT', 'spawn')
    DEFAULT_PROCESS_POOL_COUNT = int(os.getenv('DEFAULT_PROCESS_POOL_COUNT', os.cpu_count()))

    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK', '')
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', './output')

    def __init__(self, validate=True):
        if validate:
            self.validate_env()

    def validate_env(self):
        if not self.TARGET:
            raise EnvironmentError("Target is None.")


app_config = AppConfig()
