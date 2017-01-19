tic
% read the csv file
fid = fopen('slot-1.csv');
C = textscan(fid, '%s %f %s %s %f %f %f %s','delimiter', ',', 'treatAsEmpty', {'NA', 'na'});
fclose(fid);
%celldisp(C);
%C{5}
viewer = cell2mat(C(5));
%viewer = viewer(1:4000);
% n: the numbers of uploaders
[n, temp]= size(viewer);

% the whole bandwidth, namely, the bitrate
b = 13000;


% the minimal bitrate of each uploader
l = zeros(n, 1);
% the maximal bitrate of each uploader
h = zeros(n, 1);
% the price of the bandwidth
c = zeros(n, 1);
% the weight of the bandwidth
k = 100;
% the minimal bitrate
r_min = 0.6;

% initialize the minimal, maximal and the price
for i=1:n
    h(i) = 5;
    l(i) = 0.6;
    c(i) = 0.06/12;
end

% covex optimization
cvx_begin 
    variable r(n)
    %maximize( sum(log(v.*(log(1+ r./r_min) - log(2)) - k.*(r-r_min).*c)) )
    maximize( sum(viewer.*log((log(1+ r./r_min) - log(2)) - k.*(r-r_min).*c)) )
    subject to
        l <= r <= h;
        sum(r) <= b;
cvx_end
r;
toc
