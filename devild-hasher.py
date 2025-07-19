import hashlib
import os

class DevilHasher:
    """DNA-based cryptographic hasher with devilish style."""
    
    _DNA_MAP = {'00': 'A', '01': 'T', '10': 'G', '11': 'C'}
    
    def __init__(self, key=None):
        self.key = key or os.urandom(32)  # 256-bit key
    
    def _binary_to_dna(self, binary):
        """Convert binary to DNA sequence (A, T, G, C)."""
        return ''.join([self._DNA_MAP.get(binary[i:i+2], 'A') 
                      for i in range(0, len(binary), 2)])
    
    def hash(self, data):
        """Generate irreversible DNA hash."""
        if isinstance(data, str):
            data = data.encode()
        
        # SHA-512 → Binary → DNA
        binary = bin(int.from_bytes(hashlib.sha512(data).digest(), 'big'))[2:].zfill(512)
        dna = self._binary_to_dna(binary)
        
        # Keyed mutation (XOR with secret DNA key)
        key_dna = self._binary_to_dna(bin(int.from_bytes(hashlib.sha256(self.key).digest(), 'big'))[2:])
        mutated = ''.join([self._DNA_MAP[format(int(self._rev_dna(a), 2) ^ int(self._rev_dna(b), 2), '02b')]
                         for a, b in zip(dna, key_dna)])
        
        # Final shuffle
        return mutated[len(mutated)//2:] + mutated[:len(mutated)//2]
    
    def _rev_dna(self, base):
        """Convert DNA base back to binary."""
        return {'A': '00', 'T': '01', 'G': '10', 'C': '11'}.get(base, '00')

def show_banner():
    print(r"""
    ██████╗ ███████╗██╗   ██╗██╗██╗     ██████╗ 
    ██╔══██╗██╔════╝██║   ██║██║██║     ██╔══██╗
    ██║  ██║█████╗  ██║   ██║██║██║     ██║  ██║
    ██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║     ██║  ██║
    ██████╔╝███████╗ ╚████╔╝ ██║███████╗██████╔╝
    ╚═════╝ ╚══════╝  ╚═══╝  ╚═╝╚══════╝╚═════╝ 
    ██╗  ██╗ █████╗ ███████╗██╗  ██╗███████╗██████╗ 
    ██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
    ███████║███████║███████╗███████║█████╗  ██████╔╝
    ██╔══██║██╔══██║╚════██║██╔══██║██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║███████║██║  ██║███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """)

def main():
    show_banner()
    print("\n1. Hash text input")
    print("2. Hash .txt file")
    choice = input("\nSelect an option (1 or 2): ")
    
    hasher = DevilHasher()
    
    if choice == '1':
        text = input("\nEnter text to hash: ")
        result = hasher.hash(text)
    elif choice == '2':
        filename = input("\nEnter .txt file path: ")
        try:
            with open(filename, 'r') as f:
                text = f.read()
            result = hasher.hash(text)
        except FileNotFoundError:
            print("Error: File not found!")
            return
    else:
        print("Invalid choice!")
        return
    
    with open("deviled_text.txt", "w") as f:
        f.write(result)
    
    print("\nHash generated and saved to 'deviled_text.txt'")

if __name__ == "__main__":
    main()