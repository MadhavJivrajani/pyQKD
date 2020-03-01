#Alice and Bob announce some of their measured bits
#Every 4th basis reconciled bit in our case. Remove the reading from the list because Eve knows about the measurements for those readings.
#Error rate = number of errors/total compared cases
#Find optimal length of set where the probability of finding more than 1 error is least.
#Find parity in each of the sets. If equal, most likely the measurements are same for ALice and Bob. If different remove from list.
#Also remove one reading from the set for which parity was announced. To maintain security (so that Eve cannot guess)


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

for l in range(setLen, len(alice), setLen):
    i = l-k
    j-=k
    #i = alice.index(l)
    #print len(alice), len(alice_b), setLen, alice_b[j:i], find_parity(alice_b[j:i])
    par_alice.append(find_parity(alice_b[j:i]))
    alice.pop(i)
    alice_b.pop(i)
    par_bob.append(find_parity(bob_b[j:i]))
    bob.pop(i)
    bob_b.pop(i)
    j = i
    k+=1
    
if(i!=len(alice)-1):
    par_alice.append(find_parity(alice_b[i:len(alice)-1]))
    alice.pop(len(alice)-1)
    alice_b.pop(len(alice_b)-1)    
    par_bob.append(find_parity(bob_b[i:len(bob)-1]))
    bob.pop(len(bob)-1)
    bob_b.pop(len(bob_b)-1)

print alice_b, bob_b


#Selecting set length
#Formula: n-k-s
#n: total number of bits,
#k: estimated maximum number of bits known by eve (double the error rate)
#s: security parameter
#parities of these subsets becomes final key

k = int(2*error) + 1
n = len(alice_b)
