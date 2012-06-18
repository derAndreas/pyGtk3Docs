#!/usr/bin/env python

import os
import optparse
import warnings

from pyGtk3Docs import GirConverter


DEFAULT_SAVE_XML_FILENAME = 'PyGTK3Docs.xml'

def _get_opt_parser():
    """ Return a OptionParser instance
        Define the args for commandline usage of converter.py
        
        Returns optparse.OptionParser
    """
    parser = optparse.OptionParser('%prog [options]')
    
    parser.add_option("-s", "--source",
                      action="store", dest="source",
                      default=None,
                      help="the source GTK GIR file to convert")

    parser.add_option("-o", "--output",
                      action="store", dest="output", default=None,
                      help="The destination file or folder")

    parser.add_option("-f", "--format",
                      action="store", dest="format", default='JSON',
                      help="The format of the output file, default JSON, possible: JSON, EXT")
    
    return parser



def main():
    parser = _get_opt_parser()
    (options, args) = parser.parse_args()
    
    if options.source is None or os.path.exists(options.source) is None:
        raise SystemExit('[Error] Need to specifiy a source GIR file to convert')
    
    if options.output is None:
        warnings.warn('No output xml filename given, using "%s"' % DEFAULT_SAVE_XML_FILENAME, UserWarning)
        options.output = DEFAULT_SAVE_XML_FILENAME
    
    if options.format == 'JSON':
        from pyGtk3Docs.format import Json
        formatter = Json.Json
    elif options.format == 'EXT':
        from pyGtk3Docs.format import JsonExtTree
        formatter = JsonExtTree.JsonExtTree
        
    converter = GirConverter.GirConverter(options.source, options.output)
    converter.parse()
    
        
    output = formatter(converter)
    output.write(options.output)
    


if __name__ == '__main__':
    main()
