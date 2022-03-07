%==========get gray image==========
close all
clear
clc

files = dir('*.t');
dists = 0:0.1:30; % epicentral distance vector(substract 60)

dt = 0.025;

t_left = 0; t_right = 100; f_length = 3001;
t_length = (t_right - t_left) / dt + 1;

gray_matrix = zeros(f_length, t_length);

for i=1:length(files)
    file = files(i).name;
    [t, d] = readsac(file);
    S = readsac(file);
    s_prem = S.T2; % where we save the S traveltime in HEADER t2
    t1_loca = round((s_prem - t(1))/dt) + round(t_left / dt);
    t2_loca = round((s_prem - t(1))/dt) + round(t_right / dt);
    d_local = d(t1_loca:t2_loca);
    % zero
    k_local = find(d_local < 0);
    d_local(k_local) = 0;
    % Normalization
    d_max = max(d_local);
    d_local = d_local / d_max;
    % numerical matric for gray image
    dist = 3001 - round(dists(i)*100);
    gray_matrix(dist,:) = d_local;
end
gray_matrix = gray_matrix .* 100;
K_gray = mat2gray(gray_matrix, [0 100]);
figure
imshow(K_gray)