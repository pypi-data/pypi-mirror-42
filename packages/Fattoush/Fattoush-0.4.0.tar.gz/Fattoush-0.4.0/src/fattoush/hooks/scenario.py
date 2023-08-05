# (c) 2014 Mind Candy Ltd. All Rights Reserved.
# Licensed under the MIT License; you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://opensource.org/licenses/MIT.

"""
Hooks that run before and after scenarios
"""
from lettuce import (
    after,
    before,
)

from fattoush.namespace import per


@before.each_scenario
def set_per_scenario(_):
    per.scenario = {}


@before.each_scenario
def hook_rename_scenario(scenario, *_):
    feature = scenario.feature
    scenario.name = "{0}.{1}".format(feature.name, scenario.name)


def clear_browser_etc():

    browser = per.scenario.get('browser')
    if browser is not None:
        browser.delete_all_cookies()
        browser.quit()

    del per.scenario


@after.each_scenario
def clear_per_scenario(*_):
    clear_browser_etc()


@after.outline
def clear_per_iteration(*_):
    clear_browser_etc()
    set_per_scenario(_)
