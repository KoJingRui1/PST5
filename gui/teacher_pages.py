import streamlit as st
from app.teacher import TeacherUser, Course
import datetime
import pandas as pd
def success_page(title, message, detail, return_page):
    st.title(title)
    st.success(message)

    if detail:
        st.write(detail)

    if st.button("OK"):
        st.session_state.teacher_page = return_page

        if "selected_user_id" in st.session_state:
            del st.session_state.selected_user_id

        st.rerun()


def show_teacher_page(manager, user):
    st.sidebar.title("Teacher Menu")
    st.sidebar.subheader(f"{user.name}")

    if "teacher_page" not in st.session_state:
        st.session_state.teacher_page = "Profile"

    if st.sidebar.button("Profile", width="stretch"):
        st.session_state.teacher_page = "Profile"
        st.rerun()

    if st.sidebar.button("Course", width="stretch"):
        st.session_state.teacher_page = "Course"
        st.rerun()

    if st.sidebar.button("Daily Roster", width="stretch"):
        st.session_state.teacher_page = "Daily Roster"
        st.rerun()


    if st.sidebar.button("Logout", width="stretch"):
        st.session_state.user = None
        st.session_state.teacher_page = "Profile"
        st.rerun()

    page = st.session_state.teacher_page

    # ---------------------------------------------------------
    # Profile
    # ---------------------------------------------------------
    if page == "Profile":
        st.title("Teacher Profile")

        st.subheader(f"ID: {user.id}")
        st.subheader(f"Name: {user.name}")
        st.subheader(f"Speciality: {user.speciality}")
        st.subheader(f"Description: {user.description}")

        if st.button("Update Profile"):
            st.session_state.teacher_page = "Update Profile"
            st.rerun()

    # ---------------------------------------------------------
    # Update Profile
    # ---------------------------------------------------------
    elif page == "Update Profile":
        st.title("Update Profile")

        choice = st.selectbox(
            "Update Term",
            ["Name", "Password", "Description"]
        )

        # -----------------------------------------------------
        # Update Name
        # -----------------------------------------------------
        if choice == "Name":
            new_name = st.text_input(
                "Please enter your NEW NAME."
            )

            if st.button("Update"):
                if not manager.valid_name(new_name):
                    st.error("Invalid name.")
                elif new_name == user.name:
                    st.error(
                        "The new name is the same as the current name."
                    )
                else:
                    manager.update_user(
                        user.id,
                        name=new_name
                    )

                    manager._save_data()

                    st.session_state.teacher_page = (
                        "Profile Update Success"
                    )

                    st.rerun()

        # -----------------------------------------------------
        # Update Password
        # -----------------------------------------------------
        elif choice == "Password":
            current_password = st.text_input(
                "Please enter your CURRENT password.",
                type="password"
            )

            new_password = st.text_input(
                "Please enter your NEW password.",
                type="password"
            )

            confirm_password = st.text_input(
                "Please confirm your NEW password.",
                type="password"
            )

            if st.button("Update"):
                if current_password != user.password:
                    st.error("The current password is incorrect.")
                elif new_password != confirm_password:
                    st.error("The passwords do not match.")
                elif new_password == user.password:
                    st.error(
                        "The new password is the same as the current password."
                    )
                else:
                    manager.update_user(
                        user.id,
                        password=new_password
                    )

                    manager._save_data()

                    st.session_state.teacher_page = (
                        "Profile Update Success"
                    )

                    st.rerun()

        # -----------------------------------------------------
        # Update Description
        # -----------------------------------------------------
        elif choice == "Description":
            new_description = st.text_area(
                "Please enter the NEW description.",
                value=user.description
            )

            if st.button("Update"):
                if new_description == user.description:
                    st.error(
                        "The new description is the same as the current description."
                    )
                else:
                    manager.update_user(
                        user.id,
                        description=new_description
                    )

                    manager._save_data()

                    st.session_state.teacher_page = (
                        "Profile Update Success"
                    )

                    st.rerun()

    # ---------------------------------------------------------
    # Profile Update Success
    # ---------------------------------------------------------
    elif page == "Profile Update Success":
        success_page(
            "Profile Updated",
            "Your profile has been updated successfully!",
            "Your account information has been saved.",
            "Profile"
        )

    # =========================================================
    # Course
    # =========================================================

    elif page == "Course":

        st.title("Course")

        # -----------------------------------------------------
        # Only show courses belonging to the current teacher
        # -----------------------------------------------------

        teacher_courses = [
            course
            for course in manager.courses
            if course.teacher_id == user.id
        ]

        if not teacher_courses:
            st.info("You currently have no courses.")
            if st.button(
                "Add Course",
                width="stretch"
            ):
                st.session_state.teacher_page = "Add Course"
                st.rerun()
        else:

            course_data = []

            for course in teacher_courses:
                course_data.append({
                    "ID": course.id,
                    "COURSE NAME": course.name,
                    "INSTRUMENT": course.instrument,
                    "GRADE": course.grade,
                    "DESCRIPTION": course.description,
                    "MAX STUDENT": course.max_student,
                    "STUDENTS": len(course.enrolled_student_ids),
                    "Select": False
                })

            edited_courses = st.data_editor(
                course_data,
                width="stretch",
                hide_index=True,
                disabled=[
                    "ID",
                    "COURSE NAME",
                    "INSTRUMENT",
                    "GRADE",
                    "DESCRIPTION",
                    "MAX STUDENT",
                    "STUDENTS"
                ],
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select one course",
                        default=False
                    )
                },
                key="teacher_course_editor"
            )

            st.divider()

            # -------------------------------------------------
            # Get selected course
            # -------------------------------------------------

            selected_courses = [
                teacher_courses[index]
                for index, row in enumerate(edited_courses)
                if row["Select"]
            ]

            col1, col2, col3 = st.columns(3)

            # -------------------------------------------------
            # Manage Course
            # -------------------------------------------------

            with col1:
                if st.button(
                    "Manage Course",
                    width="stretch"
                ):

                    if len(selected_courses) != 1:
                        st.error(
                            "Please select exactly one course."
                        )
                    else:
                        st.session_state.selected_course_id = (
                            selected_courses[0].id
                        )
                        st.session_state.teacher_page = "Manage Course"
                        st.rerun()

            # -------------------------------------------------
            # Delete Course
            # -------------------------------------------------

            with col2:
                if st.button(
                    "Delete Course",
                    width="stretch"
                ):

                    if len(selected_courses) != 1:
                        st.error(
                            "Please select exactly one course."
                        )
                    else:
                        st.session_state.selected_course_id = (
                            selected_courses[0].id
                        )
                        st.session_state.teacher_page = "Delete Course"
                        st.rerun()

            # -------------------------------------------------
            # Add Course
            # -------------------------------------------------

            with col3:
                if st.button(
                    "Add Course",
                    width="stretch"
                ):
                    st.session_state.teacher_page = "Add Course"
                    st.rerun()
    # =========================================================
    # Add Course
    # =========================================================

    elif page == "Add Course":

        st.title("Add Course")

        st.write(f"Teacher ID: {user.id}")
        st.write(f"Teacher Name: {user.name}")

        # Instrument is automatically based on the teacher's speciality
        instrument = user.speciality

        st.text_input(
            "Instrument",
            value=instrument,
            disabled=True
        )

        course_name = st.text_input("Course Name")

        max_student = st.number_input(
            "Max Student",
            min_value=1,
            value=10,
            step=1
        )

        grade = st.number_input(
            "Grade",
            min_value=1,
            value=1,
            step=1
        )

        password = st.text_input(
            "Course Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Course Password",
            type="password"
        )

        description = st.text_area(
            "Description"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Create Course",
                width="stretch"
            ):

                if not course_name.strip():
                    st.error("Please enter the course name.")

                elif password != confirm_password:
                    st.error("The passwords do not match.")

                elif not description.strip():
                    st.error("Please enter the course description.")

                else:

                    new_course_id = manager.school_data[
                        "next_course_id"
                    ]

                    new_course = Course(
                        new_course_id,
                        course_name,
                        instrument,
                        user.id,
                        grade,
                        password,
                        description,
                        int(max_student)
                    )

                    manager.courses.append(new_course)

                    manager.school_data[
                        "next_course_id"
                    ] += 1

                    manager._save_data()

                    st.session_state.teacher_page = (
                        "Add Course Success"
                    )

                    st.rerun()

        with col2:
            if st.button(
                "Cancel",
                width="stretch"
            ):
                st.session_state.teacher_page = "Course"
                st.rerun()
    # =========================================================
    # Add Course Success
    # =========================================================

    elif page == "Add Course Success":

        st.title("Course Added")

        st.success(
            "The course has been added successfully!"
        )

        st.write(
            "The new course has been saved."
        )

        if st.button("OK"):

            st.session_state.teacher_page = "Course"

            if "selected_course_id" in st.session_state:
                del st.session_state.selected_course_id

            st.rerun()
    # =========================================================
    # Delete Course
    # =========================================================

    elif page == "Delete Course":

        st.title("Delete Course")

        if "selected_course_id" not in st.session_state:
            st.error("No course has been selected.")
            if st.button("Back"):
                st.session_state.teacher_page = "Course"
                st.rerun()

        else:

            selected_course_id = st.session_state.selected_course_id

            target_course = manager.find_course_by_id(
                selected_course_id
            )

            # -------------------------------------------------
            # Check whether the course exists
            # -------------------------------------------------

            if target_course is None:

                st.error("Course not found.")

                if st.button("Back"):
                    del st.session_state.selected_course_id
                    st.session_state.teacher_page = "Course"
                    st.rerun()

            # -------------------------------------------------
            # Check whether this course belongs to the teacher
            # -------------------------------------------------

            elif target_course.teacher_id != user.id:

                st.error(
                    "You do not have permission to delete this course."
                )

                if st.button("Back"):
                    del st.session_state.selected_course_id
                    st.session_state.teacher_page = "Course"
                    st.rerun()

            else:

                st.subheader("Course Information")

                st.write(f"Course ID: {target_course.id}")
                st.write(f"Course Name: {target_course.name}")
                st.write(f"Instrument: {target_course.instrument}")
                st.write(f"Grade: {target_course.grade}")
                st.write(f"Max Student: {target_course.max_student}")
                st.write(
                    f"Enrolled Students: "
                    f"{len(target_course.enrolled_student_ids)}"
                )
                st.write(
                    f"Description: {target_course.description}"
                )

                st.divider()

                st.warning(
                    "Deleting this course will remove the course "
                    "from the system and remove all student "
                    "enrolments for this course."
                )

                # -------------------------------------------------
                # Teacher identity confirmation
                # -------------------------------------------------

                teacher_password = st.text_input(
                    "Please enter your password to confirm your identity.",
                    type="password"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Confirm Delete Course",
                        width="stretch"
                    ):

                        if teacher_password != user.password:

                            st.error(
                                "Wrong password."
                            )

                        else:

                            deleted_course_name = target_course.name

                            manager.remove_course(
                                target_course.id
                            )

                            manager._save_data()

                            st.session_state.deleted_course_name = (
                                deleted_course_name
                            )

                            del st.session_state.selected_course_id

                            st.session_state.teacher_page = (
                                "Delete Course Success"
                            )

                            st.rerun()

                with col2:

                    if st.button(
                        "Cancel",
                        width="stretch"
                    ):

                        del st.session_state.selected_course_id

                        st.session_state.teacher_page = "Course"

                        st.rerun()
    # =========================================================
    # Delete Course Success
    # =========================================================

    elif page == "Delete Course Success":

        st.title("Course Deleted")

        st.success(
            "The course has been deleted successfully!"
        )

        st.write(
            f"{st.session_state.get('deleted_course_name', 'The course')} "
            "and its course information have been removed."
        )

        if st.button("OK"):

            st.session_state.teacher_page = "Course"

            if "deleted_course_name" in st.session_state:
                del st.session_state.deleted_course_name

            st.rerun()
    # =========================================================
    # Manage Course
    # =========================================================

    elif page == "Manage Course":

        st.title("Manage Course")

        # -----------------------------------------------------
        # Check whether a course has been selected
        # -----------------------------------------------------

        if "selected_course_id" not in st.session_state:

            st.error("No course has been selected.")

            if st.button("Back"):
                st.session_state.teacher_page = "Course"
                st.rerun()

        else:

            target_course = manager.find_course_by_id(
                st.session_state.selected_course_id
            )

            # -------------------------------------------------
            # Check course
            # -------------------------------------------------

            if target_course is None:

                st.error("Course not found.")

                if st.button("Back"):
                    del st.session_state.selected_course_id
                    st.session_state.teacher_page = "Course"
                    st.rerun()

            # -------------------------------------------------
            # Check teacher ownership
            # -------------------------------------------------

            elif target_course.teacher_id != user.id:

                st.error(
                    "You do not have permission to manage this course."
                )

                if st.button("Back"):
                    del st.session_state.selected_course_id
                    st.session_state.teacher_page = "Course"
                    st.rerun()

            else:

                # =================================================
                # Teacher Identity Verification
                # =================================================

                teacher_password = st.text_input(
                    "Please enter your password to confirm your identity.",
                    type="password"
                )

                if teacher_password != user.password:

                    if teacher_password:
                        st.error("Wrong password.")

                    st.info(
                        "Please enter your password to continue."
                    )

                else:

                    # =================================================
                    # Course Information
                    # =================================================

                    st.subheader("Course Information")

                    st.write(
                        f"Course ID: {target_course.id}"
                    )

                    st.write(
                        f"Course Name: {target_course.name}"
                    )

                    st.write(
                        f"Instrument: {target_course.instrument}"
                    )

                    st.write(
                        f"Grade: {target_course.grade}"
                    )

                    st.write(
                        f"Teacher: {user.name} (ID: {user.id})"
                    )

                    current_student_count = len(
                        target_course.enrolled_student_ids
                    )

                    st.write(
                        f"Students: {current_student_count} / "
                        f"{target_course.max_student}"
                    )

                    st.divider()
                    # =================================================
                    # Add Lesson
                    # =================================================

                    st.subheader("Add Lesson")

                    lesson_date = st.date_input(
                        "Date",
                        min_value=datetime.date.today(),
                        key=f"manage_lesson_date_{target_course.id}"
                    )

                    lesson_time = st.time_input(
                        "Time",
                        key=f"manage_lesson_time_{target_course.id}"
                    )

                    lesson_activity = st.text_input(
                        "Activity",
                        key=f"manage_lesson_activity_{target_course.id}"
                    )

                    if st.button(
                        "Add Lesson",
                        key=f"add_lesson_{target_course.id}"
                    ):

                        lesson_datetime = datetime.datetime.combine(
                            lesson_date,
                            lesson_time
                        )

                        if lesson_datetime <= datetime.datetime.now():

                            st.error(
                                "The lesson must be scheduled "
                                "for a future time."
                            )

                        elif not lesson_activity.strip():

                            st.error(
                                "Please enter the lesson activity."
                            )

                        else:

                            new_lesson = {
                                "date": lesson_date.strftime(
                                    "%Y-%m-%d"
                                ),
                                "time": lesson_time.strftime(
                                    "%H:%M"
                                ),
                                "activity": lesson_activity.strip()
                            }

                            target_course.lessons.append(
                                new_lesson
                            )

                            manager._save_data()

                            st.success(
                                "Lesson added successfully!"
                            )

                            st.rerun()

                    st.divider()

                    # =================================================
                    # Remove Future Lesson
                    # =================================================

                    st.subheader("Remove Lesson")

                    future_lessons = []

                    now = datetime.datetime.now()

                    for lesson_index, lesson in enumerate(
                        target_course.lessons,
                        start=1
                    ):

                        lesson_datetime = datetime.datetime.strptime(
                            f"{lesson['date']} {lesson['time']}",
                            "%Y-%m-%d %H:%M"
                        )

                        if lesson_datetime > now:

                            future_lessons.append(
                                (
                                    lesson_index,
                                    lesson,
                                    lesson_datetime
                                )
                            )

                    if not future_lessons:

                        st.info(
                            "There are no future lessons to remove."
                        )

                    else:

                        lesson_options = {}

                        for lesson_index, lesson, lesson_datetime in (
                            future_lessons
                        ):

                            label = (
                                f"Lesson {lesson_index}: "
                                f"{lesson['date']} "
                                f"{lesson['time']} - "
                                f"{lesson['activity']}"
                            )

                            lesson_options[label] = lesson_index

                        selected_lesson_label = st.selectbox(
                            "Select a future lesson to remove",
                            list(lesson_options.keys()),
                            key=(
                                f"remove_lesson_select_"
                                f"{target_course.id}"
                            )
                        )

                        if st.button(
                            "Remove Lesson",
                            key=f"remove_lesson_{target_course.id}"
                        ):

                            selected_lesson_index = (
                                lesson_options[
                                    selected_lesson_label
                                ]
                            )

                            removed_lesson = (
                                target_course.lessons.pop(
                                    selected_lesson_index - 1
                                )
                            )

                            manager._save_data()

                            st.success(
                                f"Lesson on "
                                f"{removed_lesson['date']} "
                                f"at "
                                f"{removed_lesson['time']} "
                                f"has been removed."
                            )

                            st.rerun()

                    st.divider()
                    # =================================================
                    # Course Settings
                    # =================================================

                    st.subheader("Course Settings")

                    max_student = st.number_input(
                        "Max Student",
                        min_value=current_student_count,
                        value=target_course.max_student,
                        step=1
                    )

                    description = st.text_area(
                        "Description",
                        value=target_course.description
                    )

                    st.subheader("Change Course Password")

                    new_password = st.text_input(
                        "New Password",
                        type="password"
                    )

                    confirm_password = st.text_input(
                        "Confirm New Password",
                        type="password"
                    )

                    st.divider()

                    # =================================================
                    # Lessons and Attendance
                    # =================================================

                    st.subheader("Lessons")

                    if not target_course.lessons:

                        st.info(
                            "No lessons have been scheduled."
                        )

                    else:

                        now = datetime.datetime.now()

                        for lesson_index, lesson in enumerate(
                            target_course.lessons,
                            start=1
                        ):

                            lesson_datetime = datetime.datetime.strptime(
                                f"{lesson['date']} {lesson['time']}",
                                "%Y-%m-%d %H:%M"
                            )

                            # =================================================
                            # Lesson Information
                            # =================================================

                            st.write(
                                f"### Lesson {lesson_index}"
                            )

                            st.write(
                                f"Date: {lesson['date']}"
                            )

                            st.write(
                                f"Time: {lesson['time']}"
                            )

                            st.write(
                                f"Activity: {lesson['activity']}"
                            )

                            # =================================================
                            # Past Lesson
                            # =================================================

                            if lesson_datetime <= now:

                                st.caption(
                                    "This lesson has already occurred."
                                )

                                st.write("Attendance")

                                if not target_course.enrolled_student_ids:

                                    st.info(
                                        "There are no students enrolled "
                                        "in this course."
                                    )

                                else:

                                    for student_id in (
                                        target_course.enrolled_student_ids
                                    ):

                                        student = (
                                            manager.find_student_by_id(
                                                student_id
                                            )
                                        )

                                        if student is None:
                                            continue

                                        attendance_exists = any(
                                            record["student_id"]
                                            == student_id
                                            and record["course_id"]
                                            == target_course.id
                                            and record["lesson_index"]
                                            == lesson_index
                                            for record
                                            in manager.attendance_log
                                        )

                                        col1, col2 = st.columns(
                                            [4, 1]
                                        )

                                        # -----------------------------------------
                                        # Student Status
                                        # -----------------------------------------

                                        with col1:

                                            if attendance_exists:

                                                st.write(
                                                    f"✓ {student.name} "
                                                    f"(ID: {student.id}) "
                                                    "- Present"
                                                )

                                            else:

                                                st.write(
                                                    f"{student.name} "
                                                    f"(ID: {student.id}) "
                                                    "- Absent"
                                                )

                                        # -----------------------------------------
                                        # Attendance Button
                                        # -----------------------------------------

                                        with col2:

                                            if attendance_exists:

                                                if st.button(
                                                    "Delete Attendance",
                                                    key=(
                                                        f"delete_attendance_"
                                                        f"{target_course.id}_"
                                                        f"{lesson_index}_"
                                                        f"{student.id}"
                                                    )
                                                ):

                                                    success = manager.delete_attendance(
                                                        student.id,
                                                        target_course.id,
                                                        selected_lesson_index
                                                    )

                                                    if success:
                                                        manager._save_data()
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to delete attendance.")
                                            else:

                                                if st.button(
                                                    "Give Attendance",
                                                    key=(
                                                        f"attendance_"
                                                        f"{target_course.id}_"
                                                        f"{lesson_index}_"
                                                        f"{student.id}"
                                                    )
                                                ):

                                                    success = manager.give_attendance(
                                                        student.id,
                                                        target_course.id,
                                                        lesson_index
                                                    )

                                                    if success:
                                                        manager._save_data()
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to give attendance.")
                            # =================================================
                            # Future Lesson
                            # =================================================

                            else:

                                st.caption(
                                    "Upcoming lesson. "
                                    "Attendance is not available yet."
                                )

                            st.divider()
                    # =================================================
                    # Save / Cancel
                    # =================================================

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "Save Changes",
                            width="stretch"
                        ):

                            if (
                                new_password
                                and new_password
                                != confirm_password
                            ):

                                st.error(
                                    "The passwords do not match."
                                )

                            elif max_student < current_student_count:

                                st.error(
                                    "Max Student cannot be lower "
                                    "than the current number of students."
                                )

                            else:

                                update_fields = {
                                    "max_student": int(max_student),
                                    "description": description
                                }

                                if new_password:
                                    update_fields["password"] = (
                                        new_password
                                    )

                                manager.update_course(
                                    target_course.id,
                                    **update_fields
                                )

                                manager._save_data()

                                del st.session_state.selected_course_id

                                st.session_state.teacher_page = (
                                    "Manage Course Success"
                                )

                                st.rerun()

                    with col2:

                        if st.button(
                            "Cancel",
                            width="stretch"
                        ):

                            del st.session_state.selected_course_id

                            st.session_state.teacher_page = "Course"

                            st.rerun()
    # =========================================================
    # Manage Course Success
    # =========================================================

    elif page == "Manage Course Success":

        st.title("Course Updated")

        st.success(
            "The course has been updated successfully!"
        )

        st.write(
            "The course information has been saved."
        )

        if st.button("OK"):

            st.session_state.teacher_page = "Course"

            if "deleted_course_name" in st.session_state:
                del st.session_state.deleted_course_name

            st.rerun()
    # ---------------------------------------------------------
    # Daily Roster
    # ---------------------------------------------------------
    elif page == "Daily Roster":

        st.title("Daily Roster")

        # -----------------------------------------------------
        # Select Date
        # -----------------------------------------------------

        selected_date = st.date_input(
            "Select Date",
            value=datetime.date.today()
        )

        selected_date_string = selected_date.strftime("%Y-%m-%d")

        # -----------------------------------------------------
        # Find lessons taught by this teacher
        # -----------------------------------------------------

        roster_data = []

        now = datetime.datetime.now()

        for course in manager.courses:

            # -------------------------------------------------
            # Teacher can only see their own courses
            # -------------------------------------------------

            if course.teacher_id != user.id:
                continue

            for lesson_index, lesson in enumerate(
                course.lessons,
                start=1
            ):

                if lesson["date"] != selected_date_string:
                    continue

                # -------------------------------------------------
                # Get lesson date and time
                # -------------------------------------------------

                lesson_datetime = datetime.datetime.strptime(
                    f"{lesson['date']} {lesson['time']}",
                    "%Y-%m-%d %H:%M"
                )

                # -------------------------------------------------
                # Count enrolled students
                # -------------------------------------------------

                expected_students = len(
                    course.enrolled_student_ids
                )

                # -------------------------------------------------
                # Count Present students
                # -------------------------------------------------

                present_students = 0

                for record in manager.attendance_log:

                    if (
                        record["course_id"] == course.id
                        and record["lesson_index"] == lesson_index
                        and record["student_id"]
                        in course.enrolled_student_ids
                    ):
                        present_students += 1

                # -------------------------------------------------
                # Attendance display
                # -------------------------------------------------

                if lesson_datetime <= now:

                    attendance = (
                        f"{present_students} / "
                        f"{expected_students}"
                    )

                else:

                    attendance = (
                        f"{expected_students} / "
                        f"{expected_students}"
                    )

                roster_data.append(
                    {
                        "Course ID": course.id,
                        "Course Name": course.name,
                        "Time": lesson["time"],
                        "Attendance": attendance,
                        "Lesson Index": lesson_index,
                        "Select": False
                    }
                )

        # -----------------------------------------------------
        # Sort by time
        # -----------------------------------------------------

        roster_data.sort(
            key=lambda x: x["Time"]
        )

        # -----------------------------------------------------
        # Display table
        # -----------------------------------------------------

        if len(roster_data) == 0:

            st.info(
                "There are no courses scheduled for this date."
            )

        else:

            roster_df = pd.DataFrame(
                roster_data,
                columns=[
                    "Course ID",
                    "Course Name",
                    "Time",
                    "Attendance",
                    "Lesson Index",
                    "Select"
                ]
            )

            edited_roster = st.data_editor(
                roster_df,
                column_config={

                    "Course ID": st.column_config.NumberColumn(
                        "Course ID",
                        width="small",
                        disabled=True
                    ),

                    "Course Name": st.column_config.TextColumn(
                        "Course Name",
                        width="medium",
                        disabled=True
                    ),

                    "Time": st.column_config.TextColumn(
                        "Time",
                        width="small",
                        disabled=True
                    ),

                    "Attendance": st.column_config.TextColumn(
                        "Attendance",
                        width="medium",
                        disabled=True
                    ),

                    "Lesson Index": st.column_config.NumberColumn(
                        "Lesson Index",
                        width="small",
                        disabled=True
                    ),

                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        width="small"
                    )
                },

                hide_index=True,
                width="stretch",
                key="teacher_daily_roster_table"
            )

            # -----------------------------------------------------
            # Select Course
            # -----------------------------------------------------

            if st.button(
                "Select Course",
                width="stretch"
            ):

                selected_rows = edited_roster[
                    edited_roster["Select"] == True
                ]

                if len(selected_rows) == 0:

                    st.error(
                        "Please select a course."
                    )

                elif len(selected_rows) > 1:

                    st.error(
                        "Please select only one course."
                    )

                else:

                    selected_row = selected_rows.iloc[0]

                    st.session_state.selected_roster_course_id = (
                        int(selected_row["Course ID"])
                    )

                    st.session_state.selected_roster_lesson_index = (
                        int(selected_row["Lesson Index"])
                    )

                    st.session_state.teacher_page = (
                        "Daily Roster Detail"
                    )

                    st.rerun()


    # =========================================================
    # Daily Roster Detail
    # =========================================================

    elif page == "Daily Roster Detail":

        st.title("Daily Roster Detail")

        # -----------------------------------------------------
        # Check selected lesson
        # -----------------------------------------------------

        if (
            "selected_roster_course_id"
            not in st.session_state
            or
            "selected_roster_lesson_index"
            not in st.session_state
        ):

            st.error("No lesson has been selected.")

            if st.button("Back to Daily Roster"):

                st.session_state.teacher_page = "Daily Roster"

                st.rerun()

        else:

            selected_course_id = (
                st.session_state.selected_roster_course_id
            )

            selected_lesson_index = (
                st.session_state.selected_roster_lesson_index
            )

            target_course = manager.find_course_by_id(
                selected_course_id
            )

            # -------------------------------------------------
            # Check course
            # -------------------------------------------------

            if target_course is None:

                st.error("Course not found.")

                if st.button("Back to Daily Roster"):

                    del st.session_state.selected_roster_course_id
                    del st.session_state.selected_roster_lesson_index

                    st.session_state.teacher_page = (
                        "Daily Roster"
                    )

                    st.rerun()

            # -------------------------------------------------
            # Check teacher ownership
            # -------------------------------------------------

            elif target_course.teacher_id != user.id:

                st.error(
                    "You do not have permission to view this course."
                )

                if st.button("Back to Daily Roster"):

                    del st.session_state.selected_roster_course_id
                    del st.session_state.selected_roster_lesson_index

                    st.session_state.teacher_page = (
                        "Daily Roster"
                    )

                    st.rerun()

            else:

                # -------------------------------------------------
                # Check lesson
                # -------------------------------------------------

                if (
                    selected_lesson_index < 1
                    or
                    selected_lesson_index
                    > len(target_course.lessons)
                ):

                    st.error("Lesson not found.")

                    if st.button("Back to Daily Roster"):

                        del st.session_state.selected_roster_course_id
                        del st.session_state.selected_roster_lesson_index

                        st.session_state.teacher_page = (
                            "Daily Roster"
                        )

                        st.rerun()

                else:

                    lesson = target_course.lessons[
                        selected_lesson_index - 1
                    ]

                    # -------------------------------------------------
                    # Lesson Information
                    # -------------------------------------------------

                    st.subheader("Lesson Information")

                    info_col1, info_col2, info_col3 = st.columns(3)

                    with info_col1:

                        st.write(
                            f"**Course:** {target_course.name}"
                        )

                    with info_col2:

                        st.write(
                            f"**Date:** {lesson['date']}"
                        )

                    with info_col3:

                        st.write(
                            f"**Time:** {lesson['time']}"
                        )

                    st.write(
                        f"**Activity:** {lesson['activity']}"
                    )

                    st.divider()

                    # -------------------------------------------------
                    # Attendance
                    # -------------------------------------------------

                    st.subheader("Attendance")

                    if not target_course.enrolled_student_ids:

                        st.info(
                            "There are no students enrolled in this course."
                        )

                    else:

                        now = datetime.datetime.now()

                        lesson_datetime = datetime.datetime.strptime(
                            f"{lesson['date']} {lesson['time']}",
                            "%Y-%m-%d %H:%M"
                        )

                        # -------------------------------------------------
                        # Count Present
                        # -------------------------------------------------

                        present_count = 0

                        for student_id in (
                            target_course.enrolled_student_ids
                        ):

                            attendance_exists = any(
                                record["student_id"] == student_id
                                and record["course_id"]
                                == target_course.id
                                and record["lesson_index"]
                                == selected_lesson_index
                                for record
                                in manager.attendance_log
                            )

                            if attendance_exists:

                                present_count += 1

                        total_students = len(
                            target_course.enrolled_student_ids
                        )

                        # -------------------------------------------------
                        # Attendance Summary
                        # -------------------------------------------------

                        if lesson_datetime <= now:

                            st.write(
                                f"**Present: "
                                f"{present_count} / "
                                f"{total_students}**"
                            )

                        else:

                            st.write(
                                f"**Expected Attendance: "
                                f"{total_students} / "
                                f"{total_students}**"
                            )

                            st.caption(
                                "This lesson has not started yet."
                            )

                        st.divider()

                        # -------------------------------------------------
                        # Student Attendance List
                        # -------------------------------------------------

                        for student_id in (
                            target_course.enrolled_student_ids
                        ):

                            student = (
                                manager.find_student_by_id(
                                    student_id
                                )
                            )

                            if student is None:
                                continue

                            attendance_exists = any(
                                record["student_id"] == student_id
                                and record["course_id"]
                                == target_course.id
                                and record["lesson_index"]
                                == selected_lesson_index
                                for record
                                in manager.attendance_log
                            )

                            col1, col2 = st.columns([4, 1])

                            with col1:

                                if attendance_exists:

                                    st.write(
                                        f"✓ **{student.name}** "
                                        f"(ID: {student.id}) - Present"
                                    )

                                else:

                                    st.write(
                                        f"**{student.name}** "
                                        f"(ID: {student.id}) - Absent"
                                    )

                            with col2:

                                # -----------------------------------------
                                # Past / Current Lesson
                                # -----------------------------------------

                                if lesson_datetime <= now:

                                    if attendance_exists:

                                        if st.button(
                                            "Delete Attendance",
                                            key=(
                                                f"teacher_delete_attendance_"
                                                f"{target_course.id}_"
                                                f"{selected_lesson_index}_"
                                                f"{student.id}"
                                            )
                                        ):

                                            manager.attendance_log = [
                                                record
                                                for record
                                                in manager.attendance_log
                                                if not (
                                                    record["student_id"]
                                                    == student.id
                                                    and
                                                    record["course_id"]
                                                    == target_course.id
                                                    and
                                                    record["lesson_index"]
                                                    == selected_lesson_index
                                                )
                                            ]

                                            manager._save_data()

                                            st.rerun()

                                    else:

                                        if st.button(
                                            "Give Attendance",
                                            key=(
                                                f"teacher_attendance_"
                                                f"{target_course.id}_"
                                                f"{selected_lesson_index}_"
                                                f"{student.id}"
                                            )
                                        ):

                                            success = manager.delete_attendance(
                                                student.id,
                                                target_course.id,
                                                lesson_index
                                            )

                                            if success:
                                                manager._save_data()
                                                st.rerun()
                                            else:
                                                st.error("Failed to delete attendance.")
                                # -----------------------------------------
                                # Future Lesson
                                # -----------------------------------------

                                else:

                                    st.caption(
                                        "Attendance is not available yet."
                                    )

                            st.divider()

                    # -------------------------------------------------
                    # Back Button
                    # -------------------------------------------------

                    if st.button(
                        "Back to Daily Roster",
                        width="stretch"
                    ):

                        del st.session_state.selected_roster_course_id
                        del st.session_state.selected_roster_lesson_index

                        st.session_state.teacher_page = (
                            "Daily Roster"
                        )

                        st.rerun()