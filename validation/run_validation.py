from __future__ import annotations
import csv,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from hex20_tc_router.processing.end_to_end_processor import EndToEndProcessor,SECRET
from scenario_factory import build
from hex20_tc_router.simulation.statistics import summarize,count_field
SCENARIOS=[("VALID_HKR",180),("VALID_MEMORY",150),("VALID_FUNCTION",130),("VALID_CONNECTION",120),("NOISE_PLUS_VALID",100),("CRC_FAULT",80),("BAD_AUTH",70),("HEADER_MISMATCH",60),("UNKNOWN_AUTH_COMMAND",40),("MALFORMED_SECURITY",30),("MALFORMED_PACKET",20),("REPLAY",20)]
OUT_JSON=ROOT/"validation"/"results.json"; OUT_CSV=ROOT/"validation"/"results.csv"
def main():
    p=EndToEndProcessor(SECRET); rows=[]; previous=None; counter=1; start=time.perf_counter()
    for scenario,n in SCENARIOS:
        for _ in range(n):
            stream=build(scenario,counter,previous)
            result=p.process_stream(stream)[0]
            if scenario=="VALID_HKR": previous=stream
            rows.append({"index":len(rows)+1,"scenario":scenario,"accepted":result.accepted,"stage":result.stage,"reason":result.reason,"command":result.command,"apid":result.apid,"service":result.service,"subtype":result.subtype,"latency_ms":result.latency_ms}); counter+=1
    elapsed=time.perf_counter()-start
    class R:
        def __init__(self,r): self.__dict__.update({k:r[k] for k in ("accepted","stage","reason","command","latency_ms")})
    objs=[R(r) for r in rows]; stats=summarize(objs,elapsed)
    summary={"configuration":{"commands_requested":1000,"scenario_distribution":dict(SCENARIOS)},"summary":stats.to_dict(),"by_scenario":{},"by_stage":count_field(objs,"stage"),"by_reason":count_field(objs,"reason"),"by_command":count_field(objs,"command"),"processor_counters":p.counters,"elapsed_s":elapsed}
    for scenario,_ in SCENARIOS:
        sub=[o for o,r in zip(objs,rows) if r["scenario"]==scenario]; summary["by_scenario"][scenario]={"total":len(sub),"accepted":sum(x.accepted for x in sub),"rejected":sum(not x.accepted for x in sub),"stages":count_field(sub,"stage"),"reasons":count_field(sub,"reason")}
    OUT_JSON.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    with OUT_CSV.open("w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    print(json.dumps(summary["summary"],indent=2)); return summary
if __name__=="__main__": main()
