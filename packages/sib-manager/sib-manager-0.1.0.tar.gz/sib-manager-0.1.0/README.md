# Startin'Blox Installer

Test it in local environment (with optional virtualenv):
```
$ pip install --user -U git+https://git.happy-dev.fr/startinblox/sib
$ sib startproject myproject -m djangoldp_project -m djangoldp_account -m djangoldp_circle --venv
```

Test it within docker:
```
$ docker run --rm -p 127.0.0.1:8000:8000 -it python:3.6 bash
# pip install git+https://git.happy-dev.fr/startinblox/sib
# sib startproject myproject -m djangoldp_project -m djangoldp_account -m djangoldp_circle
# cd myproject
# sib runserver
```
