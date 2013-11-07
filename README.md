AT-NavComputer
==============

Galaxy map and route plotter for a sci-fi universe. Requires Kivy.

Code is very rough and unfinished. Zoom control doesn't work. Initialization of app takes upwards of 2 minutes. 

Star systems are randomized instead of manually placed, making many trade routes look wonky.

Display of more than a few star system labels massively slows down the program.

Display of textures instead of square points for the stars massively slows down the program.

Instead of true 3d, or even fake 3d, all stars are plotted on a single 2d plane.

In short, there's a LOT of work left in this.

Files
=====

routeParser.py
--------------

This is a simple script meant to list systems that might be 'broken' from the 
initial parse, which I have honestly forgotten how I did.

data/main.py
------------

This is the main app. Launch this.
