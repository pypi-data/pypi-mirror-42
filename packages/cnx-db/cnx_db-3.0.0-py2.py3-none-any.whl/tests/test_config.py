import pytest

from cnxdb.config import discover_settings


def test_success(mocker):
    common_url = 'postgresql:///common'
    readonly_url = 'postgresql:///readonly'
    super_url = 'postgresql:///super'

    _patch = {
        'DB_URL': common_url,
        'DB_READONLY_URL': readonly_url,
        'DB_SUPER_URL': super_url,
    }
    mocker.patch.dict('os.environ', _patch, clear=True)

    settings = discover_settings()

    assert settings['db.common.url'] == common_url
    assert settings['db.readonly.url'] == readonly_url
    assert settings['db.super.url'] == super_url


def test_required(mocker):
    _patch = {}
    mocker.patch.dict('os.environ', _patch, clear=True)

    with pytest.raises(RuntimeError) as exc_info:
        discover_settings()

    assert 'DB_URL' in exc_info.value.args[0]


def test_other_urls_not_required(mocker):
    common_url = 'postgresql:///common'

    _patch = {
        'DB_URL': common_url,
    }
    mocker.patch.dict('os.environ', _patch, clear=True)

    settings = discover_settings()

    assert settings['db.common.url'] == common_url
    assert settings['db.readonly.url'] == common_url
    assert settings['db.super.url'] == common_url


def test_with_existing_settings(mocker):
    common_url = 'postgresql:///common'
    other_url = 'oracle:///common'

    _patch = {
        'DB_URL': other_url,
        'DB_READONLY_URL': other_url,
        'DB_SUPER_URL': other_url,
    }
    mocker.patch.dict('os.environ', _patch, clear=True)
    existing_settings = {
        'db.common.url': common_url
    }

    settings = discover_settings(existing_settings)

    assert settings['db.common.url'] == common_url
    assert settings['db.readonly.url'] == other_url
    assert settings['db.super.url'] == other_url


def test_with_existing_settings_and_no_env(mocker):
    common_url = 'postgresql:///common'

    mocker.patch.dict('os.environ', {}, clear=True)
    existing_settings = {
        'db.common.url': common_url
    }

    settings = discover_settings(existing_settings)

    assert settings['db.common.url'] == common_url
    assert settings['db.readonly.url'] == common_url
    assert settings['db.super.url'] == common_url
