# CS5551

this is a README file for CS5551 semester project using PYTHON 3

Django project is in 'mysite' folder

To install requirements: `pip install mysite/requirements.txt`

To run project: `python mysite/manage.py runserver`

Before running project Make sure to turn on Docker, Mysql server with username: root and password: root (else change your mysite/mysite/settings.py)

Run `python mysite/manage.py makemigrations`

Run `python mysite/manage.py migrate`

the design docs file contains some files that are built on 
draw.io to open these docs go to draw.io and load them to the site.

this project conisit of three main parts a mySQL DB a Flask bakc end and a vue front end 
style quides for each of these parts can be found below 

To start Redis use this commond: `docker run -p 6379:6379 -d redis:2.8`

INSTALL FOLLOWING LIBRARIES:
pip3 install django-crispy-forms
pip3 install django-bootstrap-forms
pip3 install django-channels
pip3 install channels docker
pip3 install mysqlclient


python:
https://www.python.org/dev/peps/pep-0008/

javascript:
ihttps://google.github.io/styleguide/jsguide.html

To look at Drawio diagram
https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fbrucker3%2FCS5551%2Fmaster%2FdesignDocs%2FcheckersIUmlV3.drawio


MySQL:
https://dev.mysql.com/doc/internals/en/coding-style.html
and
https://www.sqlstyle.guide/


python testing library:
https://docs.pytest.org/en/stable/

reference material on set up for basic unit testing in django:
https://djangostars.com/blog/django-pytest-testing/


code review links
https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/#:~:text=Review%20fewer%20than%20400%20lines%20of%20code%20at%20a%20time&text=In%20practice%2C%20a%20review%20of,seven%20and%20nine%20of%20them.
and 
https://medium.com/palantir/code-review-best-practices-19e02780015f






https://levelup.gitconnected.com/creating-a-board-game-checkers-with-javascript-ecd562f985c2

https://github.com/RyanBranco/Checkers

https://ryanbranco.github.io/Checkers/
