
#include <string.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>

int main()
{
	const int kBits = 1024;
	const int kExp = 3;

	int keylen;
	char *pem_key;

	RSA *rsa = RSA_generate_key(kBits, kExp, 0, 0);

	/* To get the C-string PEM form: */
	BIO *bioPvt = BIO_new(BIO_s_mem());
	PEM_write_bio_RSAPrivateKey(bioPvt, rsa, NULL, NULL, 0, NULL, NULL);

	keylen = BIO_pending(bioPvt);
	pem_key = calloc(keylen+1, 1); /* Null-terminate */
	BIO_read(bioPvt, pem_key, keylen);

	printf("%s", pem_key);

	/* To get the C-string PEM form: */
	BIO *bioPub = BIO_new(BIO_s_mem());
	PEM_write_bio_RSAPublicKey(bioPub, rsa);

	keylen = BIO_pending(bioPub);
	pem_key = calloc(keylen+1, 1); /* Null-terminate */
	BIO_read(bioPub, pem_key, keylen);

	printf("%s", pem_key);
	
	BIO_free_all(bioPvt);
	BIO_free_all(bioPub);
	RSA_free(rsa);
	free(pem_key);
}

