from django.db import models
from django.urls import reverse
from django.utils import timezone

from ..user.models import Users
from .generators import generate_client_id, generate_client_secret
from .validators import validate_uris
from .compat import parse_qsl, urlparse
from .scopes import get_scopes_backend

class Application(models.Model):

    CLIENT_CONFIDENTIAL = "confidential"
    CLIENT_PUBLIC = "public"
    CLIENT_TYPES = (
        (CLIENT_CONFIDENTIAL, "Confidential"),
        (CLIENT_PUBLIC, "Public"),
    )

    GRANT_AUTHORIZATION_CODE = "authorization-code"
    GRANT_IMPLICIT = "implicit"
    GRANT_PASSWORD = "password"
    GRANT_CLIENT_CREDENTIALS = "client-credentials"
    GRANT_TYPES = (
        (GRANT_AUTHORIZATION_CODE, "Authorization code"),
        (GRANT_IMPLICIT, "Implicit"),
        (GRANT_PASSWORD, "Resource owner password-based"),
        (GRANT_CLIENT_CREDENTIALS, "Client credentials"),
    )

    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(
        max_length=100, unique=True, default=generate_client_id, db_index=True
    )
    user = models.ForeignKey(
        Users,
        related_name="%(app_label)s_%(class)s",
        null=True, blank=True, on_delete=models.CASCADE
    )

    help_text = "Allowed URIs list, space separated"
    redirect_uris = models.TextField(
        blank=True, help_text=help_text, validators=[validate_uris]
    )
    client_type = models.CharField(max_length=32, choices=CLIENT_TYPES)
    authorization_grant_type = models.CharField(
        max_length=32, choices=GRANT_TYPES
    )
    client_secret = models.CharField(
        max_length=255, blank=True, default=generate_client_secret, db_index=True
    )
    name = models.CharField(max_length=255, blank=True)
    skip_authorization = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "application"
        verbose_name_plural = "applications"

    @property
    def default_redirect_uri(self):
        """
        Returns the default redirect_uri extracting the first item from
        the :attr:`redirect_uris` string
        """
        if self.redirect_uris:
            return self.redirect_uris.split().pop(0)

        assert False, (
            "If you are using implicit, authorization_code"
            "or all-in-one grant_type, you must define "
            "redirect_uris field in your Application model"
        )

    def redirect_uri_allowed(self, uri):
        """
        Checks if given url is one of the items in :attr:`redirect_uris` string

        :param uri: Url to check
        """
        for allowed_uri in self.redirect_uris.split():
            parsed_allowed_uri = urlparse(allowed_uri)
            parsed_uri = urlparse(uri)

            if (parsed_allowed_uri.scheme == parsed_uri.scheme and
                    parsed_allowed_uri.netloc == parsed_uri.netloc and
                    parsed_allowed_uri.path == parsed_uri.path):

                aqs_set = set(parse_qsl(parsed_allowed_uri.query))
                uqs_set = set(parse_qsl(parsed_uri.query))

                if aqs_set.issubset(uqs_set):
                    return True

        return False

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.redirect_uris \
            and self.authorization_grant_type \
            in (Application.GRANT_AUTHORIZATION_CODE,
                Application.GRANT_IMPLICIT):
            error = "Redirect_uris could not be empty with {grant_type} grant_type"
            raise ValidationError(error.format(grant_type=self.authorization_grant_type))

    def get_absolute_url(self):
        return reverse("oauth2_provider:detail", args=[str(self.id)])

    def __str__(self):
        return self.name or self.client_id

    def allows_grant_type(self, *grant_types):
        return self.authorization_grant_type in grant_types

    def is_usable(self, request):
        """
        Determines whether the application can be used.

        :param request: The HTTP request being processed.
        """
        return True

class Grant(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s"
    )
    code = models.CharField(max_length=255, unique=True)  # code comes from oauthlib
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE
    )
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=255)
    scope = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def redirect_uri_allowed(self, uri):
        return uri == self.redirect_uri

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "grant"
        verbose_name_plural = "grants"

class AccessToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(app_label)s_%(class)s"
    )
    token = models.CharField(max_length=255, unique=True, )
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, blank=True, null=True,
    )
    expires = models.DateTimeField()
    scope = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self, scopes=None):
        return not self.is_expired() and self.allow_scopes(scopes)

    def is_expired(self):
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def allow_scopes(self, scopes):
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def revoke(self):
        self.delete()

    @property
    def scopes(self):
        all_scopes = get_scopes_backend().get_all_scopes()
        token_scopes = self.scope.split()
        return {name: desc for name, desc in all_scopes.items() if name in token_scopes}

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "accessToken"
        verbose_name_plural = "accessTokens"

class RefreshToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s"
    )
    token = models.CharField(max_length=255, unique=True)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE)
    access_token = models.OneToOneField(
        AccessToken, on_delete=models.CASCADE,
        related_name="refresh_token"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def revoke(self):
        # AccessToken.objects.get(id=self.access_token.id).revoke()
        self.delete()

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "refreshToken"
        verbose_name_plural = "refreshTokens"