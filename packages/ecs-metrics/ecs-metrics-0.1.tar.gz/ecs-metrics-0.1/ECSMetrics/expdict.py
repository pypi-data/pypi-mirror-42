class Dict:

	def __init__(self):
		self.Cluster=[]
		self.Service=[]
		self.TaskD=[]
		self.CPU=[]
		self.MEMORY=[]
		self.Maxi=[]

	def expdict(self, ndict):
		nlist=ndict['clusterArns']
		self.explist(nlist)

	
	def explist(self, nlist):
		for ele in nlist:
			self.Cluster.append(ele)





	def expdict2(self, ndict2):
		nlist2=ndict2['serviceArns']
		self.explist2(nlist2)

	
	def explist2(self, nlist2):
		for ele in nlist2:
			self.Service.append(ele)






	def expdict3(self, ndict3):
		for ele in ndict3:
			if ele=='services':
				#print("FOUND1")
				self.explist3(ndict3[ele])
			if ele=='taskDefinition':
				#print("FOUND2")
				self.TaskD.append(ndict3[ele])

	
	def explist3(self, nlist3):
		for ele in nlist3:
			self.expdict3(ele)







	def expdict4(self, ndict4):
		for ele in ndict4:
			if ele=='taskDefinition':
				self.expdict4(ndict4[ele])
			if ele=='cpu':
				self.CPU.append(ndict4[ele])
			if ele=='memory':
				self.MEMORY.append(ndict4[ele])
			if ele=='containerDefinitions':
				self.explist4(ndict4[ele])

	
	def explist4(self, nlist4):
		for ele in nlist4: #will run for all the container definitions
			self.expdict4(ele)





	def expdict5(self, ndict5):
		for ele in ndict5:
			if ele=='Datapoints':
				self.explist5(ndict5[ele])
			if ele=='Maximum':
				self.Maxi.append(ndict5[ele])


	def explist5(self, nlist5):
		for ele in nlist5:
			self.expdict5(ele)


obj3=Dict()