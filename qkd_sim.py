import numpy as np
import random
import math
from optical_elements import LinearPolarizer, PolarizingBeamSplitter

class Alice:
    def __init__(self, n):
        self.n = n
        self.alice = {} #{no. : [bit encoded, basis chosen to encode in ]} no. is some unique number
                        #{1:[0,0],2:[0,1],3:[0,0]} Example

    def generate_and_encode(self): 
        """
            Will generate n bits randomly
            For each bit generated, a basis is chosen in which it is encoded
            Dependency for encoding: <class LinearPolarizer>
                0-> horizontal/vertical polarization
                1-> diagonal polarization
            
            Should generate a dictionary of the form self.alice mentioned above
        """
        LP = LinearPolarizer()
        encode = []
        count = self.n
        
        while count!= 0:
            self.alice[count] = [ random.randint(0,1), random.randint(0,1)]
            if self.alice[count][1] == 0:
                encode.append(LP.horizontal_vertical(self.alice[count][0]))
            else:
                encode.append(LP.diagonal_polarization(self.alice[count][0]))
            count-=1
        
        return encode
    

class Bob:
    def __init__(self, n):
        self.n = n
        self.bob = {} #{no. : [bit after measurement, basis chosen to measure in]}
                      #{1:[1,0],2:[0,0],3:[1,0]} Example
    
    def choose_basis_and_measure(self, received):
        """
            received : the data received by bob
            Dependency for measurement: <class PolarizingBeamSplitter>
            
                0-> horizontal/vertical polarization
                1-> diagonal polarization
            
            Should generate a dictionary of the form self.bob mentioned above
        """
        #self.bob[n][0] is the measured bit
        
        PBS = PolarizingBeamSplitter()
        count = self.n
        i = 0
        while count!= 0:
            self.bob[count] = [0, random.randint(0,1)]
            measure = PBS.measure(received[i], self.bob[count][1])
            if measure[0] == measure[1]:
                self.bob[count][0] = random.randint(0,1)
            elif measure[0] > measure[1]:
                self.bob[count][0] = 0
            else:
                self.bob[count][0] = 1
            i += 1
            count-=1

class Privacy_amplification:
    def __init__(self, n):
        
        self.n = n
        
    def find_parity(self, bits):
        count = 0
        for i in bits:
            count+=i
        par = count%2
        return par
    
    
    def privacy_amplification(self, error_rate, s, alice_bit, bob_bit):
        k = int(error_rate * 2) 
        subset_size = self.n - k - s
        final_alice = []
        final_bob = []

        alice_b = []
        bob_b = []

        alice_subsets = []
        bob_subsets = []

        for i in alice_bit:
            alice_b.append(i)

        for i in bob_bit:
            bob_b.append(i)

        for i in range(0, self.n, subset_size):
            alice_subsets.append(alice_b[i:i+subset_size])
            bob_subsets.append(bob_b[i:i+subset_size])

        bob_parity = 0
        alice_parity = 0

        #calculate parities of sets and compare and eliminate if parities dont match
        for i in range(len(alice_subsets)):

            alice = self.find_parity(alice_subsets[i])
            bob = self.find_parity(bob_subsets[i])

            if alice == bob:
                final_alice.append(alice)
                final_bob.append(bob)

        return final_alice, final_bob

class BB84:
    def __init__(self, n, delta, error_threshold):
        """
            Alice generates (4+delta)n bits 
            delta: small fraction less than one 
            error_threshold: if error while announcing n bits from 2n bits is greater than this
                                key generation is aborted 
        """
        if delta > 1:
            print("Value for delta should be lesser than 1")
            return 
        
        self.n = n
        self.total = math.ceil(4 + delta)*n
        self.alice = Alice(self.total)
        self.bob = Bob(self.total)
        
        self.error_rate = 0
        self.error = error_threshold
    
    def eve_interfere(self, intercept, intensity):
        """
            intercept: the encoeded bits alice sends to bob
            intensity: number of bits to interfere with
        """
        
        PBS = PolarizingBeamSplitter()
        lp = LinearPolarizer()
        
        indices = random.sample(list(range(self.total)), intensity)
        
        for i in indices:
            basis = random.randint(0, 1)
            measure = PBS.measure(intercept[i], basis)
            
            if measure[0] == measure[1]:
                intercept[i] = lp.diagonal_polarization(0)
            
            if measure[0] == -1 * measure[1]:
                intercept[i] = lp.diagonal_polarization(1)
            
            if measure[0] > measure[1]:
                intercept[i] = lp.horizontal_vertical(0)
            
            else:
                intercept[i] = lp.horizontal_vertical(1)
                
        return intercept
            
        
        
    def distribute(self, eve, intensity, priv_amp):
        """
            eve: if an evesdropper is present or not 
        """
        encoded = self.alice.generate_and_encode()
        
        if eve==1:
            encoded = self.eve_interfere(encoded, intensity)
                        
        self.bob.choose_basis_and_measure(encoded)

        recon = Reconciliation(self.error, self.alice.alice, self.bob.bob, self.n)

        recon_alice, recon_bob = recon.basis_reconciliation(self.alice.alice, self.bob.bob)
        try:
            final_alice, final_bob, error_rate = recon.error_correction(recon_alice, recon_bob)
            self.error_rate = error_rate
            if priv_amp:
                priv = Privacy_amplification(self.n)

                final_priv_alice, final_priv_bob = priv.privacy_amplification(error_rate, 2, final_alice, final_bob)
                return final_priv_alice, final_priv_bob
            else:
                return final_alice, final_bob

        except:
            self.abort()
            return [], []
        
    
    def abort(self):
        print("Protocol aborted")
        return 

