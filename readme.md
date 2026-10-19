This is MSMS from Ko Jing Rui in Monash University.

This is a Musical School Management System.  This update provide a test and a backup for the user.  This project also develop a function for the admin to record the payment or check the payment history. 

This is a project developed for FIT 1056 as the PST5.

The github page of the project is https://github.com/KoJingRui1/PST5

This is the project structure.

```text
PST5/
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── admin_utils.py
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
├──data/
│   ├── backup/
│   └── msms.json
├──tests/
│   └──test_schedule_manager.py
├── main.py
├── run.bat
├── msms.log
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

This file save data by using json.  The data will be saved at the file

```text
data/msms.json
```

that contains the data about the users, the schools and the courses.

I should talk about the updates before the overview, that is almost the same as the previous version.  In this version, we include a new page in the admin pages, that is finance. First, it allowed admin to record a new payment based on the student user ID and the amount of the money.

There is a list of all payment record for you to check them.

There is also a function to create a report by using scv file.  It will produce an .scv file in the PST5 folder.  You can choose to export the attendance or the finance report.

That's all about the finance page.

The next update is the admin and quality ulitity.  In this update, the system provide a backup file for the user.  It will be in the backup folder.  The function of the backup file is to backup the data.  If there is any data lost, you can recover your data at the place.

A logger is also provide in the system.  Every activity in the system will be recorded in the file msms.log in the PST5.  As an example, 
```
2026-10-19 19:13:48,098 - INFO - Admin ID 1 was successfully created. Name: aa
```
This shows that a new admin is created at 19 October 2026 at 7 o'clock in the night, 13 minutes and 48 seconds.  

The last update is this program provide a test file.  To run the test file, you should enter the terminal, and enter the code for the text file to start.

```
pytest
```

If everything is correct, you will see the following text in the terminal.

```
================================================= test session starts =================================================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Ko Jing Rui'\FIT1056_Works\FIT1056-PSTs-37120077\PST5
plugins: anyio-4.15.1
collected 23 items

tests\test_schedule_manager.py .......................                                                           [100%]

================================================= 23 passed in 0.17s ==================================================
```
That is the update.  After that is the system overview.
If you run the file without an msms.json, that means no data and start over, you will be request to create the first admin.  You should enter your name, your password and confirm your password.

Admin is an important role in the system.  Their role is to control the whole system and edit the data.  After you log in as an admin, you will see five buttons at the side bar.

The deflaut button is the profile button.  It will shows your profile, which contains your name and your ID.  You can update your profile there.  

In the update page, you can choose what to update, your name or your password.  A name should be in between 2-30 characters and does not contain a special character such as ! and , .  To update your password, you should enter your current password.

The next function is the user page.  You can choose a role type and show every user in it.  You can also filter the result with the term selectbox.  In the end of every data, there is a select box.  You can only select per person per time, and choose to update their profile or delete the user.  You cannot delete yourselves as an admin.  There is an add account function at the bottom, which you can choose to add a new account if you want.  

The third function is application.  You can see who had apply to be a teacher and their information in a table.  You can choose one and make your choice, to approve or delete.

The fourth function is courses.  It will shows all the courses in the system.  You can choose a course and edit the course.  The course also provide a function that you can add a new course.  In the update function, you can also add a new lesson in the course.

The fifth function is instrument.  You will see a table with instrument, the teachers speciality is the instrument, the student who enrol in the instrument and the course that teach the instrument.  There is a new function which you can add a new instrument inside the instrument list.

The sixth function is daily roster.  You can choose the date you need and the default date is TODAY.  You can also open the detail of the lessons by chosing them along and see about the course.  You can give attandence to the students also.

The seventh function is the finance, which is writen in the updates.

Now, the last function is for you to log out.  You will go back to the deflaut page.  In this page, you can log in or sign up.

The log in function enable you to enter the system with an existing acount.  You can enter a term such as name and ID, and choose your account.  You will be ask to enter your password. 

The sign up term enable you to create a new account.  In this system, you should be only enable to create a student account.  A teacher account requires you to apply and approve by the admin.  An admin account can only be created by another admin.

The default page for a student is the profile page.  It is exactly same as the admin.

The second page is the enrolment page.  You can enrol for a musical instrument or disenroll one.  If you disenroll one instrument, you will disenroll from the course of the enrolment too.  You can also upgrade a level if you get a certificate.

The third page is the course page.  It provide your course and the lessons that will happen in next 7 days.  You can disenroll or switch a course there.  You can also check in for a course when it is available.  At the bottom of the function, you will see all the suitable course you can get.  You can enroll if you have the password of the course.

The fourth function is the daily roster.  The student can see what they have for a day, and the default date is today.  The student can also check in easily here.

The fifth function is log out.

For the teacher's menu, the default and the first function is teacher profile, which is exactly the same as the students and the admins.

The second function is course.  A teacher can create a course and manage their course there.  The teacher can check students attandence, add lessons in the manage course session.  A teacher can also delete the course.

The daily roster function can enable a teacher to see what is the lesson they are going to teach at a day, and the default date is today.  The teacher can manage their lessons easily there.

The last function, same as admin and student, is log out.

That's all, hope you enjoy your application running.