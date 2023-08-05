[![Build Status](https://img.shields.io/travis/Yelp/pyramid_mock_server.svg)](https://travis-ci.org/Yelp/pyramid_mock_server?branch=master)
[![Coverage Status](https://img.shields.io/coveralls/Yelp/pyramid_mock_server.svg)](https://coveralls.io/r/Yelp/pyramid_mock_server)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyramid_mock_server.svg)](https://pypi.python.org/pypi/pyramid_mock_server/)
[![Latest Released Version](https://img.shields.io/pypi/v/pyramid_mock_server.svg)](https://pypi.python.org/pypi/pyramid_mock_server/)

# pyramid_mock_server
Auto-create a pyramid app from an API description and json response files.

## Documentation

More documentation is available at [http://pyramid_mock_server.readthedocs.org](http://pyramid_mock_server.readthedocs.org)

## Installation
```
$ pip install pyramid_mock_server
```

# Development

Code is documented using [Sphinx](http://www.sphinx-doc.org/en/stable/).

## Setup
```
# Run tests
tox

# Install git pre-commit hooks
tox -e pre-commit install
```

## Contributing

1. Fork it ( https://github.com/Yelp/pyramid_mock_server )
1. Create your feature branch (git checkout -b my-new-feature)
1. Add your modifications
1. Commit your changes (git commit -m "Add some feature")
1. Push to the branch (git push origin my-new-feature)
1. Create new Pull Request

## License

`pyramid_mock_server` is licensed with a [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause).
