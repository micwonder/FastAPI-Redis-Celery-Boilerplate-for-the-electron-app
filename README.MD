# How to run (contact tech.guru.k.p@gmail.com)

## Environment settings

### Database Setting

#### MySQL install for db
#### Database creation ("beta_projectx_db")
#### User creation ("projectx_root")
#### User Grant ("projectx_root")
#### SQL execution (https://github.com/ObiTracks/px-backend/beta_projectx_db.sql)


### Python Env Setting

#### Python 3.8.x (^3.8.10 preferred)
python --version
#### Virtual Env
python -m venv env
source env/scripts/activate  or  .\env\scripts\activate
pip install -r requirements.txt
#### Run the server
python main.py --env local | dev | prod --debug(optional)

