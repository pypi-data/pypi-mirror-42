from .base_mixins import BaseLoggingMixin
import logging

logstash_logger = logging.getLogger('logstash-logger')


class LoggingMixin(BaseLoggingMixin):
    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        if self.log['status_code'] == 200:
            logstash_logger.info('Success response', extra=self.log)
        else:
            error_trace = self.log.pop('errors', None)
            logstash_logger.exception('Error response', exc_info=error_trace, extra=self.log)


class LoggingErrorsMixin(LoggingMixin):
    """
    Log only errors
    """

    def should_log(self, request, response):
        return response.status_code >= 400
