Speech recognition
==================

Continuos live experiments with speech recognisers using sphinx, python and 
windows.


Installation
============

Install pocketsphinx acoustic and language model packages:

    sudo apt-get install pocketsphinx-hmm-wsj1 pocketsphinx-lm-wsj

Install the python pocket sphinx package:

    sudo apt-get install python-pocketsphinx

Install pyaudio:

    sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
    git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
    cd pyaudio
    sudo python setup.py install

For windows project, load project in Visual C++ and compile. 

Usage sphinx
============

Sphinx stand alone
------------------

This is a live standalone recogniser:

    python src/live_sphinx.py

For mor options:
    
    python src/live_sphinx.py -h

Screen server
-------------

This puts a fullscreen server which whatever receves in 127.0.0.1:5000 prints 
it

    python src/windowdisplay.py

For more help:

    python src/windowdisplay.py -h

Sphinx as a client
------------------

To connect the recongniser to the screen server execute:

    python src/live_sphinx.py --connect

Language models
---------------

Por pocketsphinx, it includes some basec language models for english and 
spanish.

Acoustic models
---------------

For english it uses the default hub8

For mexican spanish you can download models from de DIMEx100 page or you may 
be able to train some using CIEMPIESS corpus.

To automatically download DIMEx100 execute the script:

     bash scripts/getsmexspanishacousticmodel.sh 

To test it:

    python src/live_sphinx.py --config config/sino.yam



Usage WindowsRec
================

Todo


