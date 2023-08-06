
# ipython_pylint #

Magic function for running pylint on IPython / Jupyter cell.


## Installation ##


    pip install ipython_pylint

or, for the current git master branch:

    pip install 'git+https://github.com/HoverHell/ipython_pylint.git#egg=ipython_pylint'


## usage ##

Add in an ipython / jupyter cell:

    %load_ext ipython_pylint.magic

Add invocation to the top of the cell that needs to be checked:

    %%lint
    print("Hello world")

The incovation has various options:

    %%lint --optional --no-history

See `%%lint?` for the documentation.


## See also ##

See also: pycodestyle (pep8) and flake8 checker:
https://github.com/mattijn/pycodestyle_magic
