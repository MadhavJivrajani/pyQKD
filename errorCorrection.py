#Alice and Bob announce some of their measured bits
#Every 4th basis reconciled bit in our case. Remove the reading from the list because Eve knows about the measurements for those readings.
#Error rate = number of errors/total compared cases
#Find optimal length of set where the probability of finding more than 1 error is least.
#Find parity in each of the sets. If equal, most likely the measurements are same for ALice and Bob. If different remove from list.
#Also remove one reading from the set for which parity was announced. To maintain security (so that Eve cannot guess)
#if block size is large enough, and parity is different, we can do bisective searching till the error is found and reject that state for both alice and bob.


alice = ['H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H', 'D']
bob  = ['H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H','H', 'D', 'D', 'H', 'H', 'D']
alice_b = [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1]
bob_b = [0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
def calc_error_rate(alice, bob, alice_b, bob_b):
    error = 0
    count = 0
    for j in range(0, len(alice), 4):
        i = j-count
        #i = alice_b.index(j)
        #print i
        if(alice_b[i]!=bob_b[i]):
            error+=1
        count+=1
        alice_b.pop(i)
        alice.pop(i)
        bob_b.pop(i)
        bob.pop(i)
    error_rate = float(error/count)
    return error, count, error_rate, alice, bob, alice_b, bob_b

def set_length(error, count):
    s_len = int(count/error)
    if s_len<3:
        return 3
    return s_len
def find_parity(bits):
    count = 0
    for i in bits:
        count+=i
    par = count%2
    return par

def remove_last(bits):
    bits.pop()
    return bits



error, count, error_rate, alice, bob, alice_b, bob_b = calc_error_rate(alice, bob, alice_b, bob_b)
setLen = set_length(error, count)
j = 0
k = 0
par_alice = []
par_bob = []
bits = []
#m = len(alice) - len(alice)%setLen

def binary_search(alice_sub, bob_sub):
#     if len(bob_sub)>1:
#         if find_parity(alice_sub) != find_parity(bob_sub):
#             binary_search(alice_sub[:int(len(alice_sub)/2)], bob_sub[:int(len(bob_sub)/2)])
#             #print(alice_sub)
#             binary_search(alice_sub[int(len(alice_sub)/2):], bob_sub[int(len(bob_sub)/2):])
#             #print(bob_sub)
#     elif len(bob_sub)==1:
#         #print(alice_sub, bob_sub)
#         #if find_parity(alice_sub)!=find_parity(bob_sub):
#         bob_sub[0] = not bob_sub[0]
#         return
    r = len(alice_sub)
    l = 0
    
    while(l<r):
        alice = alice_sub[l:r]
        bob = bob_sub[l:r]
        m = int((l+r)/2)
        
        if (find_parity(alice)!=find_parity(bob)):
           l = m+1
        else:
            r = m-1
            
    bob_sub[m] = int(not bob_sub[m])
    
    return bob_sub

def get_subsets(error, count, alice_b, bob_b):
    alice, bob = [], []
    n = len(alice_b)
    subset_size = set_length(error, count)
    for i in range(0, n, subset_size):
        alice.append(alice_b[i:i+subset_size])
        bob.append(bob_b[i:i+subset_size])
        
    return alice, bob

def error_correction(alice_b, bob_b, error, count):
    alice_sub, bob_sub = [], []
    alice_sub, bob_sub = get_subsets(error, count, alice_b, bob_b)
    #print(alice_sub, bob_sub)
    par_alice, par_bob = [], []
    for i in range(len(alice_sub)):
        par_alice.append(find_parity(alice_sub[i]))
        alice_sub[i].pop(0)
        par_bob.append(find_parity(bob_sub[i]))
        bob_sub[i].pop(0)
    print(alice_sub, bob_sub) 
    corrected_alice, corrected_bob = [], []
    for i in range(len(par_alice)):
        if par_alice[i]==par_bob[i]:
            corrected_bob.append(bob_sub[i])
        else:
            corrected_bob.append(binary_search(alice_sub[i], bob_sub[i]))
        corrected_alice.append(alice_sub[i])
    return corrected_alice, corrected_bob
    
#--------------------------------------------------------------------#--------------------------------------------------------------------------------------#

#Selecting set length
#Formula: n-k-s
#n: total number of bits,
#k: estimated maximum number of bits known by eve (double the error rate)
#s: security parameter
#parities of these subsets becomes final key



def privacy_amplification(n, error_rate, s, alice_bit, bob_bit):
    k = int(error_rate * 2) 
    subset_size = n - k - s
    final_alice = []
    final_bob = []
    
    alice_b = []
    bob_b = []
    
    alice_subsets = []
    bob_subsets = []
    
    for i in alice_bit:
        for j in i:
            alice_b.append(j)
    
    for i in bob_bit:
        for j in i:
            bob_b.append(j)
    
    for i in range(0, n, subset_size):
        alice_subsets.append(alice_b[i:i+subset_size])
        bob_subsets.append(bob_b[i:i+subset_size])
        
    bob_parity = 0
    alice_parity = 0
    
    #calculate parities of sets and compare and eliminate if parities dont match
    for i in range(len(alice_subsets)):
        
        alice = find_parity(alice_subsets[i])
        bob = find_parity(bob_subsets[i])
                
        if alice == bob:
            final_alice.append(alice)
            final_bob.append(bob)
    
    return final_alice, final_bob
