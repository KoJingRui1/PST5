import streamlit as st

from app.schedule import ScheduleManager
from gui.default_page import show_default_page


def launch():
    st.set_page_config(
        layout="wide",
        page_title="Music School Management System"
    )

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    if "user" not in st.session_state:
        show_default_page(manager)
        return


if __name__ == "__main__":
    launch()