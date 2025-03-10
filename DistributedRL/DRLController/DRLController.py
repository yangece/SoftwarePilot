import subprocess
import os
import argparse
import time

DATA_LOC='/home/boubin/Images/'
CUBE_LOC='/home/boubin/SoftwarePilot/DistributedRL/Data/'

def consoleLog(string):
	print("#################################################")
	print("##############DRL Controller:")
	print(string)
	print("#################################################")

#Start HDFS
def startHDFS():
	consoleLog("DRL Controller Loading HDFS Containers")
	pwd = os.getcwd()
	os.chdir('../docker-hadoop')
	subprocess.call(['docker-compose','up', '-d'])
	os.chdir(pwd)
	consoleLog("HDFS Loaded")

#Start Servers
def startServers(numServs):
	serverList = []
	pwd = os.getcwd()
	os.chdir('../Gateway')
	for i in range(0, numServs):
		#subprocess.call(['docker', 'run', '--net=host', '-e SERVERNUM='+str(i),
		#		 '--name','server'+str(i), 'spcn', '/bin/bash'])
		subprocess.call(['bash','runGateway_Sim.sh', str(i),'server'+str(i)])
		consoleLog("Server" + str(i)+" Started")
		serverList.append("server"+str(i))
	os.chdir(pwd)
	return serverList

def startAggregators(numAgs):
    aggList = []
    pwd = os.getcwd()
    os.chdir('../Aggregator')
    for i in range(numAgs):
        models = '{:04b}'.format(i)
        subprocess.call(['bash', 'runAggregator_Sim.sh', models, 'Aggregator'+str(models)])
        consoleLog("Aggregator "+str(models)+" Started")
    os.chdir(pwd)
    return aggList
#Start workers and servers
def startWorkers(numServs, numWorkers):
	workerList = []
	pwd = os.getcwd()
	os.chdir('../Worker')
	for i in range(0, numServs):
		for j in range(0,numWorkers):
			#subprocess.call(['docker', 'run', '--net=host',
			#		 '-e SERVERNUM='+str(i),'-e WORKERNUM='+str(j),
			#		 '--name','worker'+str(i)+'_'+str(j),
			#		 '-v',CUBE_LOC+"Worker"+str(i)+'_'+str(j) + ':/home/mydata:Z',
			#		 '-v',DATA_LOC + ':/home/imageData:Z',
			#		 'spen', '/bin/bash', '-c \"bash run.sh\"'])
			subprocess.call(['bash','runWorker_Sim.sh',str(i), str(j),"worker"+str(i)+'_'+str(j)])
			consoleLog("Worker" + str(i)+'_'+str(j)+" Started")
			workerList.append("worker"+str(i)+'_'+str(j))
	os.chdir(pwd)
	return workerList

def startGlobal():
	pwd = os.getcwd()
	os.chdir("../Global")
	subprocess.call(['bash','runGlobal_Sim.sh',"global"])
	consoleLog("Global Started")

#start simulation

#Stop Servers
def stopServers(serverList):
	for server in serverList:
		subprocess.call(["docker", "rm", "-f", server])
		consoleLog("Server " + server + " Stopped")

#Stop Workers
def stopWorkers(workerList):
	for worker in workerList:
		subprocess.call(["docker", "rm", "-f", worker])
		consoleLog("Worker " + worker + " Stopped")

def stopGlobal():
	subprocess.call(["docker","rm","-f","global"])
	consoleLog("Global Stopped")

#kill HDFS
def killHDFS():
	consoleLog("Exiting Simulation")
	consoleLog("Killing HDFS")
	os.chdir('../docker-hadoop')
	subprocess.call(['docker-compose', 'down'])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Distributed RL Controller')
	#parser.add_argument('servers', metavar='S', type=int, nargs='+', help='Number of Server Nodes to Start')
	#parser.add_argument('workers', metavar='W', type=int, nargs='+', help='Number of Worker Nodes to Start per Server')
	#args = parser.parse_args()

	consoleLog("DRL Controller Starting")
	#Start HDFS Docker cluster
	consoleLog("Starting HDFS Cluster")

	#Currently Assuming HDFS instance runs independently of DRL Controller
	#startHDFS()

	consoleLog("Starting Global")
	startGlobal()
	consoleLog("Starting Aggregators")
	serverList = startAggregators(16)
	consoleLog("Starting Workers")
	workerList = startWorkers(2, 2)

	#Run Simulation
	#time.sleep(3600)

	#Stop Servers
	#consoleLog("Stopping Global")
	#stopGlobal()
	#consoleLog("Stopping Servers")
	#stopServers(serverList);
	#consoleLog("Stopping Workers")
	#stopWorkers(workerList)
	#consoleLog("Killing HDFS")
	#killHDFS();


