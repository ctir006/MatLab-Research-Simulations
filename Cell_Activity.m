databases = 7;                      % number of databases queried
queries = 25;                       % number of queries/ number of cells in the cluster
T_epoch = 5;                        % period in hours for rekeying and for querying databases 
lambda_join = 1;                    % mean for the join events modeled as a poisson distribution
n = 1000;                           % current number of users in a cluster
rekeying = 77;                      % time in seconds needed for performing a rekeying operation
max_n = 2000;                       % max number of users within a cluster, could be used as a convergence criterion
cluster_cells = [1 5 10 25 50];    	% array containing number of cells in the cluster / maximum number of queries
rekeying_delay = 77;   				% time in seconds needed for performing a rekeying operation
lambda_user_ON = 15;				% mean of the distribution modelling users' on periods
lambda_user_OFF = 30;				% mean of the distribution modelling users' off periods
query_delay = [1.6 2.3 3.6 13.15 17];	% array containing the time needed for the leader to query the databases and get spectrum availability information for each entry in cluster_cells
lambda_cell_ON = 15;				% mean for the number of cells that are active (i.e. some users are located there) during the current period T_epoch
user_leader_query_delay = 1;		% time in seconds for the user to get a resource from the leader after turning active

total_delay = 0;
no_of_epochs = 100;
lambda_active_cells = 25;
no_of_active_cells_in_cluster=poissrnd(lambda_active_cells,1,no_of_epochs);
for i=no_of_active_cells_in_cluster
    pos=1;
    for j=cluster_cells
        if i<j
            break
        else
            pos=pos+1;
        end
    end
    total_delay=total_delay+query_delay(pos);
end
fprintf("Average delay for one epoch is ");
disp(total_delay/no_of_epochs);
disp(total_delay);





