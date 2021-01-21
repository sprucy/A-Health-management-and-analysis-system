#!/usr/bin/env python
#coding:utf-8
 
import os
import random
import datetime
import django

from django.utils import timezone
from faker import Faker
from dateutil.relativedelta import relativedelta

fake = Faker("zh_CN")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthmanage.settings")
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth.models import Group,Permission
from django.db import models
from adminlteui.models import Options, Menu, ContentType
from healthinfo.models import UserInfo, BodyInfo, BloodPressure,Bcholesterin,SmokeDiabetesInfo,Bcholesterin
from healthinfo.models import AgeScale,WeightScale,BloodPressureScale,SmokeScale,DiabetesScale
from healthinfo.models import RiskEvaluatScale, CommonRiskScale,TCScale,BMIScale
from healthinfo.models import HealthIntervent,RiskAnalyse,SingleAssess,Indicator

citys = { '北京': ['北京'],    
            '广东': ['广州', '深圳', '珠海', '汕头', '韶关', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'],    
            '上海': ['上海'],    
            '天津': ['天津'],    
            '重庆': ['重庆'],    
            '辽宁': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'],    
            '江苏': ['南京', '苏州', '无锡', '常州', '镇江', '南通', '泰州', '扬州', '盐城', '连云港', '徐州', '淮安', '宿迁'],    
            '湖北': ['武汉', '黄石', '十堰', '荆州', '宜昌', '襄樊', '鄂州', '荆门', '孝感', '黄冈', '咸宁', '随州', '恩施土家族苗族自治州', '仙桃', '天门', '潜江', '神农架林区'],
            '四川': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'], 
            '陕西': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],    
            '河北': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'],    
            '山西': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],    
            '河南': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店'],    
            '吉林': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边朝鲜族自治州'],    
            '黑龙江': ['哈尔滨', '齐齐哈尔', '鹤岗', '双鸭山', '鸡西', '大庆', '伊春', '牡丹江', '佳木斯', '七台河', '黑河', '绥化', '大兴安岭地区'],    
            '内蒙古': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '锡林郭勒盟', '兴安盟', '阿拉善盟'],    
            '山东': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽'],    
            '安徽': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城'],    
            '浙江': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'],    
            '福建': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],    
            '湖南': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西土家族苗族自治州'],    
            '广西': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'],    
            '江西': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],    
            '贵州': ['贵阳', '六盘水', '遵义', '安顺', '铜仁地区', '毕节地区', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],    
            '云南': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州', '大理白族自治州', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州'],    
            '西藏': ['拉萨', '那曲地区', '昌都地区', '林芝地区', '山南地区', '日喀则地区', '阿里地区'],    
            '海南': ['海口', '三亚', '五指山', '琼海', '儋州', '文昌', '万宁', '东方', '澄迈县', '定安县', '屯昌县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县'],    
            '甘肃': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '酒泉', '张掖', '庆阳', '平凉', '定西', '陇南', '临夏回族自治州', '甘南藏族自治州'],    
            '宁夏': ['银川', '石嘴山', '吴忠', '固原', '中卫'],    
            '青海': ['西宁', '海东地区', '海北藏族自治州', '海南藏族自治州', '黄南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'],    
            '新疆': ['乌鲁木齐', '克拉玛依', '吐鲁番地区', '哈密地区', '和田地区', '阿克苏地区', '喀什地区', '克孜勒苏柯尔克孜自治州', '巴音郭楞蒙古自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州', '石河子', '阿拉尔', '图木舒克', '五家渠', '伊犁哈萨克自治州'],    
            '香港': ['香港'],    
            '澳门': ['澳门'],    
            '台湾': ['台北市', '高雄市', '台北县', '桃园县', '新竹县', '苗栗县', '台中县', '彰化县', '南投县', '云林县', '嘉义县', '台南县', '高雄县', '屏东县', '宜兰县', '花莲县', '台东县', '澎湖县', '基隆市', '新竹市', '台中市', '嘉义市', '台南市']}


