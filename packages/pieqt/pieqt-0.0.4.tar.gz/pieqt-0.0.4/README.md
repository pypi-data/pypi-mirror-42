## pieqt Project
------

pieqt is a module that helps you start with python qt(PySide2) with minimal effort.Many examples of PySide2 that I've seen are cumbersome, have many classes etc...
With pieqt, you just declare an app variable that holds your GUI app, and then add widgets and layouts.Finally you run it, and thats it!!!
You have a GUI app up and running.

**************Example*******************
----------------------------------------
from pieqt import*

app = App()

app.addWidget(QPushButton("Press me!"))

app.run()


---------------------------------------
**************Example******************
