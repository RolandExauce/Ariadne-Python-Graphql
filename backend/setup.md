# IN SRC FOLDER, CHANGE "your_env.env" to ".env" AND ADJUST THE CONTENT

# GENERATE ASYMMETRIC RS256 KEYS 

# SECURE YOUR GRAPHQL API WITH SSL 


# HOW TO GENERATE ASYMMETRIC KEYS: 

1. Create key pair

openssl genrsa -out keypair.pem 2048


2. Extract public part

openssl rsa -in keypair.pem -pubout -out publickey.crt

=> public key: publickey.crt


3. Extract private part

openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key

=> private key = private.key


# FOR FRONTEND, YOU CAN USE REACT, FLUTTER, DJANGO etc