import matplotlib.pyplot 
import csv
import random
import sys
import os

def generate_dummy_data():
    with open('dummy_data.csv','w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['Week','State_SEIR','Age_Cat','Value'])
        for i in ['Week 1', 'Week 2', 'Week 3']: # 3 weeks
            for j in ['S','E','I','R']:
                for k in ['Age Cat 1', 'Age Cat 2', 'Age Cat 3', 'Age Cat 4', 'Age Cat 5']:
                    csvwriter.writerow([i,j,k, int(random.random()*100)])

generate_dummy_data()


f = plot_grouped_stacks('dummy_data.csv', BGV=['State_SEIR','Week','Age_Cat'], extra_space_on_top = 30)


plt.tight_layout()

plt.savefig("output.png",dpi=500)

