import os

class DevilDecoder:
    """Decodes DNA-encoded data back to original text."""
    
    _DNA_MAP = {'A': '00', 'T': '01', 'G': '10', 'C': '11'}
    
    def __init__(self, key):
        self.key = bytes.fromhex(key) if isinstance(key, str) else key
    
    def _dna_to_bytes(self, dna):
        """Convert DNA sequence back to bytes."""
        binary = ''.join(self._DNA_MAP[base] for base in dna if base in self._DNA_MAP)
        extra_bits = len(binary) % 8
        if extra_bits:
            binary = binary[:-extra_bits]  # Remove padding
        return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    
    def decode(self, dna_data):
        """Decode DNA data back to original bytes."""
        xored_bytes = self._dna_to_bytes(dna_data)
        repeated_key = (self.key * ((len(xored_bytes) // len(self.key)) + 1))[:len(xored_bytes)]
        original = bytes(a ^ b for a, b in zip(xored_bytes, repeated_key))
        
        try:
            return original.decode('utf-8')
        except UnicodeDecodeError:
            return f"Raw bytes (hex): {original.hex()}"

def show_banner():
    print(r"""
    ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
    ██║  ██║█████╗  ██║     ██║   ██║██║  ██║█████╗  ██████╔╝
    ██║  ██║██╔══╝  ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
    ██████╔╝███████╗╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """)

def main():
    show_banner()
    encoded_file = input("\nEnter encoded .txt file path: ")
    key = input("Enter the key (hex string): ")
    
    try:
        with open(encoded_file, 'r') as f:
            dna_data = f.read().strip()
    except FileNotFoundError:
        print("Error: File not found!")
        return
    
    decoder = DevilDecoder(key)
    decoded_output = decoder.decode(dna_data)
    
    print("\nDecoded Output:")
    print("---------------")
    print(decoded_output)

if __name__ == "__main__":
    main()