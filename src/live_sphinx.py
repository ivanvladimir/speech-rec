#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Live sphinx 
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# live_sphinx.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------

# System libraries
import argparse
import sys
import yaml
import audio
import time
# Audio libraries


# Sphinx library
try:
    import pocketsphinx as ps
except:
    import pocketsphinx as ps




# Local import
import defaults


if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Speech recognition using sphinx")
    p.add_argument("-c","--config",default=None,dest='config',
            action="store", help="Configuration file for recogniser")
    p.add_argument("-d","--device",default=None,dest='device', type=int,
            action="store", help="Device")
    p.add_argument("-l", "--list",default=False,
        action="store_true", dest="list", help="Lists devices availables")
    p.add_argument("-v",'--verbose', action='store_true', 
            help="Verbose on")
    p.add_argument('--version', action='version', version='%(prog)s 0.1')
    opts = p.parse_args()

    # Setting verbose
    if opts.verbose:
       def verbose(*args):
           print " ".join([str(a) for a in args])
    else:   
       verbose = lambda *a: None 

    # Checking if ask listing devices
    if opts.list:
        verbose('List devices mode')
        for info in audio.getInDevices():
            print ' {0} - {1}'.format(*info)
        sys.exit()

    if opts.config:
        with open(opts.config) as config_file:
            config = yaml.load(config_file)
    else:
        config={}

    # Setting defaults
    for key in defaults.sphinx_config.keys():
        try:
            config[key]
        except KeyError:
            config[key]=defaults.sphinx_config[key]
            verbose("Setting",key,"to default:",config[key])


    # Setting recognizer
    speechRec = ps.Decoder(
                hmm=config['hmm'], 
                lm=config['lm'], 
                dict=config['dict'])
    
    # Setting the audio
    info = audio.getDeviceInfo(opts.device)
    stream = audio.connect(info)

    stream.start_stream()
    while True:
        if audio.status['file']:
            data = file('voz.wav', 'rb')
            data.seek(44)
            speechRec.decode_raw(data)
            print "Recongnize: ",speechRec.get_hyp()[0]
            audio.status['file']=False
        time.sleep(1)


