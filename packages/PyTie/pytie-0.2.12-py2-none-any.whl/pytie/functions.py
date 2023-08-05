### PyTie - Seismic-well tie in Python ###

import numpy as np
import sys 
import lasio
import pandas as pd
import matplotlib.pyplot as plt


def int_data(las_files, N_files, DT_id, RHOB_id, Depth_id):
    """
    EX.: DT, RHOB = pytie.int_data(las_files, N_files, DT_id, RHOB_id, Depth_id)

    This function reads one or more .las files and integrate them if they are divided in different files 
    and/or collumns. It is necessary to check if the description of your log name is unique in
    the file. Otherwise it is necessary to add or find some information to make it unique. In the 
    
    Inputs:
    
    las_file = add the folder and file(s) address(es). 
    N-files = attribute the number of files to be imported.
    DT_id = name used to identify the sonic log. 
    RHOB_id = name used to identify the density log. 
    Depth_id = name used to identify the depth index.
    
    Outputs:
    
    DT = DT log integrated - Panda DataFrame
    RHOB = RHOB log integrated - Panda DataFrame
    
    """
    
    if N_files == 1:
    
        log0 = lasio.read(las_files)
    
        STEP = log0.well.step.value
        NULL = log0.well.null.value
    
        R = log0[RHOB_id]  
        D = log0[DT_id]         
        DEPTH = log0[Depth_id]   
        
        DEP1 = np.array([DEPTH])
        D2 = np.array([D])
        D3 = np.concatenate((DEP1.T, D2.T), axis=1)
        DT = pd.DataFrame(D3, columns=('Depth', 'DT'))
        
        DEP2 = np.array([DEPTH])
        R2 = np.array([R])
        R3 = np.concatenate((DEP2.T, R2.T), axis=1)
        RHOB = pd.DataFrame(R3, columns=('Depth', 'RHOB'))
                
        return DT, RHOB
        
        
    
    else:

        log0 = lasio.read(las_files[0])

        STEP = log0.well.step.value
        NULL = log0.well.null.value

        counter = 0

        count_d = []
        count_r = []

        for i in range(N_files):                  # counting the number of columns the same log appears in each file

            with open(las_files[i]) as f:
                contents = f.read()
                count = contents.count(DT_id)
                count_d = np.append(count_d, count)

            with open(las_files[i]) as f:
                contents = f.read()
                count = contents.count(RHOB_id)
                count_r = np.append(count_r, count)


        # Analysis of the DT log            

        DEPT_S_idx = []
        DEPT_B_idx = []
        DEPT_B_idx_1 = []
        DT_idx = []
        RHOB_idx = []
        RHOB_idx_1 = []




        count_d_i = np.where(count_d>0)

        for i in range(np.asarray(count_d_i).size):

            if count_d[count_d_i[0][i]] == 1:            # verifies if the same log is divided in different files


                globals()['log_S_%s' % i] = lasio.read(las_files[count_d_i[0][i]])  # saves the logs which has DT log

                globals()['DEPT_S_%s' % i] = globals()['log_S_%s' % i][Depth_id]   # Stores the depths of each file in different parameters

                DEPT_S_idx = np.append(DEPT_S_idx, globals()['DEPT_S_%s' % i])

                globals()['DT_S_%s' % i] = globals()['log_S_%s' % i]['DT']   # Stores the depths of each file in different parameters

                DT_idx = np.append(DT_idx, globals()['DT_S_%s' % i])

                DT_idx = np.array([DT_idx])

                DEPT_S_idx = np.array([DEPT_S_idx])

                DT = np.concatenate((DEPT_S_idx.T, DT_idx.T), axis=1)

                DT = pd.DataFrame(DT, columns=('Depth', 'DT'))

                DT = DT.sort_values(by='Depth', ascending=True, kind='mergesort', na_position='last', inplace=False).reset_index(drop=True)

                DT = DT.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)

            if count_d[count_d_i[0][i]] > 1:   # verifies if the same log is divided in different columns

                globals()['log_S_%s' % i] = lasio.read(las_files[count_d_i[0][i]])  # saves the logs which has DT log

                globals()['DEPT_S_%s' % i] = globals()['log_S_%s' % i][Depth_id]   # Stores the depths of each file in different parameters

                DEPT_S_idx = np.append(DEPT_S_idx, globals()['DEPT_S_%s' % i])

                globals()['DT'] = globals()['log_S_%s' % i]['DT']  # reading the first column

                DT_idx = np.append(DT_idx, globals()['DT'] )

                DT_idx = np.array([DT_idx])

                DEPT_S_idx = np.array([DEPT_S_idx])

                DT = np.concatenate((DEPT_S_idx.T, DT_idx.T), axis=1)

                DT = pd.DataFrame(DT, columns=('Depth', 'DT'))

                DT = DT.sort_values(by='Depth', ascending=True, kind='mergesort', na_position='last', inplace=False).reset_index(drop=True)

                DT = DT.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)
                

                for i in range(int(count_d[count_d_i[0][i]]-1)):

                    globals()['log_S_%s' % i] = lasio.read(las_files[count_d_i[0][0]])

                    globals()['DT_%s' % (i+1)] = globals()['log_S_%s' % i]['DT_%s' % (i+1)]

                    globals()['DEPT_S_%s' % i] = globals()['log_S_%s' % i][Depth_id]

                    DEPT_S_idx = np.append(DEPT_S_idx, globals()['DEPT_S_%s' % i])

                    DT_idx = np.append(DT_idx, globals()['DT_%s' % (i+1)])

                    DT_idx = np.array([DT_idx])

                    DEPT_S_idx = np.array([DEPT_S_idx])

                    DT = np.concatenate((DEPT_S_idx.T, DT_idx.T), axis=1)

                    DT = pd.DataFrame(DT, columns=('Depth', 'DT'))

                    DT = DT.sort_values(by='Depth', ascending=True, kind='mergesort', na_position='last', inplace=False).reset_index(drop=True)

                    DT = DT.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)



        ### RHOB        

        count_r_i = np.where(count_r>0) 

        for i in range(np.asarray(count_r_i).size):

            if count_r[count_r_i[0][i]] == 1:                          # verifies if the same log is divided in different files

                globals()['log_B_%s' % i] = lasio.read(las_files[count_r_i[0][i]])  # saves the logs which has DT log

                globals()['DEPT_B_%s' % i] = globals()['log_B_%s' % i][Depth_id]   # Stores the depths of each file in different parameters

                DEPT_B_idx = np.append(DEPT_B_idx, globals()['DEPT_B_%s' % i])

                globals()['RHOB_B_%s' % i] = globals()['log_B_%s' % i]['RHOB']   # Stores the depths of each file in different parameters

                RHOB_idx = np.append(RHOB_idx, globals()['RHOB_B_%s' % i])

                RHOB_idx = np.array([RHOB_idx])

                DEPT_B_idx = np.array([DEPT_B_idx])

                RHOB = np.concatenate((DEPT_B_idx.T, RHOB_idx.T), axis=1)

                RHOB = pd.DataFrame(RHOB, columns=('Depth', 'RHOB'))

                RHOB = RHOB.sort_values(by='Depth', axis=0, ascending=True, kind='mergesort', na_position='last').reset_index(drop=True)

                RHOB = RHOB.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)


            if count_r[count_r_i[0][i]] > 1:   # verifies if the same log is divided in different columns

                globals()['log_B_%s' % i] = lasio.read(las_files[count_r_i[0][0]])  # saves the logs which has RHOB log

                globals()['DEPT_B_%s' % i] = globals()['log_B_%s' % i][Depth_id]   # Stores the depths of each file in different parameters

                DEPT_B_idx = np.append(DEPT_B_idx, globals()['DEPT_B_%s' % i])

                globals()['RHOB'] = globals()['log_B_%s' % i]['RHOB']  # reading the first column

                RHOB_idx = np.append(RHOB_idx, globals()['RHOB'])

                RHOB_idx = np.array([RHOB_idx])

                DEPT_B_idx = np.array([DEPT_B_idx])

                RHOB = np.concatenate((DEPT_B_idx.T, RHOB_idx.T), axis=1)

                RHOB = pd.DataFrame(RHOB, columns=('Depth', 'RHOB'))

                RHOB = RHOB.sort_values(by='Depth', axis=0, ascending=True, kind='mergesort', na_position='last').reset_index(drop=True)

                RHOB = RHOB.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)


                for i in range(int(count_r[count_r_i[0][i]]-1)): 

                    globals()['log_B_%s' % i] = lasio.read(las_files[count_r_i[0][i]]) 

                    globals()['RHOB_%s' % (i+1)] = globals()['log_B_%s' % i]['RHOB_%s' % (i+1)]

                    globals()['DEPT_B_%s' % i] = globals()['log_B_%s' % i][Depth_id] 

                    DEPT_B_idx = np.append(DEPT_B_idx, globals()['DEPT_B_%s' % i])

                    RHOB_idx = np.append(RHOB_idx, globals()['RHOB_%s' % (i+1)])

                    RHOB_idx = np.array([RHOB_idx])

                    DEPT_B_idx = np.array([DEPT_B_idx])

                    RHOB = np.concatenate((DEPT_B_idx.T, RHOB_idx.T), axis=1)

                    RHOB = pd.DataFrame(RHOB, columns=('Depth', 'RHOB'))

                    RHOB = RHOB.sort_values(by='Depth', axis=0, ascending=True, kind='mergesort', na_position='last').reset_index(drop=True)

                    RHOB = RHOB.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)   
                    
        
        return DT, RHOB

