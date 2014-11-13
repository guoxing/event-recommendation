import readGraph

G = readGraph.readGraph()

num_events = 0
num_users = 0
node = G.BegNI()
while node is not G.EndNI():
    try:
        if G.GetStrAttrDatN(node.GetId(), 'type') == 'event':
            num_events += 1
        if G.GetStrAttrDatN(node.GetId(), 'type') == 'user':
            num_users += 1
        node.Next()
    except Exception, e:
        print e
        break

num_event_user = 0
num_user_user = 0
edge = G.BegEI()
while edge != G.EndEI():
    try:
        snid = edge.GetSrcNId()
        dnid = edge.GetDstNId()
        if G.GetStrAttrDatN(snid, 'type') == G.GetStrAttrDatN(dnid, 'type'):
            num_user_user += 1
        else:
            num_event_user += 1
        edge.Next()
    except Exception, e:
        print e
        break

print '# event nodes:', num_events
print '# user nodes:', num_users
print '# user-user edges:', num_user_user / 2
print '# event-user edges:', num_event_user / 2
