


def getTexture(coor):
    llano = [
        'S10W067', 'S10W066', 'S11W070', 'S11W069', 'S11W068', 'S11W067', 'S11W066', 'S12W070', 'S12W069', 'S12W068',
        'S12W067', 'S12W066', 'S12W065', 'S13W067', 'S13W066', 'S13W065', 'S13W064', 'S13W063', 'S14W067', 'S14W066',
        'S14W065', 'S14W064', 'S14W063', 'S14W062', 'S14W061', 'S15W067', 'S15W066', 'S15W065', 'S15W064', 'S15W063',
        'S15W062', 'S15W061', 'S16W067', 'S16W066', 'S16W065', 'S16W064', 'S16W063', 'S16W062', 'S16W061', 'S17W065',
        'S17W064', 'S17W063', 'S17W062', 'S17W061', 'S17W060', 'S17W059', 'S18W064', 'S18W063', 'S18W062', 'S18W061',
        'S18W060', 'S18W059', 'S18W058', 'S19W064', 'S19W063', 'S19W062', 'S19W061', 'S19W060', 'S19W059', 'S19W058',
        'S20W064', 'S20W063', 'S20W062', 'S20W061', 'S20W060', 'S20W059', 'S20W058', 'S21W062', 'S21W059', 'S21W058'
    ]

    valle = [
        'S17W067', 'S17W066', 'S18W067', 'S18W066', 'S18W065', 'S19W066', 'S19W065', 'S20W065',
        'S21W065', 'S21W064', 'S22W065', 'S22W064', 'S22W063', 'S23W065', 'S23W064', 'S23W063'
    ]
    altiplano = [
        'S13W069', 'S13W068', 'S14W070', 'S14W069', 'S14W068', 'S15W070', 'S15W069', 'S15W068', 'S16W070', 'S16W069',
        'S16W068', 'S17W070', 'S17W069', 'S17W068', 'S18W070', 'S18W069', 'S18W068', 'S19W070', 'S19W069', 'S19W068',
        'S19W067', 'S20W069', 'S20W068', 'S20W067', 'S20W066', 'S21W069', 'S21W068', 'S21W067', 'S21W066', 'S22W069',
        'S22W068', 'S22W067', 'S22W066', 'S23W069', 'S23W068', 'S23W067', 'S23W066'
    ]
    if coor in llano:
        return 'Llano'
    elif coor in altiplano:
        return 'Altiplano'
    elif coor in valle:
        return 'Valle'


# print(getTexture('S18W064'))

#Es necesario importar las depencendias necesarias
from datetime import date
from datetime import datetime

now = datetime.now()
format = now.strftime('%d/%m/%Y')
print(format)


