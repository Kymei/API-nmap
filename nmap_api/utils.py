import json
import nmap
import uuid
import ipaddress
import datetime
from nmap_api.models import *
from sqlalchemy.orm import Session

def add_new_scan(db: Session, id_major:str, id_scan:str, host:str, protocol:str, port:int,state:str, name:str, product:str, version:str, extra:str, cpe:str,vulnerable:str):
    new_request = result(
        id_major=id_major,
        id_scan=id_scan,
        host=host,
        protocol=protocol,
        port=port,
        state=state,
        name=name,
        product=product,
        version=version,
        extra=extra,
        cpe=cpe,
        vulnerable=vulnerable
    )
    db.add(new_request)
    db.commit()
    return new_request

def add_progress_scan(db: Session, id_scan:str,id_cut:str, status:str,email:str,hosts:str,ports:str, HNO:bool,date:str, end_date:str):
    new_request_status = scan_status(
        id_scan=id_scan,
        id_cut=id_cut,
        status=status,
        email=email,
        hosts=hosts,
        ports=ports,
        HNO=HNO,
        initiation_date=date,
        ending_date=end_date
    )
    db.add(new_request_status)
    db.commit()
    return new_request_status

def get_scan_result(db: Session, id_scan:str):
    print(id_scan)
    query = db.query(scan_status).filter(scan_status.id_cut == id_scan).first()
    if not query:
        return "You can't see the results of this scan"
    query_result = db.query(result).filter(result.id_major == id_scan).all()
    hosts =[]
    resultat = []
    resultat_final = {}
    itter = 0
    for x in query_result:
        if itter == len(query_result):
            resultat_final[hosts[-1]]=resultat
            break
        if x.host not in hosts:
            if not len(hosts) == 0:
                resultat_final[hosts[-1]]=resultat
                resultat = []
                hosts.append(x.host)
            else:
                hosts.append(x.host)
        resultat.append(
            {
                'name': x.name,
                'protocol': x.protocol,
                'port': x.port,
                'state': x.state,
                'product': x.product,
                'version': x.version,
                'extrainfo': x.extra,
                'cpes': x.cpe,
                'cve': x.vulnerable
            }
        )
        itter += 1
        if (itter== len(query_result)):
            resultat_final[hosts[-1]]=resultat
    return resultat_final

def find_CIDR_from_range(IPrange): #Reveive and IP range in this format : "xxx.xxx.xxx.xxx-XXX.XXX.XXX.XXX"
    IPlist = IPrange.split("-")
    startip = ipaddress.IPv4Address(IPlist[0])
    endip = ipaddress.IPv4Address(IPlist[1])
    listRange = ipaddress.summarize_address_range(startip, endip)
    CIDRlist = []
    for CIDR in listRange:
        CIDRlist.append(str(CIDR))
    return CIDRlist
