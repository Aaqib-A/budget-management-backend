import logging
import time
logger = logging.getLogger('budget_log')

class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _log_request(self, request):
        """Log the request"""
        # user = str(getattr(request.user, 'user', ''))
        user = request.user
        method = str(getattr(request, 'method', '')).upper()
        request_path = str(getattr(request, 'path', ''))
        query_params = str(["%s: %s" %(k,v) for k, v in request.GET.items()])
        query_params = query_params if query_params else ''
        body = str(["%s: %s" %(k,v) if k != 'file' else '' for k, v in request.POST.items()])

        #logger.info("REQUEST: (%s) [%s] %s %s %s", user, method, request_path, query_params, body)
        logger.info("REQUEST: [%s | %s | %s | %s | %s]", user, method, request_path, query_params, body)
        

    def _log_response(self, request, response):
        """Log the response using values from the request"""
        #user = str(getattr(request, 'user', ''))
        user = request.user
        method = str(getattr(request, 'method', '')).upper()
        status_code = str(getattr(response, 'status_code', ''))
        status_text = str(getattr(response, 'status_text', ''))
        request_path = str(getattr(request, 'path', ''))
        size = str(len(response.content)) if 'content' in response else ''
        content = response.content if 'content' in response else ''

        #logger.info("RESPONSE: (%s) [%s] %s - %s (%s / %s) %s", user, method, request_path, status_code, status_text, size, content)
        logger.info("RESPONSE: [%s | %s | %s - %s (%s / %s) %s]", user, method, request_path, status_code, status_text, size, content)


    def __call__(self, request):
        start_time = time.time()
        self._log_request(request)
        response = self.get_response(request)
        self._log_response(request, response)
        duration = time.time() - start_time
        response_ms = duration * 1000
        # user = str(getattr(request, 'user', ''))
        user = request.user
        method = str(getattr(request, 'method', '')).upper()
        status_code = str(getattr(response, 'status_code', ''))
        request_path = str(getattr(request, 'path', ''))
        logger.info({
            "path": request_path,
            "response_time": str(response_ms) + " ms",
            "method": method,
            "user": user,
            "status_code": status_code
        })
        return response