def fill_gaps(las_files, N_files, DT, RHOB):
        
        
    """ 
    Ex.: DT, RHOB = pytie.fill_gaps(las_files, N_files, DT, RHOB)

    This function checks if there are gaps in the depth parameter.

    Inputs: 

    las_file = add the folder and file(s) address(es). 
    N-files = attribute the number of files to be imported.
    DT = DT log integrated - Panda DataFrame
    RHOB  = RHOB log integrated - Panda DataFrame

    Outputs:

    DT = DT log integrated - Panda DataFrame
    RHOB = RHOB log integrated - Panda DataFrame

    """ 
    
    if DT.size != RHOB.size:
    
        if N_files == 1:
            log0 = lasio.read(las_files)
        
        else:
            log0 = lasio.read(las_files[0])
        
        
        STEP = log0.well.step.value

        Dept = DT['Depth'].values

        for i in range(Dept.size - 1):
            if np.round((Dept[i+1] - Dept[i]), decimals=4) != STEP:
                start_1 = Dept[i]
                end_1 = Dept[i+1]

                Depth_1 = np.array([np.arange(start_1+STEP, end_1, STEP)]).T
                dt = np.array([np.full(Depth_1.size, np.nan)]).T

                data_d = pd.DataFrame(np.concatenate((Depth_1,dt), axis=1), columns= ('Depth', 'DT'))

                DT = DT.append(data_d).sort_values(by=['Depth'], na_position='last').reset_index(drop=True)

                DT['Depth'] = DT.Depth.astype(str)
                DT = DT.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
                DT['Depth'] = DT.Depth.astype(float)


        Dept2 = RHOB['Depth'].values

        for i in range(Dept2.size - 1):
            if np.round((Dept2[i+1] - Dept2[i]), decimals=4) != STEP:
                start_2 = Dept2[i]
                end_2 = Dept2[i+1]

                Depth_2 = np.array([np.arange(start_2+STEP, end_2, STEP)]).T
                rhob = np.array([np.full(Depth_2.size, np.nan)]).T

                data_r = pd.DataFrame(np.concatenate((Depth_2,rhob), axis=1), columns= ('Depth', 'RHOB'))

                RHOB = RHOB.append(data_r).sort_values(by=['Depth'], na_position='last').reset_index(drop=True)

                RHOB['Depth'] = RHOB.Depth.astype(str)
                RHOB = RHOB.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
                RHOB['Depth'] = RHOB.Depth.astype(float)


        return DT, RHOB

    else:
        print 'User: DT and RHOB have already the same number of samples. This operation is not necessary.'

    
