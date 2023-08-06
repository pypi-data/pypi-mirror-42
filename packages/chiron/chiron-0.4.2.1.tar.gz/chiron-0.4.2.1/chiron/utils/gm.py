import numpy as np
import json
import os
from tqdm import tqdm
from random import randint
class gm:
    def __init__(self,k = 5):
        self.k = k
        self.n = int(4*(4**k-1)/3)
        self.base = ['A','C','G','T']
        self.kmer_dict = {}
        self.kmer_count = np.zeros([self.n,4],dtype = int)
        for i in range(self.n):
            kmer = self._idx2kmer(i)
            self.kmer_dict[kmer] = i
    def _kmer2idx(self,kmer):
        idx = 0
        for b_idx,b in enumerate(kmer):
            idx += (self.base.index(b)+1)*len(self.base)**b_idx
        idx = idx - 1
        return idx
    def _idx2kmer(self,idx):
        idx += 1
        kmer = ''
        while idx > 0:
            kmer = self.base[idx%len(self.base)-1] + kmer
            idx = int((idx-1) / len(self.base))
        return kmer
    def count_kmer(self,seq):
        for i in tqdm(range(len(seq)),desc = 'Counting kmer',position = 1):
            if i==0:
                pass
            for k in range(min(self.k,i)):
                kmer = seq[i-k-1:i]
                if self._base_check(kmer):
                    self.kmer_count[self.kmer_dict[kmer]][self.base.index(seq[i])] +=1
    def save(self,sav_path):
        gm_dict = self.__dict__
        gm_dict['kmer_count'] = gm_dict['kmer_count'].tolist()
        print(gm_dict)
        with open(sav_path, 'w+') as f:
            json.dump(gm_dict,f)
    def load(self,model_path):
        with open(model_path,'r') as f:
            gm_dict = json.load(f)
        self.k = gm_dict['k']
        self.n = gm_dict['n']
        assert self.n == int(4*(4**self.k-1)/3)
        self.base = gm_dict['base']
        self.kmer_dict = gm_dict['kmer_dict']
        self.kmer_count = np.asarray(gm_dict['kmer_count'])
    def _base_check(self,kmer):
        for base in kmer:
            if base not in self.base:
                return False
        return True
def fasta_reader(file_list,root_folder = None):
    for name in file_list:
        if root_folder is not None:
            name = os.path.join(root_folder,name)
        seqs = {}
        with open(name,'r') as f:
            for line in f:
                if line.startswith('>'):    
                    last_seq =line[1:].strip()
                    seqs[last_seq] = ''
                else:
                    seqs[last_seq]  = seqs[last_seq]+line.strip()
        yield name,seqs
if __name__ == "__main__":
    root_folder = '/home/heavens/Reference'
    file_list = os.listdir(root_folder)
    file_list = [file_list[0]]
    gm1 = gm(k=5)
    for genome,seqs in fasta_reader(file_list,root_folder):
        for name in tqdm(seqs.keys(),desc = "Reading genome "+genome,position = 0):
            gm1.count_kmer(seqs[name])
            
    gm1.save('/home/heavens/Documents/gm_model.json')
    

    