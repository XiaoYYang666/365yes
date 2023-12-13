import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
import time
from selenium import webdriver #自动化工具
driver = webdriver.Chrome(executable_path=r"D:\Python37\chromedriver.exe")
def login():
    #     2.打开京东
    driver.get("https://www.jd.com")
    time.sleep(3)
    #3.登录
    if driver.find_element_by_link_text("你好，请登录"):
        driver.find_element_by_link_text("你好，请登录").click()
        print(f"请尽快扫码登录")
        time.sleep(10)
def picking(method):
    driver.get("https://cart.jd.com/cart_index")
    time.sleep(3)
    # 是否全选购物车
    if method == 0:
        while True:
            try:
                if driver.find_element_by_class_name("jdcheckbox"):
                    driver.find_element_by_class_name("jdcheckbox").click()
                    break
            except:
                print(f"找不到购买按钮")
    else:
        print(f"请手动勾选需要购买的商品")
        time.sleep(5)
def buy(times):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        print(now)
        if now > times:
            # 点击结算按钮
            while True:
                try:
                    if driver.find_element_by_link_text("去结算"):
                        print("here")
                        driver.find_element_by_link_text("去结算").click()
                        print(f"结算成功，准备提交订单")
                        break
                except:
                    pass

if __name__ == "__main__":
    login()
    picking(0)
    buy("2021-12-27 16:50:00.00000000")
