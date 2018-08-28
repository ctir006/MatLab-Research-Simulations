# http://connor-johnson.com/2014/02/25/spatial-point-processes/

import scipy
from scipy.stats import poisson
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import defaultdict

p_array=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
q_array=[0,0.3,0.6,0.9,1]
color=['r','g','b','c','m']
Nd_array=defaultdict(list)

for p in p_array:
	for q in q_array:
		total_no_of_cells=25
		total_no_of_users=1000
		max_number_of_users=2000
		initial_no_of_users=total_no_of_users
		total_no_of_epochs=1000
		lambda_user_join = 1
		duration_of_epoch=5       # in hours
		duration_of_t=15		  # in Minutes 
		rekeying_time = 1
		on_off_state_matrix=np.zeros((total_no_of_users,int((total_no_of_epochs*duration_of_epoch*60)/duration_of_t)),dtype=int)
		newly_joined_users=0
		users=defaultdict(dict)
		cells=defaultdict(list) 
		reassignment_time=1
		reassignment_time_array=[1,1.2,1.5,1.83,1.9,2.01,2.3,2.5,2.8,2.97,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.5,4.6,4.7,4.8]
		total_reassignment_delay=0
		total_rekeying_delay=0
		leader_db_query_delay=0
		active_cells=[]
		inactive_cells=[]
		total_delay=0
		#p = 0.5				      # user active probability
		#q = 0.1				      # user inactive probability    
		query_delay = [1.96, 3.26, 3.53, 4.85, 5.74, 7, 7.68, 8.28, 10.17, 10.73, 12.34, 12.48, 12.67, 13.21, 13.94, 14.36, 14.87, 16.46, 16.72, 17.06, 18.93, 19.49, 20.93, 21.51, 21.94]
		no_of_users_array=[]
		no_of_reassignments_array=[]
		no_of_epochs_array=[]
		reassignment_delay_array=[]
		total_no_of_distruptions_array=[]
		total_reassign_c=0
		total_no_of_distruptions=0
		def calculateDistance(x1,y1,x2,y2):  
			 dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
			 return dist  

		def PoissonPP( rt, Dx, Dy=None ):
			if Dy == None:
				Dy = Dx
				N = scipy.stats.poisson( rt ).rvs()
				t=total_no_of_cells-N
				#print("No of cells :",N)
				x = scipy.stats.uniform.rvs(0,Dx,((N,1)))
				y = scipy.stats.uniform.rvs(0,Dy,((N,1)))
				x1 = scipy.stats.uniform.rvs(0,Dx,((t,1)))
				y1 = scipy.stats.uniform.rvs(0,Dy,((t,1)))
				P = np.hstack((x,y))
				NP = np.hstack((x1,y1))
			return P,NP
			
		def NewUsersLocations( nUCount, Dx, Dy=None ):
			if Dy == None:
				Dy = Dx
				N = nUCount
				x = scipy.stats.uniform.rvs(0,Dx,((N,1)))
				y = scipy.stats.uniform.rvs(0,Dy,((N,1)))
				P = np.hstack((x,y))
			return P
			
		def uniformDisk( x, y, r ):
			r = scipy.stats.uniform( 0, r**2.0 ).rvs()
			theta = scipy.stats.uniform( 0, 2*np.pi ).rvs()
			xt = np.sqrt( r ) * np.cos( theta )
			yt = np.sqrt( r ) * np.sin( theta )
			return x+xt, y+yt
			
		def MaternPP( kappa, r, mu, Dx ):
			parents, nonParents = PoissonPP( kappa, Dx )
			M = parents.shape[0]
			MP = list()
			k=0
			while k<total_no_of_users:
				for i in range( M ):
					N = scipy.stats.poisson( mu ).rvs()
					for j in range( N ):
						k+=1
						if k>=total_no_of_users+1:
							break
						x, y = uniformDisk( parents[i,0], parents[i,1], r )
						users[k]['location']=(x,y)
						users[k]['cell']=i+1
						cells[i+1].append(k)
						if i not in active_cells:
							active_cells.append(i)
						MP.append( [ x, y ] )
					if k>=total_no_of_users:
						break
			MP = np.array( MP )
			print("Total number of user : ",k)
			return MP,parents,nonParents
			
		P,active_parents,inactive_parents=MaternPP(10,2,70,total_no_of_cells)
		parents=np.vstack((active_parents,inactive_parents))
		# print(active_parents.shape)
		# print(inactive_parents.shape)

		for i in range(total_no_of_epochs):
			no_of_epochs_array.append(i)
			no_of_users_array.append(total_no_of_users)
			leader_db_query_delay+=query_delay[len(active_cells)-1]
			a=np.zeros((newly_joined_users,int((total_no_of_epochs*duration_of_epoch*60)/duration_of_t)),dtype=int)
			new_on_off_state_matrix=np.vstack((on_off_state_matrix,a))   	
			reassignment_delay_for_the_epoch=0
			for usr in range(total_no_of_users):
				sum=0
				column=int(((i*duration_of_epoch*60)/duration_of_t))
				while sum < (duration_of_epoch*60)/duration_of_t:
					if p==0 or q==0:
						if p==0 and q==0:
							r_active=np.random.random()
							r_inactive=np.random.random()
							if r_active>r_inactive:
								new_on_off_state_matrix[usr][column]=1
							else:
								new_on_off_state_matrix[usr][column]=0
						elif p==0:
							new_on_off_state_matrix[usr][column]=0
							column+=1
						elif q==0:
							new_on_off_state_matrix[usr][column]=1
							column+=1
					elif p==1 or q==1:
						if p==1 and q==1:
							r_active=np.random.random()
							r_inactive=np.random.random()
							if r_active>r_inactive:
								new_on_off_state_matrix[usr][column]=1
							else:
								new_on_off_state_matrix[usr][column]=0
						elif p==1:
							new_on_off_state_matrix[usr][column]=1
							column+=1
						elif q==1:
							new_on_off_state_matrix[usr][column]=0
							column+=1
					else:
						r_active=np.random.random()
						r_inactive=np.random.random()
						if r_active>r_inactive:
							if r_active<p:
								s=1
							else:
								s=0
							new_on_off_state_matrix[usr][column]=s
							column+=1
						else:
							if r_inactive<q:
								s=0
							else:
								s=1
							new_on_off_state_matrix[usr][column]=s
							column+=1
					sum+=1
			#print(new_on_off_state_matrix[:10][:10])
			t=int(((i*duration_of_epoch*60)/duration_of_t))
			no_of_distruptions=0
			reassign_c=0
			while t < (((i+1)*duration_of_epoch*60)/duration_of_t)-1:
				no_of_cells_active_this_t=0
				user_state_column_vector=[i[t] for i in new_on_off_state_matrix]
				for a in active_cells:
					f=1
					for aa in cells[a]:
						if user_state_column_vector[aa-1]:
							f=0
					no_of_cells_active_this_t+=1
				#print("No of cells active in this t : ",no_of_cells_active_this_t)	
				next_user_state_column_vector=[i[t+1] for i in new_on_off_state_matrix]
				t=t+1
				equal=1
				for tt in range(len(user_state_column_vector)):
					if user_state_column_vector[tt] != next_user_state_column_vector[tt]:
						equal=0
						break
				if not equal:
					if t+1<(((i+1)*duration_of_epoch*60)/duration_of_t)-1 and new_on_off_state_matrix[1][t]==1 and new_on_off_state_matrix[1][t+1]==1:
						no_of_distruptions+=1
					reassign_time=reassignment_time_array[int(total_no_of_users/100)]
					reassign_c+=1
					reassignment_delay_for_the_epoch=reassignment_delay_for_the_epoch+reassign_time
			total_no_of_distruptions_array.append(total_no_of_distruptions)
			no_of_reassignments_array.append(reassign_c)
			total_reassign_c+=reassign_c
			##print('Reassignement delay for the epoch :',i+1," : ",reassignment_delay_for_the_epoch+1)
			##print('no of distruptions for the epoch :',i+1," : ",no_of_distruptions)
			total_no_of_distruptions+=no_of_distruptions
			total_reassignment_delay+=reassignment_delay_for_the_epoch+1;
			reassignment_delay_array.append(total_reassignment_delay)
			on_off_state_matrix=new_on_off_state_matrix

			no_of_users_joined=scipy.stats.poisson( lambda_user_join ).rvs()
			newly_joined_users=no_of_users_joined
			##print("Total no of users : ",total_no_of_users)
			if no_of_users_joined>0 and total_no_of_users+newly_joined_users<max_number_of_users:
					new_user_locations=NewUsersLocations(no_of_users_joined,total_no_of_cells)
					#print(new_user_locations)
					# for qw in range(len(new_user_locations)):   
						# ux,uy=uniformDisk( new_user_locations[qw][0], new_user_locations[qw][1], 1 )  
						# new_user_locations[qw][0]=ux
						# new_user_locations[qw][1]=uy
						
					for u in new_user_locations:
						total_no_of_users+=1
						min=None
						min_parent=None
						index=0
						for (i,v) in enumerate(parents):
							d=calculateDistance(u[0],u[1],v[0],v[1])
							if min==None or d<min:
								min=d
								min_parent=v
								u[0],u[1]=uniformDisk( v[0], v[1], 2 )
								index=i
						if index > active_parents.shape[0]-1:
							cells[index].append(total_no_of_users)
							active_cells.append(active_parents.shape[0])
							active_parents=np.vstack((active_parents,min_parent))
							P=np.vstack((P,u))
						else:
							P=np.vstack((P,u))
					total_rekeying_delay+=rekeying_time
			#print(active_cells)			
		# print(inactive_parents.shape)
		total_delay=total_reassignment_delay+leader_db_query_delay+total_rekeying_delay
		# print("Average processing time for leader : ",total_delay/total_no_of_epochs)
		# print("Average time spent on rekeying per user : ",total_rekeying_delay/total_no_of_epochs)

		# print(" Percentage of processing time over the duration of the simulation : ", (total_delay/(total_no_of_epochs*duration_of_epoch*60*60))*100)
		# print(" Percentage of reassignment time for the user : ", (total_reassignment_delay/(total_no_of_epochs*duration_of_epoch*60*60))*100)
		Nd_array[q].append(total_no_of_distruptions/total_no_of_epochs)
		# print("Total reassignment delay : ",total_reassignment_delay)
		# print("Total rekeying delay : ",total_rekeying_delay)
		# print("Average number of distruptions : ",total_no_of_distruptions/total_no_of_epochs)
		# print("Total leader database query delay : ",leader_db_query_delay)

