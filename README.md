# Backend App

## Design document

Refer to [design.md](./design.md) for more details.

## How to run the app

* First clone the repository

```commandline
git clone git@github.com:MingDevp/leads.git
```

* Go to `./leads` folder, establish a virtual environment, install Python packages
```commandline
cd ./leads
python3 -m env venv
source venv/bin/activate
pip install fastapi
pip install sqlalchemy
pip install sqlmodel
pip install psycopg2-binary
```

* Go to `./app` folder, run the liver server
```commandline
cd ./app
fastapi dev main.py
```

Should be able to check API documentation at http://127.0.0.1:8000/docs/

[![API docs](img/docs.png)](https://github.com/MingDevp/leads)

If seeing error like `ModuleNotFoundError: No module named 'passlib'`, need to install the package
```commandline
pip install passlib
```