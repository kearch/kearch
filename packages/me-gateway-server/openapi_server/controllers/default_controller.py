import connexion
import six

from openapi_server.models.connection_request_on_me import ConnectionRequestOnME  # noqa: E501
from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from openapi_server.models.summary import Summary  # noqa: E501
from openapi_server import util

import meta_gateway


def add_a_conenction_request_post(connection_request_on_me):  # noqa: E501
    """Add a connection request sent from specialist server to meta server.

     # noqa: E501

    :param connection_request_on_me: A connection request.
    :type connection_request_on_me: dict | bytes

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        connection_request_on_me = ConnectionRequestOnME.from_dict(connexion.request.get_json())  # noqa: E501
        sp_host = connection_request_on_me.sp_host()
        scheme = connection_request_on_me.scheme()
        engine_name = connection_request_on_me.engine_name()
        res = meta_gateway.add_a_connection_request(sp_host, scheme,
                                                    engine_name)
        return res


def add_a_summary_post(summary):  # noqa: E501
    """Add a summary to meta server.

     # noqa: E501

    :param summary: A summary of the specialist server.
    :type summary: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        summary = Summary.from_dict(connexion.request.get_json())  # noqa: E501
        engine_name = summary.engine_name()
        sp_host = summary.sp_host()
        dump = summary.dump()
        res = meta_gateway.add_new_sp_server(sp_host, engine_name, dump)
        return res


def delete_a_conenction_request_delete(sp_host=None):  # noqa: E501
    """Delete a connection request sent from specialist server to this meta server.

     # noqa: E501

    :param sp_host: A specialist host name of the connection request to delete.
    :type sp_host: str

    :rtype: InlineResponse2001
    """
    res = meta_gateway.delete_a_conenction_request(sp_host)
    return res


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
    res = meta_gateway.retrieve(sp_host, queries, max_urls)
    return res
