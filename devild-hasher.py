import os

class DevilHasher:
    """DNA-based cryptographic encoder (now perfectly reversible)."""
    
    _DNA_MAP = {'00': 'A', '01': 'T', '10': 'G', '11': 'C'}
    _REV_DNA_MAP = {v: k for k, v in _DNA_MAP.items()}
    
    def __init__(self, key=None):
        self.key = key or os.urandom(32)  # 256-bit key
    
    def _bytes_to_dna(self, data_bytes):
        """Convert bytes to DNA sequence."""
        binary = ''.join(format(byte, '08b') for byte in data_bytes)
        if len(binary) % 2 != 0:
            binary += '0'  # Pad to even length
        return ''.join([self._DNA_MAP.get(binary[i:i+2], 'AA') for i in range(0, len(binary), 2)])
    
    def encode(self, data):
        """Encode data into DNA format."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Repeat key to match data length
        repeated_key = (self.key * ((len(data) // len(self.key)) + 1))[:len(data)]
        xored = bytes(a ^ b for a, b in zip(data, repeated_key))
        return self._bytes_to_dna(xored)

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

def get_unique_filename(base_name):
    name, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(base_name):
        base_name = f"{name}({counter}){ext}"
        counter += 1
    return base_name

def main():
    show_banner()
    print("\n1. Encode text input")
    print("2. Encode .txt file")
    choice = input("\nSelect an option (1 or 2): ")
    
    hasher = DevilHasher()
    
    if choice == '1':
        text = input("\nEnter text to encode: ")
        result = hasher.encode(text)
    elif choice == '2':
        filename = input("\nEnter .txt file path: ")
        try:
            with open(filename, 'rb') as f:
                text = f.read().decode('utf-8')
            result = hasher.encode(text)
        except FileNotFoundError:
            print("Error: File not found!")
            return
    else:
        print("Invalid choice!")
        return
    
    output_filename = get_unique_filename("encoded_output.txt")
    with open(output_filename, "w") as f:
        f.write(result)
    
    print(f"\nEncoded output saved to '{output_filename}'")
    print(f"Key (save this for decoding): {hasher.key.hex()}")

if __name__ == "__main__":
    main()
