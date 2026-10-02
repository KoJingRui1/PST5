import streamlit as st

@st.dialog("Application Submitted")
def application_success():
    st.success("Your teacher application has been submitted!")
    st.write("Please wait for an administrator to review and approve your application.")

    if st.button("OK"):
        st.rerun()
def show_default_page(manager):
    if st.session_state.get("application_submitted", False):
        application_success()
        st.session_state.application_submitted = False
    st.title("Music School Management System")
    if manager.school_data["next_user_id"] == 1:
        st.header("Welcome to MSMS!")
        st.write("To create a new management system, you will need to create the first ADMIN.")
        name = st.text_input("Please enter your name.")
        password = st.text_input("Please enter your password.",type="password")
        confirm_password = st.text_input("Please confirm your password.",type="password")
        if st.button("Create Admin Account"):
            if not name or not password:
                st.error("Please enter your name and password.")
            elif not manager.valid_name(name):
                st.error("Invalid name.")
            elif password != confirm_password:
                st.error("The password is not same as the confirmation.")
            else:
                user = manager.add_admin(name, password)
                manager._save_data()
                st.session_state.user = user
                st.success("Create User succesfully")
                st.rerun()
        return
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "home"

    if st.session_state.auth_page == "home":
        st.write("Welcome to MSMS!")

        if st.button("Log In"):
            st.session_state.auth_page = "login"
            st.rerun()

        if st.button("Sign Up"):
            st.session_state.auth_page = "signup"
            st.rerun()
    elif st.session_state.auth_page == "signup":
        st.subheader("Sign Up")
        role = st.selectbox("Account Type", ["Student","Teacher (Application)"])
        if role == "Student":
            st.subheader("Register to be a new student")
            name = st.text_input("Please enter your name.")
            password = st.text_input("Please enter your password.",type="password")
            confirm_password = st.text_input("Please confirm your password.",type="password")
            if st.button("Create Account"):
                if not name or not password:
                    st.error("Please enter your name and password.")
                elif not manager.valid_name(name):
                    st.error("Invalid name.")
                elif password != confirm_password:
                    st.error("The password is not same as the confirmation.")
                else:
                    user = manager.add_student(name, password)
                    manager._save_data()
                    st.session_state.user = user
                    st.success("Register succesfully")
                    st.rerun()
        elif role == "Teacher (Application)":
            st.subheader("Apply to be a new teacher")
            name = st.text_input("Please enter your name.")
            speciality = st.selectbox("Please choose your speciality.",manager.school_data["instruments"])
            description = st.text_area("Please describe yourself.")
            password = st.text_input("Please enter your password.",type="password")
            confirm_password = st.text_input("Please confirm your password.",type="password")
            if st.button("Submit application."):
                if not name or not password:
                    st.error("Please enter your name and password.")
                elif not manager.valid_name(name):
                    st.error("Invalid name.")
                elif password != confirm_password:
                    st.error("The password is not same as the confirmation.")
                else:
                    manager.add_teacher_application(name, password, speciality, description)
                    manager._save_data()
                    st.success("Application submitted successfully!")
                    st.session_state.application_submitted = True
                    st.session_state.auth_page = "home"
                    st.rerun()
        left, middle, right = st.columns([1, 8, 1])

        with left:
            if st.button("Log In"):
                st.session_state.auth_page = "login"
                st.rerun()

        with right:
            if st.button("Quit"):
                st.session_state.auth_page = "home"
                st.rerun()

    elif st.session_state.auth_page == "login":

        st.subheader("Log In")
        role = st.selectbox("Account Type",["Admin", "Teacher", "Student"])
        term = st.text_input("Please enter your NAME or your ID")
        if st.button("Find your account"):
            if role == "Admin":
                result = manager.find_admin(term)
            elif role == "Teacher":
                result = manager.find_teacher(term)
            elif role == "Student":
                result = manager.find_student(term)

            if not result:
                st.error("User not found")
            else:
                st.session_state.login_results = result

        if "login_results" in st.session_state:
            results = st.session_state.login_results

            st.subheader("Matching Users")

            options = [
                f"ID: {user.id}           Name: {user.name}"
                for user in results
            ]

            selected = st.selectbox(
                "Select your account",
                options
            )

            selected_index = options.index(selected)

            user = results[selected_index]

            password = st.text_input(
                "Please enter your password.",
                type="password"
            )

            if st.button("Confirm Password"):
                if password == user.password:
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect password.")
                st.divider()

        left, middle, right = st.columns([1, 8, 1])

        with left:
            if st.button("Sign Up"):
                st.session_state.auth_page = "signup"
                st.rerun()

        with right:
            if st.button("Quit"):
                st.session_state.auth_page = "home"
                st.rerun()