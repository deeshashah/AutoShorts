# Autoshorts

Autoshorts is a Django web application, which uses the python scraper explained in this repository : [New Articles Scraper](https://github.com/deeshashah/News-Article-Scraper)
Many news websites are very cluttered and often too much of unnecessary images and information is present. Thus, in this application, we have used very minimal detailing and presented only what is required. 
The application is hosted here : [Autoshorts](https://autoshorts.herokuapp.com/)

### Working 

1. The main page : 
<kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/1.png)</kbd>
2. User has to register :
<kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/3.png)</kbd>
3. User has to login :
<kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/2.png)</kbd>
4. The dashboard : 
   Here, all the latest news are displayed.
   <kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/4.png)</kbd>
5. Short summaries can be viewed :
<kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/5.png)</kbd>
6. The full article :
<kbd>![normal](https://raw.githubusercontent.com/rikenshah/what-the-image/master/screenshots/6.png)</kbd>

### Running this application 
1. You need to first set up a python virtual environment where all the dependencies will be installed. If you are not aware of virtual environment, visit here [Setting up Python virtual environment](https://rikenshah.github.io/articles/setting-up-python-environment/)

2. The packages required for this application are added in _requirements.txt_ file. In order to install all the packages run the following command with the virtual environment activated :

```python
pip install -r requirements.txt
```

3. Once the packages are installed, start the Django application : 
```python
python manage.py runserver
```
You should get :
```python
Performing system checks...

System check identified no issues (0 silenced).
June 22, 2017 - 05:29:31
Django version 1.10.5, using settings 'newsFrontEnd.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

The application has been started at _127.0.0.1:8000_

### Technologies used :
1. _Django_ : Django is a python's framework for developing web applications. To know more about Django, visit here [Django documentation](https://docs.djangoproject.com/en/1.11/)

2. _Materialize_ : Materialize is a responsive mordern framework for developing front-end. It is based on the principles of Material design, created and developed by Google
For more on Materialize, [Materialize documentation](http://materializecss.com/about.html)

3. _Summa_ : Summa is github repository using text rank for summarisation. We have used this for generating summaries for the extracted articles. For more on using Summa [Summa](https://github.com/summanlp/textrank)

### Future Work 

1. We are working on an algorithm which automatically creates abstractive summaries of the scraped articles

2. We plan to use Machine Learning to learn user choices and add a news recommendation system

3. Working on Topic mining to classify news articles in different topics

