# Over And Over And Over
(short o3a2)

quick proof of conecpt for defining tasks and their dependencies as python functions and running them as CLI application

## demo / build instructions

create and activate a venv, then

```
python build.py install_editable
```

to create a release wheel
```
python build.py build_release
```

to run linting
```
python build.py lint
```

## usage
to bootstrap manually install o3a2, then run the following in the root of your project
```
python -m o3a2 install
```
then create a `build.py` similar to the one in this repository and add your build steps