#/bin/sh

VERSION=`python setup.py --version`
git tag "v$VERSION"
git push --tags origin master

python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypi