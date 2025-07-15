from src.schemes.enums import AuthMethod


class AuthDataValidator:
    def __init__(self, auth_data: str) -> None:
        self._auth_data = auth_data

    # Made for fast changing or scaling validation types =)
    def _validate_with_length(
            self,
            delimetr: str = " ",
            count: int = 2,
    ) -> bool:
        return len(self._auth_data.split(delimetr)) == count

    def _as_header(self) -> bool:
        return self._validate_with_length()

    def _as_cookie(self) -> bool:
        return self._validate_with_length("=")

    def validate(self, auth_method: AuthMethod) -> bool:
        if auth_method == AuthMethod.COOKIES:
            return self._as_cookie()
        return self._as_header()
