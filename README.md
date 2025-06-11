### Backend App School Management

This project to provide API core CRUD
[![Star this project](https://img.shields.io/github/stars/nguyenvanro/School_Management_BE?style=social)](https://github.com/nguyenvanro/School_Management_BE)

## Install & Run Project

# 1. Clone repository

```bash
git clone https://github.com/nguyenvanro/School_Management_BE.git
cd School_Management_BE
```

# 2. Create file .env
create file .env from .env.sample

fill information in to file .env

# 3. Setting Library
# 3.1 Creating a Python virtual environment in Linux

Step 1: Ensure Python and pip are installed
```bash
sudo apt update
sudo apt install python3 python3-pip python3-ven
```
Step 2: Create a virtual environment
```bash
python3 -m venv myenv
```
Step 3: Activate the virtual environment
```bash
source myenv/bin/activate
pip install -r requirements.txt
```
# 3.2 Creating a Python virtual environment in Windows
Step 1: Create a virtual environment
```bash
python -m venv myenv
```
Step 2: Activate the virtual environment
```bash
myenv\Scripts\activate
pip install -r requirements.txt
```

# 4. Run migrate and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

# 5. Run server
- developement
```bash
python manage.py runserver
```
- production
```bash
gunicorn core_app.wsgi:application --bind 0.0.0.0:8000
```
- docker
```bash
docker-compose up --build
```

## Contact
Github: [https://github.com/nguyenvanro]
