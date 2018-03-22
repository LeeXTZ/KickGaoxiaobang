from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
import threading

brs = webdriver.Firefox()


def autoQuiz(threadName):        # Automate the process of quiz

    print(threadName)        # Output the name of this thread
    WebDriverWait(brs, 3600, 1).until(ec.visibility_of(brs.find_element(By.CSS_SELECTOR, 'div.gxb-video-quiz-warp')))
    time.sleep(30)
    brs.find_element_by_css_selector('div.gxb-video-quiz-body')
    #brs.find_element_by_css_selector('div.quiz-title padding0_')
    #qTypeEle = brs.find_element_by_css_selector('i.quiz-type gxb-quiz-checbox')     # 定位quiz type元素
    #qType = qTypeEle.get_attribute('textContent')      # 获得元素内的Text
    js = 'var s=document.getElementsByClassName("quiz-type gxb-quiz-checbox");for(i=0;i<s.length;i++){return s[i].textContent;}'
    #qType = brs.find_element_by_css_selector('i.quiz-type gxb-quiz-checbox').text  # The type of quiz
    qType = brs.execute_script(js)
    if qType == '多选':
        # sv = brs.find_element_by_css_selector('i.gxb-btn_ submit').is_displayed()
        js = 'var sv=document.getElementsByClassName("i.gxb-btn_ submit");return sv;'
        sv = brs.execute_script(js).get_attribute('style')
        while sv == 'inline-block':
            brs.find_element_by_css_selector('div.gxb-video-quiz-warp')
            options = brs.find_elements_by_css_selector('i.gxb-icon-check unchecked')  # 定位多选题的所有选项
            for option in options:     # 循环点击所有选项
                option.click()
            # brs.find_element_by_css_selector('div.gxb-video-quiz-warp')
            # brs.find_element_by_css_selector('div.btn_').click()  # 元素为inline-block 不可见 尝试用javascript代码更改style
            brs.find_element_by_css_selector('div.gxb-video-quiz-footer')
            js = 'var s = document.getElementsByClassName("gxb-btn_ submit");for(i=0;i<s.length;i++){s[i].click();}'
            brs.execute_script(js)           # 点击提交

            js = 'var n = document.getElementsByClassName("gxb-btn_ next");for(i=0;i<n.length;i++){n[i].click();}'
            brs.execute_script(js)           # 点击下一题

        # brs.find_element_by_css_selector('i.gxb-btn_ submit').click()

        brs.find_element_by_css_selector('i.gxb-btn_ player').click()    # 点击继续观看
    elif qType == '单选':
        sv = brs.find_element_by_css_selector('i.gxb-btn_ submit').is_displayed()
        while not sv:
            brs.find_element_by_css_selector('div.gxb-video-quiz-warp')
            brs.find_element_by_css_selector('i.gxb-icon-radio').click()
            #brs.find_element_by_css_selector('div.gxb-video-quiz-warp')
            # brs.find_element_by_css_selector('div.btn_').click()  # 元素为inline-block 不可见 尝试用javascript代码更改style
            brs.find_element_by_css_selector('div.gxb-video-quiz-footer')
            js = 'var s = document.getElementsByClassName("gxb-btn_ submit");for(i=0;i<s.length;i++){s[i].click();}'
            brs.execute_script(js)

        #brs.find_element_by_css_selector('i.gxb-btn_ submit').click()

        brs.find_element_by_css_selector('i[style="display: inline-block;"]').click()
        #_thread.exit()        # 完成答题，退出线程


def autoNext(threadName):        # Automate the process of next video

    print(threadName)        # Output the name of this thread
    #WebDriverWait(brs, 3600, 1).until(ec.visibility_of(brs.find_element(By.CSS_SELECTOR, 'div.gxb-video-quiz-warp')))
    time.sleep(30)
    title = brs.find_element_by_css_selector('div>span.chapter-title').text
    if '导学：' in title:
        brs.find_element_by_css_selector('i.gxb-next-blue').click()

        #_thread.exit()
    else:
        percent = brs.find_element_by_css_selector('div>span.video-percent')
        if '100' in percent.text:
            brs.find_element_by_css_selector('i.gxb-next-blue').click()

            #_thread.exit()       # 退出线程
        else:
            WebDriverWait(brs, 3600, 1).until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, 'div>span.video-percent'), '100'))
            sb = brs.find_element_by_css_selector('i.gxb-next-blue')
            print('sb.is_displayed():', sb.is_displayed())
            #brs.find_element_by_id('learn-next').click()
            brs.find_element_by_css_selector('i.gxb-next-blue').click()
            #_thread.exit()        # 退出线程

brs.get('https://cas.gaoxiaobang.com/login?tenant_id=628&service=https%3A%2F%2Fcug.gaoxiaobang.com%2F')

print('current title:', brs.title)

#brs.set_window_size(1200, 1000)
#print('设置浏览器的size')

brs.implicitly_wait(20)
brs.find_element_by_id('username').clear()
brs.find_element_by_id('username').send_keys('15927367004')  # input username
brs.find_element_by_id('password').clear()
brs.find_element_by_id('password').send_keys('mooc.lee.lee.')  # input password

brs.find_element_by_name('submit').click()  # 点击登陆

print('current title:', brs.title)

brs.find_element_by_css_selector("div>p.download_close").click()  # 关闭APP下载界面

mystudy = brs.find_element_by_link_text('我的学习')
webdriver.ActionChains(brs).move_to_element(mystudy).perform()  # 鼠标悬停到“我的学习”上
brs.find_element_by_link_text('我的学习').click()  # 点击“我的学习”

print('current title:', brs.title)
brs.find_element_by_css_selector('p.download_close').click()  # close appdownload
ctnstudys1 = brs.find_elements_by_link_text('移动互联网思维【地大2017春季课】')
for ctnstudy1 in ctnstudys1:  # 大坑啊！！ 第一个ctnstudy1元素不可见，无法完成点击  这里对ctnstudys1进行循环，找到可见元素
    print('ctnstudy1.is_displayed()：', ctnstudy1.is_displayed())
    if ctnstudy1.is_displayed():
        ctnstudy1.click()  # 又一个坑 全屏的时候也无法跳转？？？//好像是因为APP下载页面挡住元素导致，所以在刚登陆的时候把APP页面关掉
        break
time.sleep(5)
print('current title:', brs.title)

ctnstudys2 = brs.find_elements_by_css_selector("div>p.ng-scope[ng-click='gostudy()']")
for ctnstudy2 in ctnstudys2:
    print('ctnstudy2.is_displayed()：', ctnstudy2.is_displayed())
    if ctnstudy2.is_displayed():
        ctnstudy2.click()
        break
time.sleep(5)
print('current title:', brs.title)

brs.find_element_by_id('learn-next').click()

# *******已进入播放界面********


if __name__ == '__main__':
    while True:
        autoQuiz('autoQuiz...')
        autoNext('autoNext...')
