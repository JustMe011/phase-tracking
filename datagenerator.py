
############# SIMULATOR OF THE COHERENT RECEIVER CHANNELS ############
####         main function input: 3 functions, 2 integers                    
#### 			   output: 4-channels data file, parameters plot,
####				   poincare' sphere 


from numpy import *
import matplotlib.colors
import csv
from matplotlib.pyplot import *
matplotlib.use("TkAgg") #setting Tk ad windows manager
from mpl_toolkits.mplot3d import Axes3D

def datagen(fundel,funthe,funphi, points,sphere):

	### jordan matrix model R(-t)M(d)R(t)
	def fibmod(delta,theta,phi):
		R1=array([[cos(theta),sin(theta)],[-sin(theta),cos(theta)]])
		M=array([[e**(1j*(-delta/2)),0],[0,e**(1j*(delta/2))]])
		R2=transpose(R1)
		Ein=array([cos(pi/4)*e**(1j*(pi/2)),sin(pi/4)])*e**(1j*(phi))
		return R2.dot(M.dot(R1.dot(Ein)))

	#####################################

	t,rex,imx,rey,imy,Sq,Su,Sv,dellist,thelist,philist=[],[],[],[],[],[],[],[],[],[],[]
	dd,pp,tt=0,0,0


	for i in arange(points):
		dd=fundel(i)
		tt=funthe(i)
		pp=funphi(i)
		dellist.append(dd)
		thelist.append(tt)
		philist.append(pp)

		Eout=fibmod(dd,tt,pp)
		Exr=Eout[0].real
		Exi=Eout[0].imag
		Eyr=Eout[1].real
		Eyi=Eout[1].imag
		rex.append(Exr)
		imx.append(Exi)
		rey.append(Eyr)
		imy.append(Eyi)
		
		t.append(i*4*10**(-7))

		Sq.append(Exr**2 + Exi**2 - Eyr**2 - Eyi**2)
		Su.append(2*(Exr*Eyr + Exi*Eyi))
		Sv.append(2*(Exi*Eyr - Exr*Eyi))


	###########writing file################
	outlist=list(zip(t,rex,imx,rey,imy))
	f=open("eout.csv",'w')
	w=csv.writer(f, delimiter='\t')
	w.writerows(outlist)
	f.close()

	outphilist=list(zip(philist))
	f2=open("phidiff.csv",'w')
	w=csv.writer(f2, delimiter='\t')
	w.writerows(outphilist)
	f2.close()

	####plots of the simulated functions#####

	fig1=figure(figsize=(6,4),num="Parameters Plot") #new independent window
	s1=fig1.add_subplot(1,1,1)
	s1=plot(dellist,'r',label="delta")
	s1=plot(thelist,'orange', label="theta")
	s1=plot(philist,'g',label="phi")
	legend()
	mng1= get_current_fig_manager()
	mng1.window.wm_geometry("+800+250")
	if sphere :
		u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
		x = 0.98*np.cos(u)*np.sin(v)
		y = 0.98*np.sin(u)*np.sin(v)
		z = 0.98*np.cos(v)

		fig2=figure(figsize=(6,4),num="Poincare Sphere")
		ax = Axes3D(fig2)
		arrowstyle={'length':2,'arrow_length_ratio':0.05,'color':'black'}
		ax.quiver(0,0,-1.3,0,0,1.3,**arrowstyle)
		ax.quiver(0,-1.3,0,0,1.3,0,**arrowstyle)
		ax.quiver(-1.3,0,0,1.3,0,0,**arrowstyle)
		labelstyle={'color':'black','weight':'bold'}
		ax.text(1.4,0,0,"Q",**labelstyle)
		ax.text(0,1.4,0,"U",**labelstyle)
		ax.text(0,0,1.4,"V",**labelstyle)
		#ax.plot_wireframe(x, y, z, color="r")

		cmap = cm.rainbow
		norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

		ax.scatter(Sq,Su,Sv,s=1,c=cmap(norm(linspace(0,1,points))))
		ax.set_axis_off()
		

		mng2= get_current_fig_manager()	
		mng2.window.wm_geometry("-800+250")

	show() 



