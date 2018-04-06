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
				print(current_movie)
			else:
				clean = line.rstrip().split(',')
				movie_dict[current_movie][clean[0]] = int(clean[1])

def create_csv(filename, instance_list):
	users = pickle_open("./user_movie_ratings.pickle")
	for user in users.keys():
		for movie in users[user].keys():
			instance_list.append((int(user), int(movie), int(users[user][movie])))
def save_shuffled_csv(filename, instance_list):
	shuffled = numpy.random.shuffle(instance_list)
	with open(filename, "w") as f:
		i = 1
		for user, movie, rating in shuffled:
			print(str(i) + " out of " + str(len(shuffled)))
			i += 1
			f.write(str(user) + "," + str(movie) + "," + str(rating))
def pickle_save(dict_to_save, filename):
	print("pickling")
	with open(filename, "wb") as f:
		pickle.dump(dict_to_save, f, pickle.HIGHEST_PROTOCOL)

def pickle_open(filename):
	f = open(filename, "rb")
	return pickle.load(f)

if __name__ == "__main__":
	users = {}
	movies = {}
	#organize_data_by_user("./netflix-prize-data/combined_data_1.txt", users)
	#organize_data_by_user("./netflix-prize-data/combined_data_2.txt", users)
	#organize_data_by_user("./netflix-prize-data/combined_data_3.txt", users)
	#organize_data_by_user("./netflix-prize-data/combined_data_4.txt", users)
	#pickle_save(users, "user_movie_ratings.pickle")

	#organize_data_by_movie("./netflix-prize-data/combined_data_1.txt", movies)
	#organize_data_by_movie("./netflix-prize-data/combined_data_2.txt", movies)
	#organize_data_by_movie("./netflix-prize-data/combined_data_3.txt", movies)
	#organize_data_by_movie("./netflix-prize-data/combined_data_4.txt", movies)
	#pickle_save(movies, "movie_user_ratings.pickle")

	instance = []
	#create_csv("./netflix-prize-data/combined_data_1.txt", instance)
	#create_csv("./netflix-prize-data/combined_data_2.txt", instance)
	#create_csv("./netflix-prize-data/combined_data_3.txt", instance)
	#create_csv("./netflix-prize-data/combined_data_4.txt", instance)
	#save_shuffled_csv("shuffled_user_data.csv", instance)
