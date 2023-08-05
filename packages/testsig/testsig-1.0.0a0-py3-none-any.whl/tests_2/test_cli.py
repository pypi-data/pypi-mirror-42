#!/usr/bin/python
# -*- coding: utf-8 -*-
from click.testing import CliRunner
from signate import cli
import os
import pytest
from . import mock_api

runner = None


@pytest.fixture(scope='function', autouse=True)
def preparation():
    global runner
    cli.set_api_instance({'api-token': 'tmp'})
    mock_api.convert_raise_error(cli)
    runner = CliRunner()


def test_list():
    result = runner.invoke(cli.list)
    assert result.exception.body


def test_files():
    result = runner.invoke(cli.files, ['--competition-id', 1])
    assert result.exception.body


def test_download():
    result = runner.invoke(
        cli.download, ['--competition-id', 1, '--file-id', 1])
    assert result.exception.body


def test_submit():
    with open('sample.csv', 'w') as f:
        f.write('This is sample.')
    result = runner.invoke(
        cli.submit, args=['sample.csv', '--competition-id', 1])
    os.remove('sample.csv')
    assert result.exception.body
