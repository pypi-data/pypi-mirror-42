
install_dbus: clean
	./install_dbus.sh

clean:
	rm -rf .tmp .eggs build dist *.egg-info htmlcov

test: clean
	python setup.py test

coverage: clean
	nosetests -s --with-coverage --cover-package=spoppy --cover-html --cover-html-dir=htmlcov

build: clean
	python setup.py sdist bdist_wheel

check:
	twine check dist/*

upload: build check
	twine upload dist/*

test_upload: build check
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
