POSHARDWARE_PROFILE = {
    'TICKET': {
        'Approx-appPOS80AM': {
            'name': 'Approx - appPOS80AM (80mm)',
            "config": ["0x0483", "0x5743"],
            "port": "usb",
            "column": 48,
            "cut": True,
        },
        'Approx-appPOS80AM3': {
            'name': 'Approx - appPOS80AM3 (80mm)',
            "config": ["0x1fc9", "0x2016"],
            "port": "usb",
            "column": 48,
            "cut": True,
        },
        '10POS-RP-10N': {
            'name': '10POS - RP-10N (80mm)',
            "config": ["0x0471", "0x0055", None, None, "0x02"],
            "port": "usb",
            "column": 48,
            "cut": True,
        },
        'EPSON-TM-T20II': {
            'name': 'EPSON TM-T20II (80mm)',
            "config": ["0x04b8", "0x0e15"],
            "port": "usb",
            "column": 48,
            "cut": True,
        },
        'Excelvan-ZJ-5890T': {
            'name': 'Excelvan - ZJ-5890T (58mm)',
            "config": ["0x0416", "0x5011", None, None, None, "bitImageColumn"],
            "port": "usb",
            "column": 32,
            "cut": False,
        },
    },
    'WEIGHT': {
        'PCE-BSH6000': {
            'name': 'PCE Instruments: PCE-BSH 6000',
            "config": ["usb0", 9600, "8N1"],
            "protocol": "serial"
        }
    }
}
POSHARDWARE_PROFILE['CASH'] = POSHARDWARE_PROFILE['TICKET']
