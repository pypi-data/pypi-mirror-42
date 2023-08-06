from directory_client_core.authentication import SessionSSOAuthenticator

from directory_api_client.base import AbstractAPIClient


class EnrolmentAPIClient(AbstractAPIClient):

    endpoints = {
        'enrolment': '/enrolment/',
        'trusted-code': '/trusted-code/{code}/',
        'claim-preverified-company': '/enrolment/claim-preverified/',

    }

    def send_form(self, form_data):
        return self.post(
            self.endpoints['enrolment'],
            data=form_data
        )

    def retrieve_trusted_source_signup_details(self, code):
        url = self.endpoints['trusted-code'].format(code=code)
        return self.get(url)

    def claim_prepeveried_company(self, sso_session_id, data):
        return self.post(
            self.endpoints['claim-preverified-company'],
            data=data,
            authenticator=SessionSSOAuthenticator(sso_session_id),
        )
