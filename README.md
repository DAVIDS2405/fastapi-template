# Fastapi template

To use the template yo need to use Python 3.11

## Create Template

To create the template yo need to use

- Linux

```bash
python3 -m virtualenv .venv
```

- Windows

```powershell
python -m virtuelenv .venv
```

## Install dependences

Activate environment

- Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

- Windows

```powershell
.\.venv\Scripts\activate

pip install -r .\requirements.txt
```

## Execute

Configure .env file whit

- PORT = the port if you prefer example(8000)

- HOST = url of your host example (localhost)

Then execute this command

- Linux

```bash
python3 app/main.py
```

- Windows

```powershell
python .\app\main.py
```
