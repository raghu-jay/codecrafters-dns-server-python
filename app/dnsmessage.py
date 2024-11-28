
import struct
from dataclasses import dataclass

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
        qdcount=0,
        ancount=0,
        nscount=0,
        arcount=0,
    )
    return header.to_bytes()