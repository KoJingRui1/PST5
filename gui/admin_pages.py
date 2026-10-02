import streamlit as st
import pandas as pd

from app.admin import AdminUser
from app.teacher import TeacherUser
from app.student import StudentUser


# =========================================================
# Success Page
# =========================================================

def success_page(title, message, detail, return_page):

    st.title(title)

    st.success(message)

    if detail:
        st.write(detail)

    if st.button("OK"):

        st.session_state.admin_page = return_page

        if "selected_user_id" in st.session_state:
            del st.session_state.selected_user_id

        st.rerun()


# =========================================================
# Admin Page
# =========================================================

def show_admin_page(manager, user):

    # =========================================================
    # Sidebar
    # =========================================================

    st.sidebar.title("Admin Menu")
    st.sidebar.subheader(f"{user.name}")

    if "admin_page" not in st.session_state:
        st.session_state.admin_page = "Profile"

    if st.sidebar.button("Profile", width="stretch"):
        st.session_state.admin_page = "Profile"

    if st.sidebar.button("Users", width="stretch"):
        st.session_state.admin_page = "Users"

    if st.sidebar.button("Applications", width="stretch"):
        st.session_state.admin_page = "Applications"

    if st.sidebar.button("Courses", width="stretch"):
        st.session_state.admin_page = "Courses"

    if st.sidebar.button("Instruments", width="stretch"):
        st.session_state.admin_page = "Instruments"

    st.sidebar.divider()

    if st.sidebar.button("Logout", width="stretch"):
        st.session_state.user = None
        st.session_state.auth_page = "home"
        st.rerun()

    page = st.session_state.admin_page


    # =========================================================
    # Admin Profile
    # =========================================================

    if page == "Profile":

        st.title("Admin Profile")

        st.subheader(f"User ID: {user.id}")
        st.subheader(f"User Name: {user.name}")

        if st.button("Update Profile"):

            st.session_state.admin_page = "Update Profile"

            st.rerun()

    elif page == "Delete User Success":
        success_page(
            "User Deleted",
            "The user has been deleted successfully!",
            f"{st.session_state.get('deleted_user_name', 'The user')} "
            "and their account information have been removed.",
            "Users"
        )
    # =========================================================
    # Update Current Admin Profile
    # =========================================================

    elif page == "Update Profile":

        st.title("Update Profile")

        choice = st.selectbox(
            "Update Term",
            ["Name", "Password"]
        )


        # -----------------------------------------------------
        # Name
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
                        "The new name is same as the current name."
                    )

                else:

                    manager.update_user(
                        user.id,
                        name=new_name
                    )

                    manager._save_data()

                    st.session_state.admin_page = (
                        "Profile Update Success"
                    )

                    st.rerun()


        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        elif choice == "Password":

            current_password = st.text_input(
                "Please enter your CURRENT PASSWORD",
                type="password"
            )

            new_password = st.text_input(
                "Please enter your NEW PASSWORD",
                type="password"
            )

            confirm_password = st.text_input(
                "Please confirm your NEW PASSWORD",
                type="password"
            )

            if st.button("Update"):

                if current_password != user.password:

                    st.error("Wrong password.")

                elif new_password != confirm_password:

                    st.error(
                        "The confirmation is not the same as the new password."
                    )

                elif user.password == new_password:

                    st.error(
                        "The new password is the same as the current password."
                    )

                else:

                    manager.update_user(
                        user.id,
                        password=new_password
                    )

                    manager._save_data()

                    st.session_state.admin_page = (
                        "Profile Update Success"
                    )

                    st.rerun()


    # =========================================================
    # Current Admin Profile Update Success
    # =========================================================

    elif page == "Profile Update Success":

        success_page(
            "Profile Updated",
            "Your profile has been updated successfully!",
            "Your account information has been saved.",
            "Profile"
        )


    # =========================================================
    # Users
    # =========================================================

    elif page == "Users":

        st.title("Users")

        user_list = st.selectbox(
            "Show users list",
            ["", "Admins", "Students", "Teachers"]
        )


        # =====================================================
        # ADMINS
        # =====================================================

        if user_list == "Admins":

            left, right = st.columns([1, 6])

            with left:

                term = st.selectbox(
                    "Term",
                    ["-", "ID", "NAME"],
                    key="admin_term"
                )

            with right:

                if term == "ID":

                    search_term = st.number_input(
                        "Please enter the ID.",
                        min_value=0,
                        step=1,
                        key="admin_id_search"
                    )

                elif term == "NAME":

                    search_term = st.text_input(
                        "Please enter the name.",
                        key="admin_name_search"
                    )


            admin_data = []


            for admin in manager.admins:

                if term == "-":

                    admin_data.append({
                        "ID": admin.id,
                        "Name": admin.name,
                        "Select": False
                    })

                elif term == "ID":

                    if admin.id == search_term:

                        admin_data.append({
                            "ID": admin.id,
                            "Name": admin.name,
                            "Select": False
                        })

                elif term == "NAME":

                    if search_term.lower() in admin.name.lower():

                        admin_data.append({
                            "ID": admin.id,
                            "Name": admin.name,
                            "Select": False
                        })


            admin_df = pd.DataFrame(
                admin_data,
                columns=[
                    "ID",
                    "Name",
                    "Select"
                ]
            )


            edited_admin_data = st.data_editor(
                admin_df,
                column_config={

                    "ID": st.column_config.NumberColumn(
                        "ID",
                        width="small",
                        disabled=True
                    ),

                    "Name": st.column_config.TextColumn(
                        "Name",
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
                key="admin_table"
            )


            left_button, right_button = st.columns(2)

            with left_button:

                if st.button("Update Profile", width="stretch"):

                    selected_users = edited_admin_data[
                        edited_admin_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Update User Profile"
                        st.rerun()


            with right_button:

                if st.button("Delete User", width="stretch"):

                    selected_users = edited_admin_data[
                        edited_admin_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Delete User"
                        st.rerun()


        # =====================================================
        # STUDENTS
        # =====================================================

        elif user_list == "Students":

            left, right = st.columns([1, 6])

            with left:

                term = st.selectbox(
                    "Term",
                    [
                        "-",
                        "ID",
                        "NAME",
                        "INSTRUMENT"
                    ],
                    key="student_term"
                )

            with right:

                if term == "ID":

                    search_term = st.number_input(
                        "Please enter the ID.",
                        min_value=0,
                        step=1,
                        key="student_id_search"
                    )

                elif term == "NAME":

                    search_term = st.text_input(
                        "Please enter the name.",
                        key="student_name_search"
                    )

                elif term == "INSTRUMENT":
                    search_term = st.selectbox(
                        "Please choose the instrument.",
                        manager.school_data["instruments"],
                        key="student_instrument_search"
                    )

            student_data = []


            if term == "-":

                for student in manager.students:

                    student_data.append({
                        "ID": student.id,
                        "Name": student.name,
                        "Select": False
                    })


            elif term == "ID":

                for student in manager.students:

                    if student.id == search_term:

                        student_data.append({
                            "ID": student.id,
                            "Name": student.name,
                            "Select": False
                        })


            elif term == "NAME":

                for student in manager.students:

                    if search_term.lower() in student.name.lower():

                        student_data.append({
                            "ID": student.id,
                            "Name": student.name,
                            "Select": False
                        })


            elif term == "INSTRUMENT":

                for student in manager.students:

                    if search_term in student.grades:

                        student_data.append({
                            "ID": student.id,
                            "Name": student.name,
                            "Select": False
                        })


            if len(student_data) == 0:

                st.error("No student found.")

            else:

                student_df = pd.DataFrame(
                    student_data,
                    columns=[
                        "ID",
                        "Name",
                        "Select"
                    ]
                )


                edited_student_data = st.data_editor(
                    student_df,
                    column_config={

                        "ID": st.column_config.NumberColumn(
                            "ID",
                            width="small",
                            disabled=True
                        ),

                        "Name": st.column_config.TextColumn(
                            "Name",
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
                    key="student_table"
                )


            left_button, right_button = st.columns(2)

            with left_button:

                if st.button("Update Profile", width="stretch"):

                    selected_users = edited_student_data[
                        edited_student_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Update User Profile"
                        st.rerun()


            with right_button:

                if st.button("Delete User", width="stretch"):

                    selected_users = edited_student_data[
                        edited_student_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Delete User"
                        st.rerun()

        # =====================================================
        # TEACHERS
        # =====================================================

        elif user_list == "Teachers":

            left, right = st.columns([1, 6])

            with left:

                term = st.selectbox(
                    "Term",
                    [
                        "-",
                        "ID",
                        "NAME",
                        "SPECIALITY",
                        "DESCRIPTION"
                    ],
                    key="teacher_term"
                )

            with right:

                if term == "ID":

                    search_term = st.number_input(
                        "Please enter the ID.",
                        min_value=0,
                        step=1,
                        key="teacher_id_search"
                    )

                elif term == "NAME":

                    search_term = st.text_input(
                        "Please enter the name.",
                        key="teacher_name_search"
                    )

                elif term == "SPECIALITY":

                    search_term = st.text_input(
                        "Please enter the speciality.",
                        key="teacher_speciality_search"
                    )

                elif term == "DESCRIPTION":

                    search_term = st.text_input(
                        "Please enter the description.",
                        key="teacher_description_search"
                    )


            teacher_data = []


            if term == "-":

                for teacher in manager.teachers:

                    teacher_data.append({
                        "ID": teacher.id,
                        "Name": teacher.name,
                        "Speciality": teacher.speciality,
                        "Description": teacher.description,
                        "Select": False
                    })


            elif term == "ID":

                for teacher in manager.teachers:

                    if teacher.id == search_term:

                        teacher_data.append({
                            "ID": teacher.id,
                            "Name": teacher.name,
                            "Speciality": teacher.speciality,
                            "Description": teacher.description,
                            "Select": False
                        })


            elif term == "NAME":

                for teacher in manager.teachers:

                    if search_term.lower() in teacher.name.lower():

                        teacher_data.append({
                            "ID": teacher.id,
                            "Name": teacher.name,
                            "Speciality": teacher.speciality,
                            "Description": teacher.description,
                            "Select": False
                        })


            elif term == "SPECIALITY":

                for teacher in manager.teachers:

                    if search_term.lower() in teacher.speciality.lower():

                        teacher_data.append({
                            "ID": teacher.id,
                            "Name": teacher.name,
                            "Speciality": teacher.speciality,
                            "Description": teacher.description,
                            "Select": False
                        })


            elif term == "DESCRIPTION":

                for teacher in manager.teachers:

                    if search_term.lower() in teacher.description.lower():

                        teacher_data.append({
                            "ID": teacher.id,
                            "Name": teacher.name,
                            "Speciality": teacher.speciality,
                            "Description": teacher.description,
                            "Select": False
                        })


            if len(teacher_data) == 0:

                st.error("No Teacher found.")

            else:

                teacher_df = pd.DataFrame(
                    teacher_data,
                    columns=[
                        "ID",
                        "Name",
                        "Speciality",
                        "Description",
                        "Select"
                    ]
                )


                edited_teacher_data = st.data_editor(
                    teacher_df,
                    column_config={

                        "ID": st.column_config.NumberColumn(
                            "ID",
                            width="small",
                            disabled=True
                        ),

                        "Name": st.column_config.TextColumn(
                            "Name",
                            width="medium",
                            disabled=True
                        ),

                        "Speciality": st.column_config.TextColumn(
                            "Speciality",
                            width="medium",
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
                    key="teacher_table"
                )


            left_button, right_button = st.columns(2)

            with left_button:

                if st.button("Update Profile", width="stretch"):

                    selected_users = edited_teacher_data[
                        edited_teacher_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Update User Profile"
                        st.rerun()


            with right_button:

                if st.button("Delete User", width="stretch"):

                    selected_users = edited_teacher_data[
                        edited_teacher_data["Select"] == True
                    ]

                    if len(selected_users) == 0:
                        st.error("Please select a user.")

                    elif len(selected_users) > 1:
                        st.error("Please select only one user.")

                    else:
                        selected_user_id = int(
                            selected_users.iloc[0]["ID"]
                        )

                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.admin_page = "Delete User"
                        st.rerun()


        # =====================================================
        # Add Account
        # =====================================================

        st.divider()

        if st.button("Add Account"):

            st.session_state.admin_page = "Add Account"

            st.rerun()



    # =========================================================
    # Delete Selected User
    # =========================================================

    elif page == "Delete User":

        st.title("Delete User")

        if "selected_user_id" not in st.session_state:

            st.error("No user selected.")

            if st.button("Back to Users"):

                st.session_state.admin_page = "Users"
                st.rerun()

        else:

            target_user = manager.find_user_by_id(
                st.session_state.selected_user_id
            )

            if target_user is None:

                st.error("User not found.")

                if st.button("Back to Users"):

                    st.session_state.admin_page = "Users"

                    if "selected_user_id" in st.session_state:
                        del st.session_state.selected_user_id

                    st.rerun()

            else:

                # -------------------------------------------------
                # User Information
                # -------------------------------------------------

                st.subheader("User Information")

                st.write(f"**User ID:** {target_user.id}")
                st.write(f"**Name:** {target_user.name}")

                if isinstance(target_user, AdminUser):

                    st.write("**User Type:** Admin")

                elif isinstance(target_user, TeacherUser):

                    st.write("**User Type:** Teacher")
                    st.write(
                        f"**Speciality:** {target_user.speciality}"
                    )
                    st.write(
                        f"**Description:** {target_user.description}"
                    )

                    teacher_courses = [
                        course
                        for course in manager.courses
                        if course.teacher_id == target_user.id
                    ]

                    st.write("**Courses:**")

                    if teacher_courses:

                        for course in teacher_courses:
                            st.write(
                                f"- {getattr(course, 'id', 'Unknown ID')}"
                            )

                    else:

                        st.write("No courses assigned.")

                elif isinstance(target_user, StudentUser):

                    st.write("**User Type:** Student")

                    st.write("**Instruments and Grades:**")

                    if target_user.grades:

                        for instrument, grade in target_user.grades.items():
                            st.write(
                                f"- {instrument}: Grade {grade}"
                            )

                    else:

                        st.write("No instrument enrolled.")

                    st.write("**Enrolled Course IDs:**")

                    if target_user.enrolled_course_ids:

                        for course_id in target_user.enrolled_course_ids:
                            st.write(f"- {course_id}")

                    else:

                        st.write("No courses enrolled.")

                st.warning(
                    "This action will permanently delete this user account."
                )

                # -------------------------------------------------
                # Password Confirmation
                # -------------------------------------------------

                admin_password = st.text_input(
                    "Please enter your admin password to confirm the deletion.",
                    type="password"
                )

                left_button, right_button = st.columns(2)

                with left_button:

                    if st.button(
                        "Confirm Delete User",
                        width="stretch"
                    ):

                        if not admin_password:

                            st.error("Please enter your admin password.")

                        elif admin_password != user.password:

                            st.error("Wrong admin password.")

                        else:

                            deleted_user_name = target_user.name

                            manager.remove_user(target_user.id)
                            manager._save_data()

                            st.session_state.deleted_user_name = (
                                deleted_user_name
                            )

                            if "selected_user_id" in st.session_state:
                                del st.session_state.selected_user_id

                            st.session_state.admin_page = (
                                "Delete User Success"
                            )

                            st.rerun()

                with right_button:

                    if st.button("Cancel", width="stretch"):

                        st.session_state.admin_page = "Users"

                        if "selected_user_id" in st.session_state:
                            del st.session_state.selected_user_id

                        st.rerun()


    # =========================================================
    # Update Selected User Profile
    # =========================================================

    elif page == "Update User Profile":

        st.title("Update User Profile")


        # -----------------------------------------------------
        # Confirm Admin Identity
        # -----------------------------------------------------

        admin_password = st.text_input(
            "Please enter your admin password to confirm your identity.",
            type="password"
        )


        if admin_password == user.password:

            if "selected_user_id" not in st.session_state:

                st.error("No user selected.")

            else:

                target_user = manager.find_user_by_id(
                    st.session_state.selected_user_id
                )


                if target_user is None:

                    st.error("User not found.")

                else:

                    st.subheader(
                        f"User ID: {target_user.id}"
                    )

                    st.subheader(
                        f"Current Name: {target_user.name}"
                    )
                    if isinstance(target_user, TeacherUser):
                        st.subheader(f"Current Speciality: {target_user.speciality}")
                        st.subheader(f"Current Description: {target_user.description}")
                    elif isinstance(target_user, StudentUser):
                        st.subheader("Current Istruments:")

                        if target_user.grades:
                            for instrument, grade in target_user.grades.items():
                                st.write(f"{instrument}: grade {grade}")
                        else:
                            st.write("No instrument enrolled.")


                    # -------------------------------------------------
                    # User Type
                    # -------------------------------------------------

                    if isinstance(target_user, TeacherUser):

                        update_options = [
                            "Name",
                            "Password",
                            "Speciality",
                            "Description"
                        ]
                    elif isinstance(target_user, StudentUser):
                        update_options = [
                            "Name",
                            "Password",
                            "Enroll Instrument",
                            "Disenroll Instrument",
                            "Update Enrollment"
                        ]
                    else:

                        update_options = [
                            "Name",
                            "Password"
                        ]


                    choice = st.selectbox(
                        "Update Term",
                        update_options
                    )


                    # =================================================
                    # Name
                    # =================================================

                    if choice == "Name":

                        new_name = st.text_input(
                            "Please enter the NEW NAME."
                        )


                        if st.button("Update"):

                            if not manager.valid_name(new_name):

                                st.error(
                                    "Invalid name."
                                )

                            elif new_name == target_user.name:

                                st.error(
                                    "The new name is the same as the current name."
                                )

                            else:

                                manager.update_user(
                                    target_user.id,
                                    name=new_name
                                )

                                manager._save_data()

                                st.session_state.admin_page = (
                                    "User Update Success"
                                )

                                st.rerun()


                    # =================================================
                    # Password
                    # =================================================

                    elif choice == "Password":

                        new_password = st.text_input(
                            "Please enter the NEW PASSWORD.",
                            type="password"
                        )

                        confirm_password = st.text_input(
                            "Please confirm the NEW PASSWORD.",
                            type="password"
                        )


                        if st.button("Update"):

                            if not new_password:

                                st.error(
                                    "Please enter a new password."
                                )

                            elif new_password != confirm_password:

                                st.error(
                                    "The confirmation is not the same as the new password."
                                )

                            else:

                                manager.update_user(
                                    target_user.id,
                                    password=new_password
                                )

                                manager._save_data()

                                st.session_state.admin_page = (
                                    "User Update Success"
                                )

                                st.rerun()

                    elif choice == "Enroll Instrument":

                        st.subheader("Enroll Instrument")

                        available_instruments = [
                            instrument
                            for instrument in manager.school_data["instruments"]
                            if instrument not in target_user.grades
                        ]

                        if not available_instruments:

                            st.info(
                                "The student is already enrolled in all available instruments."
                            )

                        else:

                            instrument = st.selectbox(
                                "Please choose an instrument.",
                                available_instruments,
                                key="enroll_instrument"
                            )

                            grade = st.number_input(
                                "Please enter the grade.",
                                min_value=1,
                                step=1,
                                max_value=8,
                                key="enroll_grade"
                            )


                            if st.button("Enroll"):

                                success = manager.enrol_instrument(
                                    target_user.id,
                                    instrument,
                                    grade
                                )

                                if success:

                                    manager._save_data()

                                    st.session_state.instrument_success_message = (
                                        f"{instrument} has been successfully enrolled."
                                    )

                                    st.session_state.admin_page = (
                                        "Instrument Enroll Success"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        "Failed to enroll the instrument."
                                    )


                    # =================================================
                    # Disenroll Instrument
                    # =================================================

                    elif choice == "Disenroll Instrument":

                        st.subheader("Disenroll Instrument")

                        enrolled_instruments = list(
                            target_user.grades.keys()
                        )

                        if not enrolled_instruments:

                            st.info(
                                "The student is not enrolled in any instrument."
                            )

                        else:

                            instrument = st.selectbox(
                                "Please choose an instrument to disenroll.",
                                enrolled_instruments,
                                key="disenroll_instrument"
                            )


                            if st.button("Disenroll"):

                                success = manager.disenroll_instrument(
                                    target_user.id,
                                    instrument
                                )

                                if success:

                                    manager._save_data()

                                    st.session_state.instrument_success_message = (
                                        f"{instrument} has been successfully disenrolled."
                                    )

                                    st.session_state.admin_page = (
                                        "Instrument Disenroll Success"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        "Failed to disenroll the instrument."
                                    )


                    # =================================================
                    # Update Enrollment
                    # =================================================

                    elif choice == "Update Enrollment":

                        st.subheader("Update Enrollment")

                        enrolled_instruments = list(
                            target_user.grades.keys()
                        )

                        if not enrolled_instruments:

                            st.info(
                                "The student is not enrolled in any instrument."
                            )

                        else:

                            instrument = st.selectbox(
                                "Please choose an instrument.",
                                enrolled_instruments,
                                key="update_enrollment_instrument"
                            )

                            current_grade = target_user.grades[
                                instrument
                            ]

                            st.write(
                                f"Current Grade: {current_grade}"
                            )

                            grade = st.number_input(
                                "Please enter the NEW grade.",
                                min_value=1,
                                step=1,
                                max_value=8,
                                value=int(current_grade),
                                key="update_enrollment_grade"
                            )


                            if st.button("Update Enrollment"):

                                if grade == current_grade:

                                    st.error(
                                        "The new grade is the same as the current grade."
                                    )

                                else:

                                    success = manager.update_enrollment(
                                        target_user.id,
                                        instrument,
                                        grade
                                    )

                                    if success:

                                        manager._save_data()

                                        st.session_state.instrument_success_message = (
                                            f"{instrument} enrollment has been successfully updated."
                                        )

                                        st.session_state.admin_page = (
                                            "Enrollment Update Success"
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            "Failed to update the enrollment."
                                        )
                    # =================================================
                    # Teacher Speciality
                    # =================================================

                    elif choice == "Speciality":

                        instruments = manager.school_data[
                            "instruments"
                        ]


                        if target_user.speciality in instruments:

                            current_index = instruments.index(
                                target_user.speciality
                            )

                        else:

                            current_index = 0


                        new_speciality = st.selectbox(
                            "Please choose the NEW speciality.",
                            instruments,
                            index=current_index
                        )


                        if st.button("Update"):

                            if new_speciality == target_user.speciality:

                                st.error(
                                    "The new speciality is the same as the current speciality."
                                )

                            else:

                                manager.update_user(
                                    target_user.id,
                                    speciality=new_speciality
                                )

                                manager._save_data()

                                st.session_state.admin_page = (
                                    "User Update Success"
                                )

                                st.rerun()


                    # =================================================
                    # Teacher Description
                    # =================================================

                    elif choice == "Description":

                        new_description = st.text_area(
                            "Please enter the NEW description.",
                            value=target_user.description
                        )


                        if st.button("Update"):

                            if new_description == target_user.description:

                                st.error(
                                    "The new description is the same as the current description."
                                )

                            else:

                                manager.update_user(
                                    target_user.id,
                                    description=new_description
                                )

                                manager._save_data()

                                st.session_state.admin_page = (
                                    "User Update Success"
                                )

                                st.rerun()


        elif admin_password:

            st.error(
                "Wrong admin password."
            )


        # -----------------------------------------------------
        # Back
        # -----------------------------------------------------

        if st.button("Back to Users"):

            st.session_state.admin_page = "Users"

            if "selected_user_id" in st.session_state:
                del st.session_state.selected_user_id

            st.rerun()


    # =========================================================
    # Instrument Enroll Success
    # =========================================================

    elif page == "Instrument Enroll Success":

        success_page(
            "Instrument Enrolled",
            "The instrument has been enrolled successfully!",
            st.session_state.get(
                "instrument_success_message",
                "The instrument enrollment has been saved."
            ),
            "Users"
        )


    # =========================================================
    # Instrument Disenroll Success
    # =========================================================

    elif page == "Instrument Disenroll Success":

        success_page(
            "Instrument Disenrolled",
            "The instrument has been disenrolled successfully!",
            st.session_state.get(
                "instrument_success_message",
                "The instrument disenrollment has been saved."
            ),
            "Users"
        )


    # =========================================================
    # Enrollment Update Success
    # =========================================================

    elif page == "Enrollment Update Success":

        success_page(
            "Enrollment Updated",
            "The enrollment has been updated successfully!",
            st.session_state.get(
                "instrument_success_message",
                "The enrollment changes have been saved."
            ),
            "Users"
        )


    # =========================================================
    # User Update Success
    # =========================================================

    elif page == "User Update Success":

        success_page(
            "User Profile Updated",
            "The user profile has been updated successfully!",
            "The changes have been saved.",
            "Users"
        )


    # =========================================================
    # Reset Password
    # =========================================================

    elif page == "Reset Password":

        st.title("Reset Password")

        admin_password = st.text_input(
            "Please enter your admin password to confirm your identity.",
            type="password"
        )


        if admin_password == user.password:

            user_id = st.number_input(
                "Please enter the USER ID.",
                min_value=0,
                step=1
            )

            new_password = st.text_input(
                "Please enter the new password.",
                type="password"
            )

            confirm_password = st.text_input(
                "Please confirm the new password.",
                type="password"
            )


            if st.button("Reset Password"):

                target_user = manager.find_user_by_id(
                    user_id
                )


                if target_user is None:

                    st.error(
                        "User not found."
                    )

                elif not new_password:

                    st.error(
                        "Please enter a new password."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "The confirmation is not the same as the new password."
                    )

                else:

                    manager.update_user(
                        target_user.id,
                        password=new_password
                    )

                    manager._save_data()

                    st.session_state.admin_page = (
                        "Reset Password Success"
                    )

                    st.rerun()


        elif admin_password:

            st.error(
                "Wrong admin password."
            )


    # =========================================================
    # Reset Password Success
    # =========================================================

    elif page == "Reset Password Success":

        success_page(
            "Password Reset",
            "The password has been reset successfully!",
            "The new password has been saved.",
            "Users"
        )


    # =========================================================
    # Add Account
    # =========================================================

    elif page == "Add Account":

        st.title("Add Account")

        account_type = st.selectbox(
            "Account Type",
            ["Admin", "Teacher", "Student"]
        )


        name = st.text_input(
            "Please enter the name."
        )


        password = st.text_input(
            "Please enter the password.",
            type="password"
        )


        confirm_password = st.text_input(
            "Please confirm the password.",
            type="password"
        )


        if account_type == "Teacher":

            speciality = st.selectbox(
                "Please choose the speciality.",
                manager.school_data["instruments"]
            )

            description = st.text_area(
                "Please enter the description."
            )


        if st.button("Add Account"):

            if not name or not password:

                st.error(
                    "Please enter the name and password."
                )

            elif not manager.valid_name(name):

                st.error(
                    "Invalid name."
                )

            elif password != confirm_password:

                st.error(
                    "The password is not the same as the confirmation."
                )

            elif account_type == "Admin":

                manager.add_admin(
                    name,
                    password
                )

                manager._save_data()

                st.session_state.admin_page = (
                    "Add Account Success"
                )

                st.rerun()


            elif account_type == "Teacher":

                manager.add_teacher(
                    name,
                    password,
                    speciality,
                    description
                )

                manager._save_data()

                st.session_state.admin_page = (
                    "Add Account Success"
                )

                st.rerun()


            elif account_type == "Student":

                manager.add_student(
                    name,
                    password
                )

                manager._save_data()

                st.session_state.admin_page = (
                    "Add Account Success"
                )

                st.rerun()


    # =========================================================
    # Add Account Success
    # =========================================================

    elif page == "Add Account Success":

        success_page(
            "Account Added",
            "The account has been added successfully!",
            "The new account has been saved.",
            "Users"
        )


    # =========================================================
    # Applications
    # =========================================================

    elif page == "Applications":

        st.title("Applications")

        applications = manager.school_data.get(
            "applications",
            []
        )

        # -----------------------------------------------------
        # Search / Filter
        # -----------------------------------------------------

        left, right = st.columns([1, 6])

        with left:

            term = st.selectbox(
                "Term",
                ["-", "NAME", "SPECIALITY", "DESCRIPTION"],
                key="application_term"
            )

        with right:

            if term == "NAME":

                search_term = st.text_input(
                    "Please enter the name.",
                    key="application_name_search"
                )

            elif term == "SPECIALITY":

                search_term = st.text_input(
                    "Please enter the speciality.",
                    key="application_speciality_search"
                )

            elif term == "DESCRIPTION":

                search_term = st.text_input(
                    "Please enter the description.",
                    key="application_description_search"
                )


        # -----------------------------------------------------
        # Filter Applications
        # -----------------------------------------------------

        application_indices = []
        application_data = []

        for index, application in enumerate(applications):

            if term == "-":

                matched = True

            elif term == "NAME":

                matched = (
                    search_term.lower()
                    in application["name"].lower()
                )

            elif term == "SPECIALITY":

                matched = (
                    search_term.lower()
                    in application["speciality"].lower()
                )

            elif term == "DESCRIPTION":

                matched = (
                    search_term.lower()
                    in application["description"].lower()
                )

            else:

                matched = False


            if matched:

                # Store the original index.
                # This is important because the displayed
                # DataFrame may be filtered.
                application_indices.append(index)

                application_data.append({
                    "Name": application["name"],
                    "Speciality": application["speciality"],
                    "Description": application["description"],
                    "Select": False
                })


        # -----------------------------------------------------
        # No Applications Found
        # -----------------------------------------------------

        if len(application_data) == 0:

            st.error("No Application found.")

        else:

            application_df = pd.DataFrame(
                application_data,
                columns=[
                    "Name",
                    "Speciality",
                    "Description",
                    "Select"
                ]
            )

            edited_application_data = st.data_editor(
                application_df,
                column_config={
                    "Name": st.column_config.TextColumn(
                        "Name",
                        width="medium",
                        disabled=True
                    ),

                    "Speciality": st.column_config.TextColumn(
                        "Speciality",
                        width="medium",
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
                key="application_table"
            )


            # -------------------------------------------------
            # Approve / Delete Buttons
            # -------------------------------------------------

            left_button, right_button = st.columns(2)


            # =================================================
            # Approve
            # =================================================

            with left_button:

                if st.button(
                    "Approve",
                    width="stretch"
                ):

                    selected_applications = (
                        edited_application_data[
                            edited_application_data["Select"] == True
                        ]
                    )


                    if len(selected_applications) == 0:

                        st.error(
                            "Please select an application."
                        )

                    elif len(selected_applications) > 1:

                        st.error(
                            "Please select only one application."
                        )

                    else:

                        # Index inside the filtered DataFrame
                        selected_index = (
                            selected_applications.index[0]
                        )

                        # Convert filtered index back to
                        # original applications list index
                        original_index = (
                            application_indices[selected_index]
                        )

                        application = (
                            applications[original_index]
                        )


                        # Create the teacher account
                        manager.add_teacher(
                            application["name"],
                            application["password"],
                            application["speciality"],
                            application["description"]
                        )


                        # Remove the application
                        applications.pop(original_index)


                        # Save changes
                        manager._save_data()


                        st.success(
                            "Teacher application approved!"
                        )

                        st.rerun()


            # =================================================
            # Delete
            # =================================================

            with right_button:

                if st.button(
                    "Delete",
                    width="stretch"
                ):

                    selected_applications = (
                        edited_application_data[
                            edited_application_data["Select"] == True
                        ]
                    )


                    if len(selected_applications) == 0:

                        st.error(
                            "Please select at least one application."
                        )

                    else:

                        # Get the indexes from the filtered
                        # DataFrame
                        selected_indices = (
                            selected_applications.index.tolist()
                        )


                        # Convert them to indexes of the
                        # original applications list
                        original_indices = [
                            application_indices[index]
                            for index in selected_indices
                        ]


                        # Delete from the back to the front.
                        # This prevents earlier indexes from
                        # changing while deleting.
                        for index in sorted(
                            original_indices,
                            reverse=True
                        ):

                            applications.pop(index)


                        # Save changes
                        manager._save_data()


                        st.success(
                            "Teacher application(s) deleted!"
                        )

                        st.rerun()

    # =========================================================
    # Courses
    # =========================================================

    elif page == "Courses":

        st.title("Courses")


    # =========================================================
    # Instruments
    # =========================================================

    elif page == "Instruments":
        st.title("Instruments")

        instruments = manager.school_data.get("instruments", [])

        instrument_data = []

        for instrument in instruments:
            teacher_count = sum(
                1
                for teacher in manager.teachers
                if teacher.speciality == instrument
            )

            student_count = sum(
                1
                for student in manager.students
                if instrument in student.grades
            )

            course_count = sum(
                1
                for course in manager.courses
                if course.instrument == instrument
            )

            instrument_data.append({
                "Instrument": instrument,
                "Teachers": teacher_count,
                "Students": student_count,
                "Courses": course_count
            })

        instrument_df = pd.DataFrame(
            instrument_data,
            columns=["Instrument", "Teachers", "Students", "Courses"]
        )

        st.data_editor(
            instrument_df,
            column_config={
                "Instrument": st.column_config.TextColumn(
                    "Instrument",
                    width="medium",
                    disabled=True
                ),
                "Teachers": st.column_config.NumberColumn(
                    "Teachers",
                    width="small",
                    disabled=True
                ),
                "Students": st.column_config.NumberColumn(
                    "Students",
                    width="small",
                    disabled=True
                ),
                "Courses": st.column_config.NumberColumn(
                    "Courses",
                    width="small",
                    disabled=True
                )
            },
            hide_index=True,
            width="stretch",
            disabled=True,
            key="instrument_table"
        )

        st.write("")

        st.subheader("Add Instrument")

        new_instrument = st.text_input(
            "Instrument name",
            placeholder="Enter a new instrument"
        )

        if st.button("Add Instrument", width="stretch"):
            new_instrument = new_instrument.strip()

            if new_instrument == "":
                st.error("Please enter an instrument name.")

            elif new_instrument in instruments:
                st.error("This instrument already exists.")

            else:
                manager.add_instrument(new_instrument)
                manager._save_data()
                st.success(f"{new_instrument} has been added.")
                st.rerun()