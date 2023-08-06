# Publishing new versions

git tag -a v0.0.0 -m "v0.0.0"
git push --tags
pip install -U pip setuptools wheel twine
python setup.py sdist bdist_wheel --universal
twine upload dist/*