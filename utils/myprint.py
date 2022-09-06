#!/usr/bin/env python

class myprint ():
    level = 0
    label = ""
    indent = 0
    color_info = '\033[92m' # green
    color_debug = None
    color_warning = '\033[93m' # green
    color_error = '\033[91m' # green
    bold = '\033[1m'
    endc = '\033[0m'
    def __init__ (self, label = "", level = 0, indent = 0):
        self.level = level
        self.label = label
        self.indent = "".join ([" " for ind in range (indent)])

        
    def print_color (self, msg, color = None):
        if not color: print (msg)
        print (color + msg + self.endc)
        
    def print_debug (self, msg):
        if self.level == 0 : return
        deco_msg = ("DEBUG    \t %s\t %s%s" % (self.label, self.indent, msg))
        self.print_color (deco_msg, self.color_debug)

    def print_info (self, msg):
        deco_msg = ("INFO     \t %s\t %s%s" % (self.label, self.indent, msg))
        self.print_color (deco_msg, self.color_info)

    def print_warning (self, msg):
        deco_msg = ("WARNING  \t %s\t %s%s" % (self.label, self.indent, msg))
        self.print_color (deco_msg, self.color_warning)


    def print_error (self, msg):
        deco_msg = ("ERROR    \t %s\t %s%s" % (self.label, self.indent, msg))
        self.print_color (deco_msg, self.color_error)

    def banner (self, msg):
        indent = 2
        msg_lines = [l.strip() for l in msg.split ("\n")]
        max_line_size = max ([len(l) for l in msg_lines])
        size_banner = max_line_size+indent*2
        decoration = "".join(["*" for i in range (size_banner)])
        print (self.color_info + decoration)
        for l in msg_lines: print ("  " + l + "  ")
        print (decoration + self.endc)
