import pytest
import allure

from config import settings
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from pages.courses.courses_list_page import CoursesListPage
from pages.courses.create_course_page import CreateCoursePage
from allure_commons.types import Severity

from tools.routes import AppRoute


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.COURSES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.story(AllureStory.COURSES)
@allure.suite(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.sub_suite(AllureStory.COURSES)
class TestCourses:
    @allure.title('Check displaying of empty courses list')
    @allure.severity(Severity.NORMAL)
    def test_empty_courses_list(self, courses_list_page: CoursesListPage):
        courses_list_page.visit(AppRoute.COURSES)

        courses_list_page.navbar.check_visible(settings.test_user.username)
        courses_list_page.sidebar.check_visible()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.check_visible_empty_view()

    @allure.title('Create course')
    @allure.severity(Severity.CRITICAL)
    def test_create_course(self, courses_list_page: CoursesListPage, create_course_page: CreateCoursePage):
        create_course_page.visit(AppRoute.CREATE_COURSE)

        # Проверяем страницу создания курса
        create_course_page.create_course_toolbar.check_visible()
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)
        create_course_page.check_visible_create_course_form(
            title="", estimated_time="", description="", max_score="0", min_score="0"
        )

        # Проверяем блоки создания заданий
        create_course_page.check_visible_exercises_title()
        create_course_page.check_visible_create_exercise_button()
        create_course_page.check_visible_exercises_empty_view()

        # Заполняем данные курса и создаем его
        create_course_page.image_upload_widget.upload_preview_image(settings.test_data.image_png_file)
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.fill_create_course_form(
            title="Playwright", estimated_time="2 weeks", description="Playwright", max_score="100", min_score="10"
        )
        create_course_page.click_create_course_button()

        # Проверяем данные созданного курса
        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            title="Playwright", index=0, max_score="100", min_score="10", estimated_time="2 weeks"
        )

    @allure.title('Edit course')
    @allure.severity(Severity.CRITICAL)
    def test_edit_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit(AppRoute.CREATE_COURSE)

        # Загружаем превью курса, заполняем форму создания курса валидными данными и нажимаем на кнопку создания курса
        create_course_page.image_upload_widget.upload_preview_image(settings.test_data.image_png_file)
        create_course_page.fill_create_course_form(
            title="Playwright", estimated_time="2 weeks", description="Playwright", max_score="100", min_score="10"
        )
        create_course_page.click_create_course_button()

        # Проверяем, что на странице Courses отображается карточка ранее созданного курса
        courses_list_page.course_view.check_visible(
            title="Playwright", index=0, max_score="100", min_score="10", estimated_time="2 weeks"
        )

        # Вызываем форму редактирования курса
        courses_list_page.course_view.menu.click_edit(index=0)

        # Изменяем значения в форме редактирования курса
        create_course_page.fill_create_course_form(
            title="Python", estimated_time="4 weeks", description="Python", max_score="200", min_score="20"
        )
        create_course_page.click_create_course_button()

        # Проверяем, что на странице Courses отображается курса с обновленными данными
        courses_list_page.course_view.check_visible(
            title="Python", index=0, max_score="200", min_score="20", estimated_time="4 weeks"
        )
