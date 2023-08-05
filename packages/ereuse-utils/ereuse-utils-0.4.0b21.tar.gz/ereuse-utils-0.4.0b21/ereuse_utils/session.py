import base64
import json
from typing import Any, Dict, Iterable, Tuple, Union

import boltons.urlutils
from requests import Response
from requests_toolbelt.sessions import BaseUrlSession
from werkzeug.exceptions import HTTPException

import ereuse_utils

Query = Iterable[Tuple[str, Any]]
Status = Union[int, HTTPException]
JSON = 'application/json'
ANY = '*/*'
AUTH = 'Authorization'
BASIC = 'Basic {}'
URL = Union[str, boltons.urlutils.URL]
Data = Union[str, dict, ereuse_utils.Dumpeable]
Res = Tuple[Union[Dict[str, Any], str], Response]


class Session(BaseUrlSession):
    """A BaseUrlSession that always raises for status."""

    def __init__(self, base_url=None):
        super().__init__(base_url)
        self.hooks['response'] = lambda r, *args, **kwargs: r.raise_for_status()


class DevicehubClient(Session):
    """A Session pre-configured to connect to Devicehub-like APIs."""

    def __init__(self, base_url: URL = None, token=None):
        """Initializes a session pointing to a Devicehub endpoint.

        Authentication can be passed-in as a token for endpoints
        that require them, now at ini, after when executing the method,
        or in between with ``set_auth``.

        :param base_url: An url pointing to a endpoint.
        :param token: A Base64 encoded token, as given by a devicehub.
                      You can encode tokens by executing `encode_token`.
        """
        base_url = base_url.to_text() if isinstance(base_url, boltons.urlutils.URL) else base_url
        super().__init__(base_url)
        assert base_url[-1] != '/', 'Do not provide a final slash to the URL'
        if token:
            self.set_auth(token)

    def set_auth(self, token):
        self.headers['Authorization'] = 'Basic {}'.format(token)

    @classmethod
    def encode_token(cls, token: str):
        """Encodes a token suitable for a Devicehub endpoint."""
        return base64.b64encode(str.encode(str(token) + ':')).decode()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Performs login, authenticating future requests.

        :return: The logged-in user.
        """
        user, _ = self.post('/users/login/', {'email': email, 'password': password}, status=200)
        self.set_auth(user['token'])
        return user

    def get(self,
            base_url: URL,
            uri=None,
            status: Status = 200,
            query: Query = tuple(),
            accept=JSON,
            content_type=JSON,
            headers: dict = None,
            token=None,
            **kwargs) -> Res:
        return super().get(base_url,
                           uri=uri,
                           status=status,
                           query=query,
                           accept=accept,
                           content_type=content_type,
                           headers=headers,
                           token=token, **kwargs)

    def post(self, base_url: URL,
             data: Data,
             uri=None,
             status: Status = 201,
             query: Query = tuple(),
             accept=JSON,
             content_type=JSON,
             headers: dict = None,
             token=None,
             **kwargs) -> Res:
        return super().post(base_url,
                            data=data,
                            uri=uri,
                            status=status,
                            query=query,
                            accept=accept,
                            content_type=content_type,
                            headers=headers,
                            token=token, **kwargs)

    def delete(self,
               base_url: URL,
               uri=None,
               status: Status = 204,
               query: Query = tuple(),
               accept=JSON,
               content_type=JSON,
               headers: dict = None,
               token=None,
               **kwargs) -> Res:
        return super().delete(base_url,
                              uri=uri,
                              status=status,
                              query=query,
                              accept=accept,
                              content_type=content_type,
                              headers=headers,
                              token=token, **kwargs)

    def patch(self, base_url: URL,
              data: Data,
              uri=None,
              status: Status = 201,
              query: Query = tuple(),
              accept=JSON,
              content_type=JSON,
              headers: dict = None,
              token=None,
              **kwargs) -> Res:
        return super().patch(base_url,
                             data=data,
                             uri=uri,
                             status=status,
                             query=query,
                             accept=accept,
                             content_type=content_type,
                             headers=headers,
                             token=token, **kwargs)

    def request(self,
                method,
                base_url: URL,
                uri=None,
                status: Status = 200,
                query: Query = tuple(),
                accept=JSON,
                content_type=JSON,
                data=None,
                headers: dict = None,
                token=None,
                **kw) -> Res:
        assert not kw.get('json', None), 'Do not use json; use data.'
        # We allow uris without slashes for item endpoints
        uri = str(uri) if uri else None
        headers = headers or {}
        headers['Accept'] = accept
        headers['Content-Type'] = content_type
        if token:
            headers['Authorization'] = 'Basic {}'.format(token)
        if data and content_type == JSON:
            data = json.dumps(data, cls=ereuse_utils.JSONEncoder, sort_keys=True)
        url = base_url if not isinstance(base_url, boltons.urlutils.URL) else base_url.to_text()
        assert url[-1] == '/', 'base_url should end with a slash'
        if uri:
            url = self.parse_uri(url, uri)
        if query:
            url = self.parse_query(url, query)
        response = super().request(method, url, data=data, headers=headers, **kw)
        if status:
            _status = getattr(status, 'code', status)
            if _status != response.status_code:
                raise WrongStatus('Req to {} failed bc the status is {} but it should have been {}'
                                  .format(url, response.status_code, _status))
        data = response.content if not accept == JSON or not response.content else response.json()
        return data, response

    @staticmethod
    def parse_uri(base_url, uri):
        return boltons.urlutils.URL(base_url).navigate(uri).to_text()

    @staticmethod
    def parse_query(uri, query):
        url = boltons.urlutils.URL(uri)
        url.query_params = boltons.urlutils.QueryParamDict([
            (k, json.dumps(v, cls=ereuse_utils.JSONEncoder) if isinstance(v, (list, dict)) else v)
            for k, v in query
        ])
        return url.to_text()


class WrongStatus(Exception):
    pass
