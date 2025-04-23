import pytest

from pages.dashboard.dashboard_page import DashboardPage
from pages.authentication.registration_page import RegistrationPage


@pytest.mark.regression
@pytest.mark.registration
class TestRegistration:
    def test_successful_registration(self, registration_page: RegistrationPage, dashboard_page: DashboardPage):
        registration_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")
        registration_page.check_registration_form_visible(email="", username="", password="")
        registration_page.fill_registration_form(email="user.name@gmail.com", username="username", password="password")
        registration_page.click_registration_button()
        dashboard_page.check_visible_dashboard_toolbar()
