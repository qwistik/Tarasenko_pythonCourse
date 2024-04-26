import requests
import json
from datetime import datetime, timedelta
import csv
from collections import defaultdict
from pprint import pprint



class MovieDataPreparation:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
        }
        self.movies = []
        self.fetch_data()

    def fetch_data(self):
        for page_num in range(1, self.num_pages + 1):
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page=" + str(
                page_num)
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                movies = response.json()['results']
                for movie in movies:
                    genres = self.get_genre_names(movie['genre_ids'])
                    movie['genre_names'] = genres
                self.movies.extend(movies)
            else:
                print(f"Failed to fetch data from page {page_num}")

    def get_genre_names(self, ids):
        url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
        response = requests.get(url, headers=self.headers)
        genre_names = []
        if response.status_code == 200:
            genre_data = response.json()
            genres = genre_data.get('genres', [])
            for id in ids:
                for genre in genres:
                    if genre['id'] == id:
                        genre_names.append(genre['name'].lower())
                        break
        return genre_names

    def get_all_data(self):
        return self.movies

    def get_movies_by_indexes(self, start, end, step):
        return self.movies[start:end+1:step]

    def get_most_popular_title(self):
        maximum = float('-inf')
        most_popular_movie = None
        for movie in self.movies:
            if movie['popularity'] > maximum:
                maximum = movie['popularity']
                most_popular_movie = movie['title']
        if most_popular_movie is not None:
            return most_popular_movie
        else:
            return 'Error'

    def get_titles_by_keyword(self, keyword):
        return [movie['title'] for movie in self.movies if keyword in movie['overview']]

    def get_unique_genres(self):
        genres = set()
        for movie in self.movies:
            genres.update(movie['genre_names'])
        return genres

    def delete_movies_by_genre(self, genre_id_or_name):
        if type(genre_id_or_name) == type(int) or type(genre_id_or_name) == type(float):
            self.movies = [movie for movie in self.movies if genre_id_or_name not in movie['genre_ids']]
        else:
            self.movies = [movie for movie in self.movies if genre_id_or_name.lower() not in movie['genre_names']]

    def get_popular_genres_with_counts(self):
        genre_counts = defaultdict(int)
        for movie in self.movies:
            for name in movie['genre_names']:
                genre_counts[name] += 1
        return genre_counts

    def get_movies_grouped_by_common_genres(self):
        grouped_movies = defaultdict(list)
        for movie in self.movies:
            key = tuple(sorted(movie['genre_names']))
            grouped_movies[key].append(movie['title'])
        return grouped_movies

    def replace_genre_id_in_data(self, new_genre_id):
        for movie in self.movies:
            movie['genre_ids'][0] = new_genre_id

    def get_movies_info_sorted(self):
        def last_day_in_cinema(release_date):
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
            last_day = release_date + timedelta(weeks=4 * 2 + 2 * 7)
            return last_day.strftime('%Y-%m-%d')

        sorted_movies = sorted(self.movies, key=lambda x: (int(x['vote_average']), x['popularity']), reverse=True)
        formatted_movies = []
        for movie in sorted_movies:
            formatted_movie = {
                'Title': movie['title'],
                'Popularity': round(movie['popularity'], 1),
                'Score': int(movie['vote_average']),
                'Last_day_in_cinema': last_day_in_cinema(movie['release_date'])
            }
            formatted_movies.append(formatted_movie)
        return formatted_movies

    def write_to_csv(self, file_path):
        movies_info = self.get_movies_info_sorted()
        keys = movies_info[0].keys() if movies_info else []
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for movie_info in movies_info:
                writer.writerow(movie_info)


# 1. Fetch the data from desired amount of pages
movie_prep = MovieDataPreparation(num_pages=1 )

# 2. Give a user all data
print("\n\nall")

pprint(movie_prep.get_all_data())

# 3. All data about movies with indexes from 3 till 19 with step 4
print("\n\nmovies with indexes from 3 till 19 with step 4")
pprint(movie_prep.get_movies_by_indexes(3, 19, 4))

# 4. Name of the most popular title
print("\n\nmost popular title")
pprint(movie_prep.get_most_popular_title())

# 5. Names of titles which has in description key words which a user put as parameters
print("\n\nby keyword")
pprint(movie_prep.get_titles_by_keyword('run'))

# 6. Unique collection of present genres
print("\n\nunique")
pprint(movie_prep.get_unique_genres())

# 7. Delete all movies with user provided genre
movie_prep.delete_movies_by_genre('action')
print("\n\nDeleted movies with genre Action")
print("\n\nunique")
pprint(movie_prep.get_unique_genres())

# 8. Names of most popular genres with numbers of time they appear in the data
print("\n\nPopular genres with counts:")
pprint(movie_prep.get_popular_genres_with_counts())

# 9. Collection of film titles grouped in pairs by common genres
print("\n\nMovies grouped by common genres:")
pprint(movie_prep.get_movies_grouped_by_common_genres())

# 10. Return initial data and copy of initial data where first id in list of film genres was replaced with 22
movie_prep.replace_genre_id_in_data(22)
print("\n\nReplaced genre ID with 22")

# 11. Collection of structures with part of initial data
print("\n\nSorted movies info:")
pprint(movie_prep.get_movies_info_sorted())

# 12. Write information to a CSV file
movie_prep.write_to_csv("movies_info.csv")
print("\n\nWrote information to CSV file")
