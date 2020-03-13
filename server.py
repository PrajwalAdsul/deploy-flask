from flask import Flask, render_template, request
import math
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def welcome():
    return render_template('form.html')

def gethex(bitlist):
    lookup = {
    '0000' : '0', '0001' : '1', '0010' : '2', '0011' : '3', '0100' : '4', '0101' : '5', '0110' : '6', 
    '0111' : '7', '1000' : '8', '1001' : '9', '1010' : 'A', '1011' : 'B', '1100' : 'C', '1101' : 'D', 
    '1110' : 'E', '1111' : 'F'
    }
    res = ''
    j = 0
    for i in range(0, 8):
        temp_str = ''
        temp_str = temp_str + str(bitlist[i * 4])
        temp_str = temp_str + str(bitlist[i * 4 + 1])
        temp_str = temp_str + str(bitlist[i * 4 + 2])
        temp_str = temp_str + str(bitlist[i * 4 + 3])
        res = res + lookup[temp_str]
        if(i == 7):
            break
        if(j):
            res = res + '.'
            j = 0
        else:
            j = 1
    return res

def binn(k):
    res = ''
    i = 0
    while(k > 0 and i < 8):
        x = k % 2
        res = res + str(x)
        k = k / 2
        i = i + 1
    return res

def get_bin_ip(ip):
    ip_lis = ip.split('.')
    ip = ''
    ip = ip + binn(int(ip_lis[0]))
    ip = ip + binn(int(ip_lis[1]))
    ip = ip + binn(int(ip_lis[2]))
    ip = ip + binn(int(ip_lis[3]))
    return ip

@app.route('/result', methods=['POST'])
def result():
    ip = request.form.get("IP_address", type = str)
    no_of_subnets = request.form.get("no_of_subnets", type = str)
    slash =  ip.split('/')
    ipp = slash[0]
    ippp = ipp
    bin_ip = get_bin_ip(ipp)

    slash = slash[1]
    bitlist = list()
    for i in range(0, int(slash)):
        bitlist.append(1)
    for i in range(int(slash), 32):
        bitlist.append(0)

    mask_bits_req = math.log2(int(no_of_subnets)) + int(slash); 
    max_no_of_subnets = 2 ** (32 - int(slash))  



    hex_mask = gethex(bitlist)
    bin_ip = '.'.join([bin(int(x)+256)[3:] for x in ipp.split('.')])

    j = 0
    bin_ba = [x for x in bin_ip if x != '.']
    for i in range(0, 32 - int(slash)):
        if(bin_ba == '.'):
            i = i - 1
        else:
            bin_ba[31 - j] = 1
            j = j + 1

    sbin_ba = ''
    for x in bin_ba:
        sbin_ba = sbin_ba + str(x)

    hex_ba = gethex(sbin_ba)

    bitlistt = ''
    for x in bitlist:
        bitlistt = bitlistt + str(x)

    return render_template('result.html', ipp = ippp, bin_ip = bin_ip, bin_ba = sbin_ba, hex_ba = hex_ba, hex_mask = hex_mask, 
        length = len(bitlist), subnet_mask = bitlistt,
     mask_bits_req = mask_bits_req, max_no_of_subnets = max_no_of_subnets)

if __name__ == '__main__':
    app.run(debug=True)