def fill_log(N_files, las_files, DT, RHOB):

    """
    Ex.: DEPTH, DT, RHOB = fill_log(N_files, las_files, DT, RHOB)
    
    Fills the gaps at the beginning and at the end of the logs.
    
    Inputs:
    
    las_file = add the folder and file(s) address(es). 
    N-files = attribute the number of files to be imported.
    DT = DT log integrated - Panda DataFrame
    RHOB = RHOB log integrated - Panda DataFrame

    
    Outputs:
    
    DEPTH = numpy array - vector
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    
    """
    
    
    if N_files == 1:
        log0 = lasio.read(las_files)
        
    else:
        log0 = lasio.read(las_files[0])
    
    STEP = log0.well.step.value


    if RHOB['Depth'].iloc[0] > DT['Depth'].iloc[0]:
        Depth = np.array([np.arange(DT['Depth'].iloc[0], RHOB['Depth'].iloc[0], STEP)]).T
        nan = np.array([np.full(Depth.size, np.nan)]).T
        data1 = pd.DataFrame(np.concatenate((Depth,nan), axis=1), columns= ('Depth', 'RHOB'))
        RHOB = RHOB.append(data1).sort_values(by=['Depth'],na_position='last').reset_index(drop=True)

        RHOB['Depth'] = RHOB.Depth.astype(str)
        RHOB = RHOB.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
        RHOB['Depth'] = RHOB.Depth.astype(float)

    if RHOB['Depth'].iloc[0] < DT['Depth'].iloc[0]:
        Depth = np.array([np.arange(RHOB['Depth'].iloc[0], DT['Depth'].iloc[0]-STEP, STEP)]).T
        nan = np.array([np.full(Depth.size, np.nan)]).T
        data2 = pd.DataFrame(np.concatenate((Depth,nan), axis=1), columns= ('Depth', 'DT'))
        DT = DT.append(data2).sort_values(by=['Depth'],na_position='last').reset_index(drop=True)

        DT['Depth'] = DT.Depth.astype(str)
        DT = DT.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
        DT['Depth'] = DT.Depth.astype(float)

    if RHOB['Depth'].iloc[-1] > DT['Depth'].iloc[-1]:
        Depth = np.array([np.arange(DT['Depth'].iloc[-1]+STEP, RHOB['Depth'].iloc[-1]+STEP, STEP)]).T
        nan = np.array([np.full(Depth.size, np.nan)]).T
        data3 = pd.DataFrame(np.concatenate((Depth,nan), axis=1), columns= ('Depth', 'DT'))
        DT = DT.append(data3).sort_values(by=['Depth'],na_position='last').reset_index(drop=True).reset_index(drop=True)

        DT['Depth'] = DT.Depth.astype(str)
        DT = DT.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
        DT['Depth'] = DT.Depth.astype(float)

    if RHOB['Depth'].iloc[-1] < DT['Depth'].iloc[-1]:
        Depth = np.array([np.arange(RHOB['Depth'].iloc[-1]+STEP, DT['Depth'].iloc[-1], STEP)]).T
        nan = np.array([np.full(Depth.size, np.nan)]).T
        data4 = pd.DataFrame(np.concatenate((Depth,nan), axis=1), columns= ('Depth', 'RHOB'))
        RHOB = RHOB.append(data4).sort_values(by=['Depth'],na_position='last').reset_index(drop=True).reset_index(drop=True)

        RHOB['Depth'] = RHOB.Depth.astype(str)
        RHOB = RHOB.drop_duplicates(subset='Depth', keep='first', inplace=False).reset_index(drop=True)
        RHOB['Depth'] = RHOB.Depth.astype(float)


     
    if RHOB.size > DT.size:
        add1 = DT.iloc[-1]+STEP
        DT = DT.append(add1)

    if DT.size > RHOB.size:
        add2 = RHOB.iloc[-1]+STEP
        RHOB = RHOB.append(add2)

        

        
    DEPTH = RHOB['Depth'].values
    DT = DT['DT'].values
    RHOB = RHOB['RHOB'].values   
    
    return DEPTH, DT, RHOB

    


def rhob_fill_gardner(RHOB, DT, alfa=0.23, beta=0.25):
    """
    Ex.: RHOB_fill = pytie.rhob_fill_gardner(RHOB, DT, alfa, beta)

    This function fills missing data in the RHOB log based on the Gardner's equation. 
    
    Inputs:
    
    RHOB = Bulk density log - numpy array - vector
    DT = Sonic log - numpy array - vector
    alfa = parameter of the Gardner's equation. Default value = 0.23
    beta = parameter of the Gardner's equation. Default value = 0.25
    
    Output:
    
    RHOB_fill = Bulk density log (filled) - numpy array - vector
    
    """

    RHOB_fill = np.nan_to_num(RHOB)
    for i in range(RHOB.size):
        if RHOB_fill[i] == 0:
            Vp = (1e6/DT[i])    # in feet/s
            RHOB_g = alfa*Vp**beta        # density estimated by the Gardner's equation
            np.put(RHOB_fill, [i], RHOB_g)
        
    return RHOB_fill
  
        
        
