#Store the program data with json file
import json
#The coding know the real time
import datetime
#import the data to create a user
from app.student import StudentUser
from app.teacher import TeacherUser, Course
from app.admin import AdminUser

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        #initialize all the data before start using the program
        self.data_path = data_path                  #the file path
        self.students = []                          #the students
        self.teachers = []                          #the teachers
        self.courses = []                           #the courses
        self.admins = []                            #the admin
        self.attendance_log = []                    #the attendance log
        self.school_data = {                
            "applications": [],                     #aplication of a teacher
            "next_user_id": 1,                      #record the next user id
            "next_course_id": 1,                    #record the next course id
            "instruments": ["piano", "guitar"]      #record the instruments provide by the musical schools
        }
        self._load_data()                           #load all data from the json file
    
    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""

        try:
            #try to find if the file exist or not
            with open(self.data_path, "r") as f:
                data = json.load(f)
            
            self.students = []      #store student
            self.teachers = []      #store teacher
            self.courses = []       #store course
            self.admins = []        #store admin

            for student_data in data.get("students", []):
                #create student data by using the data
                student = StudentUser(
                    student_data["id"],
                    student_data["name"],
                    student_data["password"]
                )
                #create the data that is not created when a student is create
                student.enrolled_course_ids = student_data.get(
                    "enrolled_course_ids", []
                )

                student.grades = student_data.get(
                    "grades", {}
                )

                #add the teacher data to the manager
                self.students.append(student)
            for teacher_data in data.get("teachers", []):
                #create teacher data by using the data
                teacher = TeacherUser(
                    teacher_data["id"],
                    teacher_data["name"],
                    teacher_data["password"],
                    teacher_data["speciality"],
                    teacher_data["description"]
                )
                #add the data to the manager
                self.teachers.append(teacher)
            for admin_data in data.get("admin", []):
                #create an admin data with the data
                admin = AdminUser(
                    admin_data["id"],
                    admin_data["name"],
                    admin_data["password"]
                )
                #add the admin data to the manager
                self.admins.append(admin)

            for course_data in data.get("courses", []):
                #create a course data with the data
                course = Course(
                    course_data["id"],
                    course_data["name"],
                    course_data["instrument"],
                    course_data["teacher_id"],
                    course_data["grade"],
                    course_data["password"],
                    course_data["description"],
                    course_data["max_student"]
                )
                #add the data that is not exist when course is create
                course.enrolled_student_ids = course_data.get(
                    "enrolled_student_ids", []
                )
                course.lessons = course_data.get(
                    "lessons", []
                )
                #add it to the manager
                self.courses.append(course)
            #get data of attendance
            self.attendance_log = data.get("attendance", [])
            #get data of the school data
            self.school_data = data.get("school_data", {
                "applications": [],
                "next_user_id": 1,
                "next_course_id": 1,
                "instruments": ["piano", "guitar"]
            })
        except FileNotFoundError:
            #if the file is not found, this will be shown

            print("Data file not found. Starting with a clean state.")
    def find_student_by_id(self, id):
        #find a student by enter id 
        for student in self.students:
            if student.id == id:
                return student
        return None
    def find_teacher_by_id(self, id):
        #find a teacher by enter id
        for teacher in self.teachers:
            if teacher.id == id:
                return teacher
        return None
    def find_admin_by_id(self, id):
        #find an admin by enter id
        for admin in self.admins:
            if admin.id == id:
                return admin
        return None
    def find_course_by_id(self, id):
        #find a course by entering id
        for course in self.courses:
            if course.id == id:
                return course
        return None
    def find_user_by_id(self, id):
        #find all of the user together at the same time
        result = self.find_student_by_id(id)
        if not result:
            result = self.find_teacher_by_id(id)
        if not result:
            result = self.find_admin_by_id(id)
        if not result:
            return None
        return result
    def find_teacher(self, term):
        #search for a teacher by using a term
        term = term.lower().strip()
        result = []
        #find it by using id, name, speciality or description
        for teacher in self.teachers:
            if term in teacher.name.lower() or str(teacher.id) == term or term in teacher.speciality.lower() or term in teacher.description.lower():
                result.append(teacher)
        if len(result) == 0:
            print("No match found")
            return None
        else:
            #show all the teacher that fullfilled the requirements
            for i, object in enumerate(result, 1):
                print(f"{i}. ID: {object.id}, Name: {object.name}, Speciality: {object.speciality}")
                print(f"Description: {object.description}")
            return result
    def find_student(self, term):
        #find a student with a term by id, name, or instrument that enrolled
        term = term.lower().strip()
        result = []
        for student in self.students:
            if term in student.name.lower() or str(student.id) == term or any(term in instrument.lower() for instrument in student.grades):
                result.append(student)
        if len(result) == 0:
            print("No match found")
            return None
        else:
            #print all the founded students
            for i, object in enumerate(result, 1):
                print(f"{i}. ID: {object.id}, Name: {object.name}")
            
                if not object.grades:
                    print("   No instruments recorded.")
                else:
                    print("   Grades:")
                    for instrument, level in object.grades.items():
                        print(f"     - {instrument}: Grade {level}")
            return result 
    def find_admin(self, term):
        #find all the admin using a term by their name or id
        term = term.lower().strip()
        result = []
        for admin in self.admins:
            if term in admin.name.lower() or str(admin.id) == term:
                result.append(admin)
        if len(result) == 0:
            print("No match found")
            return None
        else:
            #print all the founded admin
            for i, object in enumerate(result, 1):
                print(f"{i}. ID: {object.id}, Name: {object.name}")
            return result
    def remove_course(self, course_id):
        # Remove a course and clean the course from all related students
        # and attendance records.
        course = self.find_course_by_id(course_id)

        if not course:
            print(f"No course found with id {course_id}.")
            return False

        # Remove the course ID from every student's enrolled courses.
        for student in self.students:
            if course_id in student.enrolled_course_ids:
                student.enrolled_course_ids.remove(course_id)

        # Remove attendance records belonging to this course.
        self.attendance_log = [
            record
            for record in self.attendance_log
            if record.get("course_id") != course_id
        ]

        # Remove the course itself.
        self.courses.remove(course)

        print(f"Course ID {course_id} has been successfully deleted.")
        return True
    def remove_user(self, id):
        # remove a user
        for teacher in self.teachers:
            if teacher.id == id:
                self.teachers.remove(teacher)
                print(f"Teacher with id {id} is successfully deleted.")

                # remove every course from the teacher
                for course in self.courses.copy():
                    if course.teacher_id == id:
                        self.remove_course(course.id)

                return

        for student in self.students:
            if student.id == id:
                self.students.remove(student)
                print(f"Student with id {id} is successfully deleted.")

                # remove the student from enrolled course lists
                for course in self.courses:
                    if id in course.enrolled_student_ids:
                        course.enrolled_student_ids.remove(id)

                return

        for admin in self.admins:
            if admin.id == id:
                self.admins.remove(admin)
                print(f"Admin with id {id} is successfully deleted.")
                return

        print("No user found.")
    def add_teacher_application(
        self, name, password, speciality, description
    ):
        application = {
            "name": name,
            "password": password,
            "speciality": speciality,
            "description": description
        }

        self.school_data["applications"].append(application)
        self._save_data()
    def add_teacher(self, name, password, speciality, description):
        #add a teacher by using Teacher User
        new_id = self.school_data["next_user_id"]
        new_teacher = TeacherUser(new_id, name, password, speciality, description)
        self.teachers.append(new_teacher)
        self.school_data["next_user_id"]+=1
        return new_teacher
    def add_student(self, name, password):
        #add a new student by using Student User
        new_id = self.school_data["next_user_id"]
        new_student = StudentUser(new_id, name, password)
        self.students.append(new_student)
        self.school_data["next_user_id"]+=1
        return new_student
    def add_admin(self, name, password):
        #add an new admin by using adminuser
        new_id = self.school_data["next_user_id"]
        new_admin = AdminUser(new_id, name, password)
        self.admins.append(new_admin)
        self.school_data["next_user_id"]+=1
        return new_admin
    def update_user(self, id, **field):
        # update all of the user by their field
        for teacher in self.teachers:
            if teacher.id == id:
                # Check whether the teacher's speciality is being changed
                old_speciality = teacher.speciality
                new_speciality = field.get("speciality", old_speciality)

                # If speciality changes, remove all courses
                # belonging to this teacher
                if new_speciality != old_speciality:
                    self._remove_teacher_courses(teacher.id)

                for key, value in field.items():
                    setattr(teacher, key, value)

                print(f"User ID {id} has been successfully updated.")
                return

        for student in self.students:
            if student.id == id:
                for key, value in field.items():
                    setattr(student, key, value)

                print(f"User ID {id} has been successfully updated.")
                return

        for admin in self.admins:
            if admin.id == id:
                for key, value in field.items():
                    setattr(admin, key, value)

                print(f"User ID {id} has been successfully updated.")
                return

        print(f"No user found with id {id}.")
    def _remove_teacher_courses(self, teacher_id):
        # Find all courses belonging to this teacher
        course_ids_to_remove = {
            course.id
            for course in self.courses
            if course.teacher_id == teacher_id
        }

        # No courses to remove
        if not course_ids_to_remove:
            return

        # Remove the courses from the system
        self.courses = [
            course
            for course in self.courses
            if course.id not in course_ids_to_remove
        ]

        # Remove the deleted course IDs from every student's
        # enrolled_course_ids
        for student in self.students:
            student.enrolled_course_ids = [
                course_id
                for course_id in student.enrolled_course_ids
                if course_id not in course_ids_to_remove
            ]

        # Remove attendance records belonging to deleted courses
        self.attendance_log = [
            record
            for record in self.attendance_log
            if record.get("course_id") not in course_ids_to_remove
        ]

        print(
            f"Removed {len(course_ids_to_remove)} course(s) "
            f"belonging to Teacher ID {teacher_id}."
        )
    def update_course(self, course_id, **field):
        #update a course information
        course = self.find_course_by_id(course_id)

        if course:
            for key, value in field.items():
                setattr(course, key, value)

            print(f"Course ID {course_id} has been successfully updated.")
            return

        print(f"No course found with id {course_id}.")



    def add_course(self, name, teacher_id, grade, password, description, max_student):
        #create a new course
        new_course_id = self.school_data["next_course_id"]

        instrument = None

        for teacher in self.teachers:
            if teacher_id == teacher.id:
                instrument = teacher.speciality
                break

        if instrument is None:
            print("Teacher not found.")
            return

        new_course = Course(
            new_course_id,
            name,
            instrument,
            teacher_id,
            grade,
            password,
            description,
            max_student
        )

        self.courses.append(new_course)
        self.school_data["next_course_id"] += 1

        print("Course Created")
        print(f"ID: {new_course.id}, Name: {new_course.name}, Teacher ID: {new_course.teacher_id}")
        print(f"Instrument: {new_course.instrument}, Grade: {new_course.grade}")
        print(f"Description: {new_course.description}")
        print(f"Enrolled student ID: {new_course.enrolled_student_ids}")

    def enrol_instrument(self, id, instrument, grade):
        # add a new instrument for a student
        student = self.find_student_by_id(id)

        if not student:
            print("No student found")
            return False

        if instrument in student.grades:
            print(f"Student is already enrolled in {instrument}.")
            return False

        student.grades[instrument] = grade

        print(
            f"Successfully enrolled student ID {id} in {instrument}"
        )

        return True

    def upgrade(self, id, instrument):
        #increase the grade of an instrument
        student = self.find_student_by_id(id)

        if student:
            if instrument in student.grades:
                student.grades[instrument] += 1
                print(f"Student ID {id}, {instrument} successfully upgraded")
                return

            print("Instrument not found")
            return

        print("Student not found")

    def enrol_course(self, student_id, course_id, password):
        # Find course
        course = self.find_course_by_id(course_id)

        if not course:
            print("Course not found.")
            return

        # Check course capacity
        if len(course.enrolled_student_ids) >= course.max_student:
            print("Course is full.")
            return

        # Check course password
        if password != course.password:
            print("Incorrect course password.")
            return

        # Find student
        student = self.find_student_by_id(student_id)

        if not student:
            print("Student not found.")
            return

        # Check whether the student already enrolled
        if course_id in student.enrolled_course_ids:
            print("Student has already enrolled in this course.")
            return

        # Check whether student has the required instrument
        if course.instrument not in student.grades:
            print(f"Student does not have the required instrument: {course.instrument}.")
            return

        # Check whether student's grade is high enough
        student_grade = student.grades[course.instrument]

        if student_grade != course.grade:
            print(
                f"Student grade does not match the course requirement. "
                f"Required: {course.grade}, Student: {student_grade}."
            )
            return

        # Enrollment successful
        student.enrolled_course_ids.append(course_id)
        course.enrolled_student_ids.append(student_id)

        print(
            f"Student ID {student_id} successfully enrolled in "
            f"Course ID {course_id}."
        )

    def switch_course(self, student_id, old_course_id, new_course_id, password):
        # Find old course
        old_course = self.find_course_by_id(old_course_id)

        if not old_course:
            print("Old course not found.")
            return

        # Find new course
        new_course = self.find_course_by_id(new_course_id)

        if not new_course:
            print("New course not found.")
            return

        # Check whether student is currently enrolled in the old course
        student = self.find_student_by_id(student_id)

        if not student:
            print("Student not found.")
            return

        if old_course_id not in student.enrolled_course_ids:
            print("Student is not enrolled in the old course.")
            return

        # Check whether student is already enrolled in the new course
        if new_course_id in student.enrolled_course_ids:
            print("Student is already enrolled in the new course.")
            return

        # Check new course capacity
        if len(new_course.enrolled_student_ids) >= new_course.max_student:
            print("New course is full.")
            return

        # Check new course password
        if password != new_course.password:
            print("Incorrect course password.")
            return

        # Check whether student has the required instrument
        if new_course.instrument not in student.grades:
            print(
                f"Student does not have the required instrument: "
                f"{new_course.instrument}."
            )
            return

        # Check whether student's grade matches the new course
        student_grade = student.grades[new_course.instrument]

        if student_grade != new_course.grade:
            print(
                f"Student grade does not match the new course requirement. "
                f"Required: {new_course.grade}, Student: {student_grade}."
            )
            return

        # Remove student from old course
        student.enrolled_course_ids.remove(old_course_id)
        old_course.enrolled_student_ids.remove(student_id)

        # Add student to new course
        student.enrolled_course_ids.append(new_course_id)
        new_course.enrolled_student_ids.append(student_id)

        print(
            f"Student ID {student_id} successfully switched "
            f"from Course ID {old_course_id} to Course ID {new_course_id}."
        )

    def check_in(self, student_id, course_id, lesson_index):
        """Records a student's attendance for a specific lesson."""

        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        # Check student and course
        if not student or not course:
            print("Error: Invalid Student or Course ID.")
            return False

        # Check whether student is enrolled in this course
        if course_id not in student.enrolled_course_ids:
            print("Error: Student is not enrolled in this course.")
            return False

        # Check lesson index
        if lesson_index < 1 or lesson_index > len(course.lessons):
            print("Error: Invalid lesson.")
            return False

        # Get the selected lesson
        lesson = course.lessons[lesson_index - 1]

        # Get current date and time
        now = datetime.datetime.now()

        lesson_date = datetime.datetime.strptime(
            lesson["date"], "%Y-%m-%d"
        ).date()

        lesson_time = datetime.datetime.strptime(
            lesson["time"], "%H:%M"
        ).time()

        # Check whether today is the lesson date
        if now.date() != lesson_date:
            print("Check-in failed: This is not the lesson date.")
            return False

        # Check whether current time matches lesson time
        lesson_datetime = datetime.datetime.combine(
            lesson_date,
            lesson_time
        )

        # Allow check-in only during the lesson time
        lesson_end = lesson_datetime + datetime.timedelta(hours=1)

        if now < lesson_datetime or now > lesson_end:
            print(
                f"Check-in failed. "
                f"Check-in is only available from "
                f"{lesson['time']} to {lesson_end.strftime('%H:%M')}."
            )
            return False

        # Check whether student has already checked in
        for record in self.attendance_log:
            if (
                record["student_id"] == student_id
                and record["course_id"] == course_id
                and record["lesson_index"] == lesson_index
            ):
                print("Student has already checked in for this lesson.")
                return False

        # Create attendance record
        timestamp = now.isoformat()

        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "lesson_index": lesson_index,
            "date": lesson["date"],
            "time": lesson["time"],
            "activity": lesson["activity"],
            "timestamp": timestamp
        }

        self.attendance_log.append(check_in_record)

        self._save_data()

        print(
            f"Success: Student {student.name} checked into "
            f"{course.name}."
        )

        return True

    def valid_name(self, name):
        # Check name length
        if len(name) < 2 or len(name) > 30:
            print("Invalid name, the name should more than 2 characters and less than 30 characters")
            return False
        if name.strip() == "":
            print("Invalid name, the name shouldn't be empty")
            return False
        # Check every character
        if not all(char.isalpha() or char.isspace() for char in name):
            print("Invalid name, the name shouldn't consists special character.")
            return False
        print("Name accepted:", name)
        return True
    def add_instrument(self, instrument):
        #add a instrument to the list
        if instrument not in self.school_data["instruments"]:
            self.school_data["instruments"].append(instrument)
            print(f"{instrument} has been added.")
        else:
            print(f"{instrument} already exists.")
    def disenroll_instrument(self, id, instrument):
        student = self.find_student_by_id(id)

        if not student:
            print("No student found")
            return False

        if instrument not in student.grades:
            print(f"Student is not enrolled in {instrument}.")
            return False

        del student.grades[instrument]

        courses_to_remove = []

        for course in self.courses:
            if (
                course.id in student.enrolled_course_ids
                and course.instrument == instrument
            ):
                courses_to_remove.append(course.id)

        for course_id in courses_to_remove:
            student.enrolled_course_ids.remove(course_id)

            course = self.find_course_by_id(course_id)

            if course and id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(id)

            self.attendance_log = [
                record
                for record in self.attendance_log
                if not (
                    record.get("student_id") == id
                    and record.get("course_id") == course_id
                )
            ]

        print(
            f"Successfully disenrolled student ID {id} "
            f"from {instrument}."
        )

        return True
    def update_enrollment(self, id, instrument, grade):
        student = self.find_student_by_id(id)

        if not student:
            print("No student found")
            return False

        if instrument not in student.grades:
            print(f"Student is not enrolled in {instrument}.")
            return False

        student.grades[instrument] = grade

        print(
            f"Student ID {id}, {instrument} grade "
            f"successfully updated to {grade}."
        )

        return True
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""

        data_to_save = {
            "students": [s.__dict__ for s in self.students],    #save student data
            "teachers": [t.__dict__ for t in self.teachers],    #save teacher data
            "courses": [c.__dict__ for c in self.courses],      #save courses data
            "admin": [a.__dict__ for a in self.admins],         #save admin data
            "attendance": self.attendance_log,                  #save attendance
            "school_data": self.school_data                     #save school data
        }

        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)