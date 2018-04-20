import numpy as np
import itertools
import json

class Utils():
	
	def __init__(self):
		self.supportVectorList = [[1,1,1], [-1,1,1], [-1,-1,1], [1,-1,1], [1,1,-1], [-1,1,-1], [-1,-1,-1], [1,-1,-1],]
		self.complexGlobal = []

		simple_voxels_set_json = open('simple_voxels_set.json')
		simple_voxels_set_json_str = simple_voxels_set_json.read()
		self.simple_voxels_set = eval(json.loads(simple_voxels_set_json_str)['data'])

		# maskForAllNeighbours_set_json = open('maskForAllNeighbours_set.json')
		# maskForAllNeighbours_set_json_str = maskForAllNeighbours_set_json.read()
		# self.maskForAllNeighbours_set = eval(json.loads(maskForAllNeighbours_set_json_str)['data'])

		# isConnected_set_json = open('isConnected_set.json')
		# isConnected_set_json_str = isConnected_set_json.read()
		# self.isConnected_set = eval(json.loads(isConnected_set_json_str)['data'])

		# essentialCliques_set_json = open('essentialCliques_set.json')
		# essentialCliques_set_json_str = essentialCliques_set_json.read()
		# self.essentialCliques_set = eval(json.loads(essentialCliques_set_json_str)['data'])

		isReducible_set_json = open('isReducible_set.json')
		isReducible_set_json_str = isReducible_set_json.read()
		self.isReducible_set = eval(json.loads(isReducible_set_json_str)['data'])

	# Given a list of centres as tuples, generate the vertices for all the voxels.
	def generateVerticesForCentres(self, voxelCentreList, edgeLength=1):

		vertexListForAllCentres = []

		for centre in voxelCentreList:
		
			vertexListForOneCentre = []
			c = np.array(centre)
			
			for supportVector in self.supportVectorList:
		
				s = np.array(supportVector)
				singleVertexArray = c + (edgeLength/2.0)*s
				singleVertexList = tuple(singleVertexArray)
				vertexListForOneCentre.append(singleVertexList)

			vertexListForAllCentres.append(vertexListForOneCentre)

		return vertexListForAllCentres

	def generateCornerVertices(self, voxelCentreList, edgeLength=1):

		vertexListForAllCentres = []

		for centre in voxelCentreList:
		
			vertexListForOneCentre = {}
			vertexListForOneCentre['min'] = tuple(np.subtract(centre, (0.5, 0.5, 0.5)))
			vertexListForOneCentre['max'] = tuple(np.add(centre, (0.5, 0.5, 0.5)))
			

			vertexListForAllCentres.append(vertexListForOneCentre)

		return vertexListForAllCentres

	def build_voxel_data(self, voxelCentreList):
		temp_complex = list(voxelCentreList)
		voxel_data = {}
		for voxel in temp_complex:
			if voxel[0] not in voxel_data:
				voxel_data[voxel[0]] = {}
			if voxel[1] not in voxel_data[voxel[0]]:
				voxel_data[voxel[0]][voxel[1]] = {}
			if voxel[2] not in voxel_data[voxel[0]][voxel[1]]:
				voxel_data[voxel[0]][voxel[1]][voxel[2]] = 1
		return voxel_data

	def is_border_voxel(self, voxel, voxelCentreList):
		temp_complex = list(voxelCentreList)
		if len(self.findAll2AdjacentVoxelsForGivenVoxel(voxel, temp_complex)) == 6:
			return False
		else:
			return True

	def is_end_voxel(self, voxel, voxel_centre_list):
		temp_complex = list(voxel_centre_list)
		if len(self.findAll2AdjacentVoxelsForGivenVoxel(voxel, temp_complex)) == 1:
			return True
		else:
			return False

	def least_connected_simple(self, border_list, voxel_centre_list):
		temp_complex = list(voxel_centre_list)
		temp_border_list = list(border_list)
		simple_list = []
		for border_voxel in temp_border_list:
			if self.is_simple_voxel(border_voxel, temp_complex):
				simple_list.append(border_voxel)
		min = 25
		vox = []
		for simple_voxel in simple_list:
			neighb_len = len(self.getNeighboursForGivenVoxel(simple_voxel, temp_complex))
			if neighb_len < min:
				min = neighb_len
				vox = [simple_voxel]
			elif neighb_len == min:
				vox.append(simple_voxel)

		return vox

	def is_simple_voxel(self, voxel, voxelCentreList):
		# print 'entered is_simple_voxel'
		temp_complex = list(voxelCentreList)

		if len(voxelCentreList) == 1:
			return True

		adj_voxels = self.findAll2AdjacentVoxelsForGivenVoxel(voxel, temp_complex)
		if len(adj_voxels) == 6:
			return False
		elif len(adj_voxels) == 4:
			if self.matches_temp(voxel, adj_voxels):
				return False


		if self.is_connected(self.getNeighboursForGivenVoxel(voxel, temp_complex)):
			return True
		return False

	def matches_temp(self, voxel, adj_voxels):
		li1 = [(voxel[0]+1,voxel[1],voxel[2]),(voxel[0]-1,voxel[1],voxel[2]),(voxel[0],voxel[1]+1,voxel[2]),(voxel[0],voxel[1]-1,voxel[2])]
		li2 = [(voxel[0]+1,voxel[1],voxel[2]),(voxel[0]-1,voxel[1],voxel[2]),(voxel[0],voxel[1],voxel[2]+1),(voxel[0],voxel[1],voxel[2]-1)]
		li3 = [(voxel[0],voxel[1]+1,voxel[2]),(voxel[0],voxel[1]-1,voxel[2]),(voxel[0],voxel[1],voxel[2]+1),(voxel[0],voxel[1],voxel[2]-1)]

		if set(li1) == set(adj_voxels) or set(li2) == set(adj_voxels) or set(li3) == set(adj_voxels):
			return True
		else:
			return False

	def is_simplifier_voxel(self, border_voxel, voxel_centre_list):
		print 'entered is_simplifier_voxel'
		neighbours = self.getNeighboursForGivenVoxel(border_voxel, voxel_centre_list)
		non_simple_neighbours = []
		for neighbour in neighbours:
			if not self.is_simple_voxel(neighbour, voxel_centre_list):
				non_simple_neighbours.append(neighbour)
		temp_complex = list(voxel_centre_list)
		temp_complex.remove(border_voxel)
		for neighbour in non_simple_neighbours:
			if self.is_simple_voxel(neighbour,temp_complex):
				return True
		return False

	def all_neighbours_boundary(self, border_voxel, voxel_data, voxel_centre_list):
		neighbours = self.getNeighboursForGivenVoxel(border_voxel, voxel_centre_list)
		for neighbour in neighbours:
			if voxel_data[neighbour[0]][neighbour[1]][neighbour[2]] == 1 or voxel_data[neighbour[0]][neighbour[1]][neighbour[2]] == 0:
				return False
		return True

	def buildObjFile(self, voxelCentreList, filename):

		s = 0
		list_for_print_voxel = []
		list_for_print_faces = []
		for voxel in voxelCentreList:
			# print voxel

			i = voxel[0]
			j = voxel[1]
			k = voxel[2]
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j+1,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i,j+1,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j,k+1)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j+1,k)));
			list_for_print_voxel.append( ("v %d %d %d\n" %(i+1,j+1,k+1)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+4,s+2,s+6)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+6,s+5,s+7)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+8,s+7,s+3,s+4)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+4,s+3,s+1,s+2)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+1,s+3,s+7,s+5)));
			list_for_print_faces.append( ("f %ld %ld %ld %ld\n" %(s+2,s+1,s+5,s+6)));
			s+=8;

		file = open('./visualize/'+filename+'.obj', 'w+')

		file.write("#"+filename+'.obj')
		file.write("\n")
		file.write("g "+filename)
		file.write("\n")
		for vertex in list_for_print_voxel:
			file.write("%s" % vertex)
		file.write("\n")

		for face in list_for_print_faces:
			file.write("%s\n" % face)

		file.close()

	def updateAllLookupFiles(self):
		f = open('simple_voxels_set.json', "w")
		data = json.dumps({'data':str(self.simple_voxels_set)})
		f.write(data)
		f.close()

		f = open('isCritical_voxel_set.json', "w")
		data = json.dumps({'data':str(self.isCritical_voxel_set)})
		f.write(data)
		f.close()

		# f = open('isReducible_set.json', "w")
		# data = json.dumps({'data':str(self.isReducible_set)})
		# f.write(data)
		# f.close()

		f = open('kCriticalCliques_set.json', "w")
		data = json.dumps({'data':str(self.kCriticalCliques_set)})
		f.write(data)
		f.close()

		f = open('criticalCliques_set.json', "w")
		data = json.dumps({'data':str(self.criticalCliques_set)})
		f.write(data)
		f.close()

		f = open('essentialCliques_set.json', "w")
		data = json.dumps({'data':str(self.essentialCliques_set)})
		f.write(data)
		f.close()

		f = open('maskForAllNeighbours_set.json', "w")
		data = json.dumps({'data':str(self.maskForAllNeighbours_set)})
		f.write(data)
		f.close()

		f = open('isConnected_set.json', "w")
		data = json.dumps({'data':str(self.isConnected_set)})
		f.write(data)
		f.close()

	def clearAllLookupFiles(self):
		f = open('simple_voxels_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('isCritical_voxel_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('isReducible_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('kCriticalCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('criticalCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		f = open('essentialCliques_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		# f = open('maskForAllNeighbours_set.json', "w")
		# data = json.dumps({'data':"{}"})
		# f.write(data)
		# f.close()

		f = open('isConnected_set.json', "w")
		data = json.dumps({'data':"{}"})
		f.write(data)
		f.close()

		self.simple_voxels_set = {}
		self.isCritical_voxel_set = {}
		self.maskForAllNeighbours_set = {}
		self.isConnected_set = {}
		self.essentialCliques_set = {}
		self.criticalCliques_set = {}
		self.kCriticalCliques_set = {}

	def getSimpleVoxels(self, voxelCentreList):
		# print "complex", voxelCentreList
		print "entering getSimpleVoxels"
		if frozenset(voxelCentreList) in self.simple_voxels_set:
			# print "leaving getSimpleVoxels"
			return self.simple_voxels_set[frozenset(voxelCentreList)]
		simple_voxels = []
		for voxel in voxelCentreList:
			temp = list(voxelCentreList)
			if self.isReducible(self.getNeighboursForGivenVoxel(voxel, temp)):
				simple_voxels.append(voxel)
		simple_voxels.sort()
		simple_voxels = list(simple_voxels for simple_voxels,_ in itertools.groupby(simple_voxels))
		self.simple_voxels_set[frozenset(voxelCentreList)] = simple_voxels
		# f = open('simple_voxels_set.json', "w")
		# data = json.dumps({'data':str(simple_voxels)})
		# f.write(data)
		# f.close()
		print "leaving getSimpleVoxels"
		print "simple_voxels",simple_voxels
		return simple_voxels

	def isZeroSurface(self, voxelCentreList):
		if not len(voxelCentreList)==2:
			return False
		if self.isConnected(voxelCentreList):
			return False

		return True

	def isOneSurface(self, voxelCentreList):
		
		if not self.isConnected(voxelCentreList) or len(voxelCentreList)==0:
			return False
		for voxel in voxelCentreList:
			if not self.isZeroSurface(self.getNeighboursForGivenVoxel(voxel, voxelCentreList)):
				return False
		return True

	def isReducible(self, voxelCentreList):
		# print 'entered isReducible'
		# if frozenset(voxelCentreList) in self.isReducible_set:
		# 	return self.isReducible_set[frozenset(voxelCentreList)]
		# print "isReducible voxelCentreList",voxelCentreList
		if len(voxelCentreList) == 1:
			# self.isReducible_set[frozenset(voxelCentreList)] = True
			# f = open('isReducible_set.json', "w")
			# data = json.dumps({'data':str(self.isReducible_set)})
			# f.write(data)
			# f.close()
			return True
		for voxel in voxelCentreList:
			# print "voxel in isReducible", voxel
			temp = list(voxelCentreList)
			temp.remove(voxel)
			isNeighboursReducible = self.isReducible(self.getNeighboursForGivenVoxel(voxel, voxelCentreList))
			isOthersReducible = self.isReducible(temp)
			# print "isNeighboursReducible",isNeighboursReducible, "isOthersReducible",isOthersReducible
			if isNeighboursReducible and isOthersReducible:
				# self.isReducible_set[frozenset(voxelCentreList)] = True
				# f = open('isReducible_set.json', "w")
				# data = json.dumps({'data':str(self.isReducible_set)})
				# f.write(data)
				# f.close()
				return True
			# self.isReducible_set[frozenset(voxelCentreList)] = False
			# f = open('isReducible_set.json', "w")
			# data = json.dumps({'data':str(self.isReducible_set)})
			# f.write(data)
			# f.close()
		return False

	def getNeighboursForGivenVoxel(self, centre, voxelCentreList, edgeLength = 1):
		# print "getNeighboursForGivenVoxel centre",centre
		listOfAdjacentVoxels = self.maskForAllNeighbours(centre)
		final_list = []
		final_list = list(set(voxelCentreList).intersection(set(listOfAdjacentVoxels)))
		return final_list

	def findAllAdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):
		print "entering findAllAdjacentVoxelsForGivenVoxel"
		# print "centre in findAllAdjacentVoxelsForGivenVoxel", centre
		listOf2AdjacentVoxels = self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf1AdjacentVoxels = self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		listOf0AdjacentVoxels = self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)
		print "leaving findAllAdjacentVoxelsForGivenVoxel"
		return [listOf2AdjacentVoxels, listOf1AdjacentVoxels, listOf0AdjacentVoxels]

	# Find all the voxels centres that are 2-adjacent to the the given voxel.
	def findAll2AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength=1):
		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf2AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is2Adjacent(centre, voxelCentre, edgeLength):
				listOf2AdjacentVoxels.append(voxelCentre)
		if flag:
			voxelCentreList.append(centre)
		return listOf2AdjacentVoxels

	# Find all the voxels centres that are 1-adjacent to the the given voxel.
	def findAll1AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):

		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf1AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is1Adjacent(centre, voxelCentre, edgeLength):
				listOf1AdjacentVoxels.append(voxelCentre)

		if flag:
			voxelCentreList.append(centre)

		return listOf1AdjacentVoxels
			
	# Find all the voxels centres that are 2-adjacent to the the given voxel.
	def findAll0AdjacentVoxelsForGivenVoxel(self, centre, voxelCentreList, edgeLength):

		flag = False
		# Remove the voxel for whom the neighbours needs to be found, from the complex.
		try:
			voxelCentreList.remove(centre)
			flag = True
		except:
			pass

		listOf0AdjacentVoxels = []

		for voxelCentre in voxelCentreList:
			if self.is0Adjacent(centre, voxelCentre, edgeLength):
				listOf0AdjacentVoxels.append(voxelCentre)

		if flag:
			voxelCentreList.append(centre)

		return listOf0AdjacentVoxels

	# def extractEssential(self):
	# 	pass

	# def isRegular():
	# 	pass

	# def isCritical():
	# 	pass

	def process_output(self, complex):
		return self.processThinning(complex)

	# Given two voxel centres, find if they are 2-adjacent or not.
	def is2Adjacent(self, centre1, centre2, edgeLength):

		centre1 = list(centre1)
		centre2 = list(centre2)
		c1 = np.array(centre1)
		c2 = np.array(centre2)
		# print c1,c2
		distanceBetweenCentres = np.linalg.norm(c1-c2)

		if self.isClose(edgeLength, distanceBetweenCentres):
			return True

		return False

	# Given two voxel centres, find if they are 1-adjacent or not.
	def is1Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(list(centre1))
		c2 = np.array(list(centre2))

		distanceBetweenCentres = np.linalg.norm(c1-c2)
		
		centreToEdge = self.centreToEdgeDistance(edgeLength)
		
		if self.isClose(centreToEdge, distanceBetweenCentres/2.0):
			return True

		return False

	# Given two voxel centres, find if they are 0-adjacent or not.
	def is0Adjacent(self, centre1, centre2, edgeLength):

		c1 = np.array(list(centre1))
		c2 = np.array(list(centre2))

		distanceBetweenCentres = np.linalg.norm(c1-c2)

		centreToCorner = self.centreToCornerDistance(edgeLength)

		if self.isClose(centreToCorner, distanceBetweenCentres/2.0):
			return True

		return False

	# Given the edge length of a voxel, calculate the shortest distance from the centre of a voxel to the edge.
	def centreToEdgeDistance(self, edgeLength):

		return edgeLength/np.sqrt(2.0)

	# Given the edge length of a voxel, calculate the distance from the centre of a voxel to a corner.
	def centreToCornerDistance(self, edgeLength):
		
		return (edgeLength/2.0)*np.sqrt(3.0)

	# Check if the given complex is connected or not
	# def isConnected(self, voxelCentreList, edgeLength=1):
	# 	if len(voxelCentreList) == 1:
	# 		return True
	# 	for centre in voxelCentreList:
	# 		if self.findAll2AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll1AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[] and self.findAll0AdjacentVoxelsForGivenVoxel(centre, voxelCentreList, edgeLength)==[]:
	# 			return False
	# 	return True

	# def isConnected(self, voxelCentreList, edgeLength=1):
	# 	if frozenset(voxelCentreList) in self.isConnected_set:
	# 		return self.isConnected_set[frozenset(voxelCentreList)]
	# 	if len(voxelCentreList) == 1:
	# 		self.isConnected_set[frozenset(voxelCentreList)] = True
	# 		# f = open('isConnected_set.json', "w")
	# 		# data = json.dumps({'data':str(self.isConnected_set)})
	# 		# f.write(data)
	# 		# f.close()
	# 		return True
	# 	for centre in voxelCentreList:
	# 		if list(set(self.maskForAllNeighbours(centre)).intersection(set(voxelCentreList)))==[]:
	# 			self.isConnected_set[frozenset(voxelCentreList)] = False
	# 			# f = open('isConnected_set.json', "w")
	# 			# data = json.dumps({'data':str(self.isConnected_set)})
	# 			# f.write(data)
	# 			# f.close()
	# 			return False
	# 	self.isConnected_set[frozenset(voxelCentreList)] = True
	# 	# f = open('isConnected_set.json', "w")
	# 	# data = json.dumps({'data':str(self.isConnected_set)})
	# 	# f.write(data)
	# 	# f.close()
	# 	return True

	def is_connected(self, neighbourhood):
		i = 1
		status_dict = {}
		queue = []
		vis = {}
		for voxel in neighbourhood:
			vis[voxel]=False
		for voxel in neighbourhood:
			if vis[voxel]==False:
				i=i+1
				vis[voxel]=True
				queue.insert(0,voxel)
				while queue!=[]:
					cur = queue.pop()
					curr_neighbours = self.getNeighboursForGivenVoxel(cur, neighbourhood)
					for neighbour in curr_neighbours:
						if vis[neighbour]==False:
							vis[neighbour]=True
							queue.insert(0,neighbour)

		if i>2:
			return False
		return  True

	def generatePowerSet(self, lst):
		return reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

	# Compare two floating point numbers for almost-equality
	def isClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

	def buildComplexFromPyFile(self, list):
		voxelCentreList = []
		for voxelDict in list:
			voxelCentreList.append((voxelDict['x'],voxelDict['y'],voxelDict['z']))
		print 'complex built: ', voxelCentreList	
		return voxelCentreList


	def processThinning(self, complex):
		simple_voxels = self.getSimpleVoxels(list(complex))
		for voxel in simple_voxels:
			temp = list(complex)
			temp.remove(voxel)
			if self.isConnected(temp):
				complex.remove(voxel)
		return complex

	def maskForAllNeighbours(self,centre):
		# print "centre",centre
		temp = list(centre)
		tempxplus = list(centre)
		tempxplus[0] += 1
		tempxminus = list(centre)
		tempxminus[0] -= 1
		temp_front = list(temp)
		temp_back = list(temp)
		temp_front[2] += 1
		temp_back[2] -= 1
		temp_front_up = list(temp_front)
		temp_back_up = list(temp_back)
		temp_front_down = list(temp_front)
		temp_back_down = list(temp_back)
		temp_front_up[1] += 1
		temp_back_up[1] += 1
		temp_front_down[1] -= 1
		temp_back_down[1] -= 1
		tempxplus_front = list(tempxplus)
		tempxplus_back = list(tempxplus)
		tempxminus_front = list(tempxminus)
		tempxminus_back = list(tempxminus)
		tempxplus_front[2] += 1
		tempxplus_back[2] -= 1
		tempxminus_front[2] += 1
		tempxminus_back[2] -= 1
		temp_up = list(temp)
		tempxplus_up = list(tempxplus)
		tempxminus_up = list(tempxminus)
		tempxplus_front_up = list(tempxplus_front)
		tempxplus_back_up = list(tempxplus_back)
		tempxminus_front_up = list(tempxminus_front)
		tempxminus_back_up = list(tempxminus_back)
		temp_up[1] += 1
		tempxplus_up[1] += 1
		tempxminus_up[1] += 1
		tempxplus_front_up[1] += 1
		tempxplus_back_up[1] += 1
		tempxminus_front_up[1] += 1
		tempxminus_back_up[1] += 1
		temp_down = list(temp)
		tempxplus_down =  list(tempxplus)
		tempxminus_down =  list(tempxminus)
		tempxplus_front_down =  list(tempxplus_front)
		tempxplus_back_down =  list(tempxplus_back)
		tempxminus_front_down =  list(tempxminus_front)
		tempxminus_back_down =  list(tempxminus_back)
		temp_down[1] -= 1
		tempxplus_down[1] -= 1
		tempxminus_down[1] -= 1
		tempxplus_front_down[1] -= 1
		tempxplus_back_down[1] -= 1
		tempxminus_front_down[1] -= 1
		tempxminus_back_down[1] -= 1

		mask = [tuple(tempxplus), tuple(tempxminus), tuple(temp_front), tuple(temp_back), tuple(temp_front_up), tuple(temp_back_up), tuple(temp_front_down), tuple(temp_back_down), tuple(tempxplus_front), tuple(tempxplus_back), tuple(tempxminus_front), tuple(tempxminus_back), tuple(temp_up), tuple(tempxplus_up), tuple(tempxminus_up), tuple(tempxplus_front_up), tuple(tempxplus_back_up), tuple(tempxminus_front_up), tuple(tempxminus_back_up), tuple(temp_down), tuple(tempxplus_down), tuple(tempxminus_down), tuple(tempxplus_front_down), tuple(tempxplus_back_down), tuple(tempxminus_front_down), tuple(tempxminus_back_down)]
		
		return mask