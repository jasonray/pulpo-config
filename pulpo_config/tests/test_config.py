import unittest
from pulpo_config import Config
from parameterized import parameterized
import pytest


class TestConfig(unittest.TestCase):

    def test_config_get(self):
        options = {}
        options['k'] = 'v'
        config = Config(options=options)
        self.assertEqual(config.get('k'), 'v')

    def test_config_get_empty(self):
        options = {}
        options['k'] = 'v'
        config = Config(options=options)
        self.assertEqual(config.get('k2'), None)

    def test_config_set(self):
        config = Config()
        config.set('k', 'v')
        # print('config', config.__options)
        self.assertEqual(config.get('k'), 'v')

    def test_config_manual_nested(self):
        options = {}
        options['k'] = {'k2': 'v'}
        config = Config(options)
        self.assertEqual(config.get('k').get('k2'), 'v')

    def test_config_set_nested(self):
        config = Config()
        config.set('k.k2', 'v')
        self.assertEqual(config.get('k').get('k2'), 'v')

    def test_config_set_nested(self):
        config = Config()
        config.set('k.k2a.k3', 'v1')
        config.set('k.k2b.k3a', 'v2')
        config.set('k.k2b.k3b', 'v3')
        self.assertEqual(config.get('k').get('k2a').get('k3'), 'v1')
        self.assertEqual(config.get('k').get('k2b').get('k3a'), 'v2')
        self.assertEqual(config.get('k').get('k2b').get('k3b'), 'v3')

        self.assertEqual(config.get('k.k2a.k3'), 'v1')
        self.assertEqual(config.get('k.k2b.k3a'), 'v2')
        self.assertEqual(config.get('k.k2b.k3b'), 'v3')

        self.assertIsNone(config.get('k.k2b.k3d'))
        self.assertIsNone(config.get('k.k2b.k3.x'))
        self.assertIsNone(config.get('k.k2b.x.x'))

    def test_load_config_from_file(self):
        config = Config(json_file_path='./pulpo_config/tests/test-data/sample-config.json')
        self.assertEqual(config.get('shutdown_after_number_of_empty_iterations'), 7)
        self.assertEqual(config.get('file_queue_adapter.base_path'), '/tmp/kessel/fqa')
        self.assertEqual(config.get('file_queue_adapter').get('base_path'), '/tmp/kessel/fqa')

    def test_load_config_from_file_then_apply_args(self):
        config = Config(json_file_path='./pulpo_config/tests/test-data/sample-config.json')
        self.assertEqual(config.get('shutdown_after_number_of_empty_iterations'), 7)
        self.assertEqual(config.get('file_queue_adapter.base_path'), '/tmp/kessel/fqa')

        args = {}
        args['shutdown_after_number_of_empty_iterations'] = 10
        args['file_queue_adapter.base_path'] = '/t/k/fqa'

        config.process_args(args)

        self.assertEqual(config.get('file_queue_adapter.base_path'), '/t/k/fqa')
        self.assertEqual(config.get('file_queue_adapter').get('base_path'), '/t/k/fqa')

    # disable yapf so it does not re-format the param test
    # yapf: disable
    @parameterized.expand((
         (True, True),
         ("True", True),
         ("true", True),
         ("T", True),
         ("t", True),
         ("1", True),
         (1, True),
         (False, False),
         ("False", False),
         ("false", False),
         ("F", False),
         ("f", False),
         ("0", False),
         (0, False),
         (2, False),
         ("donkey", False),
    ))
    # yapf: enable
    def test_config_get_bool(self, input, expected_result):
        options = {}
        options['k'] = input
        config = Config(options=options)
        self.assertEqual(config.getAsBool('k'), expected_result)

    # disable yapf so it does not re-format the param test
    # yapf: disable
    @parameterized.expand((
         (1, 1),
         (10, 10),
         (1.0, 1, False),
         ("1", 1),
         ("10", 10),
         ("1.0", None, True),
         ("xyz", None, True),
         ("", None, True)
    ))
    # yapf: enable
    def test_config_get_int(self, input, expected_result, expected_error=False):
        print(f'test_config_get_int [input={input}][expected={expected_result}][expect error={expected_error}]')
        options = {}
        options['k'] = input
        config = Config(options=options)

        if expected_error:
            with pytest.raises(Exception):
                config.getAsInt('k')
        else:
            self.assertEqual(config.getAsInt('k'), expected_result)

    # disable yapf so it does not re-format the param test
    # yapf: disable
    @parameterized.expand((
         (True, True),
         ("True", True),
         ("true", True),
         ("T", True),
         ("t", True),
         ("1", True),
         (1, True),
         (False, False),
         ("False", False),
         ("false", False),
         ("F", False),
         ("f", False),
         ("0", False),
         (0, False),
         (2, False),
         ("donkey", False),
    ))
    # yapf: enable
    def test_config_get_bool_with_default(self, default, expected_result):
        options = {}
        config = Config(options=options)
        self.assertEqual(config.getAsBool('k', default), expected_result)

    def test_to_string_single(self):
        config = Config()
        config.set('k', 'v')
        self.assertEqual(str(config), "{'k': 'v'}")
        self.assertEqual(config.to_string(), "{'k': 'v'}")

    def test_to_string_two(self):
        config = Config()
        config.set('k1', 'v1')
        config.set('k2', 'v2')
        self.assertEqual(str(config), "{'k1': 'v1', 'k2': 'v2'}")
        self.assertEqual(config.to_string(), "{'k1': 'v1', 'k2': 'v2'}")

    def test_to_string_nested(self):
        config = Config()
        config.set('k1', 'v1')
        config.set('k2', 'v2')
        config.set('k.k3', 'v3')
        config.set('k.k4', 'v4')
        config.set('kk.k5', 'v5')
        self.assertEqual(str(config), "{'k1': 'v1', 'k2': 'v2', 'k': {'k3': 'v3', 'k4': 'v4'}, 'kk': {'k5': 'v5'}}")
        self.assertEqual(config.to_string(), "{'k1': 'v1', 'k2': 'v2', 'k': {'k3': 'v3', 'k4': 'v4'}, 'kk': {'k5': 'v5'}}")

    def test_to_json(self):
        config = Config()
        config.set('k1', 'v1')
        config.set('k2', 'v2')
        config.set('k.k3', 'v3')
        config.set('k.k4', 'v4')
        config.set('kk.k5', 'v5')
        self.assertEqual(config.to_json(), '{"k1": "v1", "k2": "v2", "k": {"k3": "v3", "k4": "v4"}, "kk": {"k5": "v5"}}')
