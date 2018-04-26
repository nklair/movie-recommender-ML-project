if __name__== "__main__":
	ratings = [line.rstrip('\n') for line in open('shuffled_user_data.csv')]

	l = len(ratings)
	for i in range(10):
		f = open("fold_"+str(i)+".csv","w") 
		for i in range(int(l*i/10), int(l*(i+1)/10)):
			f.write(ratings[i] + "\n")
		f.close()
