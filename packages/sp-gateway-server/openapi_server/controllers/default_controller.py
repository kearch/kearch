import connexion
import six

from openapi_server.models.connection_request_on_sp import ConnectionRequestOnSP  # noqa: E501
from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.summary import Summary  # noqa: E501
from openapi_server import util

import specialist_gateway


def add_a_conenction_request_post(connection_request_on_sp):  # noqa: E501
    """Add a connection request sent from meta server to specialist server.

     # noqa: E501

    :param connection_request_on_sp: A connection request.
    :type connection_request_on_sp: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        connection_request_on_sp = ConnectionRequestOnSP.from_dict(connexion.request.get_json())  # noqa: E501
        scheme = connection_request_on_sp.scheme()
        me_host = connection_request_on_sp.me_host()
        res = specialist_gateway.add_a_connection_request(scheme, me_host)
        return res


def delete_a_conenction_request_delete(me_host=None):  # noqa: E501
    """Delete a connection request sent from meta server to specialist server.

     # noqa: E501

    :param me_host: A meta host name of the connection request to delete.
    :type me_host: str

    :rtype: InlineResponse200
    """
    res = specialist_gateway.delete_a_conenction_request(me_host)
    return res


def get_a_summary_get(me_host=None):  # noqa: E501
    """Get summary of this specialist server.

     # noqa: E501

    :param me_host: A host name of the meta server.
    :type me_host: str

    :rtype: Summary
    """
    res = specialist_gateway.get_a_dump(me_host)
    return res


def retrieve_get(queries=None, max_urls=None):  # noqa: E501
    """Retrieve search results.

     # noqa: E501

    :param queries: Space-separated query words
    :type queries: str
    :param max_urls: Max number of URLs to retrive from specialist servers
    :type max_urls: int

    :rtype: List[Document]
    """
    res = specialist_gateway.retrieve(queries, max_urls)
    return res
