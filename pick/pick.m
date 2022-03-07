%============tick S arrivals============
close all
clear
clc

files = dir('*.BHT');

dt = 0.025;

t_min = 0; t_max = 20;

for i=1:length(files)
    file = files(i).name;
    [t,d] = readsac(file);
    S = readsac(file);
    s_prem = S.T2;  % where we save the S traveltime in HEADER t2
    t1 = s_prem + t_min;
    t2 = s_prem + t_max;
    t1_loca = round((t1-t(1))/dt);
    t2_loca = round((t2-t(1))/dt)+1;
    [dpeaks, dlocs] = findpeaks(d(t1_loca:t2_loca));
    %d_loc = 1;
    [d_max, d_loc] = max(dpeaks);
    if numel(dpeaks) > 0
        S.T3 = t(t1_loca+dlocs(d_loc)-1);
        S.KT3 = 'spick';
        status = writesac(S);
        clear S;
    end
end
