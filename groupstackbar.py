import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D 
from matplotlib import scale as mscale


def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", **kwargs):
	"""Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
	labels is a list of the names of the dataframe, used for the legend
	title is a string for the title of the plot
	H is the hatch used for identification of the different dataframe"""

	n_df = len(dfall)
	n_col = len(dfall[0].columns) 
	n_ind = len(dfall[0].index)
	fig,(axe2,axe) = plt.subplots(1,2,sharey=True)
	#axe = plt.subplot(111)
	df2 = dfall[0] # base case
	df2 = df2/1000.
	axe2 = df2.plot(kind="bar",linewidth=0,stacked=True,
					  ax=axe2,legend=False,grid=False,color=set11,**kwargs)
	hh,ll = axe2.get_legend_handles_labels() # get the handles we want to modify
	ii = 0 #only base case
	for j, pa2 in enumerate(hh[ii:ii+n_col]):
		print j, pa2
		for rect in pa2.patches: # for each index
			rect.set_x(rect.get_x() + 1 / float(n_df + 1) * ii / float(n_col))
			rect.set_width(1 / float(n_df*(n_df + 1)))
			rect.set_edgecolor("w")
	for df in dfall : # for each data frame
		df = df/1000.
		axe = df.plot(kind="bar",
					  linewidth=0,
					  stacked=True,
					  ax=axe,
					  legend=False,
					  grid=False,
					  color=set11,
					  **kwargs)  # make bar plots
	patterns = ['None','None','None','/','/','/','\\','\\','\\','-','-','-','x','x','x']
	h,l = axe.get_legend_handles_labels() # get the handles we want to modify
	for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
		print i
		for j, pa in enumerate(h[i:i+n_col]):
			print j
			for rect in pa.patches: # for each index
				rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
				print rect.get_x() 
				#rect.set_hatch(H * (i / n_col))
				if i == 0:
					
					pass
				else:
					rect.set_hatch(patterns[i])
				rect.set_width(1 / float(n_df + 1))
				rect.set_edgecolor("w")
		#patternInd += 1
	plt.rc('text', usetex=True)
	axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1) ) / 2. + 0.2) #x tick positions
	axe2.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1) ) / 2. + 0.2) #x tick positions
	#axe.set_ylabel('Quantity ('+r"$\times 10^3$"+' kilobarrels per day)',fontsize=24)
	axe.set_ylabel('Quantity (megabarrels per day, mbpd)',fontsize=24)

	axe.set_title(title,fontsize=26)
	for ax in [axe, axe2]:
		ax.set_xticklabels(df.index, rotation = 0,fontsize=22)
		ax.set_xlabel("")
		ax.set_yticklabels(np.arange(0,25,5), fontsize=22)
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)
		#axe.spines['bottom'].set_color('gray')

		ax.tick_params(axis='both', which='major', left='off', bottom='off',top='off',right='off')
		ax.yaxis.set_tick_params(pad=15)
		ax.set_ylim([0,25])
	# Only show ticks on the left and bottom spines
	#axe.yaxis.set_ticks_position('left')
	#axe.xaxis.set_ticks_position('bottom')


	for yy in np.arange(0,25,5):
		opac = 0.4
		zOrd = 0
		if yy==0:
			zOrd = 1000
			opac = 1
		axe.axhline(y=yy, linewidth=4, alpha = opac, color='gray', zorder=zOrd)
		axe2.axhline(y=yy, linewidth=4, alpha = opac, color='gray', zorder=zOrd)

	# Add invisible data to add another legend (Scenarios)
	n=[]  
	for i in range(n_df):
		#n.append(axe.bar(0, 0, color="gray", edgecolor="w",hatch=H * i))
		if i == 0:
			n.append(axe.bar(0, 0, color="gray", edgecolor="w"))
		else:
			n.append(axe.bar(0, 0, color="gray", edgecolor="w", hatch=patterns[i*n_col]))
	# Mode legend
	l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.02, 0.7], handleheight=2, handlelength=4, fontsize=18) 
	if labels is not None:
		l2 = plt.legend(n, labels, loc=[0, -0.15], handleheight=2, handlelength=4, fontsize=16,ncol= n_df)#,mode='expand') 
		#l2 = plt.legend(n, labels, loc=[1.01, 0.2], handleheight=2, handlelength=5, fontsize=18,ncol= 1)#,mode='') 
	axe.add_artist(l1)
	
	axe.lines[0].set_visible(False)
	#mscale.register_scale(CustomScaleFactory(0.5, 2))
	#axe.set_xscale('custom')
	axe2.set_xlim(0.25,.42) # most of the data
	axe.set_xlim(.92,2.92) # outliers only
	return fig
