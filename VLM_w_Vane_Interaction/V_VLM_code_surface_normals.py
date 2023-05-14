import V_VLM_code_chordwise_vectors as a
import V_VLM_code_dl_vectors_at075c as b
import numpy as np

#Take cross-products between the dl(s) and dc(s):
normals_lst=[]
for i in range(len(b.total_dl_lst)):
    x_dir=b.total_dl_lst[i][1]*a.total_dc_lst[i][2]-a.total_dc_lst[i][1]*b.total_dl_lst[i][2]
    y_dir=b.total_dl_lst[i][2]*a.total_dc_lst[i][0]-a.total_dc_lst[i][2]*b.total_dl_lst[i][0]
    z_dir=b.total_dl_lst[i][0]*a.total_dc_lst[i][1]-a.total_dc_lst[i][0]*b.total_dl_lst[i][1]
    normals_lst.append(np.array([x_dir,y_dir,z_dir]))
    
