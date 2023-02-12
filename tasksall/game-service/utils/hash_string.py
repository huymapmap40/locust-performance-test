from Crypto.Hash import SHA1
import base64

def gen_hash_string(random_string, game_id, cdata, gdata, grdata):
    idx = len(random_string) / 3
    test_string = random_string[0:idx].random_string[idx+1:len(random_string)-1]
    data_string = f'{game_id}{cdata}{gdata}{grdata}'
    sha1 = SHA1.new()
    sha1.update(f'{test_string},{data_string},{test_string}'.encode())
    return base64.b64encode(sha1.digest())
