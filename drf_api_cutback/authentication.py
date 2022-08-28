from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Overrides SessionAuthentication method to skip csrf token requirement.
    """

    def enforce_csrf(self, request):
        pass
