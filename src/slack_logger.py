import json
import logging
import os
from urllib.parse import urlparse
from logging.handlers import HTTPHandler


class SlackLogHandler(HTTPHandler):
    def __init__(self, url, username=None, icon_url=None, icon_emoji=None, channel=None, mention=None):
        o = urlparse(url)
        is_secure = o.scheme == 'https'
        HTTPHandler.__init__(self, o.netloc, o.path, method="POST", secure=is_secure)
        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji
        self.channel = channel
        self.mention = mention and mention.lstrip('@')
        self.addFilter(SlackLogFilter())
        self.setFormatter(SlackFormatter())
        self.proxy = os.getenv('APP_PROXY_HOST', None)
        if self.proxy:
            self.proxy = self.proxy.split("http://")[-1]

    def mapLogRecord(self, record):
        text = self.format(record)

        if isinstance(self.formatter, SlackFormatter):
            payload = {
                'attachments': [
                    text,
                ],
            }
            if self.mention:
                payload['text'] = '<@{0}>'.format(self.mention)
        else:
            if self.mention:
                text = '<@{0}> {1}'.format(self.mention, text)
            payload = {
                'text': text,
            }

        if self.username:
            payload['username'] = self.username
        if self.icon_url:
            payload['icon_url'] = self.icon_url
        if self.icon_emoji:
            payload['icon_emoji'] = self.icon_emoji
        if self.channel:
            payload['channel'] = self.channel

        ret = {
            'payload': json.dumps(payload),
        }
        return ret

    def getConnection(self, host, secure):
        # proxy가 존재할경우
        if self.proxy:
            connection = super().getConnection(self.proxy, secure)
            connection.set_tunnel(host)
            return connection
        else:
            return super().getConnection(host, secure)


class SlackFormatter(logging.Formatter):
    def format(self, record):
        ret = {}
        if record.levelname == 'INFO':
            ret['color'] = 'good'
        elif record.levelname == 'WARNING':
            ret['color'] = 'warning'
        elif record.levelname == 'ERROR':
            ret['color'] = '#E91E63'
        elif record.levelname == 'CRITICAL':
            ret['color'] = 'danger'

        ret['author_name'] = record.levelname
        ret['title'] = record.name
        ret['ts'] = record.created
        ret['text'] = super(SlackFormatter, self).format(record)
        return ret


class SlackLogFilter(logging.Filter):
    """
    Logging filter to decide when logging to Slack is requested, using
    the `extra` kwargs:

        `logger.info("...", extra={'notify_slack': True})`
    """

    def __init__(self, clear=True):
        super().__init__()
        self.clear = clear

    def filter(self, record):
        if self.clear:
            record._exc_info_hidden, record.exc_info = record.exc_info, None
            # clear the exception traceback text cache, if created.
            record.exc_text = None
        elif hasattr(record, "_exc_info_hidden"):
            record.exc_info = record._exc_info_hidden
            del record._exc_info_hidden
        return not getattr(record, 'skip_slack_notify', False)
