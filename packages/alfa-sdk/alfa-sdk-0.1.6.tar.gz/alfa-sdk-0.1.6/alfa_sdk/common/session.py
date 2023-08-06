import os
import json
import requests
import collections
import pkg_resources

from alfa_sdk.common.auth import Authentication
from alfa_sdk.common.helpers import EndpointHelper
from alfa_sdk.common.stores import ConfigStore
from alfa_sdk.common.exceptions import (
    RequestError,
    ResourceNotFoundError,
    AuthenticationError,
    AuthorizationError,
)


DEFAULT_ALFA_ENV = "prod"


class Session:
    def __init__(self, credentials={}, **kwargs):
        alfa_env = fetch_alfa_env(kwargs)
        self.endpoint = EndpointHelper(alfa_env=alfa_env)
        self.auth = Authentication(credentials, alfa_env=alfa_env)

        options = self.auth.authenticate_request({})
        self.http_session = requests.Session()
        self.http_session.headers.update(options["headers"])
        self.http_session.params.update(options["params"])

    def request(self, method, service, path, *, parse=True, **kwargs):
        url = self.endpoint.resolve(service, path)
        res = self.http_session.request(method, url, **kwargs)

        if parse:
            return parse_response(res)
        else:
            return res

    def invoke(self, algorithm_id, environment, problem, **kwargs):
        return_holding_response = kwargs.get("return_holding_response")
        include_details = kwargs.get("include_details")
        can_buffer = kwargs.get("can_buffer")

        if type(problem) is not dict:
            try:
                problem = json.loads(problem)
            except ValueError:
                raise ValueError("Problem must be a valid JSON string or a dict.")

        #

        body = {
            "algorithmId": algorithm_id,
            "environment": environment,
            "problem": problem,
            "returnHoldingResponse": return_holding_response,
            "includeDetails": include_details,
            "canBuffer": can_buffer,
        }
        return self.request("post", "baas", "/api/Algorithms/submitRequest", json=body)


#


def parse_response(res):
    url = res.request.url
    try:
        data = res.json()
    except:
        data = res.text

    #

    if isinstance(data, collections.Mapping) and "error" in data:
        if isinstance(data["error"], collections.Mapping):
            error = data.get("error")

            if "message" in error and error["message"] == "No token provided":
                raise AuthenticationError(error=str(error))
            elif "name" in error:
                if error["name"] == "ModelNotFoundError":
                    raise ResourceNotFoundError(url=url)
                if error["name"] == "AuthorizationError":
                    raise AuthorizationError(url=url, error=error.get("message"))
            else:
                raise RequestError(
                    url=url, status=res.status_code, error=str(data.get("error"))
                )

    #

    if res.status_code == 403:
        raise AuthorizationError(url=url, error=res.text)

    if not res.ok:
        raise RequestError(url=url, status=res.status_code, error=res.text)

    return data


def fetch_alfa_env(configuration={}):
    store = ConfigStore.get_group("alfa")
    if "alfa_env" in configuration:
        alfa_env = configuration.get("alfa_env")
    elif "ALFA_ENV" in os.environ:
        alfa_env = os.environ.get("ALFA_ENV")
    elif store and "alfa_env" in store:
        alfa_env = store["alfa_env"]
    else:
        alfa_env = DEFAULT_ALFA_ENV

    if alfa_env in ["dev", "develop", "development"]:
        alfa_env = "dev"
    if alfa_env in ["test", "test-u", "test_u"]:
        alfa_env = "test"
    if alfa_env in ["prod", "production", "prod-u", "prod_u"]:
        alfa_env = "prod"

    return alfa_env


def fetch_context():
    context = os.environ.get("ALFA_CONTEXT")
    try:
        context = json.loads(context)
    except:
        pass

    return context

