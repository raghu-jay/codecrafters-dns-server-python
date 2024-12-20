
import struct
from dataclasses import dataclass
from typing import List


@dataclass
class DNSQuestion:
    qname: bytes
    qtype: int
    qclass: int

    def to_bytes(self) -> bytes:
        return self.qname + struct.pack("!HH", self.qtype, self.qclass)

@dataclass
class DNSResource:
    name: bytes
    type_: int
    class_: int
    ttl: int
    rdlength: int
    rdata: bytes
    def to_bytes(self) -> bytes:
        return (
            self.name
            + struct.pack("!HHIH", self.type_, self.class_, self.ttl, self.rdlength)
            + self.rdata
        )


@dataclass
class DNSHeader:

    id: int = 0  # 16 bits
    qr: int = 0  # 1 bit
    opcode: int = 0  # 4 bits
    aa: int = 0  # 1 bit
    tc: int = 0  # 1 bit
    rd: int = 0  # 1 bit
    ra: int = 0  # 1 bit
    z: int = 0  # 3 bits
    rcode: int = 0  # 4 bits
    qdcount: int = 0  # 16 bits
    ancount: int = 0  # 16 bits
    nscount: int = 0  # 16 bits
    arcount: int = 0  # 16 bits

    def to_bytes(self) -> bytes:
        # Pack the first 16 bits: ID
        first_16 = self.id
        # Pack the next 16 bits: QR(1) | OPCODE(4) | AA(1) | TC(1) | RD(1) | RA(1) | Z(3) | RCODE(4)
        flags = (
            (self.qr << 15)
            | (self.opcode << 11)
            | (self.aa << 10)
            | (self.tc << 9)
            | (self.rd << 8)
            | (self.ra << 7)
            | (self.z << 4)
            | self.rcode
        )

        # Pack everything into bytes using network byte order (big-endian)
        return struct.pack(
            "!HHHHHH",
            first_16,  # ID
            flags,  # Flags
            self.qdcount,  # QDCOUNT
            self.ancount,  # ANCOUNT
            self.nscount,  # NSCOUNT
            self.arcount,  # ARCOUNT
        )

@dataclass
class DNSMessage:

    header: DNSHeader
    question: List[DNSQuestion]
    resource: List[DNSResource] = None

    def to_bytes(self) -> bytes:
        return (
            self.header.to_bytes()
            + b"".join([q.to_bytes() for q in self.question])
            + b"".join([r.to_bytes() for r in self.resource])
        )

def create_dns_response() -> bytes:
    # Create header with specified values
    header = DNSHeader(
        id=1234,  # Specified ID
        qr=1,  # This is a response
        opcode=0,
        aa=0,
        tc=0,
        rd=0,
        ra=0,
        z=0,
        rcode=0,
        qdcount=1,
        ancount=1,
        nscount=0,
        arcount=0,
    )

    question = DNSQuestion(qname=b"\x0ccodecrafters\x02io\x00", qtype=1, qclass=1)

    resource = DNSResource(
        name=b"\x0ccodecrafters\x02io\x00",
        type_=1,
        class_=1,
        ttl=60,
        rdlength=4,
        rdata=b"\x08\x08\x08\x08",
    )

    res = DNSMessage(header, [question], [resource]).to_bytes()
    return res



