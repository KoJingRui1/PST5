This is MSMS from Ko Jing Rui in Monash University.

This is a Musical School Management System.  This update provide an User Interface.  It replace the text console with a modern Graphical User interface by using streamlit.  

This is a project developed for FIT 1056 as the PST4.

This is the project structure.

```text
PST4/
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── schedule.py
│   ├── student.py
│   └── teacher.py
│
├── gui/
│   ├── __init__.py
│   ├── main_dashboard.py
│   ├── default_page.py
│   ├── student_pages.py
│   ├── teacher_pages.py
│   └── admin_pages.py
│
├── main.py
├── run.bat
└── README.md
```
The requirements of this system is python, streamlit and pandas.  The project uses a Python virtual environment for its dependencies.

How to run the application?

There are two choice for you two run the application after you had download it.  First, you can open a terminal in a root directory and run

```python
streamlit run main.py
```

or double-click this file

```text
run.bat
```

