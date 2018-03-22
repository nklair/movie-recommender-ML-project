import pickle

def organize_data_by_file(filename, user_dict):
	with open(filename, "r") as file:
		current_movie = ""
		for line in file:
			#print(line.find(":"))
			if line.find(":") != -1:
				current_movie = line.rstrip().split(':')[0]
				print(current_movie)
			else:
				clean = line.rstrip().split(',')
				if not clean[0] in user_dict.keys():
					user_dict[clean[0]] = {}

				user_dict[clean[0]][current_movie] = int(clean[1])
def pickle_save(dict_to_save, filename):
	with open(filename, "wb") as f:
		pickle.dump(dict_to_save, f, pickle.HIGHEST_PROTOCOL)

def pickle_open(filename):
	with open(filename, "wb") as f:
		pickle.load(f)

if __name__ == "__main__":
	users = {}
	organize_data_by_file("./netflix-prize-data/combined_data_1.txt", users)
	organize_data_by_file("./netflix-prize-data/combined_data_2.txt", users)
	organize_data_by_file("./netflix-prize-data/combined_data_3.txt", users)
	organize_data_by_file("./netflix-prize-data/combined_data_4.txt", users)
	pickle_save(users, "user_movie_ratings.pickle")