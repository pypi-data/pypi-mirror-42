from directory_api_client.base import AbstractAPIClient


class EnrolmentAPIClient(AbstractAPIClient):

    endpoints = {
        'enrolment': '/enrolment/',
        'trusted-code': '/trusted-code/{code}/'
    }

    def send_form(self, form_data):
        return self.post(
            self.endpoints['enrolment'],
            data=form_data
        )

    def retrieve_trusted_source_signup_details(self, code):
        url = self.endpoints['trusted-code'].format(code=code)
        return self.get(url)
