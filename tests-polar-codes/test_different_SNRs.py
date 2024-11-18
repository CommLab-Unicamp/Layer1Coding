import numpy as np
from polarcodes import *

# Initialize polar code parameters
N = 100  # Block length as 2^N
K = 50  # Number of information bits

def get_frozen_bits(design_SNR):
    """
    Constructs a polar code with the given design SNR and extracts frozen bit indices.

    Parameters:
    design_SNR (float): Design SNR in decibels.

    Returns:
    ndarray: Indices of frozen bits.
    """

    # Initialize polar code
    myPC = PolarCode(N, K)
    myPC.construction_type = 'ga'  # Use Bhattacharyya bounds

    # Construct the polar code for the given design SNR
    Construct(myPC, design_SNR)

    # Return frozen bit indices
    return myPC.frozen

# Test with two different design SNRs
design_SNR1 = 10.0  # Low SNR
design_SNR2 = -2.0  # High SNR

# Get frozen bits for both SNRs
frozen_bits_SNR1 = get_frozen_bits(design_SNR1)
frozen_bits_SNR2 = get_frozen_bits(design_SNR2)

# Print and compare frozen bits
print(f"Frozen bits at SNR={design_SNR1}: {frozen_bits_SNR1}")
print(f"Frozen bits at SNR={design_SNR2}: {frozen_bits_SNR2}")

# Identify differences
diff_frozen = set(frozen_bits_SNR1).symmetric_difference(set(frozen_bits_SNR2))
print(f"Difference in frozen bits: {diff_frozen}")