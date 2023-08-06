# ligo-gracedb
Client software for the <b>Gra</b>vitational-wave <b>C</b>andidate <b>E</b>vent <b>D</b>ata<b>b</b>ase, a web service that organizes candidate events from gravitational wave searches and provides an environment to record information about follow-ups.
Further documentation is available at https://wiki.ligo.org/Computing/GraceDB and https://gracedb.ligo.org/documentation/.

Link to new documentation

## Install
Quick install description

## Contributing
Please fork the [repository](https://git.ligo.org/lscsoft/gracedb-client) and submit a merge request if you wish to contribute to this package.


## Testing
Probably move this to the documentation soon

### Unit tests
```bash
python setup.py test
```

### Integration tests
To test the package's compatibility with a GraceDB server requires a superuser account on the server.

```bash
python setup.py integration_test
```

### Compatibility with different versions of Python

Install tox:
```bash
pip install tox
```

Run all tests with all specified versions of Python:
```bash
tox
```

Run unit tests only:
```bash
tox -e $(tox -l | grep unit_test | paste -sd "," -)
```

Run integration tests only:
```bash
tox -e $(tox -l | grep integration_test | paste -sd "," -)
```

Run all tests with one version of Python:
```bash
tox -e $(tox -l | grep py27 | paste -sd "," -)
```
