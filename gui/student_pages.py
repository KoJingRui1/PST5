import streamlit as st
import pandas as pd
import datetime
def success_page(title, message, detail, return_page):
    st.title(title)
    st.success(message)

    if detail:
        st.write(detail)

    if st.button("OK"):
        st.session_state.student_page = return_page

        if "selected_user_id" in st.session_state:
            del st.session_state.selected_user_id

        st.rerun()


def show_student_page(manager, user):
    st.sidebar.title("Student Menu")
    st.sidebar.subheader(f"{user.name}")

    if "student_page" not in st.session_state:
        st.session_state.student_page = "Profile"

    if st.sidebar.button("Profile", width="stretch"):
        st.session_state.student_page = "Profile"
        st.rerun()

    if st.sidebar.button("Enrollment", width="stretch"):
        st.session_state.student_page = "Enrollment"
        st.rerun()

    if st.sidebar.button("Course", width="stretch"):
        st.session_state.student_page = "Course"
        st.rerun()

    if st.sidebar.button("Daily Roster", width="stretch"):
        st.session_state.student_page = "Daily Roster"
        st.rerun()

    if st.sidebar.button("Logout", width="stretch"):
        st.session_state.user = None
        st.session_state.student_page = "Profile"
        st.rerun()

    page = st.session_state.student_page

    # =========================================================
    # Profile
    # =========================================================

    if page == "Profile":
        st.title("Student Profile")

        st.subheader(f"ID: {user.id}")
        st.subheader(f"Name: {user.name}")

        st.subheader("Enrolled instrument.")

        for instrument, grade in user.grades.items():
            st.write(f"- {instrument}, grade {grade}")

        if st.button("Update Profile"):
            st.session_state.student_page = "Update Profile"
            st.rerun()

    # =========================================================
    # Update Profile
    # =========================================================

    elif page == "Update Profile":
        st.title("Update Profile")

        choice = st.selectbox(
            "Update Term",
            ["Name", "Password"]
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

                    st.session_state.student_page = (
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

                    st.session_state.student_page = (
                        "Profile Update Success"
                    )

                    st.rerun()

    # =========================================================
    # Profile Update Success
    # =========================================================

    elif page == "Profile Update Success":
        success_page(
            "Profile Updated",
            "Your profile has been updated successfully!",
            "Your account information has been saved.",
            "Profile"
        )

    # =========================================================
    # Enrollment
    # =========================================================

    elif page == "Enrollment":
        st.title("Enrollment")

        # -----------------------------------------------------
        # Build enrollment table
        # -----------------------------------------------------

        enrollment_data = []

        for instrument, grade in user.grades.items():

            course_names = []

            for course_id in user.enrolled_course_ids:
                course = manager.find_course_by_id(course_id)

                if course and course.instrument == instrument:
                    course_names.append(course.name)

            if course_names:
                courses = ", ".join(course_names)
            else:
                courses = "None"

            enrollment_data.append({
                "Instrument": instrument,
                "Grade": grade,
                "Course": courses
            })

        if enrollment_data:
            st.table(enrollment_data)

        else:
            st.info("You are not enrolled in any instrument.")

        st.write("")

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Enroll New", use_container_width=True):
                st.session_state.student_enrollment_action = "Enroll New"
                st.rerun()

        with col2:
            if st.button("Disenroll", use_container_width=True):
                st.session_state.student_enrollment_action = "Disenroll"
                st.rerun()

        with col3:
            if st.button("Upgrade", use_container_width=True):
                st.session_state.student_enrollment_action = "Upgrade"
                st.rerun()

        # -----------------------------------------------------
        # Enroll New
        # -----------------------------------------------------

        if st.session_state.get("student_enrollment_action") == "Enroll New":

            st.divider()
            st.subheader("Enroll New")

            available_instruments = [
                instrument
                for instrument in manager.school_data["instruments"]
                if instrument not in user.grades
            ]

            if not available_instruments:
                st.info(
                    "You are already enrolled in all available instruments."
                )

            else:
                instrument = st.selectbox(
                    "Please choose an instrument.",
                    available_instruments,
                    key="student_enroll_instrument"
                )

                grade = st.number_input(
                    "Please enter the grade.",
                    min_value=1,
                    max_value=8,
                    step=1,
                    key="student_enroll_grade"
                )

                if st.button("Enroll", key="student_enroll_button"):

                    success = manager.enrol_instrument(
                        user.id,
                        instrument,
                        grade
                    )

                    if success:
                        manager._save_data()

                        st.session_state.student_enrollment_action = None

                        st.success(
                            f"{instrument} has been successfully enrolled."
                        )

                        st.rerun()

                    else:
                        st.error(
                            "Failed to enroll the instrument."
                        )

        # -----------------------------------------------------
        # Disenroll
        # -----------------------------------------------------

        elif st.session_state.get("student_enrollment_action") == "Disenroll":

            st.divider()
            st.subheader("Disenroll")

            enrolled_instruments = list(user.grades.keys())

            if not enrolled_instruments:
                st.info(
                    "You are not enrolled in any instrument."
                )

            else:
                instrument = st.selectbox(
                    "Please choose an instrument to disenroll.",
                    enrolled_instruments,
                    key="student_disenroll_instrument"
                )

                if st.button(
                    "Disenroll",
                    key="student_disenroll_button"
                ):

                    success = manager.disenroll_instrument(
                        user.id,
                        instrument
                    )

                    if success:
                        manager._save_data()

                        st.session_state.student_enrollment_action = None

                        st.success(
                            f"{instrument} has been successfully disenrolled."
                        )

                        st.rerun()

                    else:
                        st.error(
                            "Failed to disenroll the instrument."
                        )

        # -----------------------------------------------------
        # Upgrade
        # -----------------------------------------------------

        elif st.session_state.get("student_enrollment_action") == "Upgrade":

            st.divider()
            st.subheader("Upgrade")

            enrolled_instruments = list(user.grades.keys())

            if not enrolled_instruments:
                st.info(
                    "You are not enrolled in any instrument."
                )

            else:
                instrument = st.selectbox(
                    "Please choose an instrument to upgrade.",
                    enrolled_instruments,
                    key="student_upgrade_instrument"
                )

                current_grade = user.grades[instrument]

                st.write(
                    f"Current Grade: {current_grade}"
                )

                if current_grade >= 8:
                    st.info(
                        "This instrument is already at the maximum grade."
                    )

                else:
                    if st.button(
                        "Upgrade",
                        key="student_upgrade_button"
                    ):

                        success = manager.update_enrollment(
                            user.id,
                            instrument,
                            current_grade + 1
                        )

                        if success:
                            manager._save_data()

                            st.session_state.student_enrollment_action = None

                            st.success(
                                f"{instrument} has been successfully upgraded "
                                f"to Grade {current_grade + 1}."
                            )

                            st.rerun()

                        else:
                            st.error(
                                "Failed to upgrade the enrollment."
                            )

    # =========================================================
    # Course
    # =========================================================

    elif page == "Course":

        st.title("Course")

        # -----------------------------------------------------
        # My Courses
        # -----------------------------------------------------

        st.subheader("My Courses")

        enrolled_courses = []

        for course_id in user.enrolled_course_ids:

            course = manager.find_course_by_id(course_id)

            if course is not None:
                enrolled_courses.append(course)

        if not enrolled_courses:

            st.info(
                "You are not enrolled in any courses."
            )

        else:

            # Current date
            today = datetime.date.today()

            # Seven days from today
            end_date = today + datetime.timedelta(days=7)

            for course in enrolled_courses:

                st.subheader(
                    f"Course ID: {course.id}"
                )

                st.write(
                    f"**Course Name:** {course.name}"
                )

                st.write(
                    f"**Instrument:** {course.instrument}"
                )

                st.write(
                    f"**Grade:** {course.grade}"
                )

                teacher = manager.find_teacher_by_id(
                    course.teacher_id
                )

                if teacher:

                    st.write(
                        f"**Teacher:** {teacher.name}"
                    )

                else:

                    st.write(
                        f"**Teacher ID:** {course.teacher_id}"
                    )

                current_students = len(
                    course.enrolled_student_ids
                )

                st.write(
                    f"**Students:** "
                    f"{current_students} / "
                    f"{course.max_student}"
                )

                st.write(
                    f"**Description:** "
                    f"{course.description}"
                )

                # =================================================
                # Lessons in the next seven days
                # =================================================

                st.write("**Lessons in the next 7 days:**")

                upcoming_lessons = []

                for lesson_index, lesson in enumerate(
                    course.lessons,
                    1
                ):

                    try:

                        lesson_date = datetime.datetime.strptime(
                            lesson["date"],
                            "%Y-%m-%d"
                        ).date()

                    except (ValueError, TypeError, KeyError):

                        continue

                    if (
                        today
                        <= lesson_date
                        <= end_date
                    ):

                        upcoming_lessons.append(
                            (
                                lesson_index,
                                lesson,
                                lesson_date
                            )
                        )

                if not upcoming_lessons:

                    st.info(
                        "There are no lessons in the next 7 days."
                    )

                else:

                    for (
                        lesson_index,
                        lesson,
                        lesson_date
                    ) in upcoming_lessons:

                        st.write(
                            f"**Lesson {lesson_index}**"
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

                        # -------------------------------------------------
                        # Check whether this lesson is currently checkable
                        # -------------------------------------------------

                        now = datetime.datetime.now()

                        try:

                            lesson_time = datetime.datetime.strptime(
                                lesson["time"],
                                "%H:%M"
                            ).time()

                            lesson_datetime = (
                                datetime.datetime.combine(
                                    lesson_date,
                                    lesson_time
                                )
                            )

                            lesson_end = (
                                lesson_datetime
                                + datetime.timedelta(hours=1)
                            )

                        except (ValueError, TypeError, KeyError):

                            lesson_datetime = None
                            lesson_end = None

                        # Check existing attendance
                        already_checked_in = False

                        for record in manager.attendance_log:

                            if (
                                record.get("student_id")
                                == user.id
                                and
                                record.get("course_id")
                                == course.id
                                and
                                record.get("lesson_index")
                                == lesson_index
                            ):

                                already_checked_in = True
                                break

                        if already_checked_in:

                            st.success(
                                "Checked In"
                            )

                        elif (
                            lesson_datetime is not None
                            and
                            lesson_end is not None
                            and
                            lesson_datetime
                            <= now
                            <= lesson_end
                        ):

                            st.write(
                                "Check-in is currently available."
                            )

                            password = st.text_input(
                                "Course Password",
                                type="password",
                                key=(
                                    f"checkin_password_"
                                    f"{course.id}_"
                                    f"{lesson_index}"
                                )
                            )

                            if st.button(
                                "Check In",
                                key=(
                                    f"checkin_"
                                    f"{course.id}_"
                                    f"{lesson_index}"
                                ),
                                width="stretch"
                            ):

                                # -----------------------------------------
                                # Check course password
                                # -----------------------------------------

                                if password != course.password:

                                    st.error(
                                        "Incorrect course password."
                                    )

                                else:

                                    # -------------------------------------
                                    # Check again before recording
                                    # attendance
                                    # -------------------------------------

                                    now = datetime.datetime.now()

                                    if (
                                        now.date()
                                        != lesson_date
                                    ):

                                        st.error(
                                            "Check-in is no longer "
                                            "available for this lesson."
                                        )

                                    elif (
                                        now < lesson_datetime
                                        or
                                        now > lesson_end
                                    ):

                                        st.error(
                                            "Check-in is no longer "
                                            "available."
                                        )

                                    else:

                                        # Check again whether the
                                        # student already checked in.
                                        already_checked_in = False

                                        for record in (
                                            manager.attendance_log
                                        ):

                                            if (
                                                record.get(
                                                    "student_id"
                                                )
                                                == user.id
                                                and
                                                record.get(
                                                    "course_id"
                                                )
                                                == course.id
                                                and
                                                record.get(
                                                    "lesson_index"
                                                )
                                                == lesson_index
                                            ):

                                                already_checked_in = True
                                                break

                                        if already_checked_in:

                                            st.error(
                                                "You have already "
                                                "checked in for this lesson."
                                            )

                                        else:

                                            success = manager.check_in(
                                                user.id,
                                                course.id,
                                                lesson_index
                                            )

                                            if success:

                                                st.success(
                                                    "Check-in successful!"
                                                )

                                                st.rerun()

                                            else:

                                                st.error(
                                                    "Check-in failed. "
                                                    "Please check the lesson "
                                                    "time and your enrollment."
                                                )

                        elif (
                            lesson_datetime is not None
                            and
                            now < lesson_datetime
                        ):

                            st.info(
                                "Check-in is not available yet."
                            )

                        else:

                            st.info(
                                "Check-in is no longer available."
                            )

                        st.divider()

                # =================================================
                # Disenroll
                # =================================================

                if st.button(
                    "Disenroll",
                    key=f"disenroll_course_{course.id}",
                    width="stretch"
                ):

                    st.session_state.disenroll_course_id = (
                        course.id
                    )

                    st.rerun()

                # -------------------------------------------------
                # Disenroll confirmation
                # -------------------------------------------------

                if (
                    st.session_state.get(
                        "disenroll_course_id"
                    )
                    == course.id
                ):

                    st.warning(
                        "Please confirm your identity before "
                        "disenrolling from this course."
                    )

                    current_password = st.text_input(
                        "Please enter your CURRENT password.",
                        type="password",
                        key=(
                            f"disenroll_password_"
                            f"{course.id}"
                        )
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "Confirm Disenroll",
                            key=(
                                f"confirm_disenroll_"
                                f"{course.id}"
                            ),
                            width="stretch"
                        ):

                            if current_password != user.password:

                                st.error(
                                    "The current password is incorrect."
                                )

                            else:

                                if (
                                    course.id
                                    not in user.enrolled_course_ids
                                ):

                                    st.error(
                                        "You are no longer enrolled "
                                        "in this course."
                                    )

                                    del st.session_state.disenroll_course_id

                                    st.rerun()

                                else:

                                    user.enrolled_course_ids.remove(
                                        course.id
                                    )

                                    if (
                                        user.id
                                        in course.enrolled_student_ids
                                    ):

                                        course.enrolled_student_ids.remove(
                                            user.id
                                        )

                                    manager.attendance_log = [
                                        record
                                        for record
                                        in manager.attendance_log
                                        if not (
                                            record.get("student_id")
                                            == user.id
                                            and
                                            record.get("course_id")
                                            == course.id
                                        )
                                    ]

                                    manager._save_data()

                                    del st.session_state.disenroll_course_id

                                    st.session_state.student_page = (
                                        "Course Disenrol Success"
                                    )

                                    st.rerun()

                    with col2:

                        if st.button(
                            "Cancel",
                            key=(
                                f"cancel_disenroll_"
                                f"{course.id}"
                            ),
                            width="stretch"
                        ):

                            del st.session_state.disenroll_course_id

                            st.rerun()

                st.divider()
                # =================================================
                # Switch Course
                # =================================================

                if st.button(
                    "Switch Course",
                    key=f"switch_course_{course.id}",
                    width="stretch"
                ):

                    st.session_state.switch_course_id = (
                        course.id
                    )

                    st.rerun()

                # -------------------------------------------------
                # Switch Course confirmation
                # -------------------------------------------------

                if (
                    st.session_state.get(
                        "switch_course_id"
                    )
                    == course.id
                ):

                    st.warning(
                        "Please confirm your identity and "
                        "select the new course."
                    )

                    # ---------------------------------------------
                    # Student password
                    # ---------------------------------------------

                    student_password = st.text_input(
                        "Please enter your CURRENT password.",
                        type="password",
                        key=(
                            f"switch_student_password_"
                            f"{course.id}"
                        )
                    )

                    # ---------------------------------------------
                    # Find courses that the student can switch to
                    # ---------------------------------------------

                    switchable_courses = []

                    for new_course in manager.courses:

                        # Do not switch to the current course
                        if new_course.id == course.id:
                            continue

                        # Student must not already be enrolled
                        if (
                            new_course.id
                            in user.enrolled_course_ids
                        ):
                            continue

                        # Student must have the required instrument
                        if new_course.instrument not in user.grades:
                            continue

                        # Student grade must match the new course
                        if (
                            user.grades[new_course.instrument]
                            != new_course.grade
                        ):
                            continue

                        # New course must have space
                        if (
                            len(new_course.enrolled_student_ids)
                            >= new_course.max_student
                        ):
                            continue

                        switchable_courses.append(new_course)

                    if len(switchable_courses) == 0:

                        st.info(
                            "There are no courses available "
                            "for you to switch to."
                        )

                    else:

                        selected_new_course = st.selectbox(
                            "Please choose the new course.",
                            switchable_courses,
                            format_func=lambda c: (
                                f"Course ID {c.id} | "
                                f"{c.name} | "
                                f"{c.instrument} | "
                                f"Grade {c.grade}"
                            ),
                            key=(
                                f"switch_new_course_"
                                f"{course.id}"
                            )
                        )

                        new_course_password = st.text_input(
                            "Please enter the NEW course password.",
                            type="password",
                            key=(
                                f"switch_course_password_"
                                f"{course.id}"
                            )
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            if st.button(
                                "Confirm Switch",
                                key=(
                                    f"confirm_switch_"
                                    f"{course.id}"
                                ),
                                width="stretch"
                            ):

                                # ---------------------------------
                                # Check student's current password
                                # ---------------------------------

                                if (
                                    student_password
                                    != user.password
                                ):

                                    st.error(
                                        "The current password is incorrect."
                                    )

                                else:

                                    old_course_id = course.id
                                    new_course_id = (
                                        selected_new_course.id
                                    )

                                    # ---------------------------------
                                    # Use backend switch_course()
                                    # ---------------------------------

                                    manager.switch_course(
                                        user.id,
                                        old_course_id,
                                        new_course_id,
                                        new_course_password
                                    )

                                    # ---------------------------------
                                    # Check whether the switch succeeded
                                    # ---------------------------------

                                    if (
                                        new_course_id
                                        in user.enrolled_course_ids
                                        and
                                        old_course_id
                                        not in user.enrolled_course_ids
                                    ):

                                        manager._save_data()

                                        del st.session_state.switch_course_id

                                        st.session_state.student_page = (
                                            "Course Switch Success"
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            "The course switch could not "
                                            "be completed. Please check "
                                            "the new course password and "
                                            "course requirements."
                                        )

                        with col2:

                            if st.button(
                                "Cancel",
                                key=(
                                    f"cancel_switch_"
                                    f"{course.id}"
                                ),
                                width="stretch"
                            ):

                                del st.session_state.switch_course_id

                                st.rerun()

                st.divider()


                
        # =====================================================
        # Available Courses
        # =====================================================

        st.subheader("Available Courses")

        # -----------------------------------------------------
        # Get courses that the student is eligible for
        # -----------------------------------------------------

        eligible_courses = []

        for course in manager.courses:

            # Student must have the required instrument
            if course.instrument not in user.grades:
                continue

            # Student grade must exactly match course grade
            if (
                user.grades[course.instrument]
                != course.grade
            ):
                continue

            # Student must not already be enrolled
            if course.id in user.enrolled_course_ids:
                continue

            # Course must not be full
            current_students = len(
                course.enrolled_student_ids
            )

            if current_students >= course.max_student:
                continue

            eligible_courses.append(course)

        # =====================================================
        # Search / Filter
        # =====================================================

        left, right = st.columns([1, 6])

        with left:

            term = st.selectbox(
                "Term",
                [
                    "-",
                    "ID",
                    "COURSE NAME",
                    "DESCRIPTION",
                    "INSTRUMENT"
                ],
                key="student_course_term"
            )

        with right:

            if term == "ID":

                search_term = st.number_input(
                    "Please enter the ID.",
                    min_value=0,
                    step=1,
                    key="student_course_id_search"
                )

            elif term == "COURSE NAME":

                search_term = st.text_input(
                    "Please enter the course name.",
                    key="student_course_name_search"
                )

            elif term == "DESCRIPTION":

                search_term = st.text_input(
                    "Please enter the description.",
                    key="student_course_description_search"
                )
            elif term == "INSTRUMENT":
                search_term = st.selectbox(
                    "Please choose the instrument.",
                    manager.school_data["instruments"],
                    key="student_instrument_search"
                )
        # =====================================================
        # Filter Courses
        # =====================================================

        filtered_courses = []

        for course in eligible_courses:

            if term == "-":

                matched = True

            elif term == "ID":

                matched = (
                    course.id == search_term
                )

            elif term == "COURSE NAME":

                matched = (
                    search_term.lower()
                    in course.name.lower()
                )

            elif term == "DESCRIPTION":

                matched = (
                    search_term.lower()
                    in course.description.lower()
                )
            elif term == "INSTRUMENT":
                matched = (
                    search_term.lower()
                    in course.instrument.lower()
                )
            else:

                matched = False

            if matched:

                filtered_courses.append(course)

        # =====================================================
        # No Courses Found
        # =====================================================

        if len(filtered_courses) == 0:

            if term == "-":

                st.info(
                    "There are no courses available for you."
                )

            else:

                st.error(
                    "No Course found."
                )

        else:

            # =================================================
            # Course Table
            # =================================================

            course_data = []

            for course in filtered_courses:

                teacher = manager.find_teacher_by_id(
                    course.teacher_id
                )

                if teacher:

                    teacher_name = teacher.name

                else:

                    teacher_name = str(
                        course.teacher_id
                    )

                current_students = len(
                    course.enrolled_student_ids
                )

                course_data.append({
                    "ID": course.id,
                    "Course Name": course.name,
                    "Instrument": course.instrument,
                    "Teacher": teacher_name,
                    "Grade": course.grade,
                    "Students": (
                        f"{current_students} / "
                        f"{course.max_student}"
                    ),
                    "Description": course.description,
                    "Select": False
                })

            course_df = pd.DataFrame(
                course_data,
                columns=[
                    "ID",
                    "Course Name",
                    "Instrument",
                    "Teacher",
                    "Grade",
                    "Students",
                    "Description",
                    "Select"
                ]
            )

            edited_course_data = st.data_editor(
                course_df,
                column_config={

                    "ID": st.column_config.NumberColumn(
                        "ID",
                        width="small",
                        disabled=True
                    ),

                    "Course Name": st.column_config.TextColumn(
                        "Course Name",
                        width="medium",
                        disabled=True
                    ),

                    "Instrument": st.column_config.TextColumn(
                        "Instrument",
                        width="medium",
                        disabled=True
                    ),

                    "Teacher": st.column_config.TextColumn(
                        "Teacher",
                        width="medium",
                        disabled=True
                    ),

                    "Grade": st.column_config.NumberColumn(
                        "Grade",
                        width="small",
                        disabled=True
                    ),

                    "Students": st.column_config.TextColumn(
                        "Students",
                        width="small",
                        disabled=True
                    ),

                    "Description": st.column_config.TextColumn(
                        "Description",
                        width="large",
                        disabled=True
                    ),

                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        width="small"
                    )
                },

                hide_index=True,
                width="stretch",
                key="student_course_table"
            )

            # =================================================
            # Select Course
            # =================================================

            if st.button(
                "Select Course",
                width="stretch"
            ):

                selected_courses = edited_course_data[
                    edited_course_data["Select"] == True
                ]

                if len(selected_courses) == 0:

                    st.error(
                        "Please select a course."
                    )

                elif len(selected_courses) > 1:

                    st.error(
                        "Please select only one course."
                    )

                else:

                    selected_course_id = int(
                        selected_courses.iloc[0]["ID"]
                    )

                    st.session_state.selected_course_id = (
                        selected_course_id
                    )

                    st.session_state.student_page = (
                        "Enrol Course"
                    )

                    st.rerun()
    # =========================================================
    # Enrol Course
    # =========================================================

    elif page == "Enrol Course":

        st.title("Enrol in Course")

        if "selected_course_id" not in st.session_state:

            st.error("No course has been selected.")

            if st.button("Back"):
                st.session_state.student_page = "Course"
                st.rerun()

        else:

            target_course = manager.find_course_by_id(
                st.session_state.selected_course_id
            )

            if target_course is None:

                st.error("Course not found.")

                if st.button("Back"):

                    del st.session_state.selected_course_id

                    st.session_state.student_page = "Course"

                    st.rerun()

            else:

                # =================================================
                # Re-check all course eligibility conditions
                # =================================================

                current_students = len(
                    target_course.enrolled_student_ids
                )

                instrument_valid = (
                    target_course.instrument
                    in user.grades
                )

                grade_valid = (
                    instrument_valid
                    and
                    user.grades[target_course.instrument]
                    == target_course.grade
                )

                already_enrolled = (
                    target_course.id
                    in user.enrolled_course_ids
                )

                course_full = (
                    current_students
                    >= target_course.max_student
                )

                # -------------------------------------------------
                # Course information
                # -------------------------------------------------

                st.subheader(
                    target_course.name
                )

                st.write(
                    f"**Course ID:** "
                    f"{target_course.id}"
                )

                st.write(
                    f"**Instrument:** "
                    f"{target_course.instrument}"
                )

                st.write(
                    f"**Grade:** "
                    f"{target_course.grade}"
                )

                teacher = manager.find_teacher_by_id(
                    target_course.teacher_id
                )

                if teacher:

                    st.write(
                        f"**Teacher:** "
                        f"{teacher.name}"
                    )

                else:

                    st.write(
                        f"**Teacher ID:** "
                        f"{target_course.teacher_id}"
                    )

                st.write(
                    f"**Students:** "
                    f"{current_students} / "
                    f"{target_course.max_student}"
                )

                st.write(
                    f"**Description:** "
                    f"{target_course.description}"
                )

                st.divider()

                # =================================================
                # Failed re-check
                # =================================================

                if not instrument_valid:

                    st.error(
                        "You are not enrolled in the required "
                        "instrument for this course."
                    )

                    if st.button("Back"):
                        del st.session_state.selected_course_id
                        st.session_state.student_page = "Course"
                        st.rerun()

                elif not grade_valid:

                    st.error(
                        "Your grade does not match the "
                        "required grade for this course."
                    )

                    if st.button("Back"):
                        del st.session_state.selected_course_id
                        st.session_state.student_page = "Course"
                        st.rerun()

                elif already_enrolled:

                    st.error(
                        "You are already enrolled in this course."
                    )

                    if st.button("Back"):
                        del st.session_state.selected_course_id
                        st.session_state.student_page = "Course"
                        st.rerun()

                elif course_full:

                    st.error(
                        "This course is full."
                    )

                    st.info(
                        "Someone may have enrolled in this course "
                        "before you completed your enrollment."
                    )

                    if st.button("Back"):
                        del st.session_state.selected_course_id
                        st.session_state.student_page = "Course"
                        st.rerun()

                else:

                    # -------------------------------------------------
                    # Password
                    # -------------------------------------------------

                    course_password = st.text_input(
                        "Course Password",
                        type="password"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "Enrol in Course",
                            width="stretch"
                        ):

                            # Check capacity one more time immediately
                            # before enrollment
                            latest_student_count = len(
                                target_course.enrolled_student_ids
                            )

                            if (
                                latest_student_count
                                >= target_course.max_student
                            ):

                                st.error(
                                    "This course is full."
                                )

                            elif (
                                target_course.id
                                in user.enrolled_course_ids
                            ):

                                st.error(
                                    "You are already enrolled "
                                    "in this course."
                                )

                            elif (
                                course_password
                                != target_course.password
                            ):

                                st.error(
                                    "Incorrect course password."
                                )

                            else:

                                user.enrolled_course_ids.append(
                                    target_course.id
                                )

                                target_course.enrolled_student_ids.append(
                                    user.id
                                )

                                manager._save_data()

                                del st.session_state.selected_course_id

                                st.session_state.student_page = (
                                    "Course Enrol Success"
                                )

                                st.rerun()

                    with col2:

                        if st.button(
                            "Cancel",
                            width="stretch"
                        ):

                            del st.session_state.selected_course_id

                            st.session_state.student_page = "Course"

                            st.rerun()
    # =========================================================
    # Course Enrol Success
    # =========================================================

    elif page == "Course Enrol Success":

        st.title("Course Enrolled")

        st.success(
            "You have successfully enrolled in the course!"
        )

        st.write(
            "The course has been added to your enrolled courses."
        )

        if st.button("OK"):

            st.session_state.student_page = "Course"
            st.rerun()
    # =========================================================
    # Course Disenrol Success
    # =========================================================

    elif page == "Course Disenrol Success":

        st.title("Course Disenrolled")

        st.success(
            "You have successfully disenrolled from the course!"
        )

        st.write(
            "The course has been removed from your enrolled courses."
        )

        if st.button("OK"):

            st.session_state.student_page = "Course"

            st.rerun()
    # =========================================================
    # Daily Roster
    # =========================================================

    # =========================================================
    # Daily Roster
    # =========================================================

    # =========================================================
    # Course Switch Success
    # =========================================================

    elif page == "Course Switch Success":

        st.title("Course Switched")

        st.success(
            "You have successfully switched to the new course!"
        )

        st.write(
            "Your previous course has been replaced by the new course."
        )

        if st.button("OK"):

            st.session_state.student_page = "Course"

            st.rerun()

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
        # Find lessons from student's enrolled courses
        # -----------------------------------------------------

        roster_data = []

        for course in manager.courses:

            # -------------------------------------------------
            # Student can only see courses they are enrolled in
            # -------------------------------------------------

            if course.id not in user.enrolled_course_ids:
                continue

            for lesson_index, lesson in enumerate(
                course.lessons,
                start=1
            ):

                if lesson["date"] != selected_date_string:
                    continue

                # -------------------------------------------------
                # Check student's attendance
                # -------------------------------------------------

                present = False

                for record in manager.attendance_log:

                    if (
                        record["student_id"] == user.id
                        and record["course_id"] == course.id
                        and record["lesson_index"] == lesson_index
                    ):
                        present = True
                        break

                # -------------------------------------------------
                # Attendance Status
                # -------------------------------------------------

                if present:
                    status = "Present"
                else:
                    status = "Absent"

                roster_data.append(
                    {
                        "Course ID": course.id,
                        "Course Name": course.name,
                        "Time": lesson["time"],
                        "Status": status,
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
                    "Status",
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

                    "Status": st.column_config.TextColumn(
                        "Status",
                        width="small",
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
                key="student_daily_roster_table"
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

                    st.session_state.student_selected_roster_course_id = (
                        int(selected_row["Course ID"])
                    )

                    st.session_state.student_selected_roster_lesson_index = (
                        int(selected_row["Lesson Index"])
                    )

                    st.session_state.student_page = (
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
            "student_selected_roster_course_id"
            not in st.session_state
            or
            "student_selected_roster_lesson_index"
            not in st.session_state
        ):

            st.error(
                "No lesson has been selected."
            )

            if st.button(
                "Back to Daily Roster",
                width="stretch"
            ):

                st.session_state.student_page = (
                    "Daily Roster"
                )

                st.rerun()

        else:

            selected_course_id = (
                st.session_state.student_selected_roster_course_id
            )

            selected_lesson_index = (
                st.session_state.student_selected_roster_lesson_index
            )

            target_course = manager.find_course_by_id(
                selected_course_id
            )

            # -------------------------------------------------
            # Check course
            # -------------------------------------------------

            if target_course is None:

                st.error(
                    "Course not found."
                )

                if st.button(
                    "Back to Daily Roster",
                    width="stretch"
                ):

                    del st.session_state.student_selected_roster_course_id
                    del st.session_state.student_selected_roster_lesson_index

                    st.session_state.student_page = (
                        "Daily Roster"
                    )

                    st.rerun()

            # -------------------------------------------------
            # Student permission check
            # -------------------------------------------------

            elif target_course.id not in user.enrolled_course_ids:

                st.error(
                    "You are not enrolled in this course."
                )

                if st.button(
                    "Back to Daily Roster",
                    width="stretch"
                ):

                    del st.session_state.student_selected_roster_course_id
                    del st.session_state.student_selected_roster_lesson_index

                    st.session_state.student_page = (
                        "Daily Roster"
                    )

                    st.rerun()

            # -------------------------------------------------
            # Check lesson
            # -------------------------------------------------

            elif (
                selected_lesson_index < 1
                or
                selected_lesson_index
                > len(target_course.lessons)
            ):

                st.error(
                    "Lesson not found."
                )

                if st.button(
                    "Back to Daily Roster",
                    width="stretch"
                ):

                    del st.session_state.student_selected_roster_course_id
                    del st.session_state.student_selected_roster_lesson_index

                    st.session_state.student_page = (
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

                st.divider()

                # -------------------------------------------------
                # Activity
                # -------------------------------------------------

                st.subheader("Activity")

                st.write(
                    lesson["activity"]
                )

                st.divider()

                # -------------------------------------------------
                # Student Attendance Status
                # -------------------------------------------------

                student_present = False

                for record in manager.attendance_log:

                    if (
                        record["student_id"] == user.id
                        and record["course_id"] == target_course.id
                        and record["lesson_index"] == selected_lesson_index
                    ):
                        student_present = True
                        break

                st.subheader("Attendance Status")

                # -------------------------------------------------
                # Already Present
                # -------------------------------------------------

                if student_present:

                    st.success("Present")

                else:

                    # -------------------------------------------------
                    # Get current time
                    # -------------------------------------------------

                    now = datetime.datetime.now()

                    lesson_datetime = datetime.datetime.strptime(
                        f"{lesson['date']} {lesson['time']}",
                        "%Y-%m-%d %H:%M"
                    )

                    lesson_end = (
                        lesson_datetime
                        + datetime.timedelta(hours=1)
                    )

                    # -------------------------------------------------
                    # Student Check In
                    # -------------------------------------------------

                    if now < lesson_datetime:

                        st.info("Check-in is not available yet.")

                    elif now <= lesson_end:

                        st.info("Check-in is currently available.")

                        if st.button(
                            "Student Check In",
                            width="stretch"
                        ):
                            st.session_state.student_check_in_confirm = True
                            st.rerun()

                    else:

                        st.error("Absent")

                # -------------------------------------------------
                # Check-in Confirmation
                # -------------------------------------------------

                if (
                    st.session_state.get(
                        "student_check_in_confirm",
                        False
                    )
                    and not student_present
                ):

                    st.warning(
                        "Do you want to check in for this lesson?"
                    )

                    course_password = st.text_input(
                        "Please enter the course password.",
                        type="password",
                        key="student_check_in_password"
                    )

                    confirm_col1, confirm_col2 = st.columns(2)

                    with confirm_col1:

                        if st.button(
                            "Confirm Check In",
                            width="stretch"
                        ):

                            # -------------------------------------------------
                            # Check course password
                            # -------------------------------------------------

                            if course_password != target_course.password:

                                st.error(
                                    "Incorrect course password."
                                )

                            else:

                                success = manager.check_in(
                                    user.id,
                                    target_course.id,
                                    selected_lesson_index
                                )

                                if success:

                                    manager._save_data()

                                    st.session_state.student_check_in_confirm = False

                                    st.success(
                                        "You have successfully checked in!"
                                    )

                                    st.rerun()

                                else:

                                    st.session_state.student_check_in_confirm = False

                                    st.error(
                                        "Check-in failed."
                                    )

                    with confirm_col2:

                        if st.button(
                            "Cancel",
                            width="stretch"
                        ):

                            st.session_state.student_check_in_confirm = False

                            st.rerun()

