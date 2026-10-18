"""Generate technical plots from the two local calculation cases."""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'svg.fonttype':'none','svg.hashsalt':'technical-case-plots','figure.facecolor':'white','axes.facecolor':'white'})
C=['#0072B2','#D55E00']
def save(fig,name,caption):
 fig.subplots_adjust(left=.10,right=.97,bottom=.23,top=.88,wspace=.38)
 fig.text(.02,.025,caption,fontsize=8,va='bottom')
 fig.savefig(ROOT/'figures'/name,metadata={'Date':None})
 path=ROOT/'figures'/name
 path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 plt.close(fig)
from orbital_trade import evaluate,tangential_impulse,host_recoil
cases=[json.loads((ROOT/'cases'/name).read_text())for name in ['volley_reference.json','hosted_6u_example.json']]
labels=['Historical 3U case','Hosted 6U example']
fig,axes=plt.subplots(1,2,figsize=(10,4.4))
for i,c in enumerate(cases):
 x=np.linspace(0,20,81);orbits=[tangential_impulse(c['altitude_m'],v)for v in x]
 axes[0].plot(x,[(o['apogee_altitude_m']-c['altitude_m'])/1000 for o in orbits],color=C[i],ls=['-','--'][i],label=labels[i])
 axes[1].plot(x,[host_recoil(c['payload_mass_kg'],v,c['host_mass_kg'])*1000 for v in x],color=C[i],ls=['-','--'][i],label=labels[i])
axes[0].set(xlabel='Payload inertial tangential increment (m/s)',ylabel='Apogee increase from circular reference (km)',title='a  Two-body orbit geometry')
axes[1].set(xlabel='Payload-to-host relative separation speed (m/s)',ylabel='Remaining-host recoil magnitude (mm/s)',title='b  Exact finite-host momentum split')
for ax in axes:ax.legend(frameon=False,fontsize=8)
save(fig,'deployment-trade.svg','Independent parameter screens; the two horizontal axes use different velocity conventions.\nInputs are prescribed model scenarios; no hardware or delivery accuracy is established.')
fig,axes=plt.subplots(1,2,figsize=(10,4.4))
for i,c in enumerate(cases):
 x=np.linspace(0,20,81);o=[tangential_impulse(c['altitude_m'],v)for v in x]
 axes[0].plot(x,[a['apogee_altitude_m']/1000 for a in o],color=C[i],ls=['-','--'][i],label=labels[i]);axes[1].plot(x,[a['phase_drift_deg_day']for a in o],color=C[i],ls=['-','--'][i])
axes[0].set(xlabel='Payload inertial increment (m/s)',ylabel='Apogee altitude (km)',title='a  Altitude response');axes[1].set(xlabel='Payload inertial increment (m/s)',ylabel='Mean-motion drift magnitude (deg/day)',title='b  Phase-rate response');axes[0].legend(frameon=False,fontsize=8)
save(fig,'orbit-envelope.svg','Two-body circular-orbit screens at the two case altitudes. Phase rate is not a delivered common-epoch state.\nNo atmosphere, host control or conjunction covariance enters these curves.')
fig,axes=plt.subplots(1,3,figsize=(11,4.4));results=[evaluate(c)for c in cases]
for ax,key,label in zip(axes,['host_recoil_m_s','peak_body_rate_deg_s','attitude_offset_deg'],['Recoil magnitude (m/s)','Peak ideal body rate (deg/s)','Ideal attitude offset (deg)']):
 values=[a[key] if key in a else a['internal_move'][key]for a in results];ax.bar([0,1],values,color=C,width=.55);ax.set_xticks([0,1],['3U','6U']);ax.set_ylabel(label);ax.axhline(0,color='.4',lw=.5)
save(fig,'disturbance-budget.svg','The recoil uses each case inertial increment, converted to relative speed before the API call.\nInternal motion is an ideal rigid-body screen; residual rate is zero in that model, not a controller settling result.')
print('Three technical orbital figures generated')
