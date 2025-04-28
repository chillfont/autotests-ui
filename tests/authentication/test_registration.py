import pytest
import allure

from config import settings
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from pages.dashboard.dashboard_page import DashboardPage
from pages.authentication.registration_page import RegistrationPage
from allure_commons.types import Severity

from tools.routes import AppRoute


@pytest.mark.regression
@pytest.mark.registration
@allure.tag(AllureTag.REGRESSION, AllureTag.REGISTRATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.story(AllureStory.REGISTRATION)
@allure.suite(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.sub_suite(AllureStory.REGISTRATION)
class TestRegistration:
    @allure.title('Registration with correct email, username and password')
    @allure.severity(Severity.CRITICAL)
    def test_successful_registration(self, registration_page: RegistrationPage, dashboard_page: DashboardPage):
        registration_page.visit(AppRoute.REGISTRATION)
        registration_page.check_registration_form_visible(email="", username="", password="")
        registration_page.fill_registration_form(
            email=settings.test_user.email,
            username=settings.test_user.username,
            password=settings.test_user.password
        )
        registration_page.click_registration_button()
        dashboard_page.check_visible_dashboard_toolbar()
