def similarity(movie1, movie2, movie_dict, user_dict):
	same_user_info = []
	for user1 in movie_dict[movie1].keys():
		for user2 in movie_dict[movie2].keys():
			if user1 == user2:
				user_info = {}
				user_info["movie1"] = movie_dict[movie1][user1]
				user_info["movie2"] = movie_dict[movie2][user1]
				user_info["average"] = user_dict[user1]["average"]

				same_user_info.append(user_info)

	if len(same_user_info) >= THRESHOLD:
		numerator = 0
		denom_part1 = 0
		denom_part2 = 0
		for user in same_user_info:
			numerator += (user["movie1"] - user["average"])*(user["movie2"] - user["average"])
			denom_part1 += (user["movie1"] - user["average"])*(user["movie1"] - user["average"])
			denom_part2 += (user["movie2"] - user["average"])*(user["movie2"] - user["average"])

		denom = sqrt(denom_part2) * sqrt(denom_part1)

		return float(numerator) / float(denom)
	else:
		return 0

def similarity_matrix(movie_dict, user_dict):
	similarity_dict = {}
	movie_list = movie_dict.keys()
	for i in range(len(movie_list)):
		for j in range(i, len(movie_list)):
			sim = similarity(movie_list[i], movie_list[j], movie_dict, user_dict)
			if sim != 0:
				similarity_dict[movie_list[i]][movie_list[j]] = sim
				similarity_dict[movie_list[j]][movie_list[i]] = sim
	return similarity_dict

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
