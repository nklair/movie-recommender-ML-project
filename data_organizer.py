import pickle
import numpy

def organize_data_by_user(filename, user_dict):
	with open(filename, "r") as file:
		current_movie = ""
		for line in file:
			if line.find(":") != -1:
				current_movie = line.rstrip().split(':')[0]
			else:
				clean = line.rstrip().split(',')
				if not clean[0] in user_dict.keys():
					user_dict[clean[0]] = {}

				user_dict[clean[0]][current_movie] = int(clean[1])

def average_user_ratings(user_dict):
	for user in user_dict.keys():
		sum_rating = 0
		for movie in user_dict[user].keys():
			sum_rating += user_dict[user][movie]
		average_rating = float(sum_rating) / float(len(user_dict[user]))
		user_dict[user]["average"] = average_rating

def organize_data_by_movie(filename, movie_dict):
	with open(filename, "r") as file:
		current_movie = ""
		for line in file:
			if line.find(":") != -1:
				current_movie = line.rstrip().split(':')[0]
				movie_dict[current_movie] = {}
				#print(current_movie)
			else:
				clean = line.rstrip().split(',')
				movie_dict[current_movie][clean[0]] = int(clean[1])

def create_csv(filename):
	instance_list = []
	movies = pickle_open(filename)
	for movie in movies.keys():
		for user in movies[movie].keys():
			instance_list.append((int(user), int(movie), int(movies[movie][user])))
	return instance_list
	#instance_list = []
	#users = pickle_open(filename)
	#for user in users.keys():
	#	for movie in users[user].keys():
	#		instance_list.append((int(user), int(movie), int(users[user][movie])))
	#return instance_list

def save_shuffled_csv(filename, instance_list):
	numpy.random.shuffle(instance_list)
	with open(filename, "w") as f:
		i = 1
		for user, movie, rating in instance_list:
			#print(str(i)+" out of "+str(len(instance_list)))
			i += 1
			f.write(str(user) + "," + str(movie) + "," + str(rating) + '\n')

def pickle_save(dict_to_save, filename):
	#print("pickling")
	with open(filename, "wb") as f:
		pickle.dump(dict_to_save, f, pickle.HIGHEST_PROTOCOL)

def pickle_open(filename):
	f = open(filename, "rb")
	return pickle.load(f)

def pickle_by_user():
	users = {}
	organize_data_by_user("./netflix-prize-data/combined_data_1.txt", users)
	organize_data_by_user("./netflix-prize-data/combined_data_2.txt", users)
	organize_data_by_user("./netflix-prize-data/combined_data_3.txt", users)
	organize_data_by_user("./netflix-prize-data/combined_data_4.txt", users)
	average_user_ratings(users)
	pickle_save(users, "user_movie_ratings.pickle")

def pickle_by_movie():
	movies = {}
	organize_data_by_movie("./netflix-prize-data/combined_data_1.txt", movies)
	organize_data_by_movie("./netflix-prize-data/combined_data_2.txt", movies)
	organize_data_by_movie("./netflix-prize-data/combined_data_3.txt", movies)
	organize_data_by_movie("./netflix-prize-data/combined_data_4.txt", movies)
	pickle_save(movies, "movie_user_ratings.pickle")

def get_top_n(movies, n):
	movie_list = []
	for movie in movies:
		movie_list.append((len(movies[movie]), movie))
		
	movie_list.sort(key=lambda tup: tup[0], reverse=True)  # sorts in place
	
	new_dict = {}
	for i in range(n):
		new_dict[movie_list[i][1]] = movies[movie_list[i][1]]

	return new_dict

if __name__ == "__main__":
	
	#pickle_by_user()
	#pickle_by_movie()

	#movies = pickle_open("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/full_movie_user_ratings.pickle")
	#top_500 = get_top_n(movies, 500)
	#pickle_save(top_500, "/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/movie_user_ratings.pickle")
	#instance = create_csv("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/movie_user_ratings.pickle")
	#save_shuffled_csv("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/shuffled_user_data.csv", instance)

	# ****OLD**** instance = create_csv("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/user_movie_ratings.pickle")
	#instance = create_csv("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/movie_user_ratings.pickle")
	#save_shuffled_csv("/afs/crc.nd.edu/user/c/chiggin7/movie-recommender-ML-project/shuffled_user_data.csv", instance)


