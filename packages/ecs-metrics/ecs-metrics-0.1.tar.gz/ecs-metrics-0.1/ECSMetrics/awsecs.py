import boto3
from operations import *

class ECS:

	def awsECS(self, profile, cpuwarn, memwarn, d,h,m):

		session=boto3.session.Session(profile_name=profile)
		
		obj2.listCluster(session)

		for ele in obj3.Cluster:
			print "CLUSTER IS -- ", (ele.split('/'))[1]

			del obj3.Service[:]
			obj2.listService(session, ele)
			for ele2 in obj3.Service:
				print "CLUSTER IS -- ", (ele.split('/'))[1]
				print "SERVICE IS -- ", (ele2.split('/')[1])

				del obj3.TaskD[:]
				obj2.describeService(session, ele, ele2)

				for ele3 in obj3.TaskD:
					del obj3.CPU[:]
					del obj3.MEMORY[:]
					obj2.describeTask(session, ele3)
					MaxCPU=max(obj3.CPU)
					MaxMEMORY=max(obj3.MEMORY)

					print "CPU Units - " ,MaxCPU
					print "MEMORY Units - " ,MaxMEMORY

				
				del obj3.Maxi[:]
				obj2.getMetricStatistics(session, 'CPUUtilization', ele, ele2, d,h,m) 
				obj2.getMetricStatistics(session, 'MemoryUtilization', ele, ele2, d,h,m) 


				print "CPU Utilization % - " ,obj3.Maxi[0]
				if obj3.Maxi[0]>cpuwarn:
					print ("WARNING: CPU Usage Exceeded")

				print "Memory Utilization % - " ,obj3.Maxi[1]
				if obj3.Maxi[1]>memwarn:
					print ("WARNING: Memory Usage Exceeded")

				
				print ('\n')
				print("----------------SERVICE COMPLETED---------------------")
				print ('\n')


			print("------------CLUSTER COMPLETED------------------")
			print('\n\n')

obj=ECS()