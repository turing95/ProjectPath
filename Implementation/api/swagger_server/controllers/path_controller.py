import datetime
from datetime import timezone

import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util
from swagger_server.models import Path
from swagger_server.models import PathCoordinates

from path_recommender import user_predictions as up
from path_recommender import path_correlation as pc
from path_recommender.utils import path_to_png


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

    correlated_paths_dbf = pc.get_related_paths(pathId)

    correlated_paths = correlated_paths_dbf.to_dict(orient='record')

    response = []
    for cp in correlated_paths:
        image_url = path_to_png.plot_path_to_png(timezone=cp['time_zone'])
        print(cp['time_zone'])

        date_time_str = cp['time_zone']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        date_time_obj = date_time_obj.replace(tzinfo=timezone.utc).timestamp()

        path = Path(
            path_id=cp['pathId'],
            title=cp['path_title'],
            image_url=image_url,
            timestamp=date_time_str
        )
        response.append(path)

    return response
