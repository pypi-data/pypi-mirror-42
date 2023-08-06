import ROOT as r
from nanopyfw.base import AnalyzerBase
from nanopyfw.jitfunctions import calculate_jet_ht
import uproot as ur
from root_numpy import fill_hist
import sys


def file_to_dataset(file):
    """Example function to derive datasets from file names"""
    if "ZJet" in file:
        return "Z"
    elif "WJet" in file:
        return "W"
    elif "HToInvisible" in file:
        return "Hinv"


class JetAnalyzer(AnalyzerBase):
    def __init__(self, files):
        super(JetAnalyzer, self).__init__(files)
        self._file_to_dataset = file_to_dataset

    def _create_histograms(self):
        histos = {}
        histos["ptj"] = r.TH1D("ptj", "ptj", 200, 0, 2000)
        histos["ht"] = r.TH1D("ht", "ht", 200, 0, 2000)
        histos["lead_jet_eta"] = r.TH1D("lead_jet_eta", "lead_jet_eta", 50,-5,5)
        histos["trail_jet_eta"] = r.TH1D("trail_jet_eta", "trail_jet_eta", 50,-5,5)
        histos["jet_eta_2d"] = r.TH2D("jet_eta_2d", "jet_eta_2d", 50,-5,5,50,-5,5)
        return histos

    def _analyze(self,file):
        tree = ur.open(file)["Events"]
        arrays = tree.arrays(['Jet_pt','nJet','Jet_eta','Jet_phi','MET_pt'])
        jet_pt = arrays[b"Jet_pt"]
        jet_eta = arrays[b"Jet_eta"]
        jet_phi = arrays[b"Jet_phi"]
        met_pt = arrays[b"MET_pt"]
        n_jet = arrays[b"nJet"]

        # Select events with more than one jet
        mask =  (n_jet >1)
        jet_pt = jet_pt[mask]
        jet_phi = jet_phi[mask]
        jet_eta = jet_eta[mask]

        jet_ht = calculate_jet_ht(jet_pt)

        fill_hist(self._histos["ptj"], jet_pt.flatten())
        fill_hist(self._histos["ht"], calculate_jet_ht(jet_pt).flatten())
        fill_hist(self._histos["lead_jet_eta"],jet_eta[:,0])
        fill_hist(self._histos["trail_jet_eta"],jet_eta[:,1])

        twod = jet_eta[:,0:2].tolist()
        fill_hist(self._histos["jet_eta_2d"],twod)

def main():
    files = []
    for p in sys.argv:
        if p.endswith(".root"):
            files.append(p)

    analyzer = JetAnalyzer(files)
    analyzer.run()

if __name__ == "__main__":
    main()