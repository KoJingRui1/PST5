# gui/main_dashboard.py
import streamlit as st

from app.schedule import ScheduleManager
from gui.default_page import show_default_page
from gui.admin_pages import show_admin_page
from gui.student_pages import show_student_page
from gui.teacher_pages import show_teacher_page

def launch():
    """Sets up the main Streamlit application and navigation."""

    st.set_page_config(
        layout="wide",
        page_title="Music School Management System"
    )

    # Create the manager only once
    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    # Default page
    if "user" not in st.session_state:
        show_default_page(manager)
        return

    # Get current user
    user = st.session_state.user

    # Show the correct page according to user type
    if user.__class__.__name__ == "AdminUser":
        show_admin_page(manager, user)

    elif user.__class__.__name__ == "StudentUser":
        show_student_page(manager, user)

    elif user.__class__.__name__ == "TeacherUser":
        show_teacher_page(manager, user)

    else:
        show_default_page(manager)