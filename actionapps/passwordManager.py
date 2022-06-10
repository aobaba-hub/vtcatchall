from cryptography.fernet import Fernet
# import gpg

def managePassword(inputs):
    print("Done")


def encryptEntity(inputs):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
    plain_text = cipher_suite.decrypt(cipher_text)

    print("cipher_text:  ", cipher_text)
    print("plain_text of ", plain_text)

    # Encryption to public key specified in rkey.
    a_key = input("Enter the fingerprint or key ID to encrypt to: ")
    filename = input("Enter the filename to encrypt: ")
    with open(filename, "rb") as afile:
        text = afile.read()
    # c = gpg.core.Context(armor=True)
    # rkey = list(c.keylist(pattern=a_key, secret=False))
    # ciphertext, result, sign_result = c.encrypt(text, recipients=rkey,
    #                                             always_trust=True,
    #                                             add_encrypt_to=True)
    # with open("{0}.asc".format(filename), "wb") as bfile:
    #     bfile.write(ciphertext)
    # # Decryption with corresponding secret key
    # # invokes gpg-agent and pinentry.
    # with open("{0}.asc".format(filename), "rb") as cfile:
    #     plaintext, result, verify_result = gpg.Context().decrypt(cfile)
    # with open("new-{0}".format(filename), "wb") as dfile:
    #     dfile.write(plaintext)
    # # Matching the data.
    # # Also running a diff on filename and the new filename should match.
    # if text == plaintext:
    #     print("Hang on ... did you say *all* of GnuPG?  Yep.")
    # else:
    #     pass
