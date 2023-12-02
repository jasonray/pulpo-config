import typing
import json
import argparse
import os
import copy

class Config():
    __options = None

    def __init__(self, options: dict = None, json_file_path: str = None):
        if not options and json_file_path:
            options = self._load_options_from_file(json_file_path=json_file_path)
        elif not options:
            options = {}

        if isinstance(options, dict):
            self.__options = copy.deepcopy (options )
        elif isinstance(options, Config):
            self.__options = options.__options

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.__options)

    def to_json(self):
        return json.dumps(self.__options)

    def process_args(self, args: dict):
        if args:
            if isinstance(args, argparse.ArgumentParser):
                args = args.parse_args()
            if isinstance(args, argparse.Namespace):
                args = vars(args)

            for arg in args:
                print(f'processing args [arg={arg}]')
                # value = getattr(args, arg)
                value = args.get(arg)
                if value:
                    self.set(arg, value)

    def _load_options_from_file(self, json_file_path: str = None) -> dict:
        options = None
        with open(json_file_path, "rb") as f:
            options = json.load(f)
        return options

    def get(self, key: str, default_value: typing.Any = None):
        keys = key.split('.')

        value = self.__options
        for subkey in keys:
            if value:
                if subkey in value:
                    value = value[subkey]
                else:
                    value = None
            else:
                value = None

        if not value:
            value = default_value

        value = self._get_handle_env(value)

        return value

    def _get_handle_env(self, value):
        Environment_Variable_Prefix = '$ENV.'
        if value:
            if isinstance(value, str):
                if value.startswith(Environment_Variable_Prefix):
                    env_var_key = value[len(Environment_Variable_Prefix):]
                    value = os.getenv(env_var_key)
        return value

    def getAsBool(self, key: str, default_value: typing.Any = None) -> bool:
        value_raw = self.get(key=key, default_value=default_value)
        value = None
        true_values = [True, 'TRUE', 'T', '1', 1]
        if isinstance(value_raw, str):
            value_raw = value_raw.upper()
        value = value_raw in true_values
        return value

    def getAsInt(self, key: str, default_value: int = None) -> int:
        value_raw = self.get(key=key, default_value=default_value)
        try:
            value = int(value_raw)
        except Exception as ex:
            raise Exception(f'Invalid config value (expected numeric value) [key={key}][value={value_raw}]') from ex
        return value

    # support key=a.b.c where it will create intermediate dictionaries
    def set(self, key: str, value: typing.Any):
        keys = key.split('.')

        parent = self.__options
        for key_number in range(0, len(keys) - 1):
            key = keys[key_number]
            if not key in parent:
                parent[key] = {}
            parent = parent.get(key)

        last_key = keys[len(keys) - 1]
        parent[last_key] = value
