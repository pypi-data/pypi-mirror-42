GraphQL WS
==========

Websocket server for GraphQL subscriptions.

Currently supports: \*
`aiohttp <https://github.com/graphql-python/graphql-ws-django#aiohttp>`__ \*
`Gevent <https://github.com/graphql-python/graphql-ws-django#gevent>`__ \*
Sanic (uses `websockets <https://github.com/aaugustin/websockets/>`__
library)

Installation instructions
=========================

For instaling graphql-ws-django, just run this command in your shell

.. code:: bash

    pip install graphql-ws-django

Examples
--------

aiohttp
~~~~~~~

For setting up, just plug into your aiohttp server.

.. code:: python

    from graphql_ws_django.aiohttp import AiohttpSubscriptionServer


    subscription_server = AiohttpSubscriptionServer(schema)

    async def subscriptions(request):
        ws = web.WebSocketResponse(protocols=('graphql-ws-django',))
        await ws.prepare(request)

        await subscription_server.handle(ws)
        return ws


    app = web.Application()
    app.router.add_get('/subscriptions', subscriptions)

    web.run_app(app, port=8000)

Sanic
~~~~~

Works with any framework that uses the websockets library for it's
websocket implementation. For this example, plug in your Sanic server.

.. code:: python

    from graphql_ws_django.websockets_lib import WsLibSubscriptionServer


    app = Sanic(__name__)

    subscription_server = WsLibSubscriptionServer(schema)

    @app.websocket('/subscriptions', subprotocols=['graphql-ws-django'])
    async def subscriptions(request, ws):
        await subscription_server.handle(ws)
        return ws


    app.run(host="0.0.0.0", port=8000)

And then, plug into a subscribable schema:

.. code:: python

    import asyncio
    import graphene


    class Query(graphene.ObjectType):
        base = graphene.String()


    class Subscription(graphene.ObjectType):
        count_seconds = graphene.Float(up_to=graphene.Int())

        async def resolve_count_seconds(root, info, up_to):
            for i in range(up_to):
                yield i
                await asyncio.sleep(1.)
            yield up_to


    schema = graphene.Schema(query=Query, subscription=Subscription)

You can see a full example here:
https://github.com/graphql-python/graphql-ws-django/tree/master/examples/aiohttp

Gevent
~~~~~~

For setting up, just plug into your Gevent server.

.. code:: python

    subscription_server = GeventSubscriptionServer(schema)
    app.app_protocol = lambda environ_path_info: 'graphql-ws-django'

    @sockets.route('/subscriptions')
    def echo_socket(ws):
        subscription_server.handle(ws)
        return []

And then, plug into a subscribable schema:

.. code:: python

    import graphene
    from rx import Observable


    class Query(graphene.ObjectType):
        base = graphene.String()


    class Subscription(graphene.ObjectType):
        count_seconds = graphene.Float(up_to=graphene.Int())

        async def resolve_count_seconds(root, info, up_to=5):
            return Observable.interval(1000)\
                             .map(lambda i: "{0}".format(i))\
                             .take_while(lambda i: int(i) <= up_to)


    schema = graphene.Schema(query=Query, subscription=Subscription)

You can see a full example here:
https://github.com/graphql-python/graphql-ws-django/tree/master/examples/flask\_gevent

Django Channels
~~~~~~~~~~~~~~~

First ``pip install channels`` and it to your django apps

Then add the following to your settings.py

.. code:: python

        CHANNELS_WS_PROTOCOLS = ["graphql-ws-django", ]
        CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "asgiref.inmemory.ChannelLayer",
                "ROUTING": "django_subscriptions.urls.channel_routing",
            },

        }

Setup your graphql schema

.. code:: python

    import graphene
    from rx import Observable


    class Query(graphene.ObjectType):
        hello = graphene.String()

        def resolve_hello(self, info, **kwargs):
            return 'world'

    class Subscription(graphene.ObjectType):

        count_seconds = graphene.Int(up_to=graphene.Int())


        def resolve_count_seconds(
            root, 
            info, 
            up_to=5
        ):
            return Observable.interval(1000)\
                             .map(lambda i: "{0}".format(i))\
                             .take_while(lambda i: int(i) <= up_to)



    schema = graphene.Schema(
        query=Query,
        subscription=Subscription
    )

Setup your schema in settings.py

.. code:: python

    GRAPHENE = {
        'SCHEMA': 'path.to.schema'
    }

and finally add the channel routes

.. code:: python

    from channels.routing import route_class
    from graphql_ws_django.django_channels import GraphQLSubscriptionConsumer

    channel_routing = [
        route_class(GraphQLSubscriptionConsumer, path=r"^/subscriptions"),
    ]

Django Channels 2
~~~~~~~~~~~~~~~~~

Set up with Django Channels just takes three steps:

1. Install the apps
2. Set up your schema
3. Configure the channels router application

First ``pip install channels`` and it to your ``INSTALLED_APPS``. If you
want graphiQL, install the ``graphql_ws_django.django`` app before
``graphene_django`` to serve a graphiQL template that will work with
websockets:

.. code:: python

    INSTALLED_APPS = [
        "channels",
        "graphql_ws_django.django",
        "graphene_django",
        # ...
    ]

Next, set up your graphql schema:

.. code:: python

    import graphene
    from rx import Observable


    class Query(graphene.ObjectType):
        hello = graphene.String()

        def resolve_hello(self, info, **kwargs):
            return "world"


    class Subscription(graphene.ObjectType):

        count_seconds = graphene.Int(up_to=graphene.Int())

        def resolve_count_seconds(root, info, up_to=5):
            return (
                Observable.interval(1000)
                .map(lambda i: "{0}".format(i))
                .take_while(lambda i: int(i) <= up_to)
            )


    schema = graphene.Schema(query=Query, subscription=Subscription)

...and point to your schema in Django settings

.. code:: python

    GRAPHENE = {
        'SCHEMA': 'yourproject.schema'
    }

Finally, you can set up channels routing yourself (maybe using
``graphql_ws_django.django.routing.websocket_urlpatterns`` in your
``URLRouter``), or you can just use one of the preset channels
applications:

.. code:: python

    ASGI_APPLICATION = 'graphql_ws_django.django.routing.application'
    # or
    ASGI_APPLICATION = 'graphql_ws_django.django.routing.auth_application'

Run ``./manage.py runserver`` and go to
``http://localhost:8000/graphql`` to test!
