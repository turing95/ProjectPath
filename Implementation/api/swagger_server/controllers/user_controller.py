import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

from swagger_server.models import Path

from path_recommender import user_predictions as up
from path_recommender import path_correlation as pc
from path_recommender.utils import path_to_png



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

    _, predictions=up.recommend(userId)
    
    suggestions=predictions.to_dict(orient='records')

    result = []
    for s in suggestions:
        image_url=path_to_png.plot_path_to_png(timezone = s['time_zone'])

        path = Path(
            path_id=s['pathId'],
            title=s['title'],
            image_url=image_url
        )
        result.append(path)


    return result

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
