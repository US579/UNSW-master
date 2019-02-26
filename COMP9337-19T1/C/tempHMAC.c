#include <stdio.h>
#include <string.h>
#include <openssl/hmac.h>
 
int main() {
    // The secret key for hashing
    const char key[] = "012345678";
 
    // The data that we're going to hash
    char data[1025] = {0};
    
    // Be careful of the length of string with the choosen hash engine. SHA1 needed 20 characters.
    // Change the length accordingly with your choosen hash engine.     
    unsigned char* result;
    unsigned int len = 20;
 
    result = (unsigned char*)malloc(sizeof(char) * len);
 
    HMAC_CTX *ctx;
    ctx = HMAC_CTX_new();
    if (ctx == NULL)
	{
		printf("ctx is null\n");
		return -1;
	}

 
    // Using sha1 hash engine here.
    // You may use other hash engines. e.g EVP_md5(), EVP_sha224, EVP_sha512, etc
    HMAC_Init_ex(ctx, key, strlen(key), EVP_sha1(), NULL);

    FILE *f = fopen("lorem.txt", "rb");
    int count = 0;
    int bContinue = 1;
    while(bContinue)
    {
	count = fread(data,sizeof(unsigned char),1024,f);
//	printf("%s\n",data);
	if(count < 1024)
	{
		HMAC_Final(ctx, result, &len);
		bContinue = 0;
	}
	else
		HMAC_Update(ctx, (unsigned char*)&data, strlen(data));
	
    }//end while(true)
    
    HMAC_CTX_get_md(ctx);
 
    printf("HMAC digest: ");
 
    for (int i = 0; i != len; i++)
        printf("%02x", (unsigned int)result[i]);
 
    printf("\n");
 
    free(result);
 
    return 0;
}
/*
#Following code reads its source file and computes an HMAC signature for it:
import hmac

digest_maker = hmac.new('secret-shared-key-goes-here')

f = open('lorem.txt', 'rb')
try:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)
finally:
    f.close()

digest = digest_maker.hexdigest()
print digest
*/
