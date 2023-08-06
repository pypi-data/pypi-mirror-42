# [MyENV: Environment Variable Parsing using Type annotations][repo_ref]

MyENV parses you're environment variables using type annotations.
This allows you to configure your app/service as layed out by
[12factor.net/config](https://12factor.net/config), while keeping
your code type safe.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer v201902.0007][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][build_img]][build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |    role           |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2018-09 | -     |


<!--
  To update the TOC:
  $ pip install md-toc
  $ md_toc -i gitlab README.md
-->


[](TOC)

- [Environment Variables and Configuration](#environment-variables-and-configuration)
  - [Declaration](#declaration)
  - [Parsing](#parsing)
- [my_service/cfg.py](#my_service-cfg-py)
  - [Config Files](#config-files)
- [config/prod.env](#config-prod-env)

[](TOC)

## Environment Variables and Configuration

In order of priority, configuration is parsed from

 1. Environment variables
 2. Configuration files
 3. Defaults defined in source code


## Declaration

The `myenv` module provides a convenient way to do this parsing.
As far as your application code is concerned, it is enough to
declare a subclass of `myenv.BaseEnv`. Instances of this
subclass are populated from config files and the environment.

```python
import myenv


class Database(myenv.BaseEnv):

    _environ_prefix = "DATABASE_"

    vendor    : str  = "postgres"
    host      : str  = "127.0.0.1"
    port      : int  = 5432
    user      : str  = "myuser"
    password  : str
    name      : str  = "app_db_v1"

    @property
    def url(self) -> str:
        db = self
        return f"{db.vendor}://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"
```

For each annoatated member of `DBEnv` declare the 1. name, 2. type and
3. an optional default  variable. Members without a
default must be set by an environment variable or configuration
file, otherwise a `KeyError` will be raised.


## Parsing

To use the above configuration class, simply instanciate it.

```python
# my_service/cfg.py
import sqlalchemay as sqla

db_cfg = Database()     # populated from os.environ
db_cfg.port             # 12345          (parsed from DATABASE_PORT)
db_cfg.password         # "supersecret"  (parsed from DATABASE_PASSWORD)
db_cfg.url              # "mysql://myuser:supersecret@127.0.0.1:12345/mydb"

engine = sqla.create_engine(db_cfg.url)
```

In case you're worried about the instantiation of `Database()`,
it will return a singleton instance, so the `os.environ` and
configuration files are parsed only once.


## Config Files

When parsing configs, the following paths are parsed if they
exist. By default the configs are loaded from `${PWD}/config/`,
but you can override the location of configuration files by
setting the environment variable `ENV_CONFIG_DIR`.

 - `${ENV_CONFIG_DIR}/${ENV}.env`
 - `${ENV_CONFIG_DIR}/prod.env`

Any variables defined in these files will be set, unless it was
already set in the environ or a previous config file.

This approach allows you to satisfy typical use cases in which a
service is hosted:

 1. Development Machine
 2. Stage/Production Environment

You can put use case specifc configuration files in your project
source tree, such as:

 - `project/config/dev.env`
 - `project/config/stage.env`
 - `project/config/prod.env`

To parse the appropriate config file, all you have to do is set a
single environment variable `ENV=<envname>`. If `ENV` is not set,
it will fall back to `ENV=prod`.

The `*.env` config files are flat text files, with one KEY=value
mapping per line. The only lines which are parsed, are lines which
begin with an all upper case token, followed by an `=` character:

```ini
# config/prod.env
DATABASE_PORT=12345
DATABASE_USER=prod_user
DATABASE_NAME=prod_db
DATABASE_PASSWORD=supersecret
```

For sensitive configuration parameters, such as passwords and
authentication tokens, you may prefer to write config files
outside of your source tree, or to provide them always and only
via environment variables.



[repo_ref]: https://gitlab.com/mbarkhau/myenv

[build_img]: https://gitlab.com/mbarkhau/myenv/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/myenv/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/myenv/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/myenv/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/myenv/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/myenv/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/myenv/#files

[downloads_img]: https://pepy.tech/badge/myenv/month
[downloads_ref]: https://pepy.tech/project/myenv

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=v201902.0007&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/myenv.svg
[pyversions_ref]: https://pypi.python.org/pypi/myenv

