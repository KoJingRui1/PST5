from app.user import User


class TeacherUser(User):
    """Represents a teacher."""

    def __init__(self, user_id, name, password, speciality, description):
        #create a teacher as a user with more data
        super().__init__(user_id, name, password)

        self.speciality = speciality        #Store teacher's speciality
        self.description = description      #Store teacher's description


class Course:
    """Represents a single course offered by the school, linked to a teacher."""

    def __init__(self, course_id, name, instrument, teacher_id, grade, password, description, max_student):
        self.id = course_id             #Store course id
        self.name = name                #Store course name
        self.instrument = instrument    #Store course instrument
        self.teacher_id = teacher_id    #Store the teacher id of the course
        self.grade = grade              #Store the grade of the course
        self.password = password        #Store the password of the course
        self.description = description  #Store the description of the course
        self.max_student = max_student  #Store the maximum student of the course
        self.enrolled_student_ids = []  #Store who join the course
        self.lessons = []               #Store the lessons of the course