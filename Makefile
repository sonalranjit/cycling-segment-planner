PIP = $(VENV)/bin/pip
PYTHON = $(VENT)/bin/python
PYTHON_VERSION = 3.9
VENV = venv

$(PYTHON): setup-py

$(PIP): setup-py

setup-py: $(VENV)

$(VENV): requirements.txt
	python$(PYTHON_VERSION) -m venv $(VENV)
	. $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	touch $(VENV)

pip-freeze: 
	$(PIP) freeze > requirements.txt

clean:
	rm -rf $(VENV)

.PHONY: setup-py clean pip-freeze