def DT_fill_gardner(RHOB,DT, gamma=355):
    """
    Ex.: DT_fill = pytie.DT_fill_gardner(RHOB,DT, gamma)

    This function fills missing data in the DT log based on the Gardner's inverse equation. 
    
    Inputs:
    
    RHOB = Bulk density log - numpy array - vector
    DT = Sonic log - numpy array - vector
    gamma = parameter of the Gardner's inverse equation. Default value = 355
    
    Output:
    
    DT_fill = Sonic log (filled)
    
    """

    DT_fill = np.nan_to_num(DT)
    for i in range(DT.size):
        if DT_fill[i] == 0:
            Vp_g = (gamma*((RHOB[i])**4))*0.3048    # Velocity of the P wave in m/s
            DT_g = 1e6/(Vp_g/0.3048)   # Vagarosity of the P wave - DT log
            np.put(DT_fill, [i], DT_g)
            
    return DT_fill
        
        
def delete_NaN(DEPTH, DT, RHOB):
    """
    Ex.: DEPTH, DT, RHOB = pytie.delete_NaN(DEPTH, DT, RHOB)

    This function deletes NaN values. This step is necessary if you plan to use SciKit-Learn functions.
    
    Inputs: 
    
    DEPTH = numpy array - vector
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    
    Outputs: 
    
    DEPTH = numpy array - vector
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    
    """
    
    DEPTH = DEPTH.reshape(-1, len(DEPTH)).T
    DT = DT.reshape(-1, len(DT)).T
    RHOB = RHOB.reshape(-1, len(RHOB)).T
    
    data = np.concatenate((DEPTH, DT, RHOB), axis=1) 
    data = pd.DataFrame(data, columns=('Depth', 'DT', 'RHOB'))
    data = data.dropna().reset_index(drop=True)
    
    DEPTH = data['Depth'].values
    DT = data['DT'].values
    RHOB = data['RHOB'].values
    
    return DEPTH, DT, RHOB
    
    

def sea_water_vel(sea_bottom_depth):
    """
    Ex.: vel_predict = pytie.sea_water_vel(sea_bottom_depth)

    This function predicts the velocity of the sea water based on the sea bottom depth.
    
    Input:
    
    sea_bottom_depth = float or integer - scalar
    
    Output:
    
    vel_predict = predicted velocity - float or integer - scalar
    
    """

    vel_predict = 1517.2459 + 0.01776 * sea_bottom_depth
    
    return vel_predict   # Velocity in m/s
    


def ext_line(d_sediment, ground_level, DEPTH, DT, RHOB, STEP, depth_source=5.0): 
    """
    Ex.: DEPTH, DT, RHOB = pytie.ext_line(d_sediment, ground_level, DEPTH, DT, RHOB, STEP, depth_source)
    
    This function creates a line between the surface/sea surface and the first log registers.
    
    Inputs: 
    
    d_sediment = sediment density - float or integer - scalar
    depth_source = depth of the seismic source (generally 5 meters) - float or integer -scalar
    ground_level = altitude of the well location or the batimetry (negative values) - float or integer - scalar
    DEPTH = Depth index - numpy array - vector
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    STEP = sample interval - integer or float - scalar
    
    Outputs:
    
    DEPTH = numpy array - vector
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    
    """
    
    intercept = 1517.245944868534

    slope = 0.017764004040775282
    
    if ground_level < 0:
        
        # DT_log
        
        # Line between the source and the sea bottom:
        
        SB = ground_level*-1   # because the values are the measured depth
        
        X = np.arange(depth_source, SB, STEP)
        
        V_sea = intercept + slope * X
        
        DT_sea = (1./V_sea)*1e6*0.3048   # Us/feet
        
        
        # Line between the sea bottom and the first registers: 
        
        V_sed = (355*((d_sediment)**4))*0.3048    # in m/s
        
        DT_sed = 1e6/(V_sed/0.3048)   # converting m/s to Us/foot
        
        X2 = np.arange(SB, DEPTH[0],STEP)
        
        average = DT[:10].sum()/10
        
        DT_fix = np.linspace(DT_sed, average, num=X2.size)
        
        
        # RHOB log
    
        # Line between the source and the sea bottom:
        
        RHOB_sea = 1.025   # g/cm3
        
        RHOB_f = np.ones(X.shape)
        
        RHOB_f = RHOB_f*RHOB_sea
        
        
        # Line between the sea bottom and the first registers: 
        
        average = RHOB[:10].sum()/10
        
        RHOB_fix = np.linspace(d_sediment, average, num=X2.size)
        
        # Inserting the values
        
        DEPTH = np.insert(DEPTH, 0, X2)
        DEPTH = np.insert(DEPTH, 0, X)
        
        DT = np.insert(DT, 0, DT_fix)
        DT = np.insert(DT, 0, DT_sea)
        
        RHOB = np.insert(RHOB, 0, RHOB_fix)
        RHOB = np.insert(RHOB, 0, RHOB_f)
        
        return DEPTH, DT, RHOB

    if ground_level >= 0:
        
        V_sed = (355*((d_sediment)**4))*0.3048    # in m/s
        
        DT_sed = 1e6/(V_sed/0.3048)   # converting m/s to Us/foot
        
        X = np.arange(depth_source, DEPTH[0],STEP)
        
        average = DT[:10].sum()/10
        
        DT_fix = np.linspace(DT_sed, average, num=X.size)
        
        average2 = RHOB[:10].sum()/10
        
        RHOB_fix = np.linspace(d_sediment, average2, num=X.size)
        
        
        # Inserting the values
        
        DEPTH = np.insert(DEPTH, 0, X)
        
        DT = np.insert(DT, 0, DT_fix)
        
        RHOB = np.insert(RHOB, 0, RHOB_fix)
        
        
        return DEPTH, DT, RHOB
        
        
        
        
