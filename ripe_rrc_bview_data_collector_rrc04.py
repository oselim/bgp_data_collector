import requests
import subprocess
import gzip
import os

collectors = ["rrc04"]
year_list = ['2011', '2013', '2015', '2017', '2019', '2021']
month = '01'
day_list = [ '01', '02', '03', '04', '05', '06', '07']
hour_list = ['0759', '1559', '2359', '0000', '0800', '1600']
record_type = "bview"

dir_name_unzip = 'rrc_04_ribs_data_unzip/'
dir_name_bgpdump = 'rrc_04_ribs_data_bgpdump/'
base_url = 'http://data.ris.ripe.net/'

def decompress_file(base_file_name, compressed_content):
    with open(dir_name_unzip + base_file_name, 'wb') as f_out:
            f_out.write(gzip.decompress(compressed_content))



def bgpdump_file(file_name):
    dump_file_name = file_name + '_bgpdump'
    with open(dir_name_bgpdump + dump_file_name, 'wb') as file:
        file.write(subprocess.run(['bgpdump', "-m", dir_name_unzip + file_name ], stdout=subprocess.PIPE).stdout)
    os.remove(dir_name_unzip + file_name)


for collector in collectors:
    for year in year_list:
        for day in day_list:
            for hour in hour_list:
                base_file_name = record_type + '.' + year + month + day + '.' + hour
                gzip_file_name = base_file_name + '.gz'

                
                url = base_url + collector + '/' + year + '.' + month + '/' + gzip_file_name
                response = requests.get(url)
                print(str(response.status_code) + ' ' + collector + ' ' + base_file_name)
                if response.status_code == 200:                    
                    content = response.content
                    save_file_name = collector + '_' + base_file_name
                    decompress_file(save_file_name, content)
                    bgpdump_file(save_file_name)
print('Done!!')