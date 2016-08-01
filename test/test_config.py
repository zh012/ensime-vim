# coding: utf-8

import sexpdata
from py import path
from pytest import raises

from ensime_shared.config import ProjectConfig

confpath = path.local(__file__).dirpath() / 'resources' / 'test.conf'
config = ProjectConfig(confpath.strpath)


def test_parses_dot_ensime():
    assert config.get('scala-version') == '2.11.8'
    assert config['nest'][0]['targets'] == ['abc', 'xyz']


def test_is_immutable():
    with raises(TypeError) as excinfo:
        config['scala-version'] = 'bogus'
    assert 'does not support item assignment' in str(excinfo.value)


def test_knows_its_filepath():
    assert config.filepath == confpath.realpath()


def test_is_dict_like():
    assert set(config.keys()) == set(['name', 'scala-version', 'nest'])
    assert len(config) == 3


def test_fails_when_given_invalid_config():
    badconf = path.local(__file__).dirpath() / 'resources' / 'broken.conf'
    with raises(sexpdata.ExpectClosingBracket):
        ProjectConfig(badconf.strpath)
