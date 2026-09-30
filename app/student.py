from app.user import User


class StudentUser(User):
    """Represents a student, inheriting from the base User class."""

    def __init__(self, user_id, name, password):
        #Store student as a user
        super().__init__(user_id, name, password)

        # Courses the student has enrolled in
        self.enrolled_course_ids = []

        # Grade for each instrument
        self.grades = {}

