from hex20_tc_router.processing.end_to_end_processor import EndToEndProcessor,SECRET,build_ground_frame

def test_all_demo_commands_accept():
    p=EndToEndProcessor(SECRET)
    for i,c in enumerate(("HKR","MEM","FUN","CON"),1): assert p.process_stream(build_ground_frame(c,i,SECRET))[0].accepted

def test_faults_reject():
    p=EndToEndProcessor(SECRET)
    assert not p.process_stream(build_ground_frame("HKR",1,SECRET,tamper_tag=True))[0].accepted
    assert not p.process_stream(build_ground_frame("HKR",2,SECRET,tamper_crc=True))[0].accepted
    assert not p.process_stream(build_ground_frame("HKR",3,SECRET,service_override=6))[0].accepted
