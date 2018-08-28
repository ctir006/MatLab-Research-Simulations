import matplotlib.pyplot as plt

p=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
no_of_reassignments=[1900,1900,1900,1900,1900,1900,1900,1898,1896,831]

plt.plot(p,no_of_reassignments, '-',color='r')
plt.axis([0, 1, 0, 2000])
plt.xlabel('Probability p')
plt.ylabel('Number of reassignments when q=0.1')
plt.show()