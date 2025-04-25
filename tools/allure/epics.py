from enum import Enum


class AllureEpic(str, Enum):
    LMS = "LMS system"
    STUDENTS = "Student system"
    ADMINISTRATION = "Administration system"