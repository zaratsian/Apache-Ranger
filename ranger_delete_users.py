
import re
import requests



def ranger_get_users(ranger_host='localhost', ranger_port=6080, ranger_user='admin', ranger_pw='admin'):
    '''
    Queries Ranger to get a list of user names
    http://localhost:6080/service/xusers/users?page=0&pageSize=25&total_pages=3&totalCount=52&sortBy=id&sortType=asc&startIndex=0&userRoleList%5B%5D=ROLE_SYS_ADMIN&userRoleList%5B%5D=ROLE_USER&_=1485219402896
    '''
    url = 'http://' + str(ranger_host) + ':' + str(ranger_port) + '/service/xusers/users'
    r = requests.get(url, auth=(ranger_user,ranger_pw))
    
    if r.status_code == 200:
        usernames = [re.sub('<.*?>','',user) for user in re.findall('<name>.*?</name>',r.content)]
    else:
        usernames = []
    
    return (r.status_code, usernames)



def ranger_delete_user(username, ranger_host='localhost', ranger_port=6080, ranger_user='admin', ranger_pw='admin'):
    '''
    Deletes a user from Ranger
    '''
    url = 'http://' + str(ranger_host) + ':' + str(ranger_port) + '/service/xusers/users/userName/' + str(username) + '?forceDelete=true'
    r = requests.delete(url, auth=(ranger_user,ranger_pw))
    if r.status_code == 204:
        print '[ INFO ] Deleted ' + str(username) + ' (status: ' + str(r.status_code)
    else:
        print '[ FAILURE ] Failed to deleted ' + str(username) + ' (status: ' + str(r.status_code)



# Core Loop

status_code, usernames = ranger_get_users('localhost', 6080, 'admin', 'admin')

for username in usernames:
    
    do_not_delete_these_users = ['admin','rangerusersync','rangertagsync','hive','slider','infra-solr','atlas','ams',
                                'falcon','ranger','spark','flume','hbase','hcat','storm','zookeeper','oozie','tez',
                                'zeppelin','livy','ambari-qa','kafka','hdfs','sqoop','yarn'
                                'splash','mapred','knox','amb_ranger_admin','hadoop','nfsnobody','hue','xapolicymgr',
                                'kms','network1','network2','network3','legal1','legal2','legal3','it1','it2','it3',
                                'mktg1','mktg2','mktg3','guest','amy_ds','holger_gov','raj_ops','maria_dev','unit']
    
    if username.lower() not in do_not_delete_these_users:
        raw_input('Press Enter to DELETE user: ' + str(username))
        ranger_delete_user('tiki3', ranger_host='localhost', ranger_port=6080, ranger_user='admin', ranger_pw='admin')


#ZEND
