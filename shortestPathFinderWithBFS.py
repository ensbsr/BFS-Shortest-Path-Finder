class Node(object):
	"""
	undeba
	Node object to create a graph with edges and nodes
	"""
	def __init__(self, i, j, isObstacle, left = None, right = None, up = None, down = None):
		"""
		Constructor for Node object.

		parameters:
			i: i index on a graph that represented as list of lists, type integer
			j: j index on a graph that represented as list of lists, type integer
			isObstacle: stores if a node is an obstacle or not, type boolean
			left: left neighbour of the a node, type Node object or None
			right: right neighbour of the a node, type Node object or None
			up: up neighbour of the a node, type Node object or None
			down: down neighbour of the a node, type Node object or None

		variables:
			path: stores the shortest path to current node from origin, type string
			count: stores number of nodes visited to get current node from origin within the shortest path, type integer
		"""
		self.coordinates = (i,j)
		self.isObstacle = True if isObstacle == 1 else False
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.path = ""
		self.count = 0

	
	def edgesTo(self):
		"""
		returns all neighbour nodes as list
		"""
		return [self.up,self.down,self.left,self.right]



def createGraph(node, n, m, G, visitedList):
	"""
	graph creator function

	parameters:
		node: node to explore, type node object
		n, m: size of graph G, type integer
		G: graph as form of list of lists, type list
		visitedList: visited node list to avoid re-visits, type list
	"""

	#take i and j of current node
	i, j = node.coordinates[0],node.coordinates[1]

	#update G with the node
	G[i][j] = node

	#add this node to visitedList
	visitedList.append((i,j))

	#look for up neighbour of current node
	if i>=1:
		#if its node is not created yet
		if type(G[i-1][j]) == type(1):
			#create a node object
			up = Node(i-1,j, G[i-1][j], down = G[i][j])

			#update the graph
			G[i-1][j] = up

		#if its node is created before
		else:
			#take the created node
			up = G[i-1][j]

			#update its down neighbour with current node with indices of i and j
			up.down = G[i][j]

	#if its not eligible to be a node within the coordinate range, define it as None
	else:
		up = None

	#look for down neighbour of current node
	if i<n-1:
		#if its node is not created yet
		if type(G[i+1][j]) == type(1):
			#create a node object
			down = Node(i+1,j, G[i+1][j], up = G[i][j])

			#update the graph
			G[i+1][j] = down

		#if its node is created before
		else:
			#take the created node
			down = G[i+1][j]

			#update its up neighbour with current node with indices of i and j
			down.up = G[i][j]
	
	#if its not eligible to be a node within the coordinate range, define it as None
	else:
		down = None

	#look for right neighbour of current node
	if j>=1:
		#if its node is not created yet
		if type(G[i][j-1]) == type(1):
			#create a node object
			left = Node(i,j-1, G[i][j-1], right = G[i][j])

			#update the graph
			G[i][j-1] = left

		#if its node is created before
		else:
			#take the created node
			left = G[i][j-1]

			#update its left neighbour with current node with indices of i and j
			left.right = G[i][j]

	#if its not eligible to be a node within the coordinate range, define it as None
	else:
		left = None

	#look for left neighbour of current node
	if j<m-1:
		#if its node is not created yet
		if type(G[i][j+1]) == type(1):
			#create a node object
			right = Node(i,j+1, G[i][j+1], left = G[i][j])

			#update the graph
			G[i][j+1] = right

		#if its node is created before
		else: 
			#take the created node
			right = G[i][j+1]

			#update its left neighbour with current node with indices of i and j
			right.left = G[i][j]

	#if its not eligible to be a node within the coordinate range, define it as None
	else:
		right = None

	#update current node's neighbours with created and taken nodes
	node.left, node.right, node.up, node.down = left, right, up, down

	#define list of neighbours
	edgesTo = [left, right, up, down]

	#for every node in neighbours list
	for nd in edgesTo:
		#if it's not None
		if nd is not None:
			#take it's coordinates
			nodei, nodej = nd.coordinates[0], nd.coordinates[1]

			#if it's not visited yet
			if (nodei, nodej) not in visitedList:
				#run function recursively for this node
				createGraph(nd, n, m, G, visitedList)

	#return origin node
	return node

def BFS(endCoordinate, visitingList, visitedList):
	"""
	Breadth First Search function to find shortest path.

	parameters:
		endCoordinate: destination coordinate as (i, j) format, type tuple
		visitingList: the list of nodes to be visited, type list
		visitedList: the list of nodes visited as (i, j) format, type list of tuples
	"""

	#pop the first element from visiting list which is a node
	start = visitingList.pop(0)
	
	#if the selected node's coordinates is same with the destination coordinates
	if start.coordinates == endCoordinate:
		#return the minimum step and path data of the node
		return "Minimum Steps: %s\nPath: %s" %(start.count,start.path[:-3])

	#for every node that is neighbour with selected node
	for n in start.edgesTo():

		#if it's not none, this means it's a Node object
		if n != None:
			#if this node is not visited before, so it's not in the visitedList, also if it's not an obstacle
			if n.coordinates not in visitedList and not n.isObstacle:
					#update it's path value with the parent node's path value + it's coordinates
					n.path = start.path + "%s -> " %str(n.coordinates)

					#update it's count value with the parent node's count value + 1
					n.count = start.count + 1

					#append it to visitingList which enables us to visit this node in the next layer
					visitingList.append(n)

	#add selected node to visitedList to avoid visiting this node again
	visitedList.append(start.coordinates)

	#if there is still other nodes to visit
	if len(visitingList) != 0: 
		#return BFS function recursively until get at destination
		return BFS(endCoordinate, visitingList, visitedList)

	#if there is no other nodes to visit
	else:
		#return that there is no solution
		return "Minimum Steps: 0\nPath: No Valid Path"



def find_shortest_path(G):
	"""
	shortest path finder for given graph G

	parameters:
		G: is a graph representation in the form of list of lists, type list
	"""

	#take sizes of G
	n = len(G)
	m = len(G[0])

	#create the initial node at (0, 0)(or any other) point
	node = Node(0,0, G[0][0])

	#update it's path with initial point of (0, 0)
	node.path = "(0, 0) -> "

	#constitute the graph on G variable with createGraph function and take the zeroNode(root node in this case)
	zeroNode = createGraph(node, n, m, G, [])

	#return result of the BFS
	return BFS((n-1,m-1),[zeroNode], [])


#define G, which is a list of list representation of a graph
G = [[0,1,0,1,0,0], [0,1,0,0,0,0], [0,0,0,0,1,0], [0,0,0,1,1,0]]

#print the result of find_shortest_path function with graph G
print find_shortest_path(G)