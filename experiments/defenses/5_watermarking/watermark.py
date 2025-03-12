import hashlib
import base64
import time

def encode_whitespace(data):
    """Encodes data into whitespace characters."""
    binary_data = ''.join(format(ord(char), '08b') for char in data)
    return binary_data.replace('0', ' ').replace('1', '\t')

def decode_whitespace(encoded_text):
    """Decodes whitespace-encoded data back into a string."""
    binary_data = encoded_text.replace(' ', '0').replace('\t', '1')
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

def sign_message(message, user, timestamp):
    """Generates a hidden watermark containing user and timestamp."""
    hash_digest = hashlib.sha256((message + user + str(timestamp)).encode()).hexdigest()
    metadata = f"{user}|{timestamp}|{hash_digest[:16]}"
    return encode_whitespace(metadata)

def extract_metadata(rhyme_text):
    """Extracts user and timestamp from a hidden watermark in a rhyme."""
    try:
        start = rhyme_text.find(" ")  # Locate the first whitespace block (assumed watermark start)
        if start == -1:
            return None
        
        encoded_watermark = rhyme_text[start:].split("\n")[0]  # Extract hidden data
        decoded_metadata = decode_whitespace(encoded_watermark)
        
        user, timestamp, _ = decoded_metadata.split("|")
        return {"user": user, "timestamp": int(timestamp)}
    
    except Exception:
        return None
