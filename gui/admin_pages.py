import streamlit as st
import pandas as pd
import datetime
from app.admin import AdminUser
from app.teacher import TeacherUser, Course
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
        if "selected_course_id" in st.session_state:
            del st.session_state.selected_course_id
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

    if st.sidebar.button("Daily Roster", width="stretch"):
        st.session_state.admin_page = "Daily Roster"
    if st.sidebar.button("Financial", width="stretch"):
        st.session_state.admin_page = "Financial"
        st.rerun()
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
                    search_term = st.selectbox(
                        "Please choose the instrument.",
                        manager.school_data["instruments"],
                        key="teacher_instrument_search"
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

                    if search_term == teacher.speciality:

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
                        elif user.id == target_user.id:
                            st.error("An admin cannot remove themselves.")
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

    # =========================================================
    # Courses
    # =========================================================

    elif page == "Courses":

        st.title("Courses")

        # -----------------------------------------------------
        # Search / Filter
        # -----------------------------------------------------

        left, right = st.columns([1, 6])

        with left:

            term = st.selectbox(
                "Term",
                [
                    "-",
                    "ID",
                    "COURSE NAME",
                    "INSTRUMENT",
                    "TEACHER ID"
                ],
                key="admin_course_term"
            )

        with right:

            if term == "ID":

                search_term = st.number_input(
                    "Please enter the ID.",
                    min_value=0,
                    step=1,
                    key="admin_course_id_search"
                )

            elif term == "COURSE NAME":

                search_term = st.text_input(
                    "Please enter the course name.",
                    key="admin_course_name_search"
                )

            elif term == "INSTRUMENT":

                search_term = st.selectbox(
                    "Please choose the instrument.",
                    manager.school_data["instruments"],
                    key="admin_course_instrument_search"
                )

            elif term == "TEACHER ID":

                search_term = st.number_input(
                    "Please enter the teacher's ID.",
                    min_value=0,
                    step=1,
                    key="admin_course_teacher_id_search"
                )

        # -----------------------------------------------------
        # Course Data
        # -----------------------------------------------------

        course_data = []

        for course in manager.courses:

            if term == "-":

                matched = True

            elif term == "ID":

                matched = course.id == search_term

            elif term == "COURSE NAME":

                matched = (
                    search_term.lower()
                    in course.name.lower()
                )

            elif term == "INSTRUMENT":

                matched = course.instrument == search_term

            elif term == "TEACHER ID":

                matched = course.teacher_id == search_term

            else:

                matched = False

            if matched:

                course_data.append({
                    "ID": course.id,
                    "Course Name": course.name,
                    "Instrument": course.instrument,
                    "Teacher ID": course.teacher_id,
                    "Grade": course.grade,
                    "Description": course.description,
                    "Max Student": course.max_student,
                    "Select": False
                })

        # -----------------------------------------------------
        # Course Table
        # -----------------------------------------------------

        if len(course_data) == 0:

            st.error("No Course found.")

        else:

            course_df = pd.DataFrame(
                course_data,
                columns=[
                    "ID",
                    "Course Name",
                    "Instrument",
                    "Teacher ID",
                    "Grade",
                    "Description",
                    "Max Student",
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

                    "Teacher ID": st.column_config.NumberColumn(
                        "Teacher ID",
                        width="small",
                        disabled=True
                    ),

                    "Grade": st.column_config.NumberColumn(
                        "Grade",
                        width="small",
                        disabled=True
                    ),

                    "Description": st.column_config.TextColumn(
                        "Description",
                        width="large",
                        disabled=True
                    ),

                    "Max Student": st.column_config.NumberColumn(
                        "Max Student",
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
                key="course_table"
            )

            # -------------------------------------------------
            # Update / Delete Buttons
            # -------------------------------------------------

            left_button, right_button = st.columns(2)

            with left_button:

                if st.button(
                    "Update Course",
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

                        st.session_state.admin_page = (
                            "Update Course"
                        )

                        st.rerun()

            with right_button:

                if st.button(
                    "Delete Course",
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

                        st.session_state.admin_page = (
                            "Delete Course"
                        )

                        st.rerun()

        # -----------------------------------------------------
        # Add Course
        # -----------------------------------------------------

        st.divider()

        if st.button(
            "Add Course",
            width="stretch"
        ):

            st.session_state.admin_page = "Add Course"
            st.rerun()
    # =========================================================
    # Delete Selected Course
    # =========================================================

    elif page == "Delete Course":

        st.title("Delete Course")

        if "selected_course_id" not in st.session_state:

            st.error("No course selected.")

            if st.button("Back to Courses"):

                st.session_state.admin_page = "Courses"
                st.rerun()

        else:

            target_course = manager.find_course_by_id(
                st.session_state.selected_course_id
            )

            if target_course is None:

                st.error("Course not found.")

                if st.button("Back to Courses"):

                    st.session_state.admin_page = "Courses"

                    if "selected_course_id" in st.session_state:
                        del st.session_state.selected_course_id

                    st.rerun()

            else:

                # -------------------------------------------------
                # Course Information
                # -------------------------------------------------

                st.subheader("Course Information")

                st.write(f"**Course ID:** {target_course.id}")
                st.write(f"**Course Name:** {target_course.name}")
                st.write(f"**Instrument:** {target_course.instrument}")
                st.write(f"**Teacher ID:** {target_course.teacher_id}")
                st.write(f"**Grade:** {target_course.grade}")
                st.write(f"**Max Student:** {target_course.max_student}")
                st.write(f"**Description:** {target_course.description}")

                st.write("**Enrolled Students:**")

                if target_course.enrolled_student_ids:

                    for student_id in target_course.enrolled_student_ids:
                        st.write(f"- {student_id}")

                else:

                    st.write("No students enrolled.")

                st.warning(
                    "This action will permanently delete this course."
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
                        "Confirm Delete Course",
                        width="stretch"
                    ):

                        if not admin_password:

                            st.error(
                                "Please enter your admin password."
                            )

                        elif admin_password != user.password:

                            st.error("Wrong admin password.")

                        else:

                            deleted_course_name = target_course.name

                            manager.remove_course(
                                target_course.id
                            )

                            manager._save_data()

                            st.session_state.deleted_course_name = (
                                deleted_course_name
                            )

                            if "selected_course_id" in st.session_state:
                                del st.session_state.selected_course_id

                            st.session_state.admin_page = (
                                "Delete Course Success"
                            )

                            st.rerun()

                with right_button:

                    if st.button(
                        "Cancel",
                        width="stretch"
                    ):

                        st.session_state.admin_page = "Courses"

                        if "selected_course_id" in st.session_state:
                            del st.session_state.selected_course_id

                        st.rerun()
    # =========================================================
    # Delete Course Success
    # =========================================================

    elif page == "Delete Course Success":

        success_page(
            "Course Deleted",
            "The course has been deleted successfully!",
            f"{st.session_state.get('deleted_course_name', 'The course')} "
            "and its course information have been removed.",
            "Courses"
        )
    # =========================================================
    # Update Selected Course
    # =========================================================

    elif page == "Update Course":

        st.title("Update Course")

        # =====================================================
        # Confirm Admin Identity
        # =====================================================

        admin_password = st.text_input(
            "Please enter your admin password to confirm your identity.",
            type="password"
        )

        if admin_password != user.password:

            if admin_password:
                st.error("Wrong admin password.")

            st.info(
                "Please enter your admin password to continue."
            )

        else:

            # =================================================
            # Check Selected Course
            # =================================================

            if "selected_course_id" not in st.session_state:

                st.error("No course selected.")

                if st.button("Back to Courses"):

                    st.session_state.admin_page = "Courses"
                    st.rerun()

            else:

                target_course = manager.find_course_by_id(
                    st.session_state.selected_course_id
                )

                if target_course is None:

                    st.error("Course not found.")

                    if st.button("Back to Courses"):

                        st.session_state.admin_page = "Courses"

                        if "selected_course_id" in st.session_state:
                            del st.session_state.selected_course_id

                        st.rerun()

                else:

                    # =================================================
                    # Current Course Information
                    # =================================================

                    st.subheader("Current Course Information")

                    st.write(
                        f"**Course ID:** {target_course.id}"
                    )

                    st.write(
                        f"**Instrument:** {target_course.instrument}"
                    )

                    st.write(
                        f"**Grade:** {target_course.grade}"
                    )

                    st.write(
                        f"**Current Students:** "
                        f"{len(target_course.enrolled_student_ids)}"
                    )


                    # =================================================
                    # Course Name
                    # =================================================

                    new_course_name = st.text_input(
                        "Course Name",
                        value=target_course.name
                    )


                    # =================================================
                    # Teacher
                    # =================================================

                    compatible_teachers = [
                        teacher
                        for teacher in manager.teachers
                        if teacher.speciality == target_course.instrument
                    ]

                    if compatible_teachers:

                        teacher_options = {
                            f"{teacher.id} - {teacher.name}":
                            teacher
                            for teacher in compatible_teachers
                        }

                        current_teacher_label = None

                        for label, teacher in teacher_options.items():

                            if teacher.id == target_course.teacher_id:

                                current_teacher_label = label
                                break

                        if current_teacher_label is None:

                            current_teacher_label = list(
                                teacher_options.keys()
                            )[0]

                        selected_teacher_label = st.selectbox(
                            "Teacher",
                            list(teacher_options.keys()),
                            index=list(
                                teacher_options.keys()
                            ).index(current_teacher_label)
                        )

                        selected_teacher = teacher_options[
                            selected_teacher_label
                        ]

                    else:

                        selected_teacher = None

                        st.error(
                            "No teacher with the required "
                            "speciality is available."
                        )


                    # =================================================
                    # Instrument
                    # =================================================

                    st.text_input(
                        "Instrument",
                        value=target_course.instrument,
                        disabled=True
                    )


                    # =================================================
                    # Grade
                    # =================================================

                    st.number_input(
                        "Grade",
                        min_value=1,
                        max_value=8,
                        value=target_course.grade,
                        disabled=True
                    )


                    # =================================================
                    # Max Student
                    # =================================================

                    current_student_count = len(
                        target_course.enrolled_student_ids
                    )

                    new_max_student = st.number_input(
                        "Max Student",
                        min_value=current_student_count,
                        value=max(
                            target_course.max_student,
                            current_student_count
                        ),
                        step=1
                    )


                    # =================================================
                    # Description
                    # =================================================

                    new_description = st.text_area(
                        "Description",
                        value=target_course.description
                    )


                    # =================================================
                    # Course Password
                    # =================================================

                    st.subheader("Course Password")

                    st.write(
                        "Leave both fields empty if you do not "
                        "want to change the course password."
                    )

                    new_password = st.text_input(
                        "New Password",
                        type="password"
                    )

                    confirm_password = st.text_input(
                        "Confirm Password",
                        type="password"
                    )


                    # =================================================
                    # Enrolled Students
                    # =================================================

                    st.subheader("Enrolled Students")

                    current_students = []

                    for student_id in (
                        target_course.enrolled_student_ids
                    ):

                        student = manager.find_student_by_id(
                            student_id
                        )

                        if student:

                            current_students.append(student)


                    if current_students:

                        for student in current_students:

                            st.write(
                                f"- ID: {student.id}, "
                                f"Name: {student.name}"
                            )

                    else:

                        st.write("No students enrolled.")


                    # =================================================
                    # Remove Students
                    # =================================================

                    if current_students:

                        student_options = {
                            f"{student.id} - {student.name}":
                            student
                            for student in current_students
                        }

                        students_to_remove = st.multiselect(
                            "Remove Students",
                            list(student_options.keys())
                        )

                    else:

                        student_options = {}

                        students_to_remove = []


                    # =================================================
                    # Add Students
                    # =================================================

                    available_students = []

                    for student in manager.students:

                        # Already enrolled
                        if (
                            student.id
                            in target_course.enrolled_student_ids
                        ):
                            continue

                        # Must have required instrument
                        if (
                            target_course.instrument
                            not in student.grades
                        ):
                            continue

                        # Grade must match
                        if (
                            student.grades[
                                target_course.instrument
                            ]
                            != target_course.grade
                        ):
                            continue

                        available_students.append(student)


                    if available_students:

                        available_student_options = {
                            f"{student.id} - {student.name}":
                            student
                            for student in available_students
                        }

                        students_to_add = st.multiselect(
                            "Add Students",
                            list(
                                available_student_options.keys()
                            )
                        )

                    else:

                        available_student_options = {}

                        students_to_add = []

                        st.info(
                            "There are no eligible students "
                            "available to add to this course."
                        )


                    # =================================================
                    # Lessons
                    # =================================================

                    st.subheader("Lessons")

                    now = datetime.datetime.now()

                    if not target_course.lessons:

                        st.info("No lessons found.")

                    else:

                        for index, lesson in enumerate(
                            target_course.lessons
                        ):

                            lesson_datetime = (
                                datetime.datetime.strptime(
                                    f"{lesson['date']} "
                                    f"{lesson['time']}",
                                    "%Y-%m-%d %H:%M"
                                )
                            )

                            lesson_col1, lesson_col2, lesson_col3, lesson_col4 = (
                                st.columns(
                                    [2, 1, 4, 2]
                                )
                            )

                            with lesson_col1:

                                st.write(
                                    lesson["date"]
                                )

                            with lesson_col2:

                                st.write(
                                    lesson["time"]
                                )

                            with lesson_col3:

                                st.write(
                                    lesson["activity"]
                                )

                            with lesson_col4:

                                if lesson_datetime <= now:

                                    st.button(
                                        "Cannot Delete",
                                        disabled=True,
                                        key=(
                                            f"past_lesson_"
                                            f"{target_course.id}_"
                                            f"{index}"
                                        )
                                    )

                                else:
                                    if st.button(
                                        "Delete",
                                        key=(
                                            f"delete_lesson_"
                                            f"{target_course.id}_"
                                            f"{index}"
                                        )
                                    ):
                                        success = manager.delete_lesson(
                                            target_course.id,
                                            index
                                        )

                                        if success:
                                            st.rerun()
                                        else:
                                            st.error("Failed to delete lesson.")


                    # =================================================
                    # Add New Lesson
                    # =================================================

                    st.subheader("Add New Lesson")

                    lesson_date = st.date_input(
                        "Date",
                        min_value=datetime.date.today(),
                        key=(
                            f"new_lesson_date_"
                            f"{target_course.id}"
                        )
                    )

                    lesson_time = st.time_input(
                        "Time",
                        key=(
                            f"new_lesson_time_"
                            f"{target_course.id}"
                        )
                    )

                    lesson_activity = st.text_input(
                        "Activity",
                        key=(
                            f"new_lesson_activity_"
                            f"{target_course.id}"
                        )
                    )

                    if st.button(
                        "Add Lesson",
                        key=(
                            f"add_lesson_"
                            f"{target_course.id}"
                        )
                    ):

                        lesson_datetime = (
                            datetime.datetime.combine(
                                lesson_date,
                                lesson_time
                            )
                        )

                        if lesson_datetime <= now:

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
                                "activity": lesson_activity
                            }

                        success = manager.add_lesson(
                            target_course.id,
                            new_lesson
                        )

                        if success:
                            st.success("Lesson added successfully.")
                            st.rerun()
                        else:
                            st.error("Failed to add lesson.")

                            st.success(
                                "Lesson added successfully!"
                            )

                            st.rerun()


                    # =================================================
                    # Update / Cancel
                    # =================================================

                    st.divider()

                    left_button, right_button = st.columns(2)

                    with left_button:

                        if st.button(
                            "Update Course",
                            width="stretch"
                        ):

                            # -----------------------------------------
                            # Basic Validation
                            # -----------------------------------------

                            if not new_course_name.strip():

                                st.error(
                                    "Please enter the course name."
                                )

                            elif selected_teacher is None:

                                st.error(
                                    "Please choose a valid teacher."
                                )

                            elif (
                                new_password
                                and new_password
                                != confirm_password
                            ):

                                st.error(
                                    "The password is not the same "
                                    "as the confirmation."
                                )

                            else:

                                # -------------------------------------
                                # Calculate Student Changes
                                # -------------------------------------

                                remove_ids = []

                                for label in students_to_remove:

                                    student = student_options[
                                        label
                                    ]

                                    remove_ids.append(
                                        student.id
                                    )


                                add_ids = []

                                for label in students_to_add:

                                    student = (
                                        available_student_options[
                                            label
                                        ]
                                    )

                                    add_ids.append(
                                        student.id
                                    )


                                final_student_count = (
                                    len(
                                        target_course
                                        .enrolled_student_ids
                                    )
                                    - len(remove_ids)
                                    + len(add_ids)
                                )


                                # -------------------------------------
                                # Check Max Student
                                # -------------------------------------

                                if (
                                    new_max_student
                                    < final_student_count
                                ):

                                    st.error(
                                        "Max Student cannot be "
                                        "lower than the number "
                                        "of enrolled students."
                                    )

                                else:

                                    # -----------------------------
                                    # Update Course Information
                                    # -----------------------------

                                    update_fields = {
                                        "name":
                                            new_course_name.strip(),

                                        "teacher_id":
                                            selected_teacher.id,

                                        "description":
                                            new_description,

                                        "max_student":
                                            int(new_max_student)
                                    }


                                    # -----------------------------
                                    # Update Password
                                    # -----------------------------

                                    if new_password:

                                        update_fields[
                                            "password"
                                        ] = new_password


                                    manager.update_course(
                                        target_course.id,
                                        **update_fields
                                    )


                                    # -----------------------------
                                    # Remove Students
                                    # -----------------------------

                                    for student_id in remove_ids:

                                        student = (
                                            manager.find_student_by_id(
                                                student_id
                                            )
                                        )

                                        if student:

                                            if (
                                                target_course.id
                                                in student
                                                .enrolled_course_ids
                                            ):

                                                student.enrolled_course_ids.remove(
                                                    target_course.id
                                                )


                                        if (
                                            student_id
                                            in target_course
                                            .enrolled_student_ids
                                        ):

                                            target_course.enrolled_student_ids.remove(
                                                student_id
                                            )


                                    # -----------------------------
                                    # Add Students
                                    # -----------------------------

                                    for student_id in add_ids:

                                        student = (
                                            manager.find_student_by_id(
                                                student_id
                                            )
                                        )

                                        if not student:
                                            continue


                                        if (
                                            target_course.id
                                            not in student
                                            .enrolled_course_ids
                                        ):

                                            student.enrolled_course_ids.append(
                                                target_course.id
                                            )


                                        if (
                                            student_id
                                            not in target_course
                                            .enrolled_student_ids
                                        ):

                                            target_course.enrolled_student_ids.append(
                                                student_id
                                            )


                                    # -----------------------------
                                    # Save Everything
                                    # -----------------------------

                                    manager._save_data()

                                    st.session_state.admin_page = (
                                        "Update Course Success"
                                    )

                                    st.rerun()


                    with right_button:

                        if st.button(
                            "Cancel",
                            width="stretch"
                        ):

                            st.session_state.admin_page = (
                                "Courses"
                            )

                            if (
                                "selected_course_id"
                                in st.session_state
                            ):

                                del st.session_state[
                                    "selected_course_id"
                                ]

                            st.rerun()
    # =========================================================
    # Update Course Success
    # =========================================================

    elif page == "Update Course Success":

        success_page(
            "Course Updated",
            "The course has been updated successfully!",
            "The course information has been saved.",
            "Courses"
        )
    # =========================================================
    # Add Course
    # =========================================================

    elif page == "Add Course":

        st.title("Add Course")

        course_name = st.text_input(
            "Please enter the course name."
        )

        teacher_options = {
            f"{teacher.id} - {teacher.name}": teacher
            for teacher in manager.teachers
        }

        if teacher_options:

            selected_teacher_label = st.selectbox(
                "Please choose the teacher.",
                list(teacher_options.keys())
            )

            selected_teacher = teacher_options[
                selected_teacher_label
            ]

            instrument = selected_teacher.speciality

            st.text_input(
                "Instrument",
                value=instrument,
                disabled=True
            )

        else:

            selected_teacher = None
            instrument = None

            st.warning(
                "There are no teachers available."
            )


        max_student = st.number_input(
            "Max Student",
            min_value=1,
            step=1
        )


        grade = st.number_input(
            "Grade",
            min_value=1,
            max_value=8,
            step=1
        )


        password = st.text_input(
            "Please enter the password.",
            type="password"
        )


        confirm_password = st.text_input(
            "Please confirm the password.",
            type="password"
        )


        description = st.text_area(
            "Please enter the description."
        )


        if st.button("Add Course"):

            if not course_name or not password:

                st.error(
                    "Please enter the course name and password."
                )

            elif selected_teacher is None:

                st.error(
                    "Please choose a teacher."
                )

            elif password != confirm_password:

                st.error(
                    "The password is not the same as the confirmation."
                )

            else:

                new_course_id = manager.school_data[
                    "next_course_id"
                ]

                new_course = Course(
                    new_course_id,
                    course_name,
                    instrument,
                    selected_teacher.id,
                    grade,
                    password,
                    description,
                    max_student
                )

                manager.add_course(
                    course_name,
                    selected_teacher.id,
                    grade,
                    password,
                    description,
                    max_student
                )

                manager._save_data()

                st.session_state.admin_page = (
                    "Add Course Success"
                )

                st.rerun()
    # =========================================================
    # Add Course Success
    # =========================================================
    
    elif page == "Add Course Success":

        success_page(
            "Course Added",
            "The course has been added successfully!",
            "The new course has been saved.",
            "Courses"
        )
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
    # =========================================================
    # Daily Roster
    # =========================================================

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
        # Find all lessons on the selected date
        # -----------------------------------------------------

        roster_data = []

        now = datetime.datetime.now()

        for course in manager.courses:

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
                # Count students who are enrolled in the course
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
                # If lesson has already passed:
                #     show actual Present count
                #
                # If lesson has not happened:
                #     show expected attendance
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
                key="admin_daily_roster_table"
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

                    st.session_state.admin_page = (
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

                st.session_state.admin_page = "Daily Roster"

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

                    st.session_state.admin_page = "Daily Roster"

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

                        st.session_state.admin_page = "Daily Roster"

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

                                if attendance_exists:
                                    if st.button(
                                        "Delete Attendance",
                                        key=(
                                            f"delete_attendance_"
                                            f"{target_course.id}_"
                                            f"{selected_lesson_index}_"
                                            f"{student.id}"
                                        )
                                    ):
                                        success = manager.delete_attendance(
                                            student.id,
                                            target_course.id,
                                            selected_lesson_index
                                        )

                                        if success:
                                            st.rerun()
                                        else:
                                            st.error("Failed to delete attendance.")
                                else:
                                    if st.button(
                                        "Give Attendance",
                                        key=(
                                            f"attendance_"
                                            f"{target_course.id}_"
                                            f"{selected_lesson_index}_"
                                            f"{student.id}"
                                        )
                                    ):
                                        success = manager.give_attendance(
                                            student.id,
                                            target_course.id,
                                            selected_lesson_index
                                        )

                                        if success:
                                            st.rerun()
                                        else:
                                            st.error("Failed to give attendance.")

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

                            st.session_state.admin_page = (
                                "Daily Roster"
                            )

                            st.rerun()
    # =========================================================
    # Financial
    # =========================================================
    elif page == "Financial":

        st.title("Finance & Payments")

        # =====================================================
        # Record New Payment
        # =====================================================

        st.subheader("Record New Payment")

        with st.form("payment_form"):

            left, right = st.columns([1, 6])

            with left:
                search_term_type = st.selectbox(
                    "Search by",
                    ["-", "ID", "NAME"],
                    key="finance_payment_search_type"
                )

            with right:

                if search_term_type == "ID":

                    search_term = st.number_input(
                        "Please enter the student ID.",
                        min_value=0,
                        step=1,
                        key="finance_payment_id_search"
                    )

                elif search_term_type == "NAME":

                    search_term = st.text_input(
                        "Please enter the student name.",
                        key="finance_payment_name_search"
                    )

                else:

                    search_term = ""

            # -------------------------------------------------
            # Find Students
            # -------------------------------------------------

            filtered_students = []

            for student in manager.students:

                if search_term_type == "-":

                    matched = True

                elif search_term_type == "ID":

                    matched = student.id == int(search_term)

                elif search_term_type == "NAME":

                    matched = (
                        search_term.strip().lower()
                        in student.name.lower()
                    )

                else:

                    matched = False

                if matched:
                    filtered_students.append(student)

            # -------------------------------------------------
            # Select Student
            # -------------------------------------------------

            if filtered_students:

                student_options = {
                    f"{student.id} - {student.name}": student
                    for student in filtered_students
                }

                selected_student_label = st.selectbox(
                    "Select Student",
                    list(student_options.keys()),
                    key="finance_payment_student"
                )

                selected_student = student_options[
                    selected_student_label
                ]

                student_id = selected_student.id

            else:

                st.warning("No students found.")

                selected_student = None
                student_id = None

            # -------------------------------------------------
            # Payment Amount
            # -------------------------------------------------

            amount = st.number_input(
                "Payment Amount",
                min_value=0.01,
                step=0.01,
                key="finance_payment_amount"
            )

            # -------------------------------------------------
            # Payment Method
            # -------------------------------------------------

            method = st.text_input(
                "Payment Method (e.g., Credit Card, Cash)",
                key="finance_payment_method"
            )

            submitted = st.form_submit_button(
                "Record Payment"
            )

            # -------------------------------------------------
            # Record Payment
            # -------------------------------------------------

            if submitted:

                if selected_student is None:

                    st.error(
                        "Please select a student."
                    )

                elif not method.strip():

                    st.error(
                        "Please enter a payment method."
                    )

                else:

                    success = manager.record_payment(
                        student_id,
                        amount,
                        method.strip()
                    )

                    if success:

                        st.success(
                            f"Payment of {amount:.2f} for "
                            f"{selected_student.name} recorded."
                        )

        # =====================================================
        # Payment History
        # =====================================================

        st.subheader("View Student Payment History")

        history_left, history_right = st.columns([1, 6])

        with history_left:

            history_search_type = st.selectbox(
                "Search by",
                ["-", "ID", "NAME"],
                key="finance_history_search_type"
            )

        with history_right:

            if history_search_type == "ID":

                history_search_term = st.number_input(
                    "Please enter the student ID.",
                    min_value=0,
                    step=1,
                    key="finance_history_id_search"
                )

            elif history_search_type == "NAME":

                history_search_term = st.text_input(
                    "Please enter the student name.",
                    key="finance_history_name_search"
                )

            else:

                history_search_term = ""

        # -----------------------------------------------------
        # Find Students
        # -----------------------------------------------------

        history_filtered_students = []

        for student in manager.students:

            if history_search_type == "-":

                matched = True

            elif history_search_type == "ID":

                matched = (
                    student.id
                    == int(history_search_term)
                )

            elif history_search_type == "NAME":

                matched = (
                    history_search_term.strip().lower()
                    in student.name.lower()
                )

            else:

                matched = False

            if matched:
                history_filtered_students.append(student)

        # -----------------------------------------------------
        # Select Student
        # -----------------------------------------------------

        if history_filtered_students:

            history_student_options = {
                f"{student.id} - {student.name}": student
                for student in history_filtered_students
            }

            history_student_label = st.selectbox(
                "Select Student to View History",
                list(history_student_options.keys()),
                key="finance_history_student"
            )

            history_student = history_student_options[
                history_student_label
            ]

            history_student_id = history_student.id

            # =================================================
            # IMPORTANT:
            # Use ScheduleManager method
            # =================================================

            history = manager.get_payment_history(
                history_student_id
            )

            if history:

                history_df = pd.DataFrame(
                    history,
                    columns=[
                        "student_id",
                        "amount",
                        "method",
                        "timestamp"
                    ]
                )

                st.dataframe(
                    history_df,
                    hide_index=True,
                    width="stretch"
                )

            else:

                st.info(
                    "This student has no payment history."
                )

        else:

            st.warning("No students found.")

        # =====================================================
        # Export Report
        # =====================================================

        st.subheader("Export Report")

        report_type = st.selectbox(
            "Report Type",
            ["Finance", "Attendance"],
            key="finance_report_type"
        )

        if st.button(
            "Export Report",
            width="stretch"
        ):

            if report_type == "Finance":

                out_path = "finance_report.csv"

                manager.export_report(
                    "finance",
                    out_path
                )

            else:

                out_path = "attendance_report.csv"

                manager.export_report(
                    "attendance",
                    out_path
                )

            st.success(
                f"{report_type} report exported successfully."
            )