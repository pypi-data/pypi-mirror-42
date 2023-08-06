TranscryptFrame
===============

This is a suggestion for a transcrypt framework which offers convenient 
solutions or wrappers around common functions.
Originally created by Andreas Bunkahle 2018

Install it with:

    pip install TranscryptFrame

You can import this library with 
import TranscryptFrame as tf

and use it in your Python/Transcrypt scripts like this

myElement = tf.doc_id("intro")
tf.doc_id("demo").innerHTML = "The text from the intro paragraph is " + myElement.innerHTML

or even shorter:
myElement = tf.S("#intro", "htm")
tf.S("#demo").innerHTML = "The text from the intro paragraph is " + myElement

You can also have jQuery-like function calls like

tf.S("#demo").innerHTML = "<p>New paragraph</p>" instead of $("#demo").html("<p>New paragraph</p>") in Javascript
or document.getElementById("demo").innerHTML = "<p>New paragraph</p>" in Transcrypt

or new_var = tf.S("#demo", "htm") instead of new_var = $("#demo").html()
or new_var = document.getElementById("demo").innerHTML

Examples
========
There are several examples for running the library in 
https://github.com/bunkahle/Transcrypt-Examples/tree/master/dom

You find a tutorial for it at:
https://github.com/bunkahle/Transcrypt-Examples/blob/master/dom/changing_texts.rst

Requirements
============
The code currently only runs under Python 3 due to the fact that Transcrypt is only
available for Python 3. Of course it relies on Transcrypt for running.

License
=======
GNU GPL v3 
