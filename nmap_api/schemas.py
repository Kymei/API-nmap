from pydantic import BaseModel, root_validator
from pydantic.dataclasses import dataclass
from typing import Optional, Union
import socket
import re

class Scan_Response(BaseModel):
    detail: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "detail": "Response message"
            }
        }

@dataclass
class params:
    Host: Optional[str] = None
    Range: Optional[str] = None
    email: Union[str, None] = "name@business.fr"
    low_port: Union[int, None] = 1
    high_port: Union[int, None] = 65535
    HNO: Optional[bool] = False

    @root_validator
    def any_of(cls,v):
        if not any(v.values()):
            raise ValueError('One of Host or Range must have a value')
        i,j,k,l,m,o=v
        if v[i] and v[j]:
            raise ValueError('Only one of Host or Range must have a value')
        if len(v[k]) == 0:
            raise ValueError('You need to provide an email to perform this request')

        if v[i]:
            try:
                if len(v[i])>=15:
                    x=v[i].split(' ')
                    for z in x:
                        ip = socket.inet_aton(z)
                else:
                    ip = socket.inet_aton(v[i])
            except:
                raise ValueError('Make sure your Host is an IP address')
        if v[j]:
            # ip_range =  re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\-[0-9]{1,3}", v[j])
            ip_range =  re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\-[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", v[j])
            ip_cidr  =  re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[2-3]{1}[0-9]{1}", v[j])
            if ((len(ip_range) == 0) and (len(ip_cidr) == 0)):
                raise ValueError('Make sure your Range is an IP range formated like : \'xxx.xxx.xxx.xxx-XXX.XXX.XXX.XXX\' OR \'xxx.xxx.xxx.xxx/netmask\'')
            elif (len(ip_range) != 0):
                if ip_range[0] != v[j] : 
                    raise ValueError('Make sure your Range is an IP range formated like : \'xxx.xxx.xxx.xxx-XXX.XXX.XXX.XXX\' OR \'xxx.xxx.xxx.xxx/netmask\'')
            elif (len(ip_cidr) != 0):
                if ip_cidr[0] != v[j] : 
                    raise ValueError('Make sure your Range is an IP range formated like : \'xxx.xxx.xxx.xxx-XXX.XXX.XXX.XXX\' OR \'xxx.xxx.xxx.xxx/netmask\'')
        return v

class resultat(BaseModel):
    id_major: str =""
    id_cut: str =""
    host: str =""
    protocol: str =""
    port: int = 0
    state: str =""
    name: str =""
    product: str =""
    version: str =""
    extra: str =""
    cpe: str =""
    vulnerable: str =""
    
    class Config:
            orm_mode = True
