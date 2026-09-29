# JoyWeb Studio

A complete Flask business website for JoyWeb Studio, Ngozi, Burundi.

## Included
- Home / About / Services / Portfolio / Pricing / Contact
- Project quotation form
- SQLite lead database
- Admin login and leads dashboard
- Responsive dark + green design
- WhatsApp button
- Online deployment instructions

## Termux / Linux
```bash
cd ~/JoyWeb_Studio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="your-long-secret"
export ADMIN_PASSWORD="your-strong-password"
python app.py
```
Open http://127.0.0.1:5003

Admin: http://127.0.0.1:5003/admin/login

## Windows 10
```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set SECRET_KEY=your-long-secret
set ADMIN_PASSWORD=your-strong-password
py app.py
```

## Production
```bash
pip install -r requirements.txt
gunicorn -w 2 -b 0.0.0.0:5003 app:app
```
Use a domain, HTTPS, reverse proxy and strong secrets. For a larger production system, consider PostgreSQL/MySQL.

## Deploy on Render
Use a GitHub repository and create a Render Web Service.
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
- Environment variables: `SECRET_KEY`, `ADMIN_PASSWORD`
The included `render.yaml` contains the deployment configuration.
