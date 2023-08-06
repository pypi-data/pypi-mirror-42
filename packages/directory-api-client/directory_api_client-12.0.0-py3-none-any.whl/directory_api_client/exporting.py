from directory_api_client.base import AbstractAPIClient


class ExportingAPIClient(AbstractAPIClient):

    endpoints = {
        'lookup-by-postcode': '/exporting/lookup-by-postcode/{postcode}/',
    }

    def lookup_regional_office_by_postcode(self, postcode):
        return self.get(
            url=self.endpoints['lookup-by-postcode'].format(postcode=postcode),
            use_fallback_cache=True,
        )
