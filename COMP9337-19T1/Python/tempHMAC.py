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

