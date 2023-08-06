# -*- coding: utf-8 -*-

import pytest


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    marker = item.get_closest_marker("disable_plugin")
    if marker is None:
        yield
        return
    [plugin_name] = marker.args
    manager = item.session.config.pluginmanager
    plugin = manager.get_plugin(plugin_name)
    manager.unregister(plugin)
    yield
    item.plugin = plugin


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_teardown(item):
    marker = item.get_closest_marker("disable_plugin")
    if marker is None:
        yield
        return
    [plugin_name] = marker.args
    manager = item.session.config.pluginmanager
    plugin = manager.get_plugin(plugin_name) or item.plugin
    del item._plugin
    print("plugin", plugin)
    yield
    manager.register(plugin)
