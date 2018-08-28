 total_no_of_epochs=3;      
 duration_of_epoch=5;       %in hours
 duration_of_t=15;          %in minutes
 total_no_of_users=1000;     %initial no of users in the cluster
 on_off_state_matrix=zeros(total_no_of_users,(total_no_of_epochs*duration_of_epoch*60)/duration_of_t);
 newly_joined_users=0;
 reassignment_time=1;
 total_reassignment_delay=0;
 p = 0.5;				% user active probability
 q = 0.8;				% user inactive probability
 lambda_user_join = 1;
 rekeying = 77;                      % time in seconds needed for performing a rekeying operation
 rekeying_delay=0;
 
 
 
 for i=1:total_no_of_epochs
    new_on_off_state_matrix=[on_off_state_matrix;zeros(newly_joined_users,(total_no_of_epochs*duration_of_epoch*60)/duration_of_t)];
    reassignment_delay_for_the_epoch=0;
    for j=1:total_no_of_users
        sum=0;
        column=(((i-1)*duration_of_epoch*60)/duration_of_t)+1;
        while sum <= (duration_of_epoch*60)/duration_of_t
           r_active=rand(1);
           r_inactive=rand(1);
           if r_active>r_inactive
               new_on_off_state_matrix(j,column)=r_active>p;
               column=column+1;
           else
               new_on_off_state_matrix(j,column)=r_inactive>q;
               column=column+1;
           end
           sum=sum+1;
        end
    end
    %disp(new_on_off_state_matrix);   
    t=(((i-1)*duration_of_epoch*60)/duration_of_t)+1;
    while t < ((i*duration_of_epoch*60)/duration_of_t)
        user_state_column_vector=new_on_off_state_matrix(:,t);
        next_user_state_column_vector=new_on_off_state_matrix(:,t+1);
        t=t+1;
        if ~(isequal(user_state_column_vector,next_user_state_column_vector))
            reassignment_delay_for_the_epoch=reassignment_delay_for_the_epoch+reassignment_time;
        end
    end
    fprintf('Reassignement delay for the epoch %d : %d\n',i,reassignment_delay_for_the_epoch);
    total_reassignment_delay=total_reassignment_delay+reassignment_delay_for_the_epoch;
    newly_joined_users=poissrnd(lambda_user_join,1,1);
    if newly_joined_users
        rekeying_delay=rekeying_delay+rekeying;
    end    
    on_off_state_matrix=new_on_off_state_matrix;
    fprintf('Rekeying delay until this epoch :%d \n', rekeying_delay);
 end
 fprintf('Total Reassignement delay all the epochs : %d \n', total_reassignment_delay );