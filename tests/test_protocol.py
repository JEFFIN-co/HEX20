from hex20_tc_router.protocol.frame import TransferFrame, FrameSynchronizer, decode_frame
from hex20_tc_router.protocol.packet import SpacePacket

def test_frame_round_trip():
    raw=TransferFrame(vcid=1,payload=b"abc").encode(); frames=FrameSynchronizer().feed(b"noise"+raw+b"tail"); assert len(frames)==1; assert decode_frame(frames[0]).payload==b"abc"

def test_packet_round_trip():
    p=SpacePacket(100,3,1,b"hello",7); assert SpacePacket.decode(p.encode())==p
