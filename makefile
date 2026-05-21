PYTHON = python3
VENV = venv
APP_PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
PYTHONPATH = .

.PHONY: help install seed run serve check routes clean

help:
	@echo "Commandes disponibles:"
	@echo "  make install  - Cree le venv et installe les dependances"
	@echo "  make seed     - Remplit la base SQLite avec des donnees de test"
	@echo "  make run      - Lance l'API en mode developpement"
	@echo "  make serve    - Lance l'API en mode serveur local"
	@echo "  make check    - Verifie la syntaxe et l'import de l'application"
	@echo "  make routes   - Affiche les routes principales"
	@echo "  make clean    - Supprime les caches Python"

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

seed:
	PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python app/seed.py

run:
	PYTHONPATH=$(PYTHONPATH) $(UVICORN) app.main:app --reload

serve:
	PYTHONPATH=$(PYTHONPATH) $(UVICORN) app.main:app --host 0.0.0.0 --port 8000

check:
	@PYTHONPYCACHEPREFIX=/tmp/banking_sim_pycache $(APP_PYTHON) -m py_compile \
		app/main.py \
		app/routes/clients.py \
		app/routes/accounts.py \
		app/routes/transactions.py \
		app/models.py \
		app/schemas.py \
		app/database.py \
		app/seed.py \
		app/crud.py \
		service/risk_engine.py
	@$(APP_PYTHON) -B -c 'import app.main; print("import ok")'

routes:
	@$(APP_PYTHON) -B -c 'from app.main import app; [print("{:<12} {}".format(",".join(sorted(route.methods or [])), route.path)) for route in app.routes]'

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
