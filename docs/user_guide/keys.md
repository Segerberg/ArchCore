## Generate Keys with openssl

### Generate a Private Key

Run the following command in the Terminal to generate a private key. This command will create a file named private_key.pem
Make sure that the producers **keeps this file secure** and do not share it with anyone.

<pre>
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
</pre>

###  Generate the Public Key
To extract the public key from the private key, execute the following command
This file should be shared by the producer to the ArchCore administrative function
<pre>
openssl rsa -pubout -in private_key.pem -out public_key.pem
</pre>
