%load('userBusiness.mat')
%train = userBusiness;

%load('userBusiness_test.mat')
%test = userBusiness;

load('/home/yilunw/similarity.mat')


[train, test] = getTrainTest(0.5);
[U, V] = mf(train, 10, 0.01);
%[U, V] = mfs(train, 10, 0.01, similarity);
predict = U * V';
sqrt(sum(sum(((test > 0) .* (test - predict)).^2)) / sum(sum(test>0)))