def moving_average( data, DEPTH, window_size=15):
    """
    Ex.: DEPT_fil, data = pytie.moving_average(data,  DEPTH, window_size)
    
    This function calculates the moving average using the convolution method.
    
    The convolution operator is iqual to the window size, one of the inputs. The window
    size must be an odd number greater than 3. 
    
    Inputs:
    
    data = DT or RHOB logs - numpy array - vector 
    window_size = odd integer greater than 3 and smaller than the data size - scalar
    DEPTH = Depth index - numpy array - vector
    
    Outputs:
    
    DEPT_fil = numpy array - vector
    data = numpy array - vector (filtered)

    """

    # Verifies if the size of the window is odd:
    
    if window_size%2 !=1 or window_size < 3:
        raise TypeError("The size of the window must be greater than 3 and an odd, integer and positive number.")
    
    if window_size >= data.size:
        raise TypeError("The data must have more elements than the window size.")
    
    assert window_size >= 3, 'The window must be greater than 3'

    window = np.ones(int(window_size))/float(window_size)     
        
    data = np.convolve(data, window, 'same') 
    
    DEPT_fil = DEPTH[int(window_size/2):-int(window_size/2)]
    
    return DEPT_fil, data[int(window_size/2):-int(window_size/2)]
    
    
def despike_filter( data, DEPTH, window_size = 15, std=1):
    """
    Ex.: data_new = pytie.despike_filter( data, DEPTH, window_size, std)
    
    This function remove the spykes based on the results of the moving average function.
    
    Inputs:
    
    data = DT or RHOB logs - numpy array - vector
    DEPTH = Depth index - numpy array - vector
    window_size = odd integer greater than 3 and smaller than the data size - scalar
    std = standard deviation - integer - scalar
    
    Output:
    
    data_new = data filtered - numpy array - vector
    
    """

    DEPTH_fil, baseline = moving_average(data, DEPTH, window_size)
    
    diff = int(window_size/2)
    
    noise = data[diff:-diff] - baseline
    threshold = std * np.std(noise)
    mask = np.abs(noise) > threshold
    idx = np.array(np.where(mask == True), ndmin=0)
    
    for i in range(idx.size):
        idx[0][i] = idx[0][i]+diff
    
    data_new = np.copy(data)
    
    for i in range(idx.size):
        np.put(data_new, idx[0][i], baseline[idx[0][i]-diff])
    
    return data_new

    
def impedance(DT,RHOB):
    """
    Ex.: I = pytie.impedance(DT,RHOB)

    This function calculates the acoustic impedance. 

    Inputs: 
    
    DT = Sonic log - numpy array - vector
    RHOB = Bulk density log - numpy array - vector
    
    Output:
    
    I = Acoustic impedance - numpy array - vector
    
    """

    I = DT*RHOB
    
    return I
    


def r_coef(I):
    """
    Ex.: R_coef = pytie.r_coef(I)

    This function calculates the reflexion coefficients. 

    Input: 
    
    I = acoustic impedance - numpy array - vector
    
    Output:
    
    R_coef = reflection coefficients - numpy array - vector

    """

    R_coef=[]
    for i in range(I.size-1):
        coef=(I[i+1]-I[i])/(I[i+1]+I[i])
        R_coef = np.append(R_coef, coef)
        R_coef = np.nan_to_num(R_coef)
        
    return R_coef
 
 
 
def syn_seis( R_coef, f=20, length=0.512, dt=0.0004):
    """
    Ex.: seismogram = pytie.syn_seis( R_coef, f, length, dt)

    This function creates the synthetic seismogram convolving the reflexion coefficients with a ricker 
    wavelet. You can choose a frequency, a length and a time interval (dt).

    Inputs:
    R_coef = array of reflexion coefficients
    f =  dominant frequency 
    length = length of the wavelet
    dt = time interval of the wavelet
    """
    
    t = np.arange(-length/2, length/2, dt)
    wavelet = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    
    seismogram = np.convolve(R_coef, wavelet, mode='same')
    
    return seismogram
    
    


# Create the figure and subplots
def combo_plot1(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram, title='Synthetic Seismogram'):
    """
    Ex.: pytie.combo_plot1(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram)

    Shows the results of the integrated logs with geological markers plotted on the logs, 
    reflexion coefficients and synthetic seismogram.
    
    Inputs:
    
    top_depth = integer or float - scalar
    bottom_depth = integer or float - scalar
    title = if not mentioned, default value = 'Synthetic Seismogram'
    depths_markers = integer or float - scalar
    markers = name of the markers
    RHOB = Bulk density log - numpy array - vector
    DEPTH = Depth index - numpy array - vector
    DT = Sonic log - numpy array - vector
    R_coef = reflection coefficients - numpy array - vector
    seismogram = numpy array - vector
    
    Output:
    
    Matplotlib graph

    """
    
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(16,9), sharey=True)
    fig.suptitle(title, fontsize=22)
    fig.subplots_adjust(top=0.8,wspace=0.1)
    
