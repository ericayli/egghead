%write function and enter the name of the electrode(s) you want to analyze as strings,
%separated by commas
function extract_eeg(varargin)

mat_file = uigetfile('*.mat','MultiSelect','on');

%mat_file is a cell array of strings
mat_sz = size(mat_file);
%sz is a 1x2 array, with the 2nd column having the length of
%the mat_file cell array


%iterate through varargin cell array to match inputs to row numbers in eeg
%data

varargin_sz = size(varargin);

        f7 = 257;
        fp1 = 257;
        f3 = 257;
        f8 = 257;
        pz = 257;
        oz = 257;
        t7 = 257;
        p7 = 257;
        lm = 257;
        t8 = 257;
        fz = 257;
        c4 = 257;
        p8 = 257;
        o2 = 257;
        f4 = 257;
        rm = 257;
        nas = 257;
        fp2 = 257;
        o1 = 257;


for j = 1:1:varargin_sz(2)
    
    if strcmp(varargin{j}, 'F7')        
        f7 = 47;
    elseif strcmp(varargin{j},'Fp1')
        fp1 = 37;
    elseif strcmp(varargin{j},'F3')              
        f3 = 36;
    elseif strcmp(varargin{j},'F8')
        f8 = 2;
    elseif strcmp(varargin{j},'Pz')
         pz = 101;
     elseif strcmp(varargin{j},'Oz')
         oz = 126;
     elseif strcmp(varargin{j},'T7')
         t7 = 69;
     elseif strcmp(varargin{j}, 'P7')
         p7 = 96;
     elseif strcmp(varargin{j},'LM')
         lm = 94;
     elseif strcmp(varargin{j},'T8')
         t8 = 202;
     elseif strcmp(varargin{j},'Fz')
        fz = 21;
     elseif strcmp(varargin{j},'C4') 
         c4 = 183;
     elseif strcmp(varargin{j},'P8')
         p8 = 170;
     elseif strcmp(varargin{j},'O2')
         o2 = 150;
     elseif strcmp(varargin{j}, 'F4')
         f4 = 224;
     elseif strcmp(varargin{j},'RM')
         rm = 190;
     elseif strcmp(varargin{j},'NAS')
         nas = 31;
     elseif strcmp(varargin{j}, 'FP2')
         fp2 = 18;
    elseif strcmp(varargin{j},'O1')
        o1 = 116;        
    else 
        disp('Please type in a valid electrode.')
         break                                                                                                                               
    end
    
end


for i = 1:1:mat_sz(2)

    temp_string = mat_file{i};
    %temp_string serves as temporary string name of the matfile we are
    %working with, because it is being extracted from a single 1x1 cell
    %from the mat_file cell array
    
temp_mat = matfile(temp_string);
%matfile function extracts parts of matfile and loads it temporarily
%temp_mat is the temporary matfile that we will be manipulating



o1r = temp_mat.eeg(o1,:);
o2r = temp_mat.eeg(o2,:);

f7r = temp_mat.eeg(f7,:);
fp1r = temp_mat.eeg(fp1,:);
f3r = temp_mat.eeg(f3,:);
f8r = temp_mat.eeg(f8,:);
pzr = temp_mat.eeg(pz,:);
ozr = temp_mat.eeg(oz,:);
t7r = temp_mat.eeg(t7,:);
p7r = temp_mat.eeg(p7,:);
lmr = temp_mat.eeg(lm,:);
t8r = temp_mat.eeg(t8,:);
fzr = temp_mat.eeg(fz,:);
c4r = temp_mat.eeg(c4,:);
p8r = temp_mat.eeg(p8,:);
f4r = temp_mat.eeg(f4,:);
rmr = temp_mat.eeg(rm,:);
nasr = temp_mat.eeg(nas,:);
fp2r = temp_mat.eeg(fp2,:);

%temp_mat.eeg extracts data from the eeg matrix




electrodes_array = [transpose(o1r) transpose(o2r) transpose(f7r) transpose(fp1r) transpose(f3r) transpose(f8r) transpose(pzr) transpose(ozr) transpose(t7r) transpose(p7r) transpose(lmr) transpose(t8r) transpose(fzr) transpose(c4r) transpose(p8r) transpose(f4r) transpose(rmr) transpose(nasr) transpose(fp2r)];


% o1table = array2table(transpose(o1));
% o2table = array2table(transpose(o2));
% f7table = array2table(transpose(f7));
% fp1table = array2table(transpose(fp1));
% f3table = array2table(transpose(f3));
% f8table = array2table(transpose(f8));
% pztable = array2table(transpose(pz));
% oztable = array2table(transpose(oz));
% t7table = array2table(transpose(t7));
% p7table = array2table(transpose(p7));
% lmtable = array2table(transpose(lm));
% t8table = array2table(transpose(t8));
% fztable = array2table(transpose(fz));
% c4table = array2table(transpose(c4));
% p8table = array2table(transpose(p8));
% f4table = array2table(transpose(f4));
% rmtable = array2table(transpose(rm));
% nastable = array2table(transpose(nas));
% fp2table = array2table(transpose(fp2));



electrodes_table = array2table(electrodes_array);


x = append(temp_string(1:end-4), '.xlsx');



%table = [o1table o2table f7table fp1table f3table f8table pztable oztable t7table p7table lmtable t8table fztable c4table p8table f4table rmtable nastable fp2table];


%change name of the table to include the names of specific rows of eeg data
%we want (aka the electrodes)

writetable(electrodes_table,x)


%exports excel file based on the string x and y, which we set as .xlsx
%files
end



end


%keep temp variable to hold the string of the name of the mat at the
%beginning of each iterationfor i = 1:1:sz(2)
% B = test{i}
% end
% 
% B =
% 
%     'S001a.mat'
% 
% 
% B =
% 
%     'S001b.mat'
% 
% 
% B =
% 
%     'S001c.mat'
