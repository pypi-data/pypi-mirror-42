"""Private Catalog API class file."""

from bits.google.services.base import Base
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession


class PrivateCatalog(Base):
    """PrivateCatalog class."""

    def __init__(self, credentials, api_key):
        """Initialize a class instance."""
        self.privatecatalog = build(
            'cloudprivatecatalog',
            'v1alpha1',
            credentials=credentials,
            discoveryServiceUrl='https://cloudprivatecatalog.googleapis.com/$discovery/rest?version=v1alpha1&key=%s' % (
                api_key
            )
        )

    def get_catalogs(self, resource):
        """Return a list of catalogs."""
        return self.privatecatalog.catalogs().list(resource=resource).execute()
