function [ train, test ] = getTrainTest( ratio)
%ratio = 0.7;
load('userBusiness_total.mat')
data = userBusiness;

m = size(data, 1);
n = size(data, 2);
train = sparse(m, n);
test = sparse(m, n);

[a, b, values] = find(data);
for i = 1:length(values)
    if rand() < ratio
        train(a(i), b(i)) = values(i);
    else
        test(a(i), b(i)) = values(i);
    end
end

end