print(p)
print(q)
for i in Nd_array:
	print(i,Nd_array[i])

# No of epochs to no of distruptions Graph
# P=P.T
# plt.plot(Nd_array, p_array, '-',color='r')
# plt.axis([0, 20, 0, 1])
# plt.xlabel('Number of distruptions')
# plt.ylabel('Probability P')
#No of users to no of epochs Graph
#P=P.T
# plt.plot(no_of_epochs_array, no_of_users_array, '-',color='r')
# plt.axis([0, 1000, 0, 1100])
# plt.xlabel('Number of epochs')
# plt.ylabel('Number of users')
#No of users to no of reassignments Graph
#P=P.T
# plt.plot(no_of_epochs_array, reassignment_delay_array, '-',color='r')
# plt.axis([0, 1000, 0, 30000])
# plt.xlabel('Number of epochs')
# plt.ylabel('Reassignement delay')
#No of users to no of reassignments Graph
# P=P.T
# plt.plot(no_of_users_array, no_of_reassignments_array, '-',color='r')
# plt.axis([0, 1100, 0, 30])
# plt.xlabel('Number of users')
# plt.ylabel('Number of reassignments')
# Users Graph
# P=P.T
# plt.plot(P[0], P[1], 'o',color='g')
# plt.axis([0, 30, 0, 30])
# print(total_reassign_c)
# print(total_no_of_users)
# for i in cells:
	# print(i,cells[i])
# for i in list(users.keys())[:10]:
	# print(users[i])
plt.axis([0, 1, 0, 20])
for (p,i) in enumerate(q_array):
	plt.plot(p_array, Nd_array[i], color[p],label=i) # plotting t, a separately 
plt.xlabel('Probability P')
plt.ylabel('Number of distruptions')
plt.legend(loc='upper left', frameon=False)
plt.show()

# 0 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# 0.3 [0.0, 3.557, 3.773, 4.213, 4.935, 5.663, 6.862, 8.39, 10.109, 12.45, 0.0]
# 0.6 [0.0, 1.812, 1.933, 2.34, 2.798, 3.283, 4.332, 5.436, 6.876, 8.969, 0.0]
# 0.9 [0.0, 0.174, 0.213, 0.327, 0.524, 0.826, 1.261, 1.933, 2.898, 4.316, 0.0]
# 1 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


