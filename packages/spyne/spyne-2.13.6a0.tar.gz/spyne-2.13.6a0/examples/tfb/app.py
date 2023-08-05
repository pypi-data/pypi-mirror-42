#!/usr/bin/env python
import sys

import spyne.const
spyne.const.MIN_GC_INTERVAL = float('inf')

from lxml import html
from spyne.protocol.html import HtmlCloth

from random import randint, shuffle, choice
from contextlib import closing
from email.utils import formatdate

from neurons import TableModel, Application
from neurons.daemon import ServiceDefinition, HttpServer, StaticFileServer
from neurons.daemon.main import Bootstrapper

from spyne import Integer32, Unicode, rpc, ServiceBase, Integer, Array, Any
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

if sys.version_info[0] == 3:
    xrange = range

_is_pypy = hasattr(sys, 'pypy_version_info')

DBDRIVER = 'postgresql+psycopg2cffi' if _is_pypy else 'postgresql+psycopg2'
DBHOST = 'tfb-database'


# models
class DbSessionManager(object):
    def __init__(self, config):
        self.session = config.get_main_store().Session()

    def close(self, with_err):
        self.session.close()


class DbConnectionManager(object):
    def __init__(self, config):
        self.conn = config.get_main_store().engine.connect()

    def close(self, with_err):
        self.conn.close()


class World(TableModel):
    __tablename__ = "world"
    _type_info = [
        ('id', Integer32(primary_key=True)),
        ('random_number', Integer32(sub_name='randomNumber')),
    ]


T_INDEX = html.fromstring(open('cloths/index.html', 'rb').read())


class Fortune(TableModel):
    __tablename__ = "fortune"

    id = Integer32(primary_key=True)
    message = Unicode


outprot_plain = HttpRpc(mime_type='text/plain')


class TfbSimpleService(ServiceBase):
    @rpc(_returns=Any)
    def json(ctx):
        ctx.transport.add_header('Date', formatdate())
        return dict(message=u'Hello, World!')

    @rpc(_returns=Any)
    def plaintext(ctx):
        """Test 6: Plaintext"""
        ctx.out_protocol = outprot_plain
        return b'Hello, World!'


class TfbOrmService(ServiceBase):
    @rpc(_returns=World)
    def db(ctx):
        return ctx.udc.session.query(World).get(randint(1, 10000))

    @rpc(Integer(default=1), _returns=Array(World))
    def dbs(ctx, queries):
        queries = min(500, max(queries, 1))

        q = ctx.session.query(World)
        return [q.get(randint(1, 10000)) for _ in xrange(queries)]

    @rpc(_returns=Array(Fortune, html_cloth=T_INDEX), _body_style='out_bare')
    def fortunes(ctx):
        # This is normally specified at the application level as it's a good
        # practice to group rpc endpoints with similar return types under the
        # same url fragment. eg. https://example.com/api/json
        ctx.out_protocol = HtmlCloth()
        ctx.outprot_ctx = ctx.out_protocol.get_context(ctx, ctx.transport)

        fortunes = ctx.udc.session.query(Fortune).all()
        fortunes.append(
            Fortune(id=0, message=u"Additional fortune added at request time.")
        )

        fortunes.sort(key=lambda x: x.message)

        return fortunes

    @rpc(Integer, _returns=Array(World))
    def updates(ctx, queries):
        """Test 5: Database Updates"""

        queries = min(500, max(queries, 1))

        retval = []
        q = ctx.udc.session.query(World)
        for id in (randint(1, 10000) for _ in xrange(queries)):
            world = q.get(id)
            world.random_number = randint(1, 10000)
            retval.append(world)

        ctx.udc.session.commit()

        return retval


