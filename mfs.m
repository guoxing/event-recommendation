function [X,Y] = mfs(A, dim, epsilon, S ) 


lambda4 = 0.1;
lambda2 = 0.1;
% step size
t0 = 10;
t = t0;

dim1 = size(A,1);
dim2 = size(A,2);

X = rand(dim1,dim) ./ 1;
Y = rand(dim2,dim) ./ 1;

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
LS = diag(sum(S)) - S;
clear S;
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
      %  num
        
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
        
       % LSX = nita * LS * X;  
        
        
        
        X(i,:) = ((1 - nita * lambda4) * Xi - XLfy)- lambda2 * nita * LS(i, :) * X;
       % Y(j,:) = ((1 - nita * lambda4) * Yj - YLfy);
      %  Y(j,:) = ((1 - nita * lambda4) * Yj - YLfy) ;
      
         Y(j,:) = ((1 - nita * lambda4) * Yj - YLfy) ;
        
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
%c
X = oldX;
Y = oldY;

end