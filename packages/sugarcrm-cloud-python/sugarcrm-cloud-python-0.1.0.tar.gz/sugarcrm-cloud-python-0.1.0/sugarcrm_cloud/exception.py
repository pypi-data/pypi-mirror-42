class BaseError(Exception):
    pass


class UnsupportedVersion(BaseError):
    pass


class SugarApiExceptionError(BaseError):
    pass


class SugarApiExceptionIncorrectVersion(BaseError):
    pass


class SugarApiExceptionNeedLogin(BaseError):
    pass


class SugarApiExceptionInvalidGrant(BaseError):
    pass


class SugarApiExceptionNotAuthorized(BaseError):
    pass


class SugarApiExceptionPortalUserInactive(BaseError):
    pass


class SugarApiExceptionPortalNotConfigured(BaseError):
    pass


class SugarApiExceptionNoMethod(BaseError):
    pass


class SugarApiExceptionNotFound(BaseError):
    pass


class SugarApiExceptionEditConflict(BaseError):
    pass


class SugarApiExceptionInvalidHash(BaseError):
    pass


class SugarApiExceptionRequestTooLarge(BaseError):
    pass


class SugarApiExceptionMissingParameter(BaseError):
    pass


class SugarApiExceptionInvalidParameter(BaseError):
    pass


class SugarApiExceptionRequestMethodFailure(BaseError):
    pass


class SugarApiExceptionClientOutdated(BaseError):
    pass


class SugarApiExceptionConnectorResponse(BaseError):
    pass


class SugarApiExceptionMaintenance(BaseError):
    pass


class SugarApiExceptionServiceUnavailable(BaseError):
    pass


class SugarApiExceptionSearchUnavailable(BaseError):
    pass


class SugarApiExceptionSearchRuntime(BaseError):
    pass
