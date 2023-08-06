# source: https://medium.com/@yzhong.cs/serialize-and-deserialize-complex-json-in-python-205ecc636caa


class Result:
    @classmethod
    def from_json(cls, data):
        return cls(**data)


class LoginResult(Result):
    def __init__(self, isValid: bool, jwt: str, message: str, numberOfQueries: int, userId: int):
        # Result.__init__(self)
        self.isValid = isValid
        self.jwt = jwt
        self.message = message
        self.numberOfQueries = numberOfQueries
        self.userId = userId


class EmailExistsResult(Result):
    def __init__(self, data: str):
        self.data = data


class ApiResult(object):
    def __init__(self, is_valid: bool, result, status_code: int, version: str):
        self.IsValid = is_valid
        self.Result = result
        self.StatusCode = status_code
        self.Version = version

    @classmethod
    def from_json(cls, data: dict, result_class):
        # result = map(EmailExistsResult.from_json, data["Result"])
        # result = EmailExistsResult.from_json(data["Result"])
        result = result_class.from_json(data["Result"])
        return cls(data["IsValid"], result, data["StatusCode"], data["Version"])