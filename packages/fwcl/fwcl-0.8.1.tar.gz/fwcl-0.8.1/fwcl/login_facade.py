import json

from .base_facade import BaseFacade
from .api_results import EmailExistsResult, LoginResult
from .api_params import LoginParam


class LoginFacade(BaseFacade):

    @classmethod
    def email_exists(cls, email: str):
        #email_exists_url = "/v1/security/email:exists?Email=noob%40rw.com"
        email_exists_url = f"/v1/security/email:exists?Email={email}"

        result = super().make_get_call(email_exists_url, EmailExistsResult)
        print(result.StatusCode)
        print(result.Result.data)
        return result

    @classmethod
    def login(cls, data: LoginParam):
        login_url = "/v1/login/login"

        result = super().make_post_call(login_url, data.__dict__, LoginResult)
        return result
