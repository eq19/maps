
# 

These instructions are biased for MacOSX. If you're on Linux, these should be trivially easy.

You have [home brew](http://brew.sh/), right? Good.

Not to self: Keep on documenting with [markdown files](https://daringfireball.net/projects/markdown/basics).

## Installing Python

Start by getting python 3.

    brew install python3

If you run into an issue during the install that complains about zlib, [see this out to find the fix](https://github.com/Homebrew/homebrew/issues/23717)

In short:
    xcode-select --install

And then I found I had to reinstall python3:

    brew reinstall python3

## Virtual Envs

We're going to follow good python hygene and use virtual environments to silo our install dependencies. 

Go get  http://virtualenv.readthedocs.org/en/latest/installation.html

    pip install virtualenv

then the basic commands are:

    mkvirtualenv some-name-related-to-your-project
    lsvirtualenv list all virtual envs
    workon some-other-related-project
    deactive

## Get the virtual env working

    cd prime-hexagon
    mkvirtualenv prime-hexagon
    workon prime-hexagon
    pip install numpy
    pip install cython
    pip install primesieve
    pip install pytest





