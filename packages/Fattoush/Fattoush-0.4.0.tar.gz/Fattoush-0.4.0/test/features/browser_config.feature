Feature: Browser Configuration
  As a test developer I want to be able to set a diverse
  variety of browser configurations to facilitate a wider
  testing environment


Scenario Outline: Flat desired capabilities

  Given I pass desired capabilities of "<caps>"
  When fattoush creates a configurations from this
  Then the configuration name is "<name>"

  Examples:
    | name                          | caps                                      |
    | browser=googlechrome          | {"browser": "googlechrome"}               |
    | browser=googlechrome;foo=bar  | {"browser": "googlechrome", "foo": "bar"} |


Scenario: Nested desired capabilities

  Given I pass desired capabilities of "{"browser": "googlechrome", "foo": {"bar" : ["baz"]}}"
  When fattoush creates a configurations from this
  Then it does not crash

Scenario: Provided browser options

  Given I pass desired capabilities of "{"browser": "googlechrome"}"
    And I pass browser options:
        | option                            |
        | start-maximized                   |
        | enable-automation                 |
        | --disable-dev-shm-usage           |
        | --disable-browser-side-navigation |
        | --disable-infobars                |
        | --headless                        |
        | --no-sandbox                      |
        | --disable-gpu                     |
  When fattoush creates a configurations from this
  Then the configuration name is "browser=googlechrome"
   And the configuration has options:
        | option                            |
        | start-maximized                   |
        | enable-automation                 |
        | --disable-dev-shm-usage           |
        | --disable-browser-side-navigation |
        | --disable-infobars                |
        | --headless                        |
        | --no-sandbox                      |
        | --disable-gpu                     |
