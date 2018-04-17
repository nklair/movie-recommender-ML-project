# Functions to predict movie recommendations
def weighted_sum(user_id, movie_id, user_dict, similarity_matrix, similarity_threshhold=0.5):
	# Find all similar movies for that movie
	similar_movies = set()
	for other_movie_id in similarity_matrix[movie_id].keys():
		similarity = similarity_matrix[movie_id][other_movie_id]
		if similarity is not None and similarity > similarity_threshhold:
			similar_movies.add(other_movie_id)

	# Find all similar items which the user has rated
	user_rated_similar_movies = similar_movies & user_dict[user_id].keys()

	weighted_user_rating_sum = 0
	sum_of_similarities = 0
	for rated_movie_id in user_rated_similar_movies:
		similarity = similarity_matrix[movie_id][rated_movie]
		rating = user_dict[user_id][rated_movie]

		weighted_user_rating_sum += similarity * rating
		sum_of_similarities += abs(similarity)

	return weighted_user_rating_sum / sim_of_similarities
