# sphinx_enos_theme

## Change Log

### 0.1.2 

* Change toc deep to 4
* Hide current page toc from global toc tree
* Fix a small bug 

### 0.1.1 

* Change selected toc style 
* Add PDF download button
* Add version change dropdown list

## Usage: 

```
pip install sphinx_enos_theme
```

Change `conf.py` 

```
html_theme = "sphinx_enos_theme"
```

## Contribute

Use `gulp` `webpack` to compile CSS/JS and HTML template

### Dependencies

* Python >= 2.7
* node >= 9.0
* gulp >= 4.0
* webpack >= 4.0
* sphinx 

### Before development 

> go to src/templates/layout.html, uncomment line 151 & comment line 153

* prepare dev

```
gulp pre
```

* start dev server 

```
gulp
```

### publish new version 

> go to src/templates/layout.html, comment line 151 and uncomment line 153

update the version number in _init_.py

* build dist

```
gulp build
```

* dist python package

```
python setup.py sdist
```

* publish

```
twine upload dist/*
```