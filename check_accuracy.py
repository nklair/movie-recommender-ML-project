if __name__ == "__main__":
	total_correct = 0
	total_total = 0
	total_within_one = 0
	total_error = 0
	for i in range(1,11):
		lines = [line.rstrip('\n') for line in open("results/fold_"+str(i)+"_results.csv")]
		correct = 0
		within_one = 0
		total = 0
		sum_sq_error = 0 # this is (predicted - actual)**2
		error = 0
		for line in lines:
			split_line = line.split(',')
			predicted = float(split_line[3])
			rating = float(split_line[2])
				
			max_prediction = predicted + 0.5
			min_prediction = predicted - 0.5
			
			max_within_one = predicted + 1.5
			min_within_one = predicted - 1.5
	
			if rating < max_prediction and rating > min_prediction:
				correct += 1
			
			if rating < max_within_one and rating > min_within_one:
				within_one += 1
	
			total += 1
			
			error += predicted-rating
			sum_sq_error += (predicted-rating)**2
		
		total_correct += correct
		total_total += total
		total_within_one += within_one
		total_error += error
		print("Fold {} results:".format(i))
		print("\tcorrect = {}".format(correct))
		print("\twithin_one = {}".format(within_one))
		print("\ttotal = {}".format(total))
		print("\taccuracy = {}".format(float(correct)/float(total)))
		print("\twithin_one accuracy= {}".format(float(within_one)/float(total)))
		print("\tavg_error = {}".format(float(error)/float(total)))
		print("\tSSE = {}\n".format(sum_sq_error))

	print("Overall results:".format(i))
	print("\tcorrect = {}".format(total_correct))
	print("\twithin_one = {}".format(total_within_one))
	print("\ttotal = {}".format(total_total))
	print("\taccuracy = {}".format(float(total_correct)/float(total_total)))
	print("\twithin_one accuracy= {}".format(float(total_within_one)/float(total_total)))
	print("\tavg_error = {}".format(float(total_error)/float(total_total)))	
