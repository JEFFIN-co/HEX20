from hex20_tc_router.security.encoder import encode_three_letter,decode_three_letter
from hex20_tc_router.security.authenticator import create_auth_tag
from hex20_tc_router.security.gate import SecurityGate
SECRET="TEST-HEX20-SECRET"
def test_encoding_round_trip():
    e=encode_three_letter("HKR",SECRET); assert decode_three_letter(e,SECRET)=="HKR"
def test_auth_and_replay():
    e=encode_three_letter("HKR",SECRET); t=create_auth_tag(SECRET,e,1); g=SecurityGate(SECRET); assert g.verify(e,1,t).accepted; assert not g.verify(e,1,t).accepted
