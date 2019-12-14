import hid
import time
import sys
import requests

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

L_ACCEL_OFFSET_X = 350
L_ACCEL_OFFSET_Y = 0
L_ACCEL_OFFSET_Z = 4081
R_ACCEL_OFFSET_X = 350
R_ACCEL_OFFSET_Y = 0
R_ACCEL_OFFSET_Z = -4081

SCORE_BORDER_1 = 300000
SCORE_BORDER_2 = 800000
SCORE_BORDER_3 = 1400000

fileName = './R_data.txt'

MY_PRODUCT_ID = L_PRODUCT_ID

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

def is_left():
    return MY_PRODUCT_ID == L_PRODUCT_ID

def to_int16le_from_2bytes(hbytebe, lbytebe):
    uint16le = (lbytebe << 8) | hbytebe 
    int16le = uint16le if uint16le < 32768 else uint16le - 65536
    return int16le

def get_nbit_from_input_report(input_report, offset_byte, offset_bit, nbit):
    return (input_report[offset_byte] >> offset_bit) & ((1 << nbit) - 1)

def get_button_down(input_report):
    return get_nbit_from_input_report(input_report, 5, 0, 1)

def get_button_up(input_report):
    return get_nbit_from_input_report(input_report, 5, 1, 1)

def get_button_right(input_report):
    return get_nbit_from_input_report(input_report, 5, 2, 1)

def get_button_left(input_report):
    return get_nbit_from_input_report(input_report, 5, 3, 1)

def get_stick_left_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 6, 0, 8) | (get_nbit_from_input_report(input_report, 7, 0, 4) << 8)

def get_stick_left_vertical(input_report):
    return get_nbit_from_input_report(input_report, 7, 4, 4) | (get_nbit_from_input_report(input_report, 8, 0, 8) << 4)

def get_stick_right_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 9, 0, 8) | (get_nbit_from_input_report(input_report, 10, 0, 4) << 8)

def get_stick_right_vertical(input_report):
    return get_nbit_from_input_report(input_report, 10, 4, 4) | (get_nbit_from_input_report(input_report, 11, 0, 8) << 4)

def get_accel_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 13 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 14 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_X if is_left() else R_ACCEL_OFFSET_X))

def get_accel_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 15 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 16 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Y if is_left() else R_ACCEL_OFFSET_Y))

def get_accel_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 17 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 18 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Z if is_left() else R_ACCEL_OFFSET_Z))

def get_gyro_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 19 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 20 + sample_idx * 12, 0, 8))

def get_gyro_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 21 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 22 + sample_idx * 12, 0, 8))

def get_gyro_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 23 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 24 + sample_idx * 12, 0, 8))

def joycon_connect(joycon_device):
    joycon_device.open(VENDOR_ID, MY_PRODUCT_ID)
    # 6軸センサーを有効化
    write_output_report(joycon_device, 0, b'\x01', b'\x40', b'\x01')
    # 設定を反映するためには時間間隔が必要
    time.sleep(0.02)
    # 60HzでJoy-Conの各データを取得するための設定
    write_output_report(joycon_device, 1, b'\x01', b'\x03', b'\x30')

def calculate_score(joycon_device):
    base_time = time.time()
    score = 0
    while abs(time.time() - base_time) < 1.0:
        input_report = joycon_device.read(49)
        accel_x = get_accel_x(input_report)
        score += abs(accel_x)
    return score

if __name__ == '__main__':
    joycon_device = hid.device()
    joycon_connect(joycon_device)
    print ('joy-con L')
    player_id = '0' if is_left() else '1'
    try:
        while True:
            file = open(fileName, 'w')
            score = calculate_score(joycon_device)
            print(score)
            if SCORE_BORDER_1 > score :
                print('0')
                requests.get('https://script.google.com/macros/s/AKfycbzW8sHIrKatmbST8SIhws6x_h-Zy3nrThWzluPhGf9fWkBuJ4w/exec?player='+player_id+'&text='+'0')
            elif SCORE_BORDER_1 < score < SCORE_BORDER_2 :
                print('1')
                requests.get('https://script.google.com/macros/s/AKfycbzW8sHIrKatmbST8SIhws6x_h-Zy3nrThWzluPhGf9fWkBuJ4w/exec?player='+player_id+'&text='+'1')
            elif SCORE_BORDER_2 < score < SCORE_BORDER_3 :
                print('2')
                requests.get('https://script.google.com/macros/s/AKfycbzW8sHIrKatmbST8SIhws6x_h-Zy3nrThWzluPhGf9fWkBuJ4w/exec?player='+player_id+'&text='+'2')
            else :
                print('3')
                requests.get('https://script.google.com/macros/s/AKfycbzW8sHIrKatmbST8SIhws6x_h-Zy3nrThWzluPhGf9fWkBuJ4w/exec?player='+player_id+'&text='+'3')
            file.close()
    except KeyboardInterrupt:
        joycon_device.close()
        sys.exit()