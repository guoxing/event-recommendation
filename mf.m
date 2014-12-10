function [X,Y] = mf(A, dim, epsilon) 


lambda4 = 0.1;
% step size
t0 = 10;
t = t0;

dim1 = size(A,1);
dim2 = size(A,2);

X = rand(dim1,dim) ./ 10;
Y = rand(dim2,dim) ./ 10;

[a, b, values] = find(A);

% initialize function loss
c = zeros(size(values));
for j = 1:length(values)
    ijk = X(a(j), :) * Y(b(j), :)';
    c(j) = ijk;
end
loss_t1 = norm(c - values);
loss_t = loss_t1 + epsilon + 1;
fprintf('loss: %f\n', loss_t1);

% get the laplacian matrices
%LC = diag(sum(C)) - C;
turn = 1:1:length(values);

while loss_t - loss_t1 > epsilon   
    
    oldX = X;
    oldY = Y;
    
    % optimize each element in randomized sequence   
    for num = 1:length(values)-1     
        change = randi([num+1,length(values)]);
        temp = turn(num);
        turn(num) = turn(change);
        turn(change) = temp;
    end
   
    for num = 1:length(values) % for every nonzero entries in A
     
        
        tnum = turn(num);
        nita = 1/sqrt(t);  % step size
        t = t + 1;
        i = a(tnum);
        j = b(tnum);
        
        Xi = X(i,:);
        Yj = Y(j,:);

               
      
        Fijk = Xi * Yj';
        
        Yijk = values(tnum);
        Lfy = Fijk - Yijk;
             
        
        XLfy = double((nita * Lfy) * Yj);
        YLfy = double((nita * Lfy) * Xi);
        
        
        X(i,:) = ((1 - nita * lambda4) * Xi - XLfy);
        Y(j,:) = ((1 - nita * lambda4) * Yj - YLfy);
        
      %  LCY = nita * LC * Y;
    %    Y(j,:) = ((1 - nita * lambda4) * Yj - YLfy)' - lambda2 * LCY(j,:);       
  
        
    end
    
    % compute function loss 
    c = zeros(size(values));
    for j = 1:length(values)
        ijk = X(a(j), :) * Y(b(j), :)';
        c(j) = ijk;
    end
    loss_t = loss_t1;
    loss_t1 = norm(c - values);
    fprintf('loss: %f\n', loss_t1);    
end
fprintf('end\n');    

X = oldX;
Y = oldY;

end