def calcRedundantBits(m): 
  
    # Use the formula 2 ^ r >= m + r + 1 
    # to calculate the no of redundant bits. 
    # Iterate over 0 .. m and return the value 
    # that satisfies the equation 
  
    for i in range(m): 
        if(2**i >= m + i + 1): 
            return i 
  
def posRedundantBits(data, r): 
   
    j = 0
    k = 1
    m = len(data) 
    res = '' 
   
    for i in range(1, m + r+1): 
        if(i == 2**j): 
            res = res + '0'
            j += 1
        else: 
            res = res + data[-1 * k] 
            k += 1
  
    return res[::-1] 
  
def calcParityBits(arr, r): 
    n = len(arr) 
  
    # For finding rth parity bit, iterate over 
    # 0 to r - 1 
    for i in range(r): 
        val = 0
        for j in range(1, n + 1): 
  
            # If position has 1 in ith significant 
            # position then Bitwise OR the array value 
            # to find parity bit value. 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
                # -1 * j is given since array is reversed 
  
        # String Concatenation 
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n) 
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:] 
    return arr 
  
def detectError(arr, nr): 
    n = len(arr) 
    res = 0
  
    # Calculate parity bits again 
    for i in range(nr): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
  
        # Create a binary no by appending 
        # parity bits together. 
  
        res = res + val*(10**i) 
  
    return int(str(res), 2) 

class Reconciliation:
    def __init__(self, error_threshold, alice, bob, n):
        
        self.alice = alice
        self.bob = bob
        self.n = n
        self.error_threshold = error_threshold
        
        
    def basis_reconciliation(self, alice, bob):
        """
            alice: {no. : [bit encoded, basis chosen to encode in ]}
            bob  : {no. : [bit after measurement, basis chosen to measure in]}

            First check if the length of both lists are the same
                -> if yes, keep only those bits for alice and bob for which
                   the basis encoded in and measured in is the same. 
        """
        basis_bit_alice = list(alice.values())
        basis_bit_bob = list(bob.values())

        if len(basis_bit_alice) == len(basis_bit_bob):
            raw_key_alice = []
            raw_key_bob = []

            for i in range(len(basis_bit_alice)):
                if basis_bit_alice[i][1] == basis_bit_bob[i][1]:
                    raw_key_alice.append(basis_bit_alice[i][0])
                    raw_key_bob.append(basis_bit_bob[i][0])

            return raw_key_alice, raw_key_bob

        else:
            return None, None
    
    def abort(self):
        print("Protocol aborted here")
        return
    
    def sampling(self, raw_key_alice, raw_key_bob, n):
        
        sampled_key_alice, sampled_key_bob, sampled_key_index = [], [], []
        sampled_key_index = random.sample(list(enumerate(raw_key_alice)), n)
        indices = []
        
        for idx, val in sampled_key_index:
            sampled_key_alice.append(val)
            sampled_key_bob.append(raw_key_bob[idx])
            indices.append(idx)
        
        return sampled_key_alice, sampled_key_bob, indices
    
    def error_correction(self, raw_key_alice, raw_key_bob):
                
        if len(raw_key_alice)<2*self.n:
            self.abort()
        
        else:
            
            sampled_key_alice, sampled_key_bob, sample_indices = self.sampling(raw_key_alice, raw_key_bob, 2*self.n)

            check_alice, check_bob, indices = self.sampling(sampled_key_alice, sampled_key_bob, self.n)

            error = 0

            for i in range(len(check_alice)):
                if check_alice[i] != check_bob[i]:
                    error+=1

            error_rate = error/self.n
            if error_rate >= self.error_threshold:
                self.abort()
                
            else:
                
                req_alice = [sampled_key_alice[i] for i in range(len(sampled_key_alice)) if i not in indices]
                req_bob = [sampled_key_bob[i] for i in range(len(sampled_key_bob)) if i not in indices]
                
                if error_rate == 0.0:
                    return req_alice, req_bob, error_rate
                
                string_alice = "".join(list(map(str, req_alice)))
                string_bob = "".join(list(map(str, req_bob)))
                
                m = len(string_bob)
                r = calcRedundantBits(m) 
                arr = posRedundantBits(string_bob, r) 
                arr = calcParityBits(arr, r) 
                
                bob = []
                
                k = 0
                for i in range(self.n):
                    if i!=(2**k-1):
                        bob.append(req_bob[i])
                    else:
                        k += 1
                                                        
                
                correction = self.n - detectError(arr, r) - 1
                
                req_bob[correction] = int(not req_bob[correction])
                
                

                return req_alice, req_bob, error_rate

bb84 = BB84(10, 0.6, 0.3)
a, b = bb84.distribute(0, 3, 0)
count = 0

for i in range(len(a)):
    if a[i] != b[i]:
        count += 1

print("Weight of transmission: ", count)
print("\nDistributed Keys:\nAlice: %s \nBob: %s\n" % ("".join(list(map(str, a))), "".join(list(map(str, a)))))
print("Error rate: ", bb84.error_rate)
