from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
import sys
from time import sleep
import csv

if len(sys.argv) <= 2:
    print(sys.argv[0], '[Username] [Password]')
    exit(-1)

UNIPA_URL = 'https://portal.sa.dendai.ac.jp/uprx/'

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

XPATH_USERNAME = '//*[@id="loginForm:userId"]'
XPATH_PASSWORD = '//*[@id="loginForm:password"]'

# driver = webdriver.Firefox()
driver = webdriver.Chrome()

driver.find_elements_by_xpath(XPATH_USERNAME)[
    0].send_keys(USERNAME)  # username
driver.find_elements_by_xpath(XPATH_PASSWORD)[
    0].send_keys(PASSWORD)  # password

driver.find_elements_by_xpath(
    '/html/body/form[3]/div[1]/div/div[2]/div/p[3]/button/span[2]')[0].click()  # LOGIN

# try:
#     driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/button/span[2]')[0].click()
# except ElementNotInteractableException:
#     pass


def script_open_dialog(i, j):
    return 'PrimeFaces.ab({s:"funcForm:tabArea:0:j_idt232:' + str(i) + ':j_idt287:' + str(
        j) + ':j_idt293",p:"funcForm:tabArea:0:j_idt232:' + str(i) + ':j_idt287:' + str(j) + ':j_idt293"});'

# https://qiita.com/nabenabe0928/items/fcdf2c81e5fff3364c6f


def write_csv(file, save_dict):
    save_row = {}

    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=save_dict.keys(), delimiter=",", quotechar='"')
        # writer = csv.writer(f, delimiter=",", quotechar='"')

        writer.writeheader()
        # writer.writerow(save_dict.keys())

        k1 = list(save_dict.keys())[0]
        length = len(save_dict[k1])

        for i in range(length):
            for k, vs in save_dict.items():
                save_row[k] = vs[i]

            writer.writerow(save_row)


l = []
for i in range(30+1):
    for j in range(30+1):
        print('i,j', (i, j))
        driver.execute_script(script_open_dialog(i, j))
        sleep(1)
        # print(driver.find_element_by_xpath(
        #     '//*[@id="bsd00702:ch:j_idt472"]/tbody/tr[1]/td[2]').text) # xpath_差出人

        # d = {}
        dl = []
        keys = []
        for i_, e in enumerate(driver.find_elements_by_class_name('ui-panelgrid-cell')):
            try:
                text = e.text
            except:
                print('Text Break')
                break
            if i_ % 2 == 0:
                k = text
                keys.append(k)
            else:
                # d[k] = e.text
                if True:
                    text = text.replace('\n', '<br>')
                dl.append(text)

        t = tuple(dl)
        print(t)
        l.append(t)

l = list(set(l))

print()

# save_dict = {}
save_list = []


# for d in l:
#  for k, v in d.items():
#   if k not in save_dict:
#     save_dict[k] = []
#   save_dict[k].append(v.replace('\n', '<br>'))

# print('save_dict', save_dict)

# write_csv('keiji.csv', save_dict)

save_list.append(keys)
for e in l:
    save_list.append(e)

print('save_list', save_list)

with open('keiji.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"')
    writer.writerows(save_list)


# '//*[@id="bsd00702:ch:j_idt472"]/tbody/tr[4]/td[2]/div'  # honbun

# driver.find_elements_by_xpath('//*[@id="bsd00702:dialog"]/div[1]/a[1]/span').click()
