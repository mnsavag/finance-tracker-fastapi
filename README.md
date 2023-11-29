# finance-tracker-fastapi

Backend for finance tracker application.

At the moment the project is being rewritten to a different architecture

## Main stack

- Python
- Fastapi
- PostgreSQL
- SQLAlchemy

## Project Structure

```bash
fastapi-project
├─ alembic/
└─ src
   └─ user
      ├─ data
      │  ├─ models # db models
      │  └─ repositories
      ├─ domain
      │  ├─ schemas # pydantic models
      │  └─ services # module specific business logic
      └─ presentation
         ├─ handlers.py
         └─ router.py
      ├─ exceptions.py
      ├─ dependencies.py
      ├─ utils.py
   ├─ config.py # global configs
   ├─ models.py # global models
   ├─ exceptions.py # global exceptions
   ├─ database.py # db connection related stuff
   ├─ sql_alchemy_repository.py # global repository
   ├─ main.py
├── .env
├── .gitignore
└── alembic.ini
```
