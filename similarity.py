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