#General setting for all axis
    for axes in ax:
        axes.set_ylim (top_depth,bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.get_xaxis().set_visible(False) 
        for (i,j) in zip(depths_markers,markers):
            if ((i>=top_depth) and (i<=bottom_depth)):
                axes.axhline(y=i, linewidth=0.5, color='black')
                axes.text(0.2, i ,j, horizontalalignment='left',verticalalignment='top')
    
#1st track: DT
    
    ax01=ax[0].twiny()
    ax01.set_xlim(240.0,40.0)
    ax01.spines['top'].set_position(('outward',0))
    ax01.set_xlabel("DT [Us/foot]")
    ax01.plot(DT, DEPTH, label='DT[Us/foot]', color='black')
    ax01.set_xlabel('DT[Us/foot]',color='black')    
    ax01.tick_params(axis='x', colors='black')
    ax01.grid(True)
    
#2nd track: RHOB

    ax11=ax[1].twiny()
    ax11.set_xlim(0,3.0)
    ax11.grid(True)
    ax11.spines['top'].set_position(('outward',0))
    ax11.set_xlabel('RHOB[g/cc]', color='red')
    ax11.plot(RHOB, DEPTH, label='RHOB[g/cc]', color='red')
    ax11.tick_params(axis='x', colors='red') 
    
#3nd track: COEF
    
    ax21=ax[2].twiny()
    ax21.set_xlim(-0.5,0.5)
    ax21.spines['top'].set_position(('outward',0))
    ax21.set_xlabel("Reflection Coefficients")
    
    x = R_coef
    y = DEPTH[1:]
    
    ax21.hlines(y, 0, x, color='blue')
    #ax21.plot(x, y, 'D')  # Stem ends
    ax21.grid(True)   
    
#4nd track: Synthetic Seismogram
    
    ax31=ax[3].twiny()
    ax31.set_xlim(-1,1)
    ax31.spines['top'].set_position(('outward',0))
    ax31.set_xlabel("Synthetic Seismogram")
    ax31.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.2)  
    ax31.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax31.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax31.grid(True)  
    
    ax32=ax[3].twiny()
    ax32.set_xlim(-0.8,1.2)
    ax32.xaxis.set_visible(False)
    ax32.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax32.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax32.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax33=ax[3].twiny()
    ax33.set_xlim(-0.6,1.4)
    ax33.xaxis.set_visible(False)
    ax33.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax33.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax33.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax34=ax[3].twiny()
    ax34.set_xlim(-1.2,0.8)
    ax34.xaxis.set_visible(False)
    ax34.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax34.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax34.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax35=ax[3].twiny()
    ax35.set_xlim(-1.4,0.6)
    ax35.xaxis.set_visible(False)
    ax35.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax35.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax35.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    
    #plt.savefig ('RJS_51.png', dpi=200, format='png')
    
    
    
    
def gain( initial_depth, DEPTH, R_coef, mag=1, length=0.512, dt=0.0004, f=20):
    """
    Ex.: gain, seismogram_gain = pytie.gain( initial_depth, DEPTH, R_coef, mag, length, dt, f)

    This function applies gain to the synthetic seismogram.
    
    Inputs:
    
    mag = magnitude of the gain. Default value = 1 - integer - scalar
    initial_depth = integer or float - scalar
    DEPTH = numpy array - vector
    R_coef = numpy array - vector
    length = default value = 0.512 - integer or float - scalar
    dt = default value = 0.0004 - integar or float - scalar
    f = default value = 20 - integer or float - scalar
    
    Outputs:
    
    gain = numpy array - vector
    seismogram_gain = numpy array - vector

    """
    idx = np.where(DEPTH >= initial_depth)
    g = (R_coef[idx[0][0]:]*DEPTH[idx[0][0]:-1])/(mag*1000)
    
    gain = np.concatenate((R_coef[:(idx[0][0])], g))
    
    t = np.arange(-length/2, length/2, dt)
    wavelet = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    
    seismogram_gain = np.convolve(gain, wavelet, mode='same')
    
    return gain, seismogram_gain
    
    

# Create the figure and subplots
def combo_plot2(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram, seismogram_gain, img_adr, title = 'Comparison between seismograms with and without gain'):
    """
    
    Ex.: pytie.combo_plot2(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram, seismogram_gain, img_adr, title)

    This function shows the comparison between the seismogram with and without gain plus the imagem of the seismic section.
    
    Inputs: 
    
    top_depth = integer or float - scalar
    bottom_depth = integer or float - scalar
    title = default value: 'Comparison between seismograms with and without gain'
    depths_markers = integer or float - scalar
    markers = name of the markers
    RHOB = Bulk density log - numpy array - vector
    DEPTH = Depth index - numpy array - vector
    DT = Sonic log - numpy array - vector
    R_coef = numpy array - vector
    seismogram - numpy array - vector
    seismogram_gain = numpy array - vector
    img_adr = address of an image with seismic around the well site.
    
    Output:
    
    Matplotlib graph
    

    """
    
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(16,9), sharey=True)
    fig.suptitle(title, fontsize=22)
    fig.subplots_adjust(top=0.8,wspace=0.1)
    
