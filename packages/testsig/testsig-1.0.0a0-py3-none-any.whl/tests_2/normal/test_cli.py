#!/usr/bin/python
# -*- coding: utf-8 -*-
from .. import mock_api
from click.testing import CliRunner
from signate import cli
import pytest
import os

runner = None


@pytest.fixture(scope="function", autouse=True)
def preparation():
    global runner
    cli.set_api_instance({"api-token": "tmp"})
    mock_api.convert_normal(cli)
    runner = CliRunner()


def test_list():
    result = runner.invoke(cli.list)
    assert result.output


def test_files():
    result = runner.invoke(cli.files, ['--competition-id', 1])
    assert result.output


def test_download():
    result = runner.invoke(
        cli.download, ['--competition-id', 1, '--file-id', 1])
    assert result.output


def test_submit():
    with open('sample.csv', 'w') as f:
        f.write('This is sample.')
    result = runner.invoke(
        cli.submit, ['sample.csv', '--competition-id', 1, '--file-id', 1])
    os.remove('sample.csv')
    assert result.output
