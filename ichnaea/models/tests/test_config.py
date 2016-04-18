import uuid

from ichnaea.models.config import ExportConfig
from ichnaea.tests.base import DBTestCase


class TestExportConfig(DBTestCase):

    def test_fields(self):
        skip_keys = [uuid.uuid4().hex for i in range(3)]
        skip_sources = ['query', 'fused']
        self.session.add(ExportConfig(
            name='internal', batch=100,
            schema='internal', url='internal://',
            skip_keys=skip_keys, skip_sources=skip_sources,
        ))
        self.session.flush()

        result = self.session.query(ExportConfig).get('internal')
        self.assertEqual(result.name, 'internal')
        self.assertEqual(result.batch, 100)
        self.assertEqual(result.schema, 'internal')
        self.assertEqual(result.url, 'internal://')
        self.assertEqual(result.skip_keys, frozenset(skip_keys))
        self.assertEqual(result.skip_sources, frozenset(skip_sources))

    def test_allowed(self):
        configs = [
            ExportConfig(name='none', skip_keys=None, skip_sources=None),
            ExportConfig(name='test', skip_keys=['test'], skip_sources=None),
            ExportConfig(name='gnss', skip_keys=None, skip_sources=['gnss']),
            ExportConfig(name='query', skip_keys=['test', 'test2'],
                         skip_sources=['query']),
        ]
        self.session.add_all(configs)
        self.session.commit()

        def test(name, api_key, source, expected):
            row = (self.session.query(ExportConfig)
                               .filter(ExportConfig.name == name)).first()
            self.assertEqual(row.allowed(api_key, source), expected)

        test('none', None, None, True)
        test('none', None, 'gnss', True)
        test('none', 'test', None, True)
        test('none', 'test', 'gnss', True)

        test('test', None, None, True)
        test('test', None, 'gnss', True)
        test('test', 'test', None, False)
        test('test', 'test', 'gnss', False)
        test('test', 'test2', 'gnss', True)

        test('gnss', None, None, True)
        test('gnss', None, 'gnss', False)
        test('gnss', None, 'query', True)
        test('gnss', 'test', None, True)
        test('gnss', 'test', 'gnss', False)
        test('gnss', 'test', 'query', True)

        test('query', None, None, True)
        test('query', None, 'gnss', True)
        test('query', None, 'query', False)
        test('query', 'test', None, False)
        test('query', 'test', 'gnss', False)
        test('query', 'test', 'query', False)
        test('query', 'test2', None, False)

    def test_skip_keys(self):
        non_ascii = b'\xc3\xa4'.decode('utf-8')
        configs = [
            ExportConfig(name='none', skip_keys=None),
            ExportConfig(name='list', skip_keys=[]),
            ExportConfig(name='set', skip_keys=set()),
            ExportConfig(name='one', skip_keys=['ab']),
            ExportConfig(name='two', skip_keys=['ab', 'cd']),
            ExportConfig(name='unicode', skip_keys=['ab', non_ascii]),
        ]
        self.session.add_all(configs)
        self.session.commit()

        def test(name, expected):
            row = (self.session.query(ExportConfig)
                               .filter(ExportConfig.name == name)).first()
            self.assertEqual(row.skip_keys, expected)

        test('none', None)
        test('list', frozenset())
        test('set', frozenset())
        test('one', frozenset(['ab']))
        test('two', frozenset(['ab', 'cd']))
        test('unicode', frozenset(['ab', non_ascii]))