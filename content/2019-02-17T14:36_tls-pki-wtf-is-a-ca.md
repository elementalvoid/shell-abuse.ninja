Title: TLS/PKI -- WTF is a CA?!?!
Category: Encryption
Tags: TLS, SSL, encryption, networking, pki, cryptography
Summary: For Ilya! Recently a conversation came up on a Slack I participate in about PKI, Certificate Authorities, mTLS, etc. and how they all fit together. Ilya had been poking around at some Kubernetes stuff and was seeking more information about how the PKI system was setup. Where the CA came from, how that applied elsewhere, etc. Some others jumped in and they all began to spew information around. And, while the vast majority of it was correct there were some miscommunications that led to bad (and wrong) statements. Not to mention there was such a flurry of typing going on that some wires got crossed. Seeking to clear it all up I wrote a long form response for him which I've cleaned up a bit for this post.

### Some backstory
Ilya had been poking around at some Kubernetes stuff and was seeking more information about how the PKI system was setup. Where the CA came from, how that applied elsewhere, etc. Some others jumped in and they all began to spew information around. And, while the vast majority of it was correct there were some miscommunications that led to bad (and wrong) statements. Not to mention there was such a flurry of typing going on that some wires got crossed. Seeking to clear it all up I wrote a long form response for him.

In essence he understood how the client and server connections were handled, the purpose of server side and client side certificates were and how they were used. But he was looking for a better understanding of how it all got bootstrapped. How trust was formed at a larger scale (i.e. outside of his playground k8s cluster).

So, from here on out, pretend you're Ilya and this is all aimed at you!

---

### A short definition of PKI
PKI stands for Public Key Infrastructure. On this everyone involved agreed. It's a system (process and tooling) that allows for trusting parties/entities through the use of public key cryptography in order to be able to securely share data.

In public key cryptography you share with the world the public key and hold secure a private key. The public key is used for the remote party to encrypt data to send to you. The private key is used for decryption of that incoming message. TLS, GPG, etc. are all the same system underneath. They just have varying levels of metadata, validation, and tooling wrapped around them.

### So, CA's and such...

You are already familiar with the CA concept (and certificate chaining -- one certificate signing another which then signs another and so on). You know that a CA is created (but are curious about the how), and "trusted" by a client (browser or other). This "trust" is established, typically, by paying someone to validate that the entity making the request isn't falsifying information. So, once trust is established on the CA (root) then you implicitly trust anything that CA signs.

In short, a CA is all about trust. Trust a given CA? Well, then you implicitly also trust everything that is signed by it.

For a moment let's ignore the signature aspect. We'll come back to that in due time.

### What is the CA's certificate then?
It is a digitally signed certificate. What makes it CA is that it has a special marking which means it is allowed to be used for both encrypted communication and also to be used for "issuing" (signing) new certificates. The cacert.pem file you asked about (the example came from an Nginx server setup) is exactly this: a digitally signed certificate with the special marking.

### Okay .. what's a certificate anyway?
It's basically a bag of data. Inside this bag of data is the public key portion of the key pair (we'll use this to encrypt our messages before we send them). Secondly, it contains a set of metadata about the entity that "owns" the private key (see, we're really just trying to establish ownership of the private key). The metadata is things like the owner's name, country, business unit, etc. It should also include things like DNS names which are "owned" by the key owner, etc.

### But .. but .. let's get back to the signature already!
A digital signature is essentially the output of a mathematical function applied to the combination of the "data" and a "key". The data is the "stuff in the cert". The "key" of course is the private key. The output of this function is just more "data", except this time we can apply another mathematical function on the signature data to validate that it was created with a specific private key -- the private key for our CA. And we can do this because we have (and trust) the public key portion of the key pair. Recall that we already have a copy of the CA certificate (which as we said includes the public key portion of the key pair). Validation of a signature uses the message itself (here this means the stuff in the cert), the signature, and the public key.

### What about the private key then?
The private key servers two purposes. First, as was already discussed, it is used for decryption (though it can also be used for encryption but we aren't doing that here). Second, it is used to create a digital signature as we just discussed.

### Are we done yet?
Coming full circle to your initial question about the CA and such: As we said, a CA certificate is special kind of certificate that is not only allowed to provide encrypted communication, it is also allowed to sign other certificates. Creating a CA on your own involves self-signing: meaning you use your own private key to digitally sign the data for the certificate. So, you start by creating a private key (openssl/cfssl will allow you to "create them together" -- not really true, it still creates the key first). Then you create a certificate containing the public key portion of your key pair and your certificate metadata. Finally, you sign the certificate with your private key.

All your clients now need to be given this CA certificate in order to provide the trust relationship.

The reason that you have to have both the CA cert and the private key to "issue" (sign) other certificates is to establish the chain. All certificates have a piece of metadata called the "Subject". The CA's Subject is copied into the "Issuer" field on the issued (signed) certificate. This Issuer/Subject link is the chain.

### Addendum: mTLS (mutual TLS authentication)
There was an extra question about clients using certificates that were issued by your CA. These are not being used for serving things over TLS; rather they're being used as an authentication (not authorization) mechanism when then client connects to your Kubernetes API server. The handshake to complete authentication is too complex to bring up now (as I'm sure you're already tired of reading) but essentially the client sends its certificate (signed by the server's CA) and a message signed by the client's private key. Because the server was the Issuer it is able to validate the client certificate's signature and also the signature sent (because it now has, and trusts, the client's public key). Because of this validation the server knows that the client is who (what?) it says it is and it accepts the connection. Authorization needs to be handled separately; this just establishes an authenticated, trust, encrypted communication channel.