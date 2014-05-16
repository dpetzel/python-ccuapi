#/bin/sh

VERSION=`python setup.py --version`
git tag "v$VERSION" || exit 1
git push --tags origin master || exit 1

python setup.py sdist upload -r pypitest || exit 1
python setup.py sdist upload -r pypi || exit 1