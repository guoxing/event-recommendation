import snap
user_index = {}

def getUserID(user):
	if user in user_index:
		return user_index[user]
	else:
		user_index[user] = len(user_index)
		return user_index[user] 



fp = open('/home/yilunw/Downloads/user_friends.csv', 'r')
network = snap.PUNGraph.New()

fp.readline()
for line in fp:
	user = getUserID(int(line.split(',')[0]))
	user_friends = line.split(',')[1].split(' ')
	if not network.IsNode(user):
		network.AddNode(user)
	for friend in user_friends:
		#print friend
		try:
			friend = getUserID(int(friend))
			if not network.IsNode(friend):
				network.AddNode(friend)
			network.AddEdge(user, friend)
		except Exception:
			print Exception

snap.SaveEdgeList(network, '/home/yilunw/EventNetwork')
print network.GetNodes()
print network.GetEdges()
snap.PlotInDegDistr(network, "Event Network", "Event Network Degree")

