"""Export both committed cases at a 180 mm report width as SVG/PDF/300 dpi PNG."""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
plt.style.use(ROOT/'tools/scientific.mplstyle')
plt.rcParams.update({'pdf.fonttype':42,'savefig.dpi':300,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':10,'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'svg.fonttype':'none','svg.hashsalt':'technical-case-plots','figure.facecolor':'white','axes.facecolor':'white'})
C=['#0072B2','#D55E00']
def save(fig,name,caption):
 fig.subplots_adjust(left=.12,right=.98,bottom=.34,top=.82,wspace=.55)
 fig.text(.02,.025,caption,fontsize=10,va='bottom',linespacing=1.3)
 for extension in ('svg','pdf','png'):
  path=ROOT/'figures'/(Path(name).stem+'.'+extension)
  metadata=({'Date':None} if extension=='svg' else
            {'CreationDate':None,'ModDate':None,'Creator':'Committed local calculation cases'} if extension=='pdf' else None)
  fig.savefig(path,dpi=300,metadata=metadata)
  if extension=='svg': path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 plt.close(fig)

from orbital_trade import evaluate,tangential_impulse,host_recoil
cases=[json.loads((ROOT/'cases'/name).read_text())for name in ['volley_reference.json','hosted_6u_example.json']]
labels=['Historical 3U case','Hosted 6U example']
fig,axes=plt.subplots(1,2,figsize=(7.1,4.8))
for i,c in enumerate(cases):
 x=np.linspace(0,20,81);orbits=[tangential_impulse(c['altitude_m'],v)for v in x]
 axes[0].plot(x,[(o['apogee_altitude_m']-c['altitude_m'])/1000 for o in orbits],color=C[i],ls=['-','--'][i],label=labels[i])
 axes[1].plot(x,[host_recoil(c['payload_mass_kg'],v,c['host_mass_kg'])*1000 for v in x],color=C[i],ls=['-','--'][i],label=labels[i])
axes[0].set(xlabel='Payload inertial tangential\nincrement (m/s)',ylabel='Apogee increase from\ncircular reference (km)',title='a  Two-body orbit geometry')
axes[1].set(xlabel='Payload-to-host relative\nseparation speed (m/s)',ylabel='Remaining-host recoil\nmagnitude (mm/s)',title='b  Finite-host momentum split')
fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,1),ncol=2,frameon=False,fontsize=10)
save(fig,'deployment-trade.svg','Prescribed screens: historical volley_reference and hosted_6u_example; orbital_trade.\nPanel a uses payload inertial increment; panel b uses payload-to-host relative speed.\nTwo-body geometry / exact momentum split; no delivery accuracy. 23 Oct 2026.')
fig,axes=plt.subplots(1,2,figsize=(7.1,4.8))
for i,c in enumerate(cases):
 x=np.linspace(0,20,81);o=[tangential_impulse(c['altitude_m'],v)for v in x]
 axes[0].plot(x,[a['apogee_altitude_m']/1000 for a in o],color=C[i],ls=['-','--'][i],label=labels[i]);axes[1].plot(x,[a['phase_drift_deg_day']for a in o],color=C[i],ls=['-','--'][i])
axes[0].set(xlabel='Payload inertial\nincrement (m/s)',ylabel='Apogee altitude (km)',title='a  Altitude response');axes[1].set(xlabel='Payload inertial\nincrement (m/s)',ylabel='Mean-motion drift\nmagnitude (deg/day)',title='b  Phase-rate response');fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,1),ncol=2,frameon=False,fontsize=10)
save(fig,'orbit-envelope.svg','Two-body circular-orbit screens: both local case altitudes; orbital_trade.tangential_impulse.\nPhase rate is not a delivered common-epoch state. No atmosphere, host control or\nconjunction covariance enters these curves. Presentation revision: 23 Oct 2026.')
fig,axes=plt.subplots(1,3,figsize=(7.1,4.8));results=[evaluate(c)for c in cases]
for ax,key,label in zip(axes,['host_recoil_m_s','peak_body_rate_deg_s','attitude_offset_deg'],['Recoil\nmagnitude (m/s)','Peak ideal body\nrate (deg/s)','Ideal attitude\noffset (deg)']):
 values=[a[key] if key in a else a['internal_move'][key]for a in results];ax.bar([0,1],values,color=C,width=.55);ax.set_xticks([0,1],['3U','6U']);ax.set_ylabel(label);ax.axhline(0,color='.4',lw=.5)
save(fig,'disturbance-budget.svg','Recoil converts each prescribed inertial impulse to relative speed before host_recoil.\nInternal motion is an ideal rigid-body screen; zero residual rate is a model result.\nNo host-controller settling or flexible response is solved. 23 Oct 2026.')
print('Three 180 mm orbital figures exported as SVG, embedded-font PDF and 300 dpi PNG')
