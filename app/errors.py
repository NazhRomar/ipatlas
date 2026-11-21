"""Application exceptions. Each maps to an HTTP status and a stable error code."""


class IPAtlasError(Exception):
    status_code = 500
    code = "internal_error"
    default_message = "Unexpected error."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class InvalidIPError(IPAtlasError):
    status_code = 400
    code = "invalid_ip"
    default_message = "Not a valid IPv4 or IPv6 address."


class InvalidParameterError(IPAtlasError):
    status_code = 400
    code = "invalid_parameter"
    default_message = "Invalid request parameter."


class ReservedIPError(IPAtlasError):
    status_code = 422
    code = "reserved_ip"
    default_message = "Private or reserved addresses cannot be geolocated."


class RateLimitError(IPAtlasError):
    status_code = 429
    code = "rate_limited"
    default_message = "The geolocation provider rate limit was reached. Try again later."


class UpstreamError(IPAtlasError):
    status_code = 502
    code = "upstream_error"
    default_message = "An upstream service returned an unexpected response."


class UpstreamTimeout(UpstreamError):
    status_code = 504
    code = "upstream_timeout"
    default_message = "An upstream service timed out."