#General setting for all axis
    for axes in ax:
        axes.set_ylim (top_depth,bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.get_xaxis().set_visible(False) 
        for (i,j) in zip(depths_markers,markers):
            if ((i>=top_depth) and (i<=bottom_depth)):
                axes.axhline(y=i, linewidth=0.5, color='black')
                axes.text(0.2, i ,j, horizontalalignment='left',verticalalignment='top')
    
    
#1nd track: COEF
    
    ax01=ax[0].twiny()
    ax01.set_xlim(-0.5,0.5)
    ax01.spines['top'].set_position(('outward',0))
    ax01.set_xlabel("Reflection Coefficients")
    
    x = R_coef
    y = DEPTH[1:]
    
    ax01.hlines(y, 0, x, color='blue')
    #ax21.plot(x, y, 'D')  # Stem ends
    ax01.grid(True)   
    
#2nd track: Synthetic Seismogram
    
    ax11=ax[1].twiny()
    ax11.set_xlim(-1,1)
    ax11.spines['top'].set_position(('outward',0))
    ax11.set_xlabel("Synthetic Seismogram")
    ax11.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.2)  
    ax11.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax11.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax11.grid(True)  
    
    ax12=ax[1].twiny()
    ax12.set_xlim(-0.8,1.2)
    ax12.xaxis.set_visible(False)
    ax12.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax12.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax12.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax13=ax[1].twiny()
    ax13.set_xlim(-0.6,1.4)
    ax13.xaxis.set_visible(False)
    ax13.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax13.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax13.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax14=ax[1].twiny()
    ax14.set_xlim(-1.2,0.8)
    ax14.xaxis.set_visible(False)
    ax14.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax14.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax14.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax15=ax[1].twiny()
    ax15.set_xlim(-1.4,0.6)
    ax15.xaxis.set_visible(False)
    ax15.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax15.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax15.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
      
    #3nd track: Synthetic Seismogram with gain
    
    ax21=ax[2].twiny()
    ax21.set_xlim(-1,1)
    ax21.spines['top'].set_position(('outward',0))
    ax21.set_xlabel("Seismogram with gain")
    ax21.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.2)  
    ax21.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax21.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax21.grid(True)  
    
    ax22=ax[2].twiny()
    ax22.set_xlim(-0.8,1.2)
    ax22.xaxis.set_visible(False)
    ax22.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax22.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax22.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax23=ax[2].twiny()
    ax23.set_xlim(-0.6,1.4)
    ax23.xaxis.set_visible(False)
    ax23.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax23.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax23.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax24=ax[2].twiny()
    ax24.set_xlim(-1.2,0.8)
    ax24.xaxis.set_visible(False)
    ax24.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax24.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax24.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax25=ax[2].twiny()
    ax25.set_xlim(-1.4,0.6)
    ax25.xaxis.set_visible(False)
    ax25.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax25.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax25.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    
    # image of the seismic
    
    import matplotlib.image as mpimg
    ax31=ax[3].twiny()
    img = mpimg.imread(img_adr)
    imgplot = ax31.imshow(img)
    
    
    #plt.savefig ('RJS_51.png', dpi=200, format='png')
    
    
    

def freq_corr( depth_change, DEPTH, gain, f=20, length=0.512, dt=0.0004):
    """
    Ex.: seism_freq = pytie.freq_corr( depth_change, DEPTH, gain, f, length, dt)

    This function changes the frequency of the synthetic seismogram to a lower frequency from a certain 
    depth (depth_change). 
    
    Inputs:
    
    f = frequency of the wavelet - integer or float - scalar
    depth_change = depth of the change in frequency - integer or float - scalar
    DEPTH = numpy array - vector
    length = integer or float - scalar
    dt = integer or float - scalar
    gain = numpy array - vector
    
    Output:
    
    seism_freq = numpy array - vector

    """
    
    freq = f*0.6
    idx = np.where(DEPTH >= depth_change)
    
    t = np.arange(-length/2, length/2, dt)
    wavelet1 = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    wavelet2 = (1.-2.*(np.pi**2)*(freq**2)*(t**2))*np.exp(-(np.pi**2)*(freq**2)*(t**2))
    
    seismogram1 = np.convolve(gain[:idx[0][0]], wavelet1, mode='same')
    seismogram2 = np.convolve(gain[idx[0][0]:], wavelet2, mode='same')
    seism_freq = np.concatenate((seismogram1, seismogram2), axis=0)
    
    return seism_freq
    
    
    
# Create the figure and subplots
def combo_plot3(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram, seismogram_gain, seism_freq, title='Comparison between seismograms with and without change in frequency'):
    """
    Ex.: pytie.combo_plot3(top_depth,bottom_depth, depths_markers, markers, RHOB, DEPTH, DT, R_coef, seismogram, seismogram_gain, seism_freq, title)

    This function shows the comparison between the seismogram with and without change in frequency.
    
    Inputs:
    
    top_depth = integer or float - scalar
    bottom_depth = integer or float - scalar
    title='Comparison between seismograms with and without change in frequency'
    depths_markers = list 
    markers = name of the markers
    RHOB = Bulk density log - numpy array - vector
    DEPTH = Depth index - numpy array - vector
    DT = Sonic log - numpy array - vector
    R_coef = numpy array - vector
    seismogram - numpy array - vector
    seismogram_gain = numpy array - vector
    seism_freq = numpy array - vector
    
    Output:
    
    Matplotlib graph

    """
    
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(16,9), sharey=True)
    fig.suptitle(title, fontsize=22)
    fig.subplots_adjust(top=0.8,wspace=0.1)
    
