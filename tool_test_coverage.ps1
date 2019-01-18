#################################################################
#
# Script to package and upload Isogeo Python package.
#
#################################################################

"-- STEP -- Creating virtualenv"
py -3 -m venv env3_tests
./env3_tests/Scripts/activate

"-- STEP -- Install and display dependencies within the virtualenv"
python -m pip install -U pip pipenv
pipenv install --dev

"-- STEP -- Python code style"
pycodestyle isogeo_xml_toolbelt/switch_from_geosource.py --ignore="E265,E501" --statistics --show-source
pycodestyle isogeo_xml_toolbelt/csv_reporter.py --ignore="E265,E501" --statistics --show-source
pycodestyle isogeo_xml_toolbelt/reader_iso19110.py --ignore="E265,E501" --statistics --show-source
pycodestyle isogeo_xml_toolbelt/reader_iso19139.py --ignore="E265,E501" --statistics --show-source

"-- STEP -- Run coverage"
coverage run -m unittest discover -s tests/

"-- STEP -- Build and open coverage report"
coverage html
Invoke-Item htmlcov/index.html

"-- STEP -- Exit virtualenv"
deactivate
