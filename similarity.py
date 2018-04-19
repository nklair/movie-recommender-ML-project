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
		for user in merged:
			user_info = {}
			user_info["movie1"] = movie_dict[movie1][user]
			user_info["movie2"] = movie_dict[movie2][user]
			user_info["average"] = user_dict[user]["average"]

			same_user_info.append(user_info)
		
		#for user in movie_dict[movie1].keys():
		#	if user in movie_dict[movie2].keys():
		#		user_info = {}
		#		user_info["movie1"] = movie_dict[movie1][user]
		#		user_info["movie2"] = movie_dict[movie2][user]
		#		user_info["average"] = user_dict[user]["average"]
	
		#		same_user_info.append(user_info)
	
		#if len(same_user_info) >= 5:
		if len(same_user_info) >= 1:
			numerator = 0
			denom_part1 = 0
			denom_part2 = 0
			for user in same_user_info:
				numerator += (user["movie1"] - user["average"])*(user["movie2"] - user["average"])
				denom_part1 += (user["movie1"] - user["average"])*(user["movie1"] - user["average"])
				denom_part2 += (user["movie2"] - user["average"])*(user["movie2"] - user["average"])
	
			denom = pow(denom_part2, .5) * pow(denom_part1, .5)
	
			return float(numerator) / float(denom)
		else:
			return 0
	
	def threaded_similarity_matrix(self, start, end, movie_dict, user_dict):
		#print("thread started")
		movie_list = list(movie_dict.keys())
		for i in range(start, end):
			for j in range(i, len(movie_list)):
				print(i, j)
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

def pickle_open(filename):
	f = open(filename, "rb")
	return pickle.load(f)

if __name__ == "__main__":
	users = pickle_open("user_movie_ratings.pickle")
	movies = pickle_open("movie_user_ratings.pickle")
	sim_matrix = Sim_Matrix(movies)
	sim_matrix.create_similarity_matrix(movies, users)
	predicted_rating = weighted_sum(1932640, 14574, users, sim_matrix.similarity_dict)
	print("Predicted rating for user 1932640 and movie 14574 should be 2, it is: ")
	print(predicted_rating)
	#1932640,14574,2
