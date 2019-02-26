#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h> 

/* AES key for Encryption and Decryption */
const static unsigned char aes_key[]={0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF};
 
int main( )
{
	/* Input data to encrypt */
	unsigned char plain_text[]="hello world 1234";
	
	/* Init vector */
	unsigned char iv[AES_BLOCK_SIZE];
	memset(iv, 0x00, AES_BLOCK_SIZE);
	
	/* Buffers for Encryption and Decryption */
	unsigned char cipher_text[128]={0};
	unsigned char msg[128]={0};
	
	/* AES-128 bit CBC Encryption */
	AES_KEY enc_key, dec_key;
	AES_set_encrypt_key(aes_key, sizeof(aes_key)*8, &enc_key);
	AES_cbc_encrypt(plain_text, cipher_text, sizeof(plain_text), &enc_key, iv, AES_ENCRYPT);
	/* AES-128 bit CBC Decryption */
	memset(iv, 0x00, AES_BLOCK_SIZE); // don't forget to set iv vector again, else you can't decrypt data properly
	AES_set_decrypt_key(aes_key, sizeof(aes_key)*8, &dec_key); // Size of key is in bits
	AES_cbc_encrypt(cipher_text, msg, sizeof(plain_text), &dec_key, iv, AES_DECRYPT);
	
	/* Printing and Verifying */
	printf("AES Clear Text: %s\n",plain_text);

	printf("AES Encryption: %s\n", cipher_text);
	
	printf("AES Decryption: %s \n", msg);
	return 0;
}
 