class TfbRawService(ServiceBase):
    # returning both Any+dict or ObjectMarker+ListOfLists works
    @rpc(Integer(default=1), _returns=Any)
    def dbsraw(ctx, queries):
        queries = min(500, max(queries, 1))

        retval = []
        conn = ctx.udc.conn
        for i in xrange(queries):
            wid = randint(1, 10000)
            result = conn.execute(
                "SELECT id, random_number FROM world WHERE id = %s", wid) \
                .fetchone()
            retval.append(dict(id=result[0], randomNumber=result[1]))

        return retval

    @rpc(_returns=Array(Fortune, html_cloth=T_INDEX), _body_style='out_bare')
    def fortunesraw(ctx):
        # This is normally specified at the application level as it's a good
        # practice to group rpc endpoints with similar return types under the
        # same url fragment. eg. https://example.com/api/json
        ctx.out_protocol = HtmlCloth()
        ctx.outprot_ctx = ctx.out_protocol.get_context(ctx, ctx.transport)

        res = ctx.udc.conn.execute("SELECT id, message FROM fortune")
        fortunes = res.fetchall()

        fortunes.append(Fortune(
            id=0,
            message=u"Additional fortune added at request time."
        ))

        fortunes.sort(key=lambda x: x.message)

        return fortunes

    @rpc(Integer(default=1), _returns=Any)
    def updatesraw(ctx, queries):
        """Test 5: Database Updates"""
        queries = min(500, max(queries, 1))

        conn = ctx.udc.conn

        ids = [randint(1, 10000) for _ in xrange(queries)]

        retval = []
        for i in ids:
            wid, rn = conn.execute(
                         "SELECT id, random_number FROM world WHERE id=%s", i) \
                .fetchone()

            rn = randint(1, 10000)
            retval.append(dict(id=wid, randomNumber=rn))

            conn.execute("UPDATE World SET randomNumber=%s WHERE id=%s",
                                                                        rn, wid)

        return retval


def _on_method_call_db_sess(ctx):
    ctx.transport.add_header('Date', formatdate())
    ctx.udc = DbSessionManager(ctx.app.config)


def _on_method_call_db_conn(ctx):
    ctx.transport.add_header('Date', formatdate())
    ctx.udc = DbConnectionManager(ctx.app.config)


TfbRawService.event_manager.add_listener("method_call", _on_method_call_db_conn)
TfbOrmService.event_manager.add_listener("method_call", _on_method_call_db_sess)


def init_app(config):
    subconfig = config.services['root']

    app = Application(
        [TfbOrmService, TfbRawService, TfbSimpleService],
        tns='http://techempower.com/benchmarks/Python/Spyne',
        in_protocol=HttpRpc(),
        out_protocol=JsonDocument(),
        config=config,
    )
    if subconfig.subapps is None:
        subconfig.subapps = {}

    subconfig.subapps.update({'': app})


def init(config):
    return {
        'root': ServiceDefinition(
            init=init_app,
            default=HttpServer(
                type='tcp4',
                host='127.0.0.1',
                port=8080,
            ),
        ),
    }


def parse_config(argv):
    from neurons.daemon.main import boot

    retcode, config = boot('tfb', argv, init, bootstrapper=TfbBootstrap)

    if retcode is not None:
        sys.exit(retcode)

    return config


def gen_wsgi_app():
    config = parse_config([])
    return WsgiApplication(config.services['root'].subapps[''])


words = 'some random words for you and me somebody else if then the'.split()


class TfbBootstrap(Bootstrapper):
    # noinspection PyUnresolvedReferences
    def after_tables(self, config):
        print("Generating data...")
        with closing(config.get_main_store().Session()) as session:
            ints = list(range(10000))
            shuffle(ints)
            for _ in range(10000):
                session.add(World(random_number=ints.pop()))

            for _ in range(100):
                session.add(Fortune(
                    message=' '.join([choice(words)
                                                for _ in range(randint(3, 10))])
                ))

            session.commit()


if __name__ == '__main__':
    parse_config(sys.argv)
else:
    application = gen_wsgi_app()
