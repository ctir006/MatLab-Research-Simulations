no_of_cells = 25;
initial_no_of_users = 1000;
for i=1:no_of_cells
    cell(i).id=i;
    cell(i).users=[];
    cell(i).active=[];
    cell(i).inactive=[];
end
for i=shuffle(1:10)
  disp(i)
end
 
for i=1:initial_no_of_users
    cid=mod(i,no_of_cells);
    if cid
        cell(mod(i,no_of_cells)).users=[cell(mod(i,no_of_cells)).users; i];
    else
        cell(no_of_cells).users=[cell(no_of_cells).users; i];
    end
end

for i=1:no_of_cells
    fprintf("cell id : %d \n",i);
    %disp(cell(i).users);
end