#随机生成用户数据
#参数：num-生成用户的数量，days-生成数据的天数
def createuserdata(num,days):

    while num > 0:
        #username = fake.user_name()
        username = 'user'+str(num).zfill(4)
        if len(username)<8:
            username += str(fake.random_number(digits=(8-len(username))))
        if User.objects.filter(username=username).count()==0:
            num = num - 1
            sex = random.choice(('M', 'F'))
            if sex=='M':
                firstname = fake.first_name_male()
            else:
                firstname = fake.first_name_female()
            lastname = fake.last_name()
            ssn=fake.ssn()
            birthday =datetime.datetime.strptime(ssn[6:14], '%Y%m%d')
            #birthday = fake.date_between(start_date="-50y", end_date="now")-relativedelta(years=fake.random_int(max=80,min=30))
            email=fake.email()
            province = random.choice(list(citys.keys()))
            city=random.choice(citys[province])
            job=fake.job()
            phone = fake.phone_number()
            address = fake.address()
            org = fake.company()
            print(username,ssn,lastname,firstname,sex,birthday,email,phone,address,org,province,city,job)
            #print(fake.simple_profile())#生成一个简单的用户数据
            #print(fake.profile())#生成一个详细的用户数据
            #print(fake.random_int(max=100,min=60)) #整数
            #print(fake.pyfloat(left_digits=2, right_digits=3, positive=True)) #生成浮点数，可以指定小数点左右数字的位数，正负
            #注册用户
            user=User.objects.create_user(username=username,password='!qq12345',email=email,last_name=lastname,first_name=firstname,is_staff=True,) 
            group = Group.objects.get(name='个人用户') 
            group.user_set.add(user)

            #生成用户信息
            
            userinfo=UserInfo(user=user,ssn=ssn,sex=sex,birthday=birthday,phone=phone,org=org,job=job,province=province,city=city,address=address)
            userinfo.save()
            max=datetime.date.today().year - birthday.year
            if max < 15:
                smoke=False
                drink=False
            else:
                smoke = random.choice((True, False))
                drink = random.choice((True, False))
            if smoke:
                smokestart = birthday + relativedelta(years=fake.random_int(max=max, min=1))
            else:
                smokestart = None
            if drink:
                drinkstart = birthday + relativedelta(years=fake.random_int(max=max, min=1))
            else:
                drinkstart = None
            diabetes = random.choice((True, False))
            if diabetes:
                diabetesstart = birthday + relativedelta(years=fake.random_int(max=datetime.date.today().year - birthday.year, min=0))
            else:
                diabetesstart = None
            smokediabetes = SmokeDiabetesInfo(user=user, smokestart=smokestart, smoke=smoke, \
                drink =drink,drinkstart =drinkstart,diabetesstart=diabetesstart,diabetes=diabetes)
            smokediabetes.save()


            startdate=timezone.now()
            #生成身高体重数据
            v1 = fake.random_int(max=180,min=150) 
            bmi=random.uniform(14,45)
            v2 =  v1/100*v1/100*bmi
            nomalheight = pow(v2 / bmi, 0.5) * 100
            
            v3 = fake.random_int(max=105,min=95)*0.42*nomalheight/100
            i=0
            while i<days:
                curdate= startdate-relativedelta(days=i)
                i += 1
                x1 = round(v1+random.random()*random.choice((-1,1)),2)
                x2 = round(v2+ random.uniform(0,3)*random.choice((-1,1)),2)
                x3 = round(v3+ random.uniform(0,3)*random.choice((-1,1)),2)
                print(curdate,x1,x2,x3)
                modobj=BodyInfo(user=user,measuretime=curdate,height = x1,weight =x2,waist = x3)
                modobj.save()
            #生成血压数据
            v1 = fake.random_int(max=180,min=70) 
            v2 = v1-fake.random_int(max=50,min=30) 
            v3 = fake.random_int(max=90,min=40)
            i=0
            while i<days:
                curdate= startdate-relativedelta(days=i)
                i += 1
                x1 = v1+random.randint(0,10)*random.choice((-1,1))
                x2 = v2+random.randint(0,10)*random.choice((-1,1))
                x3 = v3+random.randint(0,5)*random.choice((-1,1))
                print(curdate,x1,x2,x3)
                modobj=BloodPressure(user=user,measuretime=curdate,DBP = x1,SBP =x2,HR = x3)
                modobj.save()

            #生成血脂数据
            v1 = random.uniform(0.15,4)
            v2 = random.uniform(1.5,6.5) 
            v3 = random.uniform(0.8,2)
            v4 = random.uniform(0.3,2.2)
            i=0
            while i<days:
                curdate= startdate-relativedelta(months=i)
                i += 1
                x1 = round(v1+random.uniform(0.015,0.2)*random.choice((-1,1)),2)
                x2 = round(v2+random.uniform(0.15,0.4)*random.choice((-1,1)),2)
                x3 = round(v3+random.uniform(0.02,0.2)*random.choice((-1,1)),2)
                x4 = round(v4+random.uniform(0.03,0.2)*random.choice((-1,1)),2)
                print(curdate,x1,x2,x3,x4)
                modobj=Bcholesterin(user=user,measuretime=curdate,LDL = x1,TC =x2,HDL = x3,TG = x4)
                modobj.save()


def main():
    num=100
    days=30
    print('随机生成{}个用户和{}天健康数据'.format(num,days))
    createuserdata(num=num,days=days)
    print('Run End ......')


if __name__ == "__main__":  
    main()