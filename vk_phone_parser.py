import vk_api
import configparser

def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def read_users():
    users_list = []
    #f=open('users.txt', 'r')
    f=open('users_test.txt', 'r')
    for line in f:
        users_list.append(line.strip())        
    f.close
    return users_list

def write_phones(data):
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(data)

'''
def parse_ids(users, vk):
    ids = vk.users.get({'user_ids':users})
    print(ids)
    ids = ids['phone']
    return ids
'''    

def main():
    parsed = []
    users = []
    users_str = ''
    #Загружаем ИД юзеров
    users_list = read_users()
    # Загружаем конфиг
    conf = configparser.RawConfigParser()
    conf.read('config.cfg')
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    print('Loggin into ' + login)
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    vk = vk_session.get_api()
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    #Поочередно собираем все телефоны с каждого пользователя    
    for user in users_list:
        users_str = user + ',' + users_str
    users_str = users_str[:-1]    
    vk = vk_session.get_api()
    response = vk.users.get(user_ids=users_str,fields='contacts')
    parsed = ''
    for user in response:        
        if user.get('mobile_phone'):
            parsed = parsed + str(user.get('id')) + ';' \
                    + str(user.get('first_name')) + ';' \
                    + str(user.get('last_name')) + ';' \
                    + str(user.get('mobile_phone')) + ';' + '\n'
        if user.get('home_phone'):
            parsed = parsed + str(user.get('id')) + ';'\
                    + str(user.get('first_name')) + ';' \
                    + str(user.get('last_name')) + ';' \
                    + str(user.get('home_phone')) + ';' + '\n'
    write_phones(parsed)
    print(parsed)
    print('Done!')
    input('Press Enter...')


if __name__ == '__main__':
        main()
