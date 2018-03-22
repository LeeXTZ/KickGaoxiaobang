from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time

print('输入账号：')
account = '20151001251'
print('输入密码：')
code = 'mooc.lee.lee.'
print('1-->计算思维【地大2017春季课】')
print('2-->创业基础2.0【地大2017春季课】')
print('3-->创新思维开发与落地【地大2017春季课】')
print('4-->移动互联网思维【地大2017春季课】')
print('5-->孙子兵法战略思维【地大2017春季课】')
print('6-->创业启蒙与案例分享【地大2017春季课】')
print('7-->创业基本功与精益创业方法论【地大2017春季课】')
print('8-->打造无敌商业计划书【地大2017春季课】')

lesson = {'1': '计算思维【地大2017春季课】',
          '2': '创业基础2.0【地大2017春季课】',
          '3': '创新思维开发与落地【地大2017春季课】',
          '4': '移动互联网思维【地大2017春季课】',
          '5': '孙子兵法战略思维【地大2017春季课】',
          '6': '创业启蒙与案例分享【地大2017春季课】',
          '7': '创业基本功与精益创业方法论【地大2017春季课】',
          '8': '打造无敌商业计划书【地大2017春季课】'
}

print('输入课程序号：')
lessonName = lesson[input()]

brs = webdriver.Firefox()

#brs.set_window_size('1700', '1000')


def isEleExist_Css(eleCss):
    try:
        brs.find_element_by_css_selector(eleCss)
        return True
    except:
        return False


def isEleExist_Class(eleClass):
    try:
        brs.find_element_by_class_name(eleClass)
        return True
    except:
        return False


def autoQuiz(threadName):        # Automate the process of quiz

    print('      > > > > > > > > > > > > > > ', threadName)        # Output the name of this thread
    time.sleep(3)
    print('      > > > > > > > > > > > > > >  autoQuiz Launched...')

    isQuizOccur = isEleExist_Css('div.gxb-video-quiz-warp')  # 判断quiz是否出现
    if not isQuizOccur:     # 如果没有出现，退出autoQuiz函数
        print('      > > > > > > > > > > > > > >  quiz Not Occur')
        return
    else:
        print('      > > > > > > > > > > > > > >  quiz Occur')

    brs.find_element_by_css_selector('div.gxb-video-quiz-body')

    js = 'var s=document.getElementsByClassName("quiz-type gxb-quiz-checbox");for(i=0;i<s.length;i++){return s[i].textContent;}'
    qType = brs.execute_script(js)     # The type of quiz

    isQuizing = isEleExist_Css('div.gxb-video-quiz-warp')  # quiz是否退出
    while isQuizing:  # 如果界面未退出，执行循环
        brs.find_element_by_css_selector('div.gxb-video-quiz-warp')       # 定位到quiz界面

        if qType == '多选':
            options = brs.find_elements_by_css_selector('i.gxb-icon-check unchecked')  # 定位多选题的所有选项
            for option in options:  # 循环点击所有选项
                option.click()
        elif qType == '单选':
            brs.find_element_by_css_selector('i.gxb-icon-radio').click()

        # brs.find_element_by_css_selector('div.gxb-video-quiz-warp')
        # brs.find_element_by_css_selector('div.btn_').click()  # 元素为inline-block 不可见 尝试用javascript代码更改style
        brs.find_element_by_css_selector('div.gxb-video-quiz-footer')
        js = 'var s = document.getElementsByClassName("gxb-btn_ submit");for(i=0;i<s.length;i++){s[i].click();}'
        brs.execute_script(js)  # 点击提交

        js = 'var n = document.getElementsByClassName("gxb-btn_ next");for(i=0;i<n.length;i++){return n[i].style.display;}'
        isDp = str(brs.execute_script(js))        # 判断下一题按钮的display属性（是否可见）
        print('      > > > > > > > > > > > > > >  下一题：', isDp)
        if isDp == 'inline-block':
            js = 'var n = document.getElementsByClassName("gxb-btn_ next");for(i=0;i<n.length;i++){n[i].click();}'
            brs.execute_script(js)  # 点击下一题
        else:
            js = 'var p = document.getElementsByClassName("gxb-btn_ player");for(i=0;i<p.length;i++){p[i].click();}'
            brs.execute_script(js)  # 点击继续观看

        isQuizing = isEleExist_Css('div.gxb-video-quiz-warp')  # 判断quiz界面是否退出
        
        
