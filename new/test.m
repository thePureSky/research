tic
% read the csv file
fid = fopen('slot-1.csv');
C = textscan(fid, '%s %f %s %s %f %f %f %s','delimiter', ',', 'treatAsEmpty', {'NA', 'na'});
fclose(fid);
%celldisp(C);
%C{5}
viewer = cell2mat(C(5));
% n: the numbers of uploaders
[n, temp]= size(viewer);
n
toc
