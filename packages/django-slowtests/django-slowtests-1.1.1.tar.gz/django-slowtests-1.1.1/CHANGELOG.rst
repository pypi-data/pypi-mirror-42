Changelog
=========

Current
-------
- Nothing yet

1.1.1 (2019-02-12)
- Return error code to shell in case of failed tests

1.1.0 (2019-02-07)
- Added option to generate full tests reports by passing None to NUM_SLOW_TESTS

1.0.3 (2019-02-05)
- Fixed cast error, leading to slow test ordering issues
- Fixed test case

1.0.2 (2019-02-05)
- Handle django not installed case to ease installation

1.0.1 (2019-02-05)
- Fixed report printed to console

1.0.0 (2019-02-05)
-------
- Dropped Django 1.5* support
- Dropped Python 3.3* support
- Added Django 1.11.* support
- Fixed an issue preventing settings to be taken into account in some case (#24)
- Added an option to generate a report on demand only using a command line
  parameter
- Reports are now compatible with django tests' --parallel option
- Added an option to generate a json file containing the report, instead of
  printing in to console.

0.5.1 (2019-02-04)
------------------
- Initial release at changelog creation.
