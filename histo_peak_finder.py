# -*- coding: utf-8 -*-

"""
Translated from the C++ macro at
https://root.cern.ch/drupal/content/how-find-peaks-histograms
"""

import ROOT as rt
from array import array

# # randomly fill a multi-peaked histogram
# rt.gRandom.SetSeed(1234)
# mygaus1 = rt.TF1("mygaus1","TMath::Gaus(x,40,10)",0,100);
# h1 = rt.TH1F("h1", "h1", 100, 0, 100)
# h1.FillRandom("mygaus1", 5000)

# mygaus1b = rt.TF1("mygaus1b","TMath::Gaus(x,20,10)",0,100);
# h1b = rt.TH1F("h1b", "h1b", 100, 0, 100)
# h1b.FillRandom("mygaus1b", 5000)

# mygaus2 = rt.TF1("mygaus2","TMath::Gaus(x,80,7)",0,100);
# h2 = rt.TH1F("h2", "h2", 100, 0, 100)
# h2.FillRandom("mygaus2", 1000)

# h = h2.Clone()
# h.Add(h1)
# h.Add(h1b)


h = rt.TH1F("h", "h", 40, 0, 4000)
f = open("/home/estelle/Téléchargements/obs_test.csv", "r")
lines = f.readlines()
data = array("d", map(lambda x: float(x.split(",")[1]), lines))
weights = array("d", [1.0]*len(lines)) # unit weights
h.FillN(len(lines), data, weights)

# some statistics on the full histo
hmean = h.GetMean()
hstd = h.GetStdDev()
N = 1
res = array("d", [0.]*N)
q = array("d", [0.5])
h.GetQuantiles(N, res, q)
hmed = res[0]
print "Histo stats"
print "mean", hmean
print "med", hmed
print "std", hstd

# peak finder with TSpectrum.Search
npeaks = 3
s = rt.TSpectrum()
nfound = s.Search(h, 2, "nobackground nodraw noMarkov")
xpeaks = s.GetPositionX()
print nfound, "candidate peaks"
print "peaks found at positions", [xpeaks[m] for m in range(nfound)]

percentage = 0.2
fit_peak = 0 
for p in range(0, nfound):
    xpeak = xpeaks[p]
    if (xpeak-hmean) > hstd * percentage:
        fit_peak=xpeak
        print xpeak, "is presumably a peak to be removed... "
        
g1 = rt.TF1("g1","gaus", fit_peak-hstd/2.,fit_peak+hstd/2.);
h.Fit(g1, "R0")

# Drawing 
functions = h.GetListOfFunctions()
pm = functions.FindObject("TPolyMarker")
fit = functions.FindObject("g1")

c = rt.TCanvas("c", "c", 800, 600)
h.SetLineColor(rt.kBlue)
h.Draw("")
pm.SetMarkerSize(2)
pm.Draw()
fit.SetLineColor(rt.kRed)
fit.Draw("same")

# remove second peak 
hb = h.Clone()
x_limit = fit.GetParameter(1) - fit.GetParameter(2)*2
bin_limit = hb.GetXaxis().FindBin(x_limit)
for b in range(bin_limit, hb.GetXaxis().GetNbins()):
    hb.SetBinContent(b, 0)
#hb.GetXaxis().SetRangeUser(0,)
hb.SetLineColor(rt.kGreen+2)
hb.Draw("same")

print "New hist stats"
hb.GetQuantiles(N, res, q)
hmed = res[0]
print "med", hmed
