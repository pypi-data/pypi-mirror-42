import pytz
from datetime import *
from expdict import *


class Operations:


	def listCluster(self,session):
		ecs_client=session.client('ecs')

		ndict=ecs_client.list_clusters()  #List the clusters #fills Cluster list
		obj3.expdict(ndict)


	def listService(self,session, clust):
		ecs_client=session.client('ecs')

		ndict2=ecs_client.list_services(cluster=clust) #List the services #fills Cluster list
		obj3.expdict2(ndict2)


	def describeService(self,session, clust, serv): #adds in task definition
		ecs_client=session.client('ecs')

		ndict3=ecs_client.describe_services(cluster=clust,services=[serv]) #fills TaskDef for a particular service
		obj3.expdict3(ndict3)

	def describeTask(self, session, task):
		ecs_client=session.client('ecs')

		ndict4=ecs_client.describe_task_definition(taskDefinition=task) #Only 1 task definition in each service
		obj3.expdict4(ndict4)




	def getMetricStatistics(self,session, str, clust, serv, d,h,m): #delta in minutes
		cw_client=session.client('cloudwatch', region_name = 'ap-south-1')

		tz=pytz.timezone("Asia/Kolkata")

		ds=d*24*60*60
		hs=h*60*60
		ms=m*60
		peri=ds+hs+ms


		cl= (clust.split('/'))[1]
		se=(serv.split('/'))[1]

		ndict5=cw_client.get_metric_statistics(Namespace='AWS/ECS',MetricName=str,Dimensions=[{'Name':'ClusterName','Value':cl},{'Name':'ServiceName','Value':se}],StartTime=datetime.now(tz) - timedelta(days=d,hours=h,minutes=m),EndTime=datetime.now(tz),Period=peri, Statistics=['Maximum'])
		#print ndict5
		obj3.expdict5(ndict5)



obj2=Operations()