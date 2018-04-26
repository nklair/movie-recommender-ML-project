import pickle
import threading

class Sim_Matrix:
	def __init__(self, movie_dict):
		self.similarity_dict = {}
		for movie in movie_dict.keys():
			self.similarity_dict[movie] = {}

	def similarity(self, movie1, movie2, movie_dict, user_dict):
		same_user_info = []
		l1 = list(movie_dict[movie1].keys())
		l2 = list(movie_dict[movie2].keys())
		merged = list(set(l1).intersection(l2))
		
		#if len(merged) >= 5:
		if len(merged) >= 1:
			for user in merged:
				user_info = {}
				user_info["movie1"] = movie_dict[movie1][user]
				user_info["movie2"] = movie_dict[movie2][user]
				user_info["average"] = user_dict[user]["average"]
				user_info["num_reviews"] = len(user_dict[user])

				same_user_info.append(user_info)
		
			numerator = 0
			denom_part1 = 0
			denom_part2 = 0
			for user in same_user_info:
				m1_metric = user["num_reviews"] * (user["movie1"] - user["average"])
				m2_metric = user["num_reviews"] * (user["movie2"] - user["average"])
				numerator += (m1_metric)*(m2_metric)
				denom_part1 += (m1_metric)*(m1_metric)
				denom_part2 += (m2_metric)*(m2_metric)
	
			denom = pow(denom_part2, .5) * pow(denom_part1, .5)
	
			return float(numerator) / float(denom)
		else:
			return 0
	
	def threaded_similarity_matrix(self, start, end, movie_dict, user_dict):
		#print("thread started")
		movie_list = list(movie_dict.keys())
		for i in range(start, end):
			for j in range(i, len(movie_list)):
				#print(i, j)
				sim = self.similarity(movie_list[i], movie_list[j], movie_dict, user_dict)
				if sim != 0:
					self.similarity_dict[movie_list[i]][movie_list[j]] = sim
					self.similarity_dict[movie_list[j]][movie_list[i]] = sim
		#print("thread ended")

	def create_similarity_matrix(self, movie_dict, user_dict):
		#print("create_similarity_matrix")
		splits = [0, 21, 43, 67, 91, 118, 146, 177, 211, 250, 295, 355, 500]
		#splits = [0, 757, 1549, 2382, 3263, 4200, 5206, 6301, 7512, 8886, 10516, 12640, 17770]
		threads = []
		for i in range(len(splits) - 1):
			threads.append(threading.Thread(target=self.threaded_similarity_matrix, args=(splits[i], splits[i+1], movie_dict, user_dict,)))
		
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()
		#print("all threads joined")
	
		try:
			pickle_save(self.similarity_dict, "../matrix_fold_10.pickle")
		except:
			pass
		
def weighted_sum(user_id, movie_id, user_dict, similarity_matrix, similarity_threshhold=0.5):
	
	# Find all similar movies for that movie
	similar_movies = []
	for other_movie_id in similarity_matrix[movie_id].keys():
		similarity = similarity_matrix[movie_id][other_movie_id]
		if similarity is not None and similarity > similarity_threshhold:
			similar_movies.append(other_movie_id)

	# Find all similar items which the user has rated
	user_movies = list(user_dict[user_id].keys())
	user_rated_similar_movies = list(set(similar_movies).intersection(user_movies))

	weighted_user_rating_sum = 0
	sum_of_similarities = 0
	for rated_movie_id in user_rated_similar_movies:
		similarity = similarity_matrix[movie_id][rated_movie_id]
		rating = user_dict[user_id][rated_movie_id]

		weighted_user_rating_sum += similarity * rating
		sum_of_similarities += abs(similarity)

	return weighted_user_rating_sum / sum_of_similarities

def pickle_save(dict_to_save, filename):
	with open(filename, "wb") as f:
		pickle.dump(dict_to_save, f, pickle.HIGHEST_PROTOCOL)

def pickle_open(filename):
	f = open(filename, "rb")
	return pickle.load(f)

if __name__ == "__main__":
	users = pickle_open("../user_movie_ratings.pickle")
	
	#movies = pickle_open("movie_user_ratings.pickle")
	movies = {}
	for i in range(9):
		ratings = [line.rstrip('\n') for line in open('../folds/fold_'+str(i)+'.csv')]
		for rating in ratings:
			split_rating = rating.split(',')
			if split_rating[1] not in movies.keys():
				movies[split_rating[1]] = {}
			movies[split_rating[1]][split_rating[0]] = int(split_rating[2])

	sim_matrix = Sim_Matrix(movies)
	sim_matrix.create_similarity_matrix(movies, users)

	f = open("../fold_10_results.txt", w)
	test_data = [line.rstrip('\n') for line in open('../folds/fold_9.csv')]
	for line in test_data:
		split_line = line.split(',')
		predicted_rating = weighted_sum(split_line[0], split_line[1], users, sim_matrix.similarity_dict)
		
		# user, movie, rating, prediction
		f.write("u{},m{},{},{}\n".format(split_line[1], split_line[0], split_line[2], predicted_rating))
	f.close()
