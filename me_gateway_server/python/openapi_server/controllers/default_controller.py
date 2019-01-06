import connexion
import six

from openapi_server.models.connection_request_on_me import ConnectionRequestOnME  # noqa: E501
from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from openapi_server.models.summary import Summary  # noqa: E501
from openapi_server import util


def add_a_conenction_request_post(connection_request_on_me):  # noqa: E501
    """Add a connection request sent from specialist server to meta server.

     # noqa: E501

    :param connection_request_on_me: A connection request.
    :type connection_request_on_me: dict | bytes

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        connection_request_on_me = ConnectionRequestOnME.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_a_summary_post(summary):  # noqa: E501
    """Add a summary to meta server.

     # noqa: E501

    :param summary: A summary of the specialist server.
    :type summary: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        summary = Summary.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_a_conenction_request_delete(sp_host=None):  # noqa: E501
    """Delete a connection request sent from specialist server to this meta server.

     # noqa: E501

    :param sp_host: A specialist host name of the connection request to delete.
    :type sp_host: str

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def retrieve_get(queries=None, max_urls=None, sp_host=None):  # noqa: E501
    """Retrieve search results.

     # noqa: E501

    :param queries: Space-separated query words
    :type queries: str
    :param max_urls: Max number of URLs to retrive from specialist servers
    :type max_urls: int
    :param sp_host: A host name to retrieve results from.
    :type sp_host: str

    :rtype: List[Document]
    """
    return 'do some magic!'
