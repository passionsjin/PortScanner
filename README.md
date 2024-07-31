# PortScanner


## Options
| 옵션         | 설명                    | 비고            |
|------------|-----------------------|---------------|
| -v -vv     | verbose, more verbose |               |
| -d -dd     | debug, more debug     |               |
| -sS        | syn 스캔                |               |
| -p {port}  | scan port 범위          |               |
| -oX {path} | xml 출력                | `-` stdout 출력 |
| -O         | OS detect             |               |

## Option 예시

#### OS detect, Syn Scan, port 0~10000, 많은정보(fingerprint 포함), xml 출력
`nmap -vv -oX -sS -O -p 0-10000 192.168.0.0/24`

## 성능측정

#### Local 환경 기준
- 192.168.0.0/24
  - Single Process : 0s
  - Multi Process : 0s
