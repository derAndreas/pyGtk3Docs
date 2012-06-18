pyGtk3Docs
==========

Custom documentation project for PyGTK3+

Online version available at: http://derandreas.github.com/pyGtk3Docs/output/index.html

Background Information
----------------------
Project was created to start learning PyGTK and have a simple documentation
for easy and fast lookup of usage.

It's based on Sencha Ext2.1 with the design and look of the Ext Documentation.



Getting Started
---------------

The documentation is based on the GTK3+ GIR (XML) Files.
There is an outdated file of GTK3.4 in `test/support` folder.
Weekly updated GIR files can be found at

- https://github.com/roojs/gir-1.2-gtk-3.4
- https://github.com/roojs/gir-1.2-gtk-3.0

A python script converts the GIR files into custom objects and those
objects can be saved to any file you wish, based on the output formatter.

For the start there is just a JSON and JSONExtTree output formatter to generate
the JSON files for the ExtJs Treesystem.

After the JSON files are generated, push the "output" folder to a webserver
or start a simple Python HTTP Server and open the URL in your Browser.



### Converting GIR Files
The python script uses `etree` to work through the XML.

Use it with the arguments:

    python converter.py --help
    Usage: converter.py [options]

    Options:
      -h, --help            show this help message and exit
      -s SOURCE, --source=SOURCE
                            the source GTK GIR file to convert
      -o OUTPUT, --output=OUTPUT
                            The destination file or folder
      -f FORMAT, --format=FORMAT
                            The format of the output file, default JSON, possible:
                            JSON, EXT

To generate the Docs for the ExtJs system use

    python converter.py -s test/support/Gtk-3.0.xml -o output/data/ -f EXT 
    
The Javascript is looking for the JSON files at `output/data/'


### Open in Browser

After that you should be able to open the index.html file via HTTP (not file://).
Use python's HTTPServer if there is no apache (or else) around

     python -m SimpleHTTPServer


Open `http://127.0.0.1:8000/output/index.html` in your Browser


Future plans
------------
The idea is to create a github based open documentation project.
Maybe with the github wiki system or simply by pull request the documentation
should grow and be better.
This is just an idea and there is nothing done right now, to accomplish that.


Last informations
--------------------
Project uses git-flow
I never wrote an pyGTK application, I have no idea if this documentation is really helpful


License
-------
Added License for ExtJs2.1 in the folder `output/resources/js/ext`.
I though EXT2.1 was LGPL, but it seems to be GPL. 

The PyGTKDocs project itself is licensed under MIT...

    Copyright (c) 2012 Andreas Mairhofer

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
