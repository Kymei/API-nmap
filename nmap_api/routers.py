import json
import nmap
import uuid
import datetime
from sqlalchemy import desc
from netaddr import *
from database import get_db
from app.schemas import ResponseModel
from fastapi import APIRouter, Body, Depends
from fastapi.responses import FileResponse, JSONResponse, Response
from multiprocessing import Pool
from app.utils import uuid_log
from typing import Union, Optional
from nmap_api.utils import *
from nmap_api.schemas import *
from nmap_api.models import *
from logger import lg

db = get_db()
router = APIRouter(prefix="/scan",tags=["Scan"])

@router.post(
    "/create",
    summary="Create a new scan",
    responses={
        201: {
            "description": "Scan created",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=201
)
def create_scan(
    param:params,
    db: Session = Depends(get_db)):
    nm = nmap.PortScanner()
    log_id = uuid_log()
    scan_id = str(uuid.uuid4()).replace("-", "")
    lg.info(f"{log_id} - Access on /scan/create.")
    lg.info(f"{log_id} - User is {param.email}.")
    date = datetime.datetime.now()
    ports = str(param.low_port)+"-"+str(param.high_port)
    if param.Host:
        query = db.query(scan_status).filter(scan_status.hosts == param.Host).filter(scan_status.status == "to do").first()
        if query:
            return JSONResponse(status_code=400,content={"details":"This scan has already been created"})
        Host = param.Host
        if "127.0.0.1" in Host:
            lg.warning(f"{log_id} - Parameters :\n{json.dumps(dict(host= param.Host, low_port= param.low_port, high_port=param.high_port, email=param.email), default=str)}.")
            return JSONResponse(status_code=403,content={"details":"You can't scan this IP"})
        else:
            add_progress_scan(db, scan_id, scan_id, "to do",param.email,param.Host,ports,param.HNO,date, "")
    elif param.Range:
        query = db.query(scan_status).filter(scan_status.hosts == param.Range).filter(scan_status.status == "to do").first()
        if query:
            return JSONResponse(status_code=400,content={"details":"This scan has already been created"})
        
        if (("/" in param.Range) and (param.Range[-2:] < '30')):
            ip = IPNetwork(param.Range)
            ip_list =list(ip.subnet(30))
            for cidr in ip_list:
                scan_id_cut = str(uuid.uuid4()).replace("-", "")
                add_progress_scan(db, scan_id, scan_id_cut, "to do",param.email,str(cidr),ports,param.HNO,date, "")
        elif ("/" in param.Range):  
            add_progress_scan(db, scan_id, scan_id, "to do",param.email,param.Range,ports,param.HNO,date, "")
        else:
            ip_list = find_CIDR_from_range(param.Range)
            for cidr in ip_list:
                scan_id_cut = str(uuid.uuid4()).replace("-", "")
                add_progress_scan(db, scan_id, scan_id_cut, "to do",param.email,str(cidr),ports,param.HNO,date, "")

    lg.info(f"{log_id} - Scan {scan_id} has been inserted.")
    return JSONResponse(status_code=201, content=scan_id)

@router.get(
    "/to_launch",
    summary="Get the next scan to launch",
    responses={
        200: {
            "description": "Scan gotten",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=200
)
def get_next_scan(
    db: Session = Depends(get_db)):
    date = datetime.datetime.now()
    date = str(date).split(' ')
    log_id = uuid_log()
    lg.info(f"{log_id} - Access on /scan/get_status/.")
    if ("22:00:00" > date[1] > "04:00:00"):
        scan_todo = db.query(scan_status).order_by(desc(-scan_status.initiation_date)).filter(scan_status.status == "to do", scan_status.HNO != True).first()
        if scan_todo:
            db.query(scan_status).filter(scan_status.id_cut == scan_todo.id_cut).update({scan_status.status: "in progress"})
            db.commit()
            return JSONResponse(status_code=200,content={'id_scan':scan_todo.id_scan, 'id_cut':scan_todo.id_cut, 'hosts':scan_todo.hosts, 'port':scan_todo.ports})
    else:
        scan_todo = db.query(scan_status).filter(scan_status.status == "to do").first()
        if scan_todo:
            db.query(scan_status).filter(scan_status.id_cut == scan_todo.id_cut).update({scan_status.status: "in progress"})
            db.commit()
            return JSONResponse(status_code=200,content={'id_scan':scan_todo.id_scan, 'id_cut':scan_todo.id_cut, 'hosts':scan_todo.hosts, 'port':scan_todo.ports})
    return Response(status_code=204)

@router.get(
    "/get/{email}",
    summary="get the scans done by a user",
    responses={
        200: {
            "description": "Scan gotten",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=200
)
def get_scans(
    email: str,
    db: Session = Depends(get_db)):
    log_id = uuid_log()
    lg.info(f"{log_id} - Access on /scan/get/'user'.")
    lg.info(f"{log_id} - User is {email}.")
    lg.info(f"{log_id} - Parameters :\n{json.dumps(dict(email=email), default=str)}.")
    scans = db.query(scan_status).filter(scan_status.email == email).all()
    response = {}
    for scan in scans:
        if scan.id_scan != scan.id_cut:
            if not scan.id_scan in response:
                response[scan.id_scan] = []
                response[scan.id_scan].append({scan.id_cut:scan.status})
            else:
                response[scan.id_scan].append({scan.id_cut:scan.status})    
        else:
            response[scan.id_scan]=scan.status
    return JSONResponse(status_code=200,content=response)

@router.get(
    "/{id_scan}",
    summary="get the result of a scan",
    responses={
        200: {
            "description": "Scan gotten",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=200
)
def get_scans(
    id_scan: str,
    db: Session = Depends(get_db)):
    log_id = uuid_log()
    lg.info(f"{log_id} - Access on /scan/get/'user'/'id_scan'.")
    lg.info(f"{log_id} - Parameters :\n{json.dumps(dict(id_scan=id_scan), default=str)}.")
    status = db.query(scan_status).filter(scan_status.id_scan == id_scan).all()
    response = []
    if not status:
        return JSONResponse(status_code=404,content={'detail':'this scan does not exists'})
    for scan in status:
        if scan.status == "done":
            response_result = get_scan_result(db, scan.id_cut)
            response.append({scan.id_cut : response_result})
        else:
            response.append({scan.id_cut:scan.status})
    return JSONResponse(status_code=200,content=response)
    
@router.put(
    "/{id_scan}",
    summary="Update the scan status",
    responses={
        200: {
            "description": "Scan gotten",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=200
)
def update_scans_status(
    id_scan : str,
    status : str,
    db: Session = Depends(get_db)):
    log_id = uuid_log()
    lg.info(f"{log_id} - Access on /scan/update_status/.")
    if (status == "to do"):
        return JSONResponse(status_code=403,content="Can put that status")
    elif(status == "done"):
        end_date = datetime.datetime.now()
        db.query(scan_status).filter(scan_status.id_cut == id_scan).update({scan_status.ending_date: end_date})
    db.query(scan_status).filter(scan_status.id_cut == id_scan).update({scan_status.status: status})
    db.commit()
    return JSONResponse(status_code=200,content="Status updated")

@router.post(
    "/{id_scan}",
    summary="Populate the database with scan results",
    responses={
        200: {
            "description": "Scan gotten",
            "model": ResponseModel
        },
        403: {
            "description": "Invalid token",
            "model": ResponseModel
        },
        404: {
            "description": "Not Found",
            "model": ResponseModel
        },
        400: {
            "description": "Bad Request",
            "model": ResponseModel
        }
    },
    status_code=200
)
def update_scans_result(
    id_scan : str,
    result : resultat,
    db: Session = Depends(get_db)):
    log_id = uuid_log()
    lg.info(f"{log_id} - POST Access on /scan/'id_scan' .")
    add_new_scan(db, result.id_major, result.id_cut, result.host, result.protocol, result.port, result.state, result.name, result.product, result.version, result.extra, result.cpe, result.vulnerable)
    return JSONResponse(status_code=200,content="Status updated")