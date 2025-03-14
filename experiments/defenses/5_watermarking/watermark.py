import hashlib
import base64
import time
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
    encoded_signature = encode_whitespace(metadata)

    # Log ASCII representation of the signature
    ascii_signature = " ".join(str(ord(c)) for c in encoded_signature)
    logger.info(f"Generated signature (ASCII): {ascii_signature}")

    return encoded_signature

def extract_metadata(rhyme_text):
    """Extracts user and timestamp from a hidden watermark in the second line."""
    try:
        lines = rhyme_text.split("\n")
        if len(lines) < 2:
            logger.warning("The rhyme does not contain a second line for the watermark.")
            return None

        watermark_line = lines[1]  # The second line contains the watermark

        if not re.fullmatch(r"[ \t]+", watermark_line):
            logger.warning("The second line does not contain a valid whitespace-based watermark.")
            return None

        # Log ASCII representation of extracted signature
        ascii_extracted = " ".join(str(ord(c)) for c in watermark_line)
        logger.info(f"Extracted signature (ASCII): {ascii_extracted}")

        decoded_metadata = decode_whitespace(watermark_line)
        logger.info(f"Decoded metadata: {decoded_metadata}")

        user, timestamp, _ = decoded_metadata.split("|")
        logger.info(f"Extracted user: {user}, timestamp: {timestamp}")

        return {"user": user, "timestamp": int(timestamp), "signature": watermark_line}

    except Exception as e:
        logger.error(f"Error extracting metadata: {e}")
        return None
