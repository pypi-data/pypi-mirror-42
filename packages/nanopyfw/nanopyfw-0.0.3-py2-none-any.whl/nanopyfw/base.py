#!/usr/bin/env python

import logging

import ROOT as r

__version__ = "0.0.3"

def dummy_file_to_dataset(file):
    """Find dataset name associated to file

    Can parse the file name, query a data base, whatever
    
    :param file: Path of the input file
    :type file: string
    :return: Dataset name associated to that file
    :rtype: string
    """
    return "dummy"


class AnalyzerBase(object):
    def __init__(self,files):
        
        ### Internal 
        # Files to run over
        self._files = files

        # File to save output in
        self._outfile = r.TFile("outfile.root","RECREATE")

        # Current TDirectory in the output file
        self._curdir = None

        # Dictionary to hold histograms
        self._histos = None 
        # The dataset currently being analyzed
        self._dataset = None
        
        # Function that matches file names to datasets
        self._file_to_dataset = dummy_file_to_dataset
    
    def _create_histograms(self):
        histos = {}

        # Initialize your histograms here, e.g.:
        # histos["ptj"] = ROOT.TH1D("ptj", "ptj", 200, 0, 2000)

        return histos
    

    def _change_dataset(self, new_dataset):
        """Perform all actions associated to a change in dataset

        Necessary actions are:
        1. Change of TDirectory where histograms are saved
        2. Change of histograms to fill

        For both actions, it is first checked whether the dataset and histograms
        already exist. If so, they are loaded from file. If not, they are created.

        :param new_dataset: New dataset to change to
        :type new_dataset: str
        :return: True on success, False otherwise
        :rtype: bool
        """        
        if new_dataset in self._outfile.GetListOfKeys():
            logging.debug("Found existing folder for dataset '{}'.".format(new_dataset))
            logging.debug("Loading histograms from file.")
            directory = self._outfile.Get(new_dataset)
            histos = {}
            for key in directory.GetListOfKeys():
                histos[key.GetName()] = directory.Get(key.GetName())
        else:
            logging.debug("No folder found for dataset '{}'.".format(new_dataset))

            directory = self._outfile.mkdir(new_dataset)
            directory.cd()
            histos = self._create_histograms()

        # Update everything
        self._curdir = directory
        self._histos = histos
        self._dataset = new_dataset

    
    def _write_histos(self):
        """Write histograms to file"""
        logging.debug("Writing histograms to file.")
        if self._curdir:
            self._curdir.cd()
            for tag, histogram in self._histos.items():
                logging.debug("Writing historam '{}'.".format(tag))
                histogram.Write("",r.TObject.kOverwrite)

    def _finish(self):
        """Perform all actions necessary to end a run

        Necessary actions are
        1. Writing histograms to file
        2. Closing the file
        """
        self._write_histos()
        self._outfile.Close()

    def _file_loop(self):
        """Loop over files and analyze each one"""
        nfiles = len(self._files)
        for i, file in enumerate(self._files):
            logging.info("File {} of {}: {}".format(i+1, nfiles, file))
            dataset = self._file_to_dataset(file)
            if dataset != self._dataset:
                self._change_dataset(dataset)
                self._dataset = dataset
            self._analyze(file)

    def run(self):
        """Run the analysis"""
        logging.info("Starting analyzer run.")
        self._file_loop()
        logging.info("Finished analyzing files.")
        self._finish()

    
    def _analyze(self,file):
        # Do your analysis task
        return True

