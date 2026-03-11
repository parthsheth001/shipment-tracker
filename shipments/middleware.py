from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only rate limit API endpoints
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        # Identify client by IP address
        ip = self.get_client_ip(request)
        cache_key = f'rate_limit:{ip}'

        # Get current request count for this IP
        request_count = cache.get(cache_key, 0)

        if request_count >= 100:
            return JsonResponse(
                {
                    'error': 'Rate limit exceeded. Maximum 100 requests per minute.',
                    'retry_after': '60 seconds'
                },
                status=429
            )

        # Increment counter — set TTL of 60 seconds on first request
        if request_count == 0:
            cache.set(cache_key, 1, 60)
        else:
            cache.incr(cache_key)

        response = self.get_response(request)

        # Add rate limit headers so client knows their limit status
        response['X-RateLimit-Limit'] = '100'
        response['X-RateLimit-Remaining'] = str(max(0, 100 - request_count - 1))

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')