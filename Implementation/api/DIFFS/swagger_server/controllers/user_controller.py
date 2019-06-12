import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def get_suggested_paths(userId, limit=None, offset=None):  # noqa: E501
    """Get suggested paths

    Get a set of suggested paths for the current user # noqa: E501

    :param userId: 
    :type userId: int
    :param limit: 
    :type limit: int
    :param offset: 
    :type offset: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def user_get_friends(userId, limit=None, offset=None):  # noqa: E501
    """Get user&#39;s friends

    Get all the friends of a given user # noqa: E501

    :param userId: 
    :type userId: int
    :param limit: 
    :type limit: int
    :param offset: 
    :type offset: int

    :rtype: List[User]
    """
    return 'do some magic!'
