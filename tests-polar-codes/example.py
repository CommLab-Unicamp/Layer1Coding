import numpy as np
from polarcodes import *
from custom_AWGN import custom_AWGN

def simulate(variance):
    # initialise polar code
    myPC = PolarCode(8192, 140*8)
    myPC.construction_type = 'bb'

    # mothercode construction
    design_SNR = -10.0
    Construct(myPC, design_SNR)
    print(myPC, "\n\n")

    # set message
    my_message = np.random.randint(2, size=myPC.K)
    myPC.set_message(my_message)
    print("The message is:", my_message)

    # encode message
    Encode(myPC)
    print("The coded message is:", myPC.get_codeword())

    # transmit the codeword
    channel = custom_AWGN(myPC, variance)
    tx = channel.get_transmitted_signal()
    rx = channel.get_received_signal(tx)
    channel.calculate_likelihoods(rx)

    print("Transmitted signal:", tx)
    print("Received signal:", rx)

    print("The log-likelihoods are:", myPC.likelihoods)

    # decode the received codeword
    Decode(myPC)
    print("The decoded message is:", myPC.message_received)

    # calculate bit error rate (BER)
    bit_errors = np.sum(my_message != myPC.message_received)
    bit_error_rate = bit_errors / len(my_message)
    print(f"The bit error rate (BER) is: {bit_error_rate:.6f}")

simulate(1)
