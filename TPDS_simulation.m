databases = 7;                      % number of databases queried
queries = 25;                       % number of queries/ number of cells in the cluster
T_epoch = 5;                        % period in hours for rekeying and for querying databases 
lambda_join = 1;                    % mean for the join events modeled as a poisson distribution
n = 1000;                           % current number of users in a cluster
rekeying = 77;                      % time in seconds needed for performing a rekeying operation
max_n = 2000;                       % max number of users within a cluster, could be used as a convergence criterion
cluster_cells = [1 5 10 25];    	% array containing number of cells in the cluster / maximum number of queries
rekeying_delay = 77;   				% time in seconds needed for performing a rekeying operation
lambda_user_ON = 15;				% mean of the distribution modelling users' on periods
lambda_user_OFF = 30;				% mean of the distribution modelling users' off periods
query_delay = [1.6 2.3 3.6 13.15];	% array containing the time needed for the leader to query the databases and get spectrum availability information for each entry in cluster_cells
lambda_cell_ON = 15;				% mean for the number of cells that are active (i.e. some users are located there) during the current period T_epoch
user_leader_query_delay = 1;		% time in seconds for the user to get a resource from the leader after turning active


% Rekeying operation code start

number_of_time_slots=1000;
r_delays = [65,70,75,80,85,90,95,100,105,110];
p=poissrnd(0.5,1,number_of_time_slots);
delay=0;
n_users_joined=0;
for i=p
    if i~=0
        n_users_joined=n_users_joined+i;
        if n>max_n
            break
        end
        n=n+i;
        if (floor(n_users_joined/100)+1) > 10
            break
        end
        delay=delay+r_delays(floor(n_users_joined/100)+1);
        %disp(delay);
    end
end
fprintf("Number of users joined : ");
disp(n_users_joined);
fprintf("Total Number of users :");
disp(n);
fprintf("Total Amount of delay : ");
disp(delay);
fprintf("Average delay per user : ");
disp(delay/number_of_time_slots);

% Rekeying operation code end