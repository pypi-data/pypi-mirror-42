#%% import
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mcr import MCR
from mcr.efa import efa

sns.set_context("talk")
sns.set_palette("Set1")

#%% purespecs
wavel = np.arange(290, 510, 3)

spec1 = np.exp(-((wavel - 380) / 30) ** 2)
spec2 = np.exp(-((wavel - 430) / 16) ** 2)

Nobs = 20
obs = np.arange(Nobs)
c1 = 0.7 * np.exp(-(obs / 5) ** 2) + 0.15
c1 = np.exp(-(obs / 5) ** 2)
c2 = 1 - c1

C = np.c_[c1, c2]
B = np.c_[spec1, spec2]
M = B @ C.T


#%% plot initial data
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

ax1.plot(wavel, spec1)
ax1.plot(wavel, spec2)

ax2.plot(obs, c1)
ax2.plot(obs, c2)
ax2.set_xlim(0, Nobs - 1)

for i in range(Nobs):
    ax3.plot(wavel, M[:, i])

ax1.set_ylim(0, 1.05)
ax1.set_yticks(())
fig.tight_layout()

#%% EFA

efa(M.T, ncomp=2, plot=True)

#%% Defaults
mcr = MCR(maxiter=1000, chkpnt=10, tol=1e-10)

C_ = np.c_[np.arange(Nobs) / Nobs, 1 - np.arange(Nobs) / Nobs]

mcr.fit(M, C=C_, debug=True)

l1 = plt.plot(obs, C_[:, 0], "--", label="Start")[0]
l2 = plt.plot(obs, C_[:, 1], "--")[0]
plt.plot(obs, mcr.C[:, 0], color=l1.get_color(), label="MCR")
plt.plot(obs, mcr.C[:, 1], color=l2.get_color())
plt.plot(obs, C[:, 0], ":", color=l1.get_color(), label="Real")
plt.plot(obs, C[:, 1], ":", color=l2.get_color())
plt.xlim(0, Nobs - 1)
plt.ylim(0, 1)
plt.legend(framealpha=False)
plt.title("Conc. profiles")

plt.figure()
plt.plot(wavel, mcr.B[:, 0], color=l1.get_color(), label="MCR")
plt.plot(wavel, mcr.B[:, 1], color=l2.get_color())
plt.plot(wavel, B[:, 0], ":", color=l1.get_color(), label="Real")
plt.plot(wavel, B[:, 1], ":", color=l2.get_color())
plt.legend(framealpha=False)
plt.xlim(290, 510)
plt.ylim(0, 1.05)
plt.title("Pure spectra")

plt.figure()
plt.plot(mcr.error)
plt.xlabel("Trial / Checkpoint")
plt.xlim(left=0)
plt.ylabel("Error")
plt.title(f'Convergence ({"" if mcr.converged else "Not "}Converged!)')
#%%
