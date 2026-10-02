import streamlit as st

from app.schedule import ScheduleManager
from app.admin import AdminUser
from app.student import StudentUser
from app.teacher import TeacherUser
from gui.default_page import show_default_page
from gui.admin_pages import show_admin_page
from gui.student_pages import show_student_page
from gui.teacher_pages import show_teacher_page
def launch():
    st.set_page_config(
        layout="wide",
        page_title="Music School Management System"
    )

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    if "user" not in st.session_state or st.session_state.user is None:
        show_default_page(manager)
        return
    user = st.session_state.user

    if isinstance(user, AdminUser):
        show_admin_page(manager, user)
    if isinstance(user, StudentUser):
        show_student_page(manager, user)
    if isinstance(user, TeacherUser):
        show_teacher_page(manager, user)
if __name__ == "__main__":
    launch()