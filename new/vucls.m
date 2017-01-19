% the whole bandwidth, namely, the bitrate
b = 20;
% the numbers of uploaders
n = 10;
% the minimal bitrate of each uploader
l = zeros(n, 1);
% the maximal bitrate of each uploader
h = zeros(n, 1);
% the price of the bandwidth
c = zeros(n, 1);
% the weight of the bandwidth
k = 10;
% the minimal bitrate
r_min = 0.6;

% initialize the minimal, maximal and the price
for i=1:n
    h(i) = 5;
    l(i) = 0.6;
    c(i) = 0.06/12;
end

% the viewers of each uploader
v = [100 95 90 85 80 2 7 10 15 20];
%v = [10000 95 90 85 80 2 7 10 15 20];
%v = [10000 950 90 85 80 2 7 10 15 20];
%v = [100000 9500 900 85 80 2 7 10 15 20];
% reshape the v(1, 10) to v(10, 1) for using the .* multiplier
v = reshape(v, 10, 1);

% covex optimization
cvx_begin 
    variable r(n)
    %maximize( sum(log(v.*(log(1+ r./r_min) - log(2)) - k.*(r-r_min).*c)) )
    maximize( sum(v.*log((log(1+ r./r_min) - log(2)) - k.*(r-r_min).*c)) )
    subject to
        l <= r <= h;
        sum(r) <= b;
cvx_end
r