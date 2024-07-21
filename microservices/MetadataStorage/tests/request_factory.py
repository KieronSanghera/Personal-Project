import factory
from uuid import uuid4
from starlette.requests import Request
from starlette.datastructures import Headers, URL
from starlette.types import Scope, Receive, Send
from typing import Callable, Dict, Any


class RequestFactory(factory.Factory):
    class Meta:
        model = Request

    @factory.lazy_attribute
    def scope(self) -> Scope:
        return {
            "type": "http",
            "http_version": "1.1",
            "method": "POST",
            "scheme": "http",
            "path": "/saveFile",
            "query_string": b"",
            "headers": [
                (b"host", b"testserver"),
            ],
            "client": ("testclient", 50000),
            "server": ("testserver", 80),
        }

    @factory.lazy_attribute
    def receive(self) -> Receive:
        async def receive() -> Dict[str, Any]:
            return {"type": "http.request", "body": b"", "more_body": False}

        return receive

    @factory.post_generation
    def build_request(self, create, extracted, **kwargs):
        # This makes sure the returned object is an actual Request instance
        return Request(self.scope, self.receive)
