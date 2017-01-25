

import sys,re
import requests


ranger_host = raw_input("\nEnter Ranger host: ")
ranger_port = raw_input("\nEnter Ranger port: ")
ranger_user = raw_input("\nEnter Ranger user: ")
ranger_pw   = raw_input("\nEnter Ranger pw: ")


def ranger_get_groups(ranger_host='localhost', ranger_port=6080, ranger_user='admin', ranger_pw='admin'):
    '''
    Queries Ranger to get a list of groups
    http://localhost:6080/service/xusers/groups?page=0&pageSize=25&startIndex=0&_=1485222679700
    '''
    url = 'http://' + str(ranger_host) + ':' + str(ranger_port) + '/service/xusers/groups?page=0&pageSize=5000&startIndex=0'
    r = requests.get(url, auth=(ranger_user,ranger_pw))
    
    if r.status_code == 200:
        groups = [re.sub('<.*?>','',group) for group in re.findall('<name>.*?</name>',r.content)]
    else:
        groups = []
    
    return (r.status_code, groups)


def ranger_delete_group(group, ranger_host='localhost', ranger_port=6080, ranger_user='admin', ranger_pw='admin'):
    '''
    Deletes a group from Ranger
    '''
    url = 'http://' + str(ranger_host) + ':' + str(ranger_port) + '/service/xusers/groups/groupName/' + str(group) + '?forceDelete=true'
    r = requests.delete(url, auth=(ranger_user,ranger_pw))
    if r.status_code == 204:
        print '[ INFO ] Deleted ' + str(group) + ' (status: ' + str(r.status_code)
    else:
        print '[ FAILURE ] Failed to deleted ' + str(group) + ' (status: ' + str(r.status_code)


####################################################################################
#
#   Core Loop
#
####################################################################################

status_code, groups = ranger_get_groups(ranger_host, ranger_port, ranger_user, ranger_pw)

for group in groups:
    
    do_not_delete_these_groups = ['public','hadoop','slider','users','ranger','hdfs','splash','root',
                                'nfsnobody','hue','admin','xapolicymgr','kms','network','legal','it',
                                'marketing','guest','amy_ds','holger_gov','raj_ops','maria_dev','unit']
    
    if group.lower() not in do_not_delete_these_groups:
        raw_input('\nPress Enter to DELETE group: ' + str(group))
        ranger_delete_group(str(group), ranger_host, ranger_port, ranger_user, ranger_pw)


#ZEND
