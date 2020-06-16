import pandas as pd
import matplotlib.pyplot as plt

def getFlows(scenario):
	# try:
	# 	flow = pd.read_excel('./ProdFlows.xlsx','Flows') # read flows from ProdFlows (linked to mfm_report)
	# 	flow = flow[flow.scenario == scenario]
	# except:
	# 	flow = pd.read_excel('./ProdFlows_'+scenario+'.xlsx','Flows') # read flows from ProdFlows (linked to mfm_report)
	flow = pd.read_excel('./ProdFlows_'+scenario+'.xlsx','Flows') # read flows from ProdFlows (linked to mfm_report)
	flow = flow.dropna() # drop zero values
	#flow = flow[flow.node_out!='usa'] # remove USA region (avoid PADD dupes)
	#flow = flow[flow.node_in!='usa'] # remove USA region (avoid PADD dupes)
	flow = flow[flow.disaggregation!='region'] # 10/29/15 - new format
	flow = flow[flow.values!=-1] # remove non-flow (likely redundant)
	# flow.arc = flow.arc.str.split('_').str.get(0) # not necessary (already done in ProdFlows)
	flow = flow[flow.type=='flow'] # consider only flows not caps
	flow = flow[flow.season=='Y'] # restrict to one season to avoid dupes

	# Auxiliary rail nodes are denoted "*_R". Removes this suffix for ease of plotting
	flow.node_out = flow.node_out.str.split('_').str.get(0)
	flow.node_in = flow.node_in.str.split('_').str.get(0)

	flow.drop_duplicates(inplace=True)  # drop duplicate values
	return flow

def scenarioflows(scenario):
	flow = getFlows(scenario)
	df = flow[flow.scenario == scenario]
	#df = df.set_index(['year','arctype'])
	df[df.node_out != 'EC']
	df[df.node_out != 'MX'] 
	df[df.node_out != 'RW'] 
	df[df.node_out != 'WC']
	df[df.node_in != 'RW'] 
	df[df.node_in != 'EC']
	df[df.node_in != 'MX']
	df[df.node_in != 'WC']

	grouped = df.groupby(['year','arctype'])['value'].agg({'value' : np.sum})
	grouped = grouped.reset_index()
	grouped = grouped.pivot(index='year',columns='arctype',values='value')
	grouped = grouped.fillna(0)
	for a in ['BargeR','BargeS','Ship']:
		if a not in grouped.columns:
			grouped[a] = 0
	grouped['Ship/Barge'] = grouped['Ship'] + grouped['BargeS'] + grouped['BargeR']
	grouped = grouped[['Rail','Pipeline','Ship/Barge']]
	if scenario != 'base':
		grouped.ix[2012] = 0
	return grouped


dfBase = scenarioflows('base')
dfBase = dfBase.sort_index()
dfBan = scenarioflows('US_export_ban_lifted')
dfBan = dfBan.sort_index()
dfPipe = scenarioflows('US_midwest_pipelines')
dfPipe = dfPipe.sort_index()
dfCap = scenarioflows('bakken_rail_cap')
dfCap = dfCap.sort_index()
dfBanP = scenarioflows('US_ban_pipelines')
dfBanP = dfBanP.sort_index()



def barFlows():
	plot_clustered_stacked([dfBase, dfCap, dfPipe, dfBan, dfBanP],
		['Base Case','Capping Bakken Rail Flows', 'U.S. Midwest Pipeline Investments', 'U.S. Oil Export Ban Lifted', 'U.S. Exports + Midwest Pipelines + Bakken Rail Caps'],
		title = "")
		#"Annual intra-U.S. multimodal crude oil flows by scenario")
	# plot_clustered_stacked([dfBase, dfPipe, dfCap],
	# 	['Base', 'Capping Flows From Bakken Region', 'US Midwest Pipeline Investments'],
	# 	title = "Annual intra-US multimodal crude oil flows by scenario")
	# 	#ecolor="none")
	plt.subplots_adjust(wspace=0)
	plt.show()	