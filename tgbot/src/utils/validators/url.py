from urllib.parse import urlparse


class URLValidator:
    """
    Validates URLs, optionally restricting them to a whitelist of allowed hosts.

    A URL is considered valid if:
    1. It's not None or empty.
    2. It has a scheme (e.g., 'http', 'https').
    3. It has a network location (e.g., 'example.com', '192.168.1.1').
    4. The scheme is 'http' or 'https'.
    5. If a whitelist is provided, its netloc (host) is in the whitelist.
    """
    def __init__(self, allowed_hosts: list[str] | None = None) -> None:
        self._allowed_hosts = {host.lower() for host in allowed_hosts} if allowed_hosts else None


    def is_valid(self, url_string: str) -> bool:
        if not url_string:
            return False
        try:
            result = urlparse(url_string)
            if not all([result.scheme, result.netloc, result.scheme in ("http", "https")]):
                return False

            if self._allowed_hosts is not None: # Validation with white list
                host = result.hostname.lower()
                if host not in self._allowed_hosts:
                    return False
        except ValueError:
            return False
        else:
            return True
