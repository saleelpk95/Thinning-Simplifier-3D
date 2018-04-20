from utils import *
from canstick6 import lookup

if __name__ == '__main__':
	util = Utils()
	# voxel_centre_list = [(0,0,0),(0,1,0),(1,2,-1),(2,2,-1),(2,1,-1) ,(2,0,-1),(2,0,0),(2,1,0)]
	voxel_centre_list = util.buildComplexFromPyFile(lookup)
	# voxel_centre_list = [(0,0,0),(1,0,0),(2,0,0),(0,1,0),(1,1,0),(2,1,0),(0,2,0),(1,2,0),(2,2,0),(0,0,1),(1,0,1),(2,0,1),(0,1,1),(1,1,1),(2,1,1),(0,2,1),(1,2,1),(2,2,1),(0,0,2),(1,0,2),(2,0,2),(0,1,2),(1,1,2),(2,1,2),(0,2,2),(1,2,2),(2,2,2)]
	temp_voxel_centre_list = list(voxel_centre_list)
	util.buildObjFile(list(voxel_centre_list),"complex")
	voxel_data = util.build_voxel_data(voxel_centre_list)
	border_list = [voxel for voxel in voxel_centre_list if util.is_border_voxel(voxel,voxel_centre_list)]
	print 'initial border list is ',border_list
	skeleton = []
	for border_voxel in border_list:
		voxel_data[border_voxel[0]][border_voxel[1]][border_voxel[2]] = 2

	num_deleted_voxels = -1
	i=0
	while num_deleted_voxels != 0 or len(voxel_centre_list)>1:
		print i
		print 'entered loop'
		if num_deleted_voxels == 0:
			print 'v1',voxel_centre_list
			print 'b1', border_list
			rem_voxels = util.least_connected_simple(border_list, voxel_centre_list)
			print 'rem_voxels',rem_voxels
			for rem_voxel in rem_voxels:
				adjacent_voxels = util.findAll2AdjacentVoxelsForGivenVoxel(rem_voxel, voxel_centre_list)
				for voxel in adjacent_voxels:
					if voxel_data[voxel[0]][voxel[1]][voxel[2]] == 1:
						voxel_data[voxel[0]][voxel[1]][voxel[2]] = 2
						border_list.append(voxel)
				voxel_data[rem_voxel[0]][rem_voxel[1]][rem_voxel[2]] = 0
				border_list.remove(rem_voxel)
				voxel_centre_list.remove(rem_voxel)
		num_deleted_voxels = 0
		# print "entered. ",num_deleted_voxels
		temp_border_list = list(border_list)
		for border_voxel in border_list:
			print 'border loop entered'
			if (util.is_simplifier_voxel(border_voxel, voxel_centre_list) and util.is_end_voxel(border_voxel, voxel_centre_list)) or (not(util.is_simple_voxel(border_voxel, voxel_centre_list))):
				print 'skeleton voxel identified'
				skeleton.append(border_voxel)
				voxel_data[border_voxel[0]][border_voxel[1]][border_voxel[2]] = 3
				temp_border_list.remove(border_voxel)
				temp_voxel_centre_list.remove(border_voxel)
				num_deleted_voxels = num_deleted_voxels + 1
				# print_voxel_data(voxel_data,"elements of skeleton"+str(i))
			elif util.is_simple_voxel(border_voxel, voxel_centre_list) and not util.is_simplifier_voxel(border_voxel, voxel_centre_list):
				print 'simple voxel identified'
				print "yes simple it is"
				if util.all_neighbours_boundary(border_voxel, voxel_data, voxel_centre_list):
					skeleton.append(border_voxel)
					voxel_data[border_voxel[0]][border_voxel[1]][border_voxel[2]] = 3
					temp_border_list.remove(border_voxel)
				else:	
					# print "simple voxel",border_voxel
					voxel_data[border_voxel[0]][border_voxel[1]][border_voxel[2]] = 0
					temp_border_list.remove(border_voxel)
					num_deleted_voxels = num_deleted_voxels + 1
					adjacent_voxels = util.findAll2AdjacentVoxelsForGivenVoxel(border_voxel, voxel_centre_list)
					for voxel in adjacent_voxels:
						if voxel_data[voxel[0]][voxel[1]][voxel[2]] == 1:
							voxel_data[voxel[0]][voxel[1]][voxel[2]] = 2
							temp_border_list.append(voxel)
					# voxel_centre_list.remove(border_voxel)
					temp_voxel_centre_list.remove(border_voxel)
			else:
				print 'simply simplifier'
		border_list = list(temp_border_list)
		voxel_centre_list = list(temp_voxel_centre_list)
		print 'bb2',border_list
		print 'leaving loop'
		util.buildObjFile(voxel_centre_list,"intermediate"+str(i))
		print 'complex intermediate',voxel_centre_list
		print 'skeleton',skeleton
		i=i+1
		# print "leaving. ",num_deleted_voxels
		# print "voxel_data \n",voxel_data
	# print voxel_data
	# print 'skeleton',skeleton
	if skeleton ==[]:
		skeleton = voxel_centre_list
	util.buildObjFile(skeleton,"skeleton")