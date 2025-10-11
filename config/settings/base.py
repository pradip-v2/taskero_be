# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

import ssl
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# taskero_be/
APPS_DIR = BASE_DIR / "taskero_be"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_tenants",
    "graphene_django",
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    "django_filters",
]

LOCAL_SHARED_APPS = [
    "taskero_be.tenants",
    "taskero_be.users",
]


SHARED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_SHARED_APPS

TENANT_APPS = [
    "taskero_be.core",
    "taskero_be.users",
    "taskero_be.projects",
    "taskero_be.tasks",
]

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"


# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "taskero_be.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "taskero_be.users.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Pradip Bankar""", "pradipbankar0097@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-hijack-root-logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_LOGIN_METHODS = {"email"}
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "taskero_be.users.adapters.AccountAdapter"
# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "taskero_be.users.forms.UserSignupForm"}
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "taskero_be.users.adapters.SocialAccountAdapter"
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "taskero_be.users.forms.UserSocialSignupForm"}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "taskero_be.pagination.TaskeroPageNumberPagination",
    "PAGE_SIZE": 100,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "my-app-auth",
    "JWT_AUTH_REFRESH_COOKIE": "my-refresh-token",
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    # A regex specifying the common denominator for all operation paths. If
    # SCHEMA_PATH_PREFIX is set to None, drf-spectacular will attempt to estimate
    # a common prefix. Use '' to disable.
    # Mainly used for tag extraction, where paths like '/api/v1/albums' with
    # a SCHEMA_PATH_PREFIX regex '/api/v[0-9]' would yield the tag 'albums'.
    "SCHEMA_PATH_PREFIX": None,
    # Remove matching SCHEMA_PATH_PREFIX from operation path. Usually used in
    # conjunction with appended prefixes in SERVERS.
    "SCHEMA_PATH_PREFIX_TRIM": False,
    # Insert a manual path prefix to the operation path, e.g. '/service/backend'.
    # Use this for example to align paths when the API is mounted as a sub-resource
    # behind a proxy and Django is not aware of that. Alternatively, prefixes can
    # also specified via SERVERS, but this makes the operation path more explicit.
    "SCHEMA_PATH_PREFIX_INSERT": "",
    # Coercion of {pk} to {id} is controlled by SCHEMA_COERCE_PATH_PK. Additionally,
    # some libraries (e.g. drf-nested-routers) use "_pk" suffixed path variables.
    # This setting globally coerces path variables like "{user_pk}" to "{user_id}".
    "SCHEMA_COERCE_PATH_PK_SUFFIX": False,
    # Schema generation parameters to influence how components are constructed.
    # Some schema features might not translate well to your target.
    # Demultiplexing/modifying components might help alleviate those issues.
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    # Create separate components for PATCH endpoints (without required list)
    "COMPONENT_SPLIT_PATCH": True,
    # Split components into request and response parts where appropriate
    # This setting is highly recommended to achieve the most accurate API
    # description, however it comes at the cost of having more components.
    "COMPONENT_SPLIT_REQUEST": False,
    # Aid client generator targets that have trouble with read-only properties.
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    # Adds "minLength: 1" to fields that do not allow blank strings. Deactivated
    # by default because serializers do not strictly enforce this on responses and
    # so "minLength: 1" may not always accurately describe API behavior.
    # Gets implicitly enabled by COMPONENT_SPLIT_REQUEST, because this can be
    # accurately modeled when request and response components are separated.
    "ENFORCE_NON_BLANK_FIELDS": False,
    # This version string will end up the in schema header. The default OpenAPI
    # version is 3.0.3, which is heavily tested. We now also support 3.1.0,
    # which contains the same features and a few mandatory, but minor changes.
    "OAS_VERSION": "3.0.3",
    # Configuration for serving a schema subset with SpectacularAPIView
    "SERVE_URLCONF": None,
    # complete public schema or a subset based on the requesting user
    "SERVE_PUBLIC": True,
    # include schema endpoint into schema
    "SERVE_INCLUDE_SCHEMA": True,
    # list of authentication/permission classes for spectacular's views.
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    # None will default to DRF's AUTHENTICATION_CLASSES
    "SERVE_AUTHENTICATION": None,
    # Dictionary of general configuration to pass to the SwaggerUI({ ... })
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    # The settings are serialized with json.dumps(). If you need customized JS, use a
    # string instead. The string must then contain valid JS and is passed unchanged.
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": False,
    },
    # Initialize SwaggerUI with additional OAuth2 configuration.
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/
    "SWAGGER_UI_OAUTH2_CONFIG": {},
    # Dictionary of general configuration to pass to the Redoc.init({ ... })
    # https://redocly.com/docs/redoc/config/#functional-settings
    # The settings are serialized with json.dumps(). If you need customized JS, use a
    # string instead. The string must then contain valid JS and is passed unchanged.
    "REDOC_UI_SETTINGS": {},
    # CDNs for swagger and redoc. You can change the version or even host your
    # own depending on your requirements. For self-hosting, have a look at
    # the sidecar option in the README.
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
    "SWAGGER_UI_FAVICON_HREF": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png",
    "REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@latest",
    # Append OpenAPI objects to path and components in addition to the generated objects
    "APPEND_PATHS": {},
    "APPEND_COMPONENTS": {},
    # STRONGLY DISCOURAGED (with the exception for the djangorestframework-api-key library)
    # please don't use this anymore as it has tricky implications that
    # are hard to get right. For authentication, OpenApiAuthenticationExtension are
    # strongly preferred because they are more robust and easy to write.
    # However if used, the list of methods is appended to every endpoint in the schema!
    "SECURITY": [],
    # Postprocessing functions that run at the end of schema generation.
    # must satisfy interface result = hook(generator, request, public, result)
    "POSTPROCESSING_HOOKS": ["drf_spectacular.hooks.postprocess_schema_enums"],
    # Preprocessing functions that run before schema generation.
    # must satisfy interface result = hook(endpoints=result) where result
    # is a list of Tuples (path, path_regex, method, callback).
    # Example: 'drf_spectacular.hooks.preprocess_exclude_path_format'
    "PREPROCESSING_HOOKS": [],
    # Determines how operations should be sorted. If you intend to do sorting with a
    # PREPROCESSING_HOOKS, be sure to disable this setting. If configured, the sorting
    # is applied after the PREPROCESSING_HOOKS. Accepts either
    # True (drf-spectacular's alpha-sorter), False, or a callable for sort's key arg.
    "SORT_OPERATIONS": True,
    # enum name overrides. dict with keys "YourEnum" and their choice values "field.choices"
    # e.g. {'SomeEnum': ['A', 'B'], 'OtherEnum': 'import.path.to.choices'}
    "ENUM_NAME_OVERRIDES": {},
    # Adds "blank" and "null" enum choices where appropriate. disable on client generation issues
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": True,
    # Add/Append a list of (``choice value`` - choice name) to the enum description string.
    "ENUM_GENERATE_CHOICE_DESCRIPTION": True,
    # Optional suffix for generated enum.
    # e.g. {'ENUM_SUFFIX': "Type"} would produce an enum name 'StatusType'.
    "ENUM_SUFFIX": "Enum",
    # function that returns a list of all classes that should be excluded from doc string extraction
    "GET_LIB_DOC_EXCLUDES": "drf_spectacular.plumbing.get_lib_doc_excludes",
    # Function that returns a mocked request for view processing. For CLI usage
    # original_request will be None.
    # interface: request = build_mock_request(method, path, view, original_request, **kwargs)
    "GET_MOCK_REQUEST": "drf_spectacular.plumbing.build_mock_request",
    # Camelize names like "operationId" and path parameter names
    # Camelization of the operation schema itself requires the addition of
    # 'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields'
    # to POSTPROCESSING_HOOKS. Please note that the hook depends on
    # ``djangorestframework_camel_case``, while CAMELIZE_NAMES itself does not.
    "CAMELIZE_NAMES": False,
    # Changes the location of the action/method on the generated OperationId. For example,
    # "POST": "group_person_list", "group_person_create"
    # "PRE":  "list_group_person", "create_group_person"
    "OPERATION_ID_METHOD_POSITION": "POST",
    # Determines if and how free-form 'additionalProperties' should be emitted in the schema. Some
    # code generator targets are sensitive to this. None disables generic 'additionalProperties'.
    # allowed values are 'dict', 'bool', None
    "GENERIC_ADDITIONAL_PROPERTIES": "dict",
    # Path converter schema overrides (e.g. <int:foo>). Can be used to either modify default
    # behavior or provide a schema for custom converters registered with register_converter(...).
    # Takes converter labels as keys and either basic python types, OpenApiType, or raw schemas
    # as values. Example: {'aint': OpenApiTypes.INT, 'bint': str, 'cint': {'type': ...}}
    "PATH_CONVERTER_OVERRIDES": {},
    # Determines whether operation parameters should be sorted alphanumerically or just in
    # the order they arrived. Accepts either True, False, or a callable for sort's key arg.
    "SORT_OPERATION_PARAMETERS": True,
    # @extend_schema allows to specify status codes besides 200. This functionality is usually used
    # to describe error responses, which rarely make use of list mechanics. Therefore, we suppress
    # listing (pagination and filtering) on non-2XX status codes by default. Toggle this to enable
    # list responses with ListSerializers/many=True irrespective of the status code.
    "ENABLE_LIST_MECHANICS_ON_NON_2XX": False,
    # This setting allows you to deviate from the default manager by accessing a different model
    # property. We use "objects" by default for compatibility reasons. Using "_default_manager"
    # will likely fix most issues, though you are free to choose any name.
    "DEFAULT_QUERY_MANAGER": "objects",
    # Controls which authentication methods are exposed in the schema. If not None, will hide
    # authentication classes that are not contained in the whitelist. Use full import paths
    # like ['rest_framework.authentication.TokenAuthentication', ...].
    # Empty list ([]) will hide all authentication methods. The default None will show all.
    "AUTHENTICATION_WHITELIST": None,
    # Controls which parsers are exposed in the schema. Works analog to AUTHENTICATION_WHITELIST.
    # List of allowed parsers or None to allow all.
    "PARSER_WHITELIST": None,
    # Controls which renderers are exposed in the schema. Works analog to AUTHENTICATION_WHITELIST.
    # rest_framework.renderers.BrowsableAPIRenderer is ignored by default if whitelist is None
    "RENDERER_WHITELIST": None,
    # Option for turning off error and warn messages
    "DISABLE_ERRORS_AND_WARNINGS": False,
    # Runs exemplary schema generation and emits warnings as part of "./manage.py check --deploy"
    "ENABLE_DJANGO_DEPLOY_CHECK": True,
    # General schema metadata. Refer to spec for valid inputs
    # https://spec.openapis.org/oas/v3.0.3#openapi-object
    "TITLE": "Taskero API",
    "DESCRIPTION": "",
    "TOS": None,
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {},
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {},
    # Statically set schema version. May also be an empty string. When used together with
    # view versioning, will become '0.0.0 (v2)' for 'v2' versioned requests.
    # Set VERSION to None if only the request version should be rendered.
    "VERSION": "0.1.0",
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
    "SERVERS": [],
    # Tags defined in the global scope
    "TAGS": [],
    # Optional: List of OpenAPI 3.1 webhooks. Each entry should be an import path to an
    # OpenApiWebhook instance.
    "WEBHOOKS": [],
    # Optional: MUST contain 'url', may contain "description"
    "EXTERNAL_DOCS": {},
    # Arbitrary specification extensions attached to the schema's info object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_INFO": {},
    # Arbitrary specification extensions attached to the schema's root object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_ROOT": {},
    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://spec.openapis.org/oas/v3.0.3#oauth-flows-object
    "OAUTH2_FLOWS": [],
    "OAUTH2_AUTHORIZATION_URL": None,
    "OAUTH2_TOKEN_URL": None,
    "OAUTH2_REFRESH_URL": None,
    "OAUTH2_SCOPES": None,
}
# Your stuff...
# ------------------------------------------------------------------------------

RUNSCRIPT_CHDIR = BASE_DIR

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

JWT_AUTH_HTTPONLY = False
