#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Window that display text pass by a socket connection 
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# windowndisplay.py is free software: you can redistribute it and/or modify
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


import pygtk
pygtk.require('2.0')
import gtk
import argparse
import socket
import threading
import pango


class DesktopWindow(gtk.Window):
    """ A transparent and borderless window, fixed on the desktop."""
    
    # Based upon the composited window example from:
    # http://www.pygtk.org/docs/pygtk/class-gdkwindow.html
    
    def __init__(self, full,*args):
        
        gtk.Window.__init__(self, *args)
       
        if not full:
            self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.stick()
        
        self.screen = self.get_screen()
        rgba = self.screen.get_rgba_colormap()
        self.set_colormap(rgba)
        self.set_app_paintable(True)


    def get_screen_width(self):
        return self.screen.get_width()

    def get_screen_height(self):
        return self.screen.get_height()


class SentenceW:
    """ An example widget, which shows a quote embedded into your desktop."""
    
    def __init__(self,full):
        
        self.window = DesktopWindow(full)

        if full:
            self.window.fullscreen()
        
        self.box = gtk.VBox()
                
        self.window.add(self.box)
       
        self.label = gtk.Label()
        self.label.modify_font(pango.FontDescription("ubuntu 32"))
        self.label.set_line_wrap(True)
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.box.pack_start(self.label, expand=True)

               
    def main(self):
        gtk.gdk.threads_init()
        gtk.main()

    def hide(self):
        self.label.set_text("")
        self.label.show()        

    def show(self,str):
        self.label.set_text(str)
        h2=self.window.get_screen_height()
        w2=self.window.get_screen_width()
        (w,h)=self.window.get_size()
        self.window.move((w2-w)/2, (h2-h)/2-(h/2))
        self.window.show_all()        
        

class SCKT(threading.Thread):
       def __init__(self,bind,sentence):
           threading.Thread.__init__(self)
           gtk.gdk.threads_init()
           self.bind=bind
           self.sentence=sentence

       def socketListen(self):
            try:
                 print "Listening to %s:%d"%bind
                 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 s.bind(self.bind) #bound to 127.0.0.1 and port 5000
                 s.listen(1) #At this point only listening for one connection
                 self.clientConn, addrinfo=s.accept()
                 print addrinfo
            except Exception as e:
                print e

       def run(self):
            self.socketListen()
            try:
                running=True
                while(running):
                    MSG=self.clientConn.recv(1024)
                    if len(MSG)==0:
                        running=False
                        gtk.main_quit()
                   
                    if MSG.startswith(':quit'):
                        self.clientConn.close()
                        if opts.verbose:
                            print "Connection finishing"
                        self.sentence.hide()
                        gtk.main_quit()
                    elif MSG.startswith(':hide'):
                        self.sentence.hide()
                    elif MSG.startswith(':record'):
                        self.sentence.record()
                    else:
                        self.sentence.show(MSG)

                    if opts.verbose:
                        print "Displaying:",MSG

            except Exception as e:
                print e
               



if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Speech recognition using sphinx")
    p.add_argument("-i","--ip",default="127.0.0.1",dest="ip",
            action="store", help="IP Addresss to listen")
    p.add_argument("-p","--port",default=5000,dest="port",type=int,
            action="store", help="Por to listen from")
    p.add_argument("-v",'--verbose', action='store_true', 
            help="Verbose on")
    p.add_argument('--version', action='version', version='%(prog)s 0.1')
    opts = p.parse_args()


    bind=(opts.ip,opts.port)


    sentence=SentenceW(False)
    sckt=SCKT(bind,sentence)
    sckt.start()
    sentence.show("")
    sentence.hide()
    sentence.main()



