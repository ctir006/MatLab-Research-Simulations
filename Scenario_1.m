 total_no_of_epochs=3;      
 duration_of_epoch=5;       %in hours
 duration_of_t=15;          %in minutes
 total_no_of_users=1000;     %initial no of users in the cluster
 on_off_state_matrix=zeros(total_no_of_users,total_no_of_epochs*duration_of_epoch*60);
 newly_joined_users=0;
 user_waiting_time_matrix=zeros(total_no_of_users,1);
 reassignment_time=1;
 total_reassignment_delay=0;
 lambda_user_ON = 15;				% mean of the distribution modelling users' on periods
 lambda_user_OFF = 30;				% mean of the distribution modelling users' off periods
 lambda_user_join = 1;
 rekeying = 77;                      % time in seconds needed for performing a rekeying operation
 rekeying_delay=0;
 
 
 
 for i=1:total_no_of_epochs
    new_on_off_state_matrix=[on_off_state_matrix;zeros(newly_joined_users,total_no_of_epochs*duration_of_epoch*60)];
    new_user_waiting_time_matrix=[user_waiting_time_matrix;zeros(newly_joined_users,1)];
    reassignment_delay_for_the_epoch=0;
    for j=1:total_no_of_users
        state=round(rand);
        sum=0;
        column=((i-1)*duration_of_epoch*60)+1;
        while sum<= duration_of_epoch*60
            if state
                r=poissrnd(lambda_user_ON,1,1);
                sum=sum+r;
                for l=1:r
                    new_on_off_state_matrix(j,column)=state;
                    column=column+1;
                end
                state=0;
            else
                r=poissrnd(lambda_user_OFF,1,1);
                sum=sum+r;
                for l=1:r
                    new_on_off_state_matrix(j,column)=state;
                    column=column+1;
                end
                state=1;
            end
        end
    end
    t=((i-1)*duration_of_epoch*60)+1;
    while t < (i*duration_of_epoch*60)
        user_state_column_vector=new_on_off_state_matrix(:,t);
        next_user_state_column_vector=new_on_off_state_matrix(:,t+duration_of_t);
        t=t+duration_of_t;
        for q=1:total_no_of_users
            if user_state_column_vector(q)==0 && next_user_state_column_vector(q)==1
                wait_time=0;
                for w=1:duration_of_t
                    if new_on_off_state_matrix(q,t-i)==0
                        break
                    else
                        wait_time=wait_time+1;
                    end
                end
                new_user_waiting_time_matrix(q)=wait_time;
            end
        end
        if ~(isequal(user_state_column_vector,next_user_state_column_vector))
            reassignment_delay_for_the_epoch=reassignment_delay_for_the_epoch+reassignment_time;
        end
    end
    fprintf('Reassignement delay for the epoch %d : %d\n',i,reassignment_delay_for_the_epoch);
    total_reassignment_delay=total_reassignment_delay+reassignment_delay_for_the_epoch;
    user_waiting_time_matrix=new_user_waiting_time_matrix;
    user_waiting_time_matrix=user_waiting_time_matrix+new_user_waiting_time_matrix;
    newly_joined_users=poissrnd(lambda_user_join,1,1);
    if newly_joined_users
        rekeying_delay=rekeying_delay+rekeying;
    end    
    on_off_state_matrix=new_on_off_state_matrix;
    fprintf('Rekeying delay until this epoch :%d \n', rekeying_delay);
  
 end
 fprintf('Total Reassignement delay all the epochs : %d \n', total_reassignment_delay );