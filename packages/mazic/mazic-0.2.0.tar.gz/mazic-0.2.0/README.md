# mazic
🐱

when push a new release version, remember to do the following

- 1. modify 'setup.py' (version, dependency...)
- 2. run `python setup.py sdist`
- 3. run `twine upload dist/mazic-0.2.0.tar.gz`
