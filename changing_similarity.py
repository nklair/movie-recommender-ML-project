#!/opt/crc/p/python/3.6.4/gcc/bin/python3

import pickle
import similarity

for i in range(2, 9):
	users = similarity.pickle_open("../user_movie_ratings.pickle")
	sim_threshold = float(i)/10
	
	movies = {}
	training_folds = [1,2,3,4,5,6,7,8,9,10]
	for j in range(1, 11):
		del(training_folds[0])
		
		for k in training_folds:
			ratings = [line.rstrip('\n') for line in open('../folds/fold_'+str(k)+'.csv')]
			for rating in ratings:
				split_rating = rating.split(',')
				if split_rating[1] not in movies.keys():
					movies[split_rating[1]] = {}
				movies[split_rating[1]][split_rating[0]] = int(split_rating[2])
	
		sim_matrix = similarity.Sim_Matrix(movies)
		sim_matrix.set_dict_from_pickle("../matrix_pickles/matrix_fold_"+str(j)+".pickle")

		f = open("../results/fold_"+str(j)+"_sim_."+str(i)+"_results.csv", "w")
		test_data = [line.rstrip('\n') for line in open('../folds/fold_'+str(i)+'.csv')]
		for line in test_data:
			split_line = line.split(',')
			predicted_rating = similarity.weighted_sum(split_line[0], split_line[1], users, sim_matrix.similarity_dict)
		
			# user, movie, rating, prediction
			f.write("u{},m{},{},{}\n".format(split_line[1], split_line[0], split_line[2], predicted_rating))
		f.close()
	
		training_folds.append(i)

