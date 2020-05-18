import typing as t
from dataclasses import dataclass

from flask import Flask  # type: ignore
from flask import request

from glue.chain import Chain


@dataclass
class FlaskAPIChain(Chain):
    url_path: str
    method: str


class Generator:
    def __init__(self, app: Flask):
        self.app = app

    def __call__(self, chains: t.List[FlaskAPIChain]):
        handlers: t.Dict[str, t.Dict[str, t.Callable]] = {}
        # group handlers by url. we can't add 2 routes on
        # same url with different methods
        for chain in chains:
            url_handlers = handlers.get(chain.url_path, dict())
            url_handlers[chain.method] = chain.compose()
            handlers[chain.url_path] = url_handlers
        for url, url_handlers in handlers.items():
            print("generate handler for", url)
            print("handlers", url_handlers)

            def handle_(*args, **kwargs):
                print("handle", url, request.method, args, kwargs)
                return url_handlers.get(request.method)(*args, **kwargs)

            # handle_.__name__ = f"{url}"
            methods = list(url_handlers.keys())
            print("methods", methods)
            self.app.route(url, methods=methods)(handle_)
