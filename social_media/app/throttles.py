from rest_framework.throttling import SimpleRateThrottle

class UserFriendRequestThrottle(SimpleRateThrottle):
    scope = 'user_search'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return f'throttle_{self.scope}_{request.user.pk}'
        else:
            return self.get_ident(request)