#General setting for all axis
    for axes in ax:
        axes.set_ylim (top_depth,bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.get_xaxis().set_visible(False) 
        for (i,j) in zip(depths_markers,markers):
            if ((i>=top_depth) and (i<=bottom_depth)):
                axes.axhline(y=i, linewidth=0.5, color='black')
                axes.text(0.2, i ,j, horizontalalignment='left',verticalalignment='top')
    
    
#1nd track: COEF
    
    ax01=ax[0].twiny()
    ax01.set_xlim(-0.5,0.5)
    ax01.spines['top'].set_position(('outward',0))
    ax01.set_xlabel("Reflection Coefficients")
    
    x = R_coef
    y = DEPTH[1:]
    
    ax01.hlines(y, 0, x, color='blue')
    #ax21.plot(x, y, 'D')  # Stem ends
    ax01.grid(True)   
    
#2nd track: Synthetic Seismogram
    
    ax11=ax[1].twiny()
    ax11.set_xlim(-1,1)
    ax11.spines['top'].set_position(('outward',0))
    ax11.set_xlabel("Synthetic Seismogram")
    ax11.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.2)  
    ax11.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax11.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax11.grid(True)  
    
    ax12=ax[1].twiny()
    ax12.set_xlim(-0.8,1.2)
    ax12.xaxis.set_visible(False)
    ax12.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax12.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax12.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax13=ax[1].twiny()
    ax13.set_xlim(-0.6,1.4)
    ax13.xaxis.set_visible(False)
    ax13.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax13.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax13.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax14=ax[1].twiny()
    ax14.set_xlim(-1.2,0.8)
    ax14.xaxis.set_visible(False)
    ax14.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax14.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax14.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax15=ax[1].twiny()
    ax15.set_xlim(-1.4,0.6)
    ax15.xaxis.set_visible(False)
    ax15.plot(seismogram, DEPTH[1:], lw=1, color='black', alpha=0.0)  
    ax15.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram > 0., interpolate=False, color='blue', alpha = 0.5)
    ax15.fill_betweenx(DEPTH[1:], seismogram, 0., seismogram < 0., interpolate=False, color='red', alpha = 0.5)
      
    #3nd track: Synthetic Seismogram with gain
    
    ax21=ax[2].twiny()
    ax21.set_xlim(-1,1)
    ax21.spines['top'].set_position(('outward',0))
    ax21.set_xlabel("Seismogram with gain")
    ax21.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.2)  
    ax21.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax21.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax21.grid(True)  
    
    ax22=ax[2].twiny()
    ax22.set_xlim(-0.8,1.2)
    ax22.xaxis.set_visible(False)
    ax22.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax22.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax22.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax23=ax[2].twiny()
    ax23.set_xlim(-0.6,1.4)
    ax23.xaxis.set_visible(False)
    ax23.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax23.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax23.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax24=ax[2].twiny()
    ax24.set_xlim(-1.2,0.8)
    ax24.xaxis.set_visible(False)
    ax24.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax24.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax24.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax25=ax[2].twiny()
    ax25.set_xlim(-1.4,0.6)
    ax25.xaxis.set_visible(False)
    ax25.plot(seismogram_gain, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax25.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain > 0., interpolate=False, color='blue', alpha = 0.5)
    ax25.fill_betweenx(DEPTH[:-1], seismogram_gain, 0., seismogram_gain < 0., interpolate=False, color='red', alpha = 0.5)
    
    # Seismogram with two frequencies
    
    ax31=ax[3].twiny()
    ax31.set_xlim(-1,1)
    ax31.spines['top'].set_position(('outward',0))
    ax31.set_xlabel("Seismogram with two frequencies")
    ax31.plot(seism_freq, DEPTH[:-1], lw=1, color='black', alpha=0.2)  
    ax31.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq > 0., interpolate=False, color='blue', alpha = 0.5)
    ax31.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax31.grid(True)  
    
    ax32=ax[3].twiny()
    ax32.set_xlim(-0.8,1.2)
    ax32.xaxis.set_visible(False)
    ax32.plot(seism_freq, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax32.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq > 0., interpolate=False, color='blue', alpha = 0.5)
    ax32.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax33=ax[3].twiny()
    ax33.set_xlim(-0.6,1.4)
    ax33.xaxis.set_visible(False)
    ax33.plot(seism_freq, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax33.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq > 0., interpolate=False, color='blue', alpha = 0.5)
    ax33.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax34=ax[3].twiny()
    ax34.set_xlim(-1.2,0.8)
    ax34.xaxis.set_visible(False)
    ax34.plot(seism_freq, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax34.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq > 0., interpolate=False, color='blue', alpha = 0.5)
    ax34.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq < 0., interpolate=False, color='red', alpha = 0.5)
    
    ax35=ax[3].twiny()
    ax35.set_xlim(-1.4,0.6)
    ax35.xaxis.set_visible(False)
    ax35.plot(seism_freq, DEPTH[:-1], lw=1, color='black', alpha=0.0)  
    ax35.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq > 0., interpolate=False, color='blue', alpha = 0.5)
    ax35.fill_betweenx(DEPTH[:-1], seism_freq, 0., seism_freq < 0., interpolate=False, color='red', alpha = 0.5)
    
    
    #plt.savefig ('RJS_51.png', dpi=200, format='png')
    
    


def time_depth(N_files, las_files, DT, DEPTH):
    """
    Ex.:time_depth_table = pytie.time_depth(N_files, las_files, DT, DEPTH)

    This function creates the time-depth table.
    
    Inputs: 
    
    N_files = number of files imported
    las_files = address and name of the files
    DT = Sonic log - numpy array - vector
    DEPTH = Depth index - numpy array - vector
    
    Output:
    
    time_depth_table = Pandas DataFrame

    """
    
    if N_files == 1:
        log0 = lasio.read(las_files)
        
    else:
        log0 = lasio.read(las_files[0])
    
    STEP = log0.well.step.value
    
    Vp = (1e6/DT)*0.3048
    
    ti=0
    time = []
    t_d_table = []
    

    for i in range(DT.size):
        t = (STEP*2)/ Vp[i]   
        ti = (t + ti)
        time = np.append(time, ti)

    time = time*1000     # in milliseconds
    
    Time = np.array([time])
    Depth = np.array([DEPTH])   # Measured depth

    t_d_table = np.concatenate((Depth.T, Time.T), axis=1)
    
    time_depth_table = pd.DataFrame(t_d_table, columns=('Depth (m)','Time (ms)'))
    
    return time_depth_table
    
    
    
    
