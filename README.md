<h1 align = 'center'> Qgen </h1>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[![](https://img.shields.io/badge/Made_with-Django-blue?style=for-the-badge&logo=Django)](https://www.djangoproject.com/) 
&emsp;
[![](https://img.shields.io/badge/Made_with-sqlite3-blue?style=for-the-badge&logo=SQLite)](https://docs.python.org/2/library/sqlite3.html)
&emsp;
[![](https://img.shields.io/badge/IDE-Visual_Studio_Code-blue?style=for-the-badge&logo=visual-studio-code)](https://code.visualstudio.com/ "Visual Studio Code")
&emsp;

<h2 align='center'> About </h2>
<p align='center'>
Many times, we read our notes again and again, without ever getting any information inside our head. Havent you noticed that whenver there is a quiz, or whenever you take a test, you learn the material better? Hence, we have created an app, which used Machine Learning and Natural Language Processing to generate flashcards, quizzes, and summary from your notes! Moreover, we have three types of questions: MCQ, Fill in the blanks, and True or False questions to test you on your notes.
You can also upload handwritten notes to generate quizzes so that you can directly upload a photo and generate a quiz.
</p>

-----------------------------------

### Preview

<p align="center">
  <img src ="./assets/qgen-final.gif" width = 900px>
</p>
             
-----------------------------------


### 🚀 Features

<p align="left">
   <ul>
      <li>Add/Edit Notes📕</li>
      <li>Based on your notes generate</li>
      <ul>
         <li>Quiz</li>   
            <ul>
               <li>MCQs 📝</li>
               <li>True/False ✔️ ❎</li>
               <li>Fill in the blanks ❓</li>   
            </ul>
         <li>Summary ✒️</li>
         <li>Flashcards 🔖</li>
         <li>Q/A from images 🚞</li>
      </ul>
      
      
   </ul>
</p>


-----------------------------------
###             💻 Tech stack
`Backend` : Django <br>
`Database` : SQLite <br>
`Frontend` : ReactJs, CSS, HTML, Bootstrap, jQuery  <br>
`ML`: BERT, Spacy, NLTK

-----------------------------------

### :guide_dog: Installation Guide

A step by step series of examples that tell you how to get a development env running

In your cmd:

```
git clone https://github.com/Deep-Matrix/qgen-backend
```

Then,

```
cd qgen-backend
```

Create a virtual environment and activate the virtual environment: 

```
python3 -m venv env
source env/bin/activate
```

Install dependencies using the following: 

```
pip install -r requirements.txt
```

Now run the backend using the following:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


You are done with the setup now!

------------------------------------------
