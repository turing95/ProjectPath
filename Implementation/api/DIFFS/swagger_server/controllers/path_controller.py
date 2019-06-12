import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def get_related_paths(pathId, limit=None, offset=None):  # noqa: E501
    """Returns related paths

    Returns a collection of paths related to the given one # noqa: E501

    :param pathId: 
    :type pathId: int
    :param limit: 
    :type limit: int
    :param offset: 
    :type offset: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'
