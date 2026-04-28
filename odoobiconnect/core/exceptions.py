class OdooBIException(Exception):
    pass


class InvalidModelException(OdooBIException):
    pass


class InvalidFieldException(OdooBIException):
    pass


class SecurityViolation(OdooBIException):
    pass


class LicenseInvalid(OdooBIException):
    pass
