# tests/test_schedule_manager.py
import sys
import os
import pytest
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.schedule import ScheduleManager
@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)
def test_add_student(fresh_manager):
    # ARRANGE
    # fresh_manager is provided by the fixture.

    # ACT
    student = fresh_manager.add_student("Test Student", "123456")

    # ASSERT
    assert student.name == "Test Student"
    assert student.password == "123456"
    assert student in fresh_manager.students
def test_add_admin(fresh_manager):
    # ARRANGE
    # fresh_manager is provided by the fixture.

    # ACT
    admin = fresh_manager.add_admin("Test Admin", "123456")

    # ASSERT
    assert admin.name == "Test Admin"
    assert admin.password == "123456"
    assert admin in fresh_manager.admins
def test_add_teacher(fresh_manager):
    # ARRANGE
    # fresh_manager is provided by the fixture.

    # ACT
    teacher = fresh_manager.add_teacher("Test Teacher", "123456", "piano", "Test description")

    # ASSERT
    assert teacher.name == "Test Teacher"
    assert teacher.password == "123456"
    assert teacher.speciality == "piano"
    assert teacher.description == "Test description"
    assert teacher in fresh_manager.teachers
def test_update_student(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    # ACT
    fresh_manager.update_user(
        student.id,
        name="Updated Student",
        password="654321"
    )

    # ASSERT
    assert student.name == "Updated Student"
    assert student.password == "654321"
def test_update_teacher(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Old description"
    )

    # ACT
    fresh_manager.update_user(
        teacher.id,
        name="Updated Teacher",
        password="654321",
        description="New description"
    )

    # ASSERT
    assert teacher.name == "Updated Teacher"
    assert teacher.password == "654321"
    assert teacher.description == "New description"
def test_update_admin(fresh_manager):
    # ARRANGE
    admin = fresh_manager.add_admin("Test Admin", "123456")

    # ACT
    fresh_manager.update_user(
        admin.id,
        name="Updated Admin",
        password="654321"
    )

    # ASSERT
    assert admin.name == "Updated Admin"
    assert admin.password == "654321"
def test_add_instrument(fresh_manager):
    # ARRANGE
    instrument = "Test instrument"

    # ACT
    fresh_manager.add_instrument(instrument)

    # ASSERT
    assert instrument in fresh_manager.school_data["instruments"]
def test_enrol_instrument(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    # ACT
    result = fresh_manager.enrol_instrument(student.id, "violin", 1)

    # ASSERT
    assert result is True
    assert student.grades["violin"] == 1
def test_disenroll_instrument(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")
    fresh_manager.enrol_instrument(student.id, "piano", 1)

    # ACT
    result = fresh_manager.disenroll_instrument(student.id, "piano")

    # ASSERT
    assert result is True
    assert "piano" not in student.grades
def test_update_enrollment(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")
    fresh_manager.enrol_instrument(student.id, "piano", 1)

    # ACT
    result = fresh_manager.update_enrollment(student.id, "piano", 2)

    # ASSERT
    assert result is True
    assert student.grades["piano"] == 2
def test_upgrade(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")
    fresh_manager.enrol_instrument(student.id, "piano", 1)

    # ACT
    fresh_manager.upgrade(student.id, "piano")

    # ASSERT
    assert student.grades["piano"] == 2
def test_enrol_course(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    fresh_manager.enrol_instrument(student.id, "piano", 1)

    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course_id = fresh_manager.courses[0].id

    # ACT
    fresh_manager.enrol_course(student.id, course_id, "1234")

    # ASSERT
    assert course_id in student.enrolled_course_ids
    assert student.id in fresh_manager.courses[0].enrolled_student_ids

def test_add_course(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    # ACT
    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    # ASSERT
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"
    assert fresh_manager.courses[0].teacher_id == teacher.id
    assert fresh_manager.courses[0].instrument == "piano"
    assert fresh_manager.courses[0].grade == 1
def test_delete_course(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course_id = fresh_manager.courses[0].id

    # ACT
    result = fresh_manager.remove_course(course_id)

    # ASSERT
    assert result is True
    assert len(fresh_manager.courses) == 0
def test_disenrol_course(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.enrol_instrument(student.id, "piano", 1)

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course_id = fresh_manager.courses[0].id

    fresh_manager.enrol_course(
        student.id,
        course_id,
        "1234"
    )

    # ACT
    result = fresh_manager.disenrol_course(student.id, course_id)

    # ASSERT
    assert result is True
    assert course_id not in student.enrolled_course_ids
    assert student.id not in fresh_manager.courses[0].enrolled_student_ids
def test_update_course(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Old description"
    )

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Old description",
        10
    )

    course = fresh_manager.courses[0]

    # ACT
    fresh_manager.update_course(
        course.id,
        name="Updated Piano",
        grade=2,
        description="New description",
        max_student=20
    )

    # ASSERT
    assert course.name == "Updated Piano"
    assert course.grade == 2
    assert course.description == "New description"
    assert course.max_student == 20
def test_add_lesson(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course = fresh_manager.courses[0]

    # ACT
    result = fresh_manager.add_lesson(
        course.id,
        "2026-10-20",
        "10:00",
        "Piano practice"
    )

    # ASSERT
    assert result is True
    assert len(course.lessons) == 1
    assert course.lessons[0]["date"] == "2026-10-20"
    assert course.lessons[0]["time"] == "10:00"
    assert course.lessons[0]["activity"] == "Piano practice"
def test_delete_lesson(fresh_manager):
    # ARRANGE
    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course = fresh_manager.courses[0]

    fresh_manager.add_lesson(
        course.id,
        "2026-10-20",
        "10:00",
        "Piano practice"
    )

    # ACT
    result = fresh_manager.delete_lesson(course.id, 0)

    # ASSERT
    assert result is True
    assert len(course.lessons) == 0
def test_record_payment_and_history(fresh_manager):
    pass
    # ARRANGE: Add a dummy student to the manager for the test.
    # This test verifies the core financial logic you added in Fragment 5.1.
    # fresh_manager.students.append(...)
    student_id_to_test = 1

    # ACT: Record a payment for that student.
    fresh_manager.record_payment(student_id_to_test, 100.00, "Credit Card")
    
    # ACT 2: Get the payment history.
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT: Check the results.
    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"
def test_give_attendance(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.enrol_instrument(student.id, "piano", 1)

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course = fresh_manager.courses[0]

    fresh_manager.enrol_course(
        student.id,
        course.id,
        "1234"
    )

    fresh_manager.add_lesson(
        course.id,
        "2026-10-20",
        "10:00",
        "Piano practice"
    )

    # ACT
    result = fresh_manager.give_attendance(
        student.id,
        course.id,
        1
    )

    # ASSERT
    assert result is True
    assert len(fresh_manager.attendance_log) == 1
    assert fresh_manager.attendance_log[0]["student_id"] == student.id
    assert fresh_manager.attendance_log[0]["course_id"] == course.id
    assert fresh_manager.attendance_log[0]["lesson_index"] == 1
def test_delete_attendance(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.enrol_instrument(student.id, "piano", 1)

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course = fresh_manager.courses[0]

    fresh_manager.enrol_course(
        student.id,
        course.id,
        "1234"
    )

    fresh_manager.add_lesson(
        course.id,
        "2026-10-20",
        "10:00",
        "Piano practice"
    )

    fresh_manager.give_attendance(
        student.id,
        course.id,
        1
    )

    # ACT
    result = fresh_manager.delete_attendance(
        student.id,
        course.id,
        1
    )

    # ASSERT
    assert result is True
    assert len(fresh_manager.attendance_log) == 0
def test_check_in(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student("Test Student", "123456")

    teacher = fresh_manager.add_teacher(
        "Test Teacher",
        "123456",
        "piano",
        "Test description"
    )

    fresh_manager.enrol_instrument(student.id, "piano", 1)

    fresh_manager.add_course(
        "Beginner Piano",
        teacher.id,
        1,
        "1234",
        "Test course",
        10
    )

    course = fresh_manager.courses[0]

    fresh_manager.enrol_course(
        student.id,
        course.id,
        "1234"
    )

    now = datetime.datetime.now()
    lesson_time = now - datetime.timedelta(minutes=30)

    fresh_manager.add_lesson(
        course.id,
        now.strftime("%Y-%m-%d"),
        lesson_time.strftime("%H:%M"),
        "Piano practice"
    )

    # ACT
    result = fresh_manager.check_in(
        student.id,
        course.id,
        1
    )

    # ASSERT
    assert result is True
    assert len(fresh_manager.attendance_log) == 1
    assert fresh_manager.attendance_log[0]["student_id"] == student.id
    assert fresh_manager.attendance_log[0]["course_id"] == course.id
    assert fresh_manager.attendance_log[0]["lesson_index"] == 1
def test_record_payment_and_history(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student(
        "Test Student",
        "123456"
    )

    # ACT
    result = fresh_manager.record_payment(
        student.id,
        100.00,
        "Credit Card"
    )

    history = fresh_manager.get_payment_history(student.id)

    # ASSERT
    assert result is True
    assert len(history) == 1
    assert history[0]["student_id"] == student.id
    assert history[0]["amount"] == 100.00
    assert history[0]["method"] == "Credit Card"
def test_get_payment_history_no_results(fresh_manager):
    # ARRANGE
    student = fresh_manager.add_student(
        "Test Student",
        "123456"
    )

    # ACT
    history = fresh_manager.get_payment_history(student.id)

    # ASSERT
    assert history == []