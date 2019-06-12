import os
import time
import gc
import argparse

# data science imports
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz


class KnnRecommender:
    """
    This is an item-based collaborative filtering recommender with
    KNN implmented by sklearn
    """
    def __init__(self, path_paths, path_ratings):
        """
        Recommender requires path to data: paths data and ratings data
        Parameters
        ----------
        path_paths: str, path data file path
        path_ratings: str, ratings data file path
        """
        self.path_paths = path_paths
        self.path_ratings = path_ratings
        self.path_rating_thres = 0
        self.user_rating_thres = 0
        self.model = NearestNeighbors()

    def set_filter_params(self, path_rating_thres, user_rating_thres):
        """
        set rating frequency threshold to filter less-known paths and
        less active users
        Parameters
        ----------
        paths_rating_thres: int, minimum number of ratings received by users
        user_rating_thres: int, minimum number of ratings a user gives
        """
        self.path_rating_thres = path_rating_thres
        self.user_rating_thres = user_rating_thres

    def set_model_params(self, n_neighbors, algorithm, metric, n_jobs=None):
        """
        set model params for sklearn.neighbors.NearestNeighbors
        Parameters
        ----------
        n_neighbors: int, optional (default = 5)
        algorithm: {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
        metric: string or callable, default 'minkowski', or one of
            ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']
        n_jobs: int or None, optional (default=None)
        """
        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _prep_data(self):
        """
        prepare data for recommender
        1. path-user scipy sparse matrix
        2. hashmap of path to row index in path-user scipy sparse matrix
        """
        # read data
        df_paths = pd.read_csv(
            os.path.join(self.path_paths),
            usecols=['id', 'time_zone'],
            dtype={'id': 'int32', 'time_zone': 'str'})
        df_rating = pd.read_csv(
            os.path.join(self.path_ratings),
            usecols=['user', 'path', 'rating'],
            dtype={'user': 'int32', 'path': 'int32', 'rating': 'float32'})
        df_ratings= df_rating.drop_duplicates(subset=['user', 'path'])
        # filter data
        df_path_cnt = pd.DataFrame(
            df_ratings.groupby('path').size(),
            columns=['count'])
        popular_paths = list(set(df_path_cnt.query('count >= @self.path_rating_thres').index))  # noqa
        paths_filter = df_ratings.path.isin(popular_paths).values

        df_users_cnt = pd.DataFrame(
            df_ratings.groupby('user').size(),
            columns=['count'])
        active_users = list(set(df_users_cnt.query('count >= @self.user_rating_thres').index))  # noqa
        users_filter = df_ratings.user.isin(active_users).values

        df_ratings_filtered = df_ratings[paths_filter & users_filter]

        # pivot and create path-user matrix
        path_user_mat = df_ratings_filtered.pivot(
            index='path', columns='user', values='rating').fillna(0)
        # create mapper from path title to index
        hashmap = {
            path: i for i, path in
            enumerate(list(df_paths.set_index('id').loc[path_user_mat.index].time_zone)) # noqa
        }
        # transform matrix to scipy sparse matrix
        path_user_mat_sparse = csr_matrix(path_user_mat.values)

        # clean up
        del df_paths, df_path_cnt, df_users_cnt
        del df_ratings, df_ratings_filtered, path_user_mat
        gc.collect()
        return path_user_mat_sparse, hashmap

    def _fuzzy_matching(self, hashmap, fav_path):
        """
        return the closest match via fuzzy ratio.
        If no match found, return None
        Parameters
        ----------
        hashmap: dict, map movie title name to index of the movie in data
        fav_movie: str, name of user input movie
        Return
        ------
        index of the closest match
        """
        match_tuple = []
        # get match
        for title, idx in hashmap.items():
            ratio = fuzz.ratio(title.lower(), fav_path.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
        else:
            print('Found possible matches in our database: '
                  '{0}\n'.format([x[0] for x in match_tuple]))
            return match_tuple[0][1]

    def _inference(self, model, data, hashmap,
                   fav_path, n_recommendations):
        """
        return top n similar movie recommendations based on user's input movie
        Parameters
        ----------
        model: sklearn model, knn model
        data: movie-user matrix
        hashmap: dict, map movie title name to index of the movie in data
        fav_movie: str, name of user input movie
        n_recommendations: int, top n recommendations
        Return
        ------
        list of top n similar movie recommendations
        """
        # fit
        model.fit(data)
        # get input movie index
        print('You have input movie:', fav_path)
        idx = self._fuzzy_matching(hashmap, fav_path)
        # inference
        print('Recommendation system start to make inference')
        print('......\n')
        t0 = time.time()
        distances, indices = model.kneighbors(
            data[idx],
            n_neighbors=n_recommendations+1)
        # get list of raw idx of recommendations
        raw_recommends = \
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                ),
                key=lambda x: x[1]
            )[:0:-1]
        print('It took my system {:.2f}s to make inference \n\
              '.format(time.time() - t0))
        # return recommendation (movieId, distance)
        return raw_recommends

    def make_recommendations(self, fav_path, n_recommendations):
        """
        make top n movie recommendations
        Parameters
        ----------
        fav_movie: str, name of user input movie
        n_recommendations: int, top n recommendations
        """
        # get data
        path_user_mat_sparse, hashmap = self._prep_data()
        # get recommendations
        raw_recommends = self._inference(
            self.model, path_user_mat_sparse, hashmap,
            fav_path, n_recommendations)
        # print results
        reverse_hashmap = {v: k for k, v in hashmap.items()}
        print('Recommendations for {}:'.format(fav_path))
        for i, (idx, dist) in enumerate(raw_recommends):
            print('{0}: {1}, with distance '
                  'of {2}'.format(i+1, reverse_hashmap[idx], dist))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Path Recommender",
        description="Run KNN path Recommender")
    parser.add_argument('--path', nargs='?', default=os.getcwd(),
                        help='input data path')
    parser.add_argument('--paths_filename', nargs='?', default='paths.csv',
                        help='provide paths filename')
    parser.add_argument('--ratings_filename', nargs='?', default='interactions.csv',
                        help='provide ratings filename')
    parser.add_argument('--path_name', nargs='?', default='',
                        help='provide your favorite path')
    parser.add_argument('--top_n', type=int, default=10,
                        help='top n path recommendations')
    return parser.parse_args()


if __name__ == '__main__':
    # get args
    args = parse_args()
    data_path = args.path
    paths_filename = args.paths_filename
    ratings_filename = args.ratings_filename
    path_name = args.path_name
    top_n = args.top_n
    # initial recommender system
    recommender = KnnRecommender(
        os.path.join(data_path, paths_filename),
        os.path.join(data_path, ratings_filename))
    # set params
    recommender.set_filter_params(50, 50)
    recommender.set_model_params(20, 'brute', 'cosine', -1)
    # make recommendations
recommender.make_recommendations(path_name, top_n)