def fuckPause():
    # js = 'var s = document.getElementsByClassName("jw-video jw-reset");for(i=0;i<s.length;i++){s[i].currentSrc;}'
    # print('      > > > > > > > > > > > > > >  url of video', brs.execute_script(js))
    js = 'var s = document.getElementsByClassName("jw-video jw-reset");for(i=0;i<s.length;i++){s[i].play();}'
    brs.execute_script(js)


def autoNext(threadName):        # Automate the process of next video

    print('      > > > > > > > > > > > > > > ', threadName)        # Output the name of this thread
    #WebDriverWait(brs, 3600, 1).until(ec.visibility_of(brs.find_element(By.CSS_SELECTOR, 'div.gxb-video-quiz-warp')))
    time.sleep(3)
    print('      > > > > > > > > > > > > > >  autoNext Launched...')

    title = brs.find_element_by_css_selector('div>span.chapter-title').text
    if ('导学' in title) or ('讨论' in title) or ('测验' in title):         # 跳过导学、讨论、测验
        brs.find_element_by_css_selector('i.gxb-next-blue').click()
        print('导学、讨论、测验。Pass')
        return

    if isEleExist_Css('div.jw-controlbar.jw-background-color.jw-reset'):
        percent = brs.find_element_by_css_selector('div.jw-progress.jw-reset').get_attribute('style')
        if '100'in str(percent):
            print('      > > > > > > > > > > > > > >  Video Process:100%')
            brs.find_element_by_css_selector('i.gxb-next-blue').click()
        else:
            print('      > > > > > > > > > > > > > >  Video Process:', percent)
            fuckPause()
    else:
        return



brs.get('https://cas.gaoxiaobang.com/login?tenant_id=628&service=https%3A%2F%2Fcug.gaoxiaobang.com%2F')

print('      > > > > > > > > > > > > > >  Current Title:', brs.title)

brs.implicitly_wait(20)
brs.find_element_by_id('username').clear()
brs.find_element_by_id('username').send_keys(account)  # input username
brs.find_element_by_id('password').clear()
brs.find_element_by_id('password').send_keys(code)  # input password

brs.find_element_by_name('submit').click()  # 点击登陆

print('      > > > > > > > > > > > > > >  Current Title:', brs.title)

# brs.find_element_by_css_selector("div>p.download_close").click()  # 关闭APP下载界面
time.sleep(5)
mystudy = brs.find_element_by_link_text('我的学习')
webdriver.ActionChains(brs).move_to_element(mystudy).perform()  # 鼠标悬停到“我的学习”上
brs.find_element_by_link_text('我的学习').click()  # 点击“我的学习”

time.sleep(15)
print('      > > > > > > > > > > > > > >  Current Title:', brs.title)
# brs.find_element_by_css_selector('p.download_close').click()  # close appdownload
ctnstudys1 = brs.find_elements_by_link_text(lessonName)
for ctnstudy1 in ctnstudys1:  # 大坑啊！！ 第一个ctnstudy1元素不可见，无法完成点击  这里对ctnstudys1进行循环，找到可见元素
    print('ctnstudy1.is_displayed()：', ctnstudy1.is_displayed())
    if ctnstudy1.is_displayed():
        ctnstudy1.click()  # 又一个坑 全屏的时候也无法跳转？？？//好像是因为APP下载页面挡住元素导致，所以在刚登陆的时候把APP页面关掉
        break
time.sleep(10)
print('      > > > > > > > > > > > > > >  Current Title:', brs.title)

ctnstudys2 = brs.find_elements_by_css_selector("div>p.ng-scope[ng-click='gostudy()']")
for ctnstudy2 in ctnstudys2:
    print('ctnstudy2.is_displayed()：', ctnstudy2.is_displayed())
    if ctnstudy2.is_displayed():
        ctnstudy2.click()
        break
time.sleep(5)
print('      > > > > > > > > > > > > > >  Current Title:', brs.title)

brs.find_element_by_id('learn-next').click()

# *******已进入播放界面********


if __name__ == '__main__':

    while True:
        autoQuiz('autoQuiz Loading...')
        autoNext('autoNext Loading...')
        # fuckPause()
