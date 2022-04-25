from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('data/Key.key', 'wb') as mykey:
    mykey.write(key)


f = Fernet(key)

with open('data/Test_Energies.csv', 'rb') as original_file:
    original = original_file.read()

encrypted = f.encrypt(original)

with open('data/Test_Energies_Enc.csv', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)