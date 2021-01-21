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

def createscale():
    print("清除所有评价标准表数据")
    AgeScale.objects.all().delete()
    WeightScale.objects.all().delete()
    BloodPressureScale.objects.all().delete()
    TCScale.objects.all().delete()
    RiskEvaluatScale.objects.all().delete()
    CommonRiskScale.objects.all().delete()
    SmokeScale.objects.all().delete()
    DiabetesScale.objects.all().delete()
    BMIScale.objects.all().delete()
    RiskAnalyse.objects.all().delete()
    HealthIntervent.objects.all().delete()
    SingleAssess.objects.all().delete()
    Indicator.objects.all().delete()

    print("增加 {} 数据".format(Indicator._meta.verbose_name))
    parents=['危险因素','BMI评价']
    childs=[['吸烟','危险因素'],
            ['饮酒','危险因素'],
            ['糖尿病','危险因素'],
            ['体重消瘦','危险因素'],
            ['体重肥胖','危险因素'],
            ['体重偏瘦','BMI评价'],
            ['体重正常','BMI评价'],
            ['体重偏胖','BMI评价'],
            ['I度肥胖','BMI评价'],
            ['II度肥胖','BMI评价'],
            ['III度肥胖','BMI评价'],
            ['低血压','危险因素'],
            ['高血压','危险因素'],        
            ['高脂血','危险因素'],
            ['低脂血','危险因素'],
            ['心动过速','危险因素'],
            ['心动过缓','危险因素'],]
    for parent in parents:
        Indicator.objects.get_or_create(name=parent)
    for child in childs:
        id=Indicator.objects.filter(name=child[1]).first()
        Indicator.objects.get_or_create(name=child[0],parent=id)

    print("增加 {} 数据".format(AgeScale._meta.verbose_name))
    lines = [
        ['M',40,0],
        ['M',45,1],
        ['M',50,2],
        ['M',55,3],
        ['M',60,4],
        ['M',65,5],
        ['M',70,6],
        ['M',75,7],
        ['M',80,8],
        ['M',85,9],
        ['M',90,10],
        ['M',95,11],
        ['M',120,12],
        ['F',40,0],
        ['F',45,1],
        ['F',50,2],
        ['F',55,3],
        ['F',60,4],
        ['F',65,5],
        ['F',70,6],
        ['F',75,7],
        ['F',80,8],
        ['F',85,9],
        ['F',90,10],
        ['F',95,11],
        ['F',120,12]]
    for line in lines:
        AgeScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(WeightScale._meta.verbose_name))
    lines = [
        ['M',24,0],
        ['M',28,1],
        ['M',50,2],
        ['F',24,0],
        ['F',28,1],
        ['F',50,2]]
    for line in lines:
        WeightScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(BloodPressureScale._meta.verbose_name))
    lines = [
        ['M',120,-2],
        ['M',130,0],
        ['M',140,1],
        ['M',160,2],
        ['M',180,5],
        ['M',280,8],
        ['F',120,-2],
        ['F',130,0],
        ['F',140,1],
        ['F',160,2],
        ['F',180,3],
        ['F',280,4]]
    for line in lines:
        BloodPressureScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(TCScale._meta.verbose_name))
    lines = [
        ['M',5.18,0],
        ['M',10,1],
        ['F',5.18,0],
        ['F',10,1]]
    for line in lines:
        TCScale.objects.get_or_create(sex = line[0],maxv =line[1],score =line[2]) 

    print("增加 {} 数据".format(RiskEvaluatScale._meta.verbose_name))
    lines = [
        ['M',-2,0.2],
        ['M',-1,0.3],
        ['M',0,0.5],
        ['M',1,0.6],
        ['M',2,0.8],
        ['M',3,1.1],
        ['M',4,1.5],
        ['M',5,2.1],
        ['M',6,2.9],
        ['M',7,3.9],
        ['M',8,5.4],
        ['M',9,7.3],
        ['M',10,9.7],
        ['M',11,12.8],
        ['M',12,16.8],
        ['M',13,21.7],
        ['M',14,27.7],
        ['M',15,35.3],
        ['M',16,44.3],
        ['M',17,52.6],
        ['F',-2,0.1],
        ['F',-1,0.2],
        ['F',0,0.2],
        ['F',1,0.3],
        ['F',2,0.5],
        ['F',3,0.8],
        ['F',4,1.2],
        ['F',5,1.8],
        ['F',6,2.8],
        ['F',7,4.4],
        ['F',8,6.8],
        ['F',9,10.3],
        ['F',10,15.6],
        ['F',11,23],
        ['F',12,32.7],
        ['F',13,43.1],
        ['F',14,43.1],
        ['F',15,43.1],
        ['F',16,43.1],
        ['F',17,43.1],]
    for line in lines:
        RiskEvaluatScale.objects.get_or_create(sex = line[0],risk =line[2],score =line[1]) 

    print("增加 {} 数据".format(CommonRiskScale._meta.verbose_name))
    lines = [
        ['M',40,1,0.3],
        ['M',45,1.4,0.4],
        ['M',50,1.9,0.5],
        ['M',55,2.6,0.7],
        ['M',120,3.6,1],
        ['F',40,0.3,0.1],
        ['F',45,0.4,0.1],
        ['F',50,0.6,0.2],
        ['F',55,0.9,0.3],
        ['F',120,1.4,0.5]]
    for line in lines:
        CommonRiskScale.objects.get_or_create(sex = line[0],age =line[1],avgrisk =line[2],minrisk=line[3]) 

    print("增加 {} 数据".format(SmokeScale._meta.verbose_name))
    SmokeScale.objects.get_or_create(sex = 'M',smoke =False,score =0) 
    SmokeScale.objects.get_or_create(sex = 'M',smoke =True,score =2) 
    SmokeScale.objects.get_or_create(sex = 'F',smoke =False,score =0) 
    SmokeScale.objects.get_or_create(sex = 'F',smoke =True,score =1) 

    print("增加 {} 数据".format(DiabetesScale._meta.verbose_name))
    DiabetesScale.objects.get_or_create(sex = 'M',diabetes =False,score =0) 
    DiabetesScale.objects.get_or_create(sex = 'M',diabetes =True,score =1) 
    DiabetesScale.objects.get_or_create(sex = 'F',diabetes =False,score =0) 
    DiabetesScale.objects.get_or_create(sex = 'F', diabetes=True, score=2)

    print("增加 {} 数据".format(BMIScale._meta.verbose_name))
    lines = [
        ['体重偏瘦',18.5],
        ['体重正常',24],
        ['体重偏胖',27],
        ['I度肥胖',30],
        ['II度肥胖',40],
        ['III度肥胖',50]]
    for line in lines:
        wtype=Indicator.objects.filter(name=line[0]).first()
        BMIScale.objects.get_or_create(wtype = wtype,bmi =line[1]) 

    print("增加 {} 数据".format(SingleAssess._meta.verbose_name))
    lines = [
        ['血压','收缩压',90,140],
        ['血压','舒张压',60,90],
        ['血压','心率',60,100],
        ['血脂', '总胆固醇', 2.35, 5.18],
        ['血脂','低密度',0.25,3.11],
        ['血脂','高密度',1.16,1.42],
        ['血脂','甘油三酯',0.51,1.7],]
    for line in lines:
        SingleAssess.objects.get_or_create(assesstype = line[0],assessname=line[1],minv=line[2],maxv=line[3]) 

    print("增加{}、{}数据".format(RiskAnalyse._meta.verbose_name,HealthIntervent._meta.verbose_name))

    lines = (
        ('吸烟','流行病学调查表明，吸烟是肺癌的重要致病因素之一，特别是鳞状上皮细胞癌和小细胞未分化癌。吸烟可降低自然杀伤细胞的活性，从而削弱机体对肿瘤细胞生长的监视、杀伤和清除功能。吸烟者喉癌发病率较不吸烟者高十几倍、膀胱癌发病率增加3倍。此外，吸烟与唇癌、舌癌、口腔癌、食道癌、胃癌、结肠癌、胰腺癌、肾癌和子宫颈癌的发生都有一定关系。临床研究和动物实验表明，烟雾中的致癌物质还能通过胎盘影响胎儿，致使其子代的癌症发病率显著增高。'),
        ('吸烟','吸烟是许多心、脑血管疾病的主要危险因素，吸烟者的冠心病、高血压病、脑血管病及周围血管病的发病率均明显升高。统计资料表明，冠心病和高血压病患者中75%有吸烟史。冠心病发病率吸烟者较不吸烟者高3.5倍，冠心病病死率前者较后者高6倍，心肌梗塞发病率前者较后者高2~6倍。吸烟者发生中风的危险是不吸烟者的2~3.5倍；如果吸烟和高血压同时存在，中风的危险性就会升高近20倍。此外，吸烟者易患闭塞性动脉硬化症和闭塞性血栓性动脉炎，吸烟可引起慢性阻塞性肺病，导致肺原性心脏病。'),
        ('吸烟','吸烟是慢性支气管炎、肺气肿和慢性气道阻塞的主要诱因之一。实验研究发现，长期吸烟可使支气管粘膜的纤毛受损、变短，影响纤毛的清除功能,吸烟者患慢性气管炎较不吸烟者高2～4倍，且与吸烟量和吸烟年限成正比例，患者往往有慢性咳嗽、咯痰和活动时呼吸困难。年轻的无症状的吸烟者也有轻度肺功能减退。吸烟导致的慢性阻塞性肺病易致自发性气胸。吸烟者常患有慢性咽炎和声带炎。'),
        ('吸烟','吸烟可引起胃酸分泌增加，比不吸烟者增加91.5%，并能抑制胰腺分泌碳酸氢钠，致使十二指肠酸负荷增加，诱发溃疡。烟草中烟碱可使幽门括约肌张力降低，使胆汁易于返流，从而削弱胃、十二指肠粘膜的防御因子，促使慢性炎症及溃疡发生，并使原有溃疡延迟愈合。此外，吸烟可降低食管下括约肌的张力，易造成返流性食管炎。烟草进入人体后，会干扰人体对钙离子的吸收就会受到影响，从而引起骨密度下降。'),
        ('饮酒','长期大量饮酒会导致心血管系统受损，饮酒之后产生多余的谷氨酸盐，会引起心脏的亢奋和血压升高，因此长期饮酒的人容易患高血压、心血管疾病，肾脏是人体的排毒器官之一，而酒精会损害肾脏和消化系统，当酒精进入肾脏之后，肾脏会直接将水送到膀胱而不能收回，导致身体缺水，而且大量的进入胃肠之后会刺激胃粘膜引起不适，严重的会导致胃溃疡和胃出血。'),
        ('饮酒','长期大量饮酒损害人的消化系统，酒精中含有大量的乙醇，而乙醇很容易被身体吸收，然后被肝脏分解，经常喝酒会给肝脏带来极大的负担，造成肝脏损害，很容易患上脂肪肝等其他疾病。大量的饮酒后会破坏身体的内分泌系统，会导致半乳糖赖量降低、甘油三酯合成增加，脂质过氧化增加，国际杂志BMC Public Health的研究报告中，来自瑞典于默奥大学的研究人员通过研究发现，从16岁开始，有规律的大量饮酒和酗酒或许和女性后期机体血液中较高的葡萄糖浓度直接相关，而血糖水平较高是2型糖尿病的一种风险因子。'),
        ('饮酒','长期大量饮酒会损害人的中枢神经系统，或导致人出现精神恍惚、倦怠无力、幻听、幻视、记忆减退、智力下降等，发表在《BMJ》杂志上的研究表明，即使中度的饮酒也会导致慢性的大脑认知水平的下降。'),
        ('糖尿病','糖尿病是一组以高血糖为特征的代谢性疾病。高血糖则是由于胰岛素分泌缺陷或其生物作用受损，或两者兼有引起。糖尿病时长期存在的高血糖，导致各种组织，特别是眼、肾、心脏、血管、神经的慢性损害、功能障碍。糖尿病存在明显的遗传异质性，具有家族发病倾向，1/4～1/2患者有糖尿病家族史。临床上至少有60种以上的遗传综合征可伴有糖尿病。'),
        ('体重消瘦','体重过轻的人常常会缺钙,而且因为脂肪量很少,很难练成肌肉,这样会影响骨细胞的功能和代谢,易致骨质疏松。过于消瘦者普遍存在营养摄入不均衡的问题,铁、叶酸、维生素B12等造血物质本身就摄入不足,进而发展为贫血。'),       
        ('体重消瘦','容易导致对病毒的抵抗力会下降，还容易出现疲劳的情况，产生摄入热量不足,消耗体内的脂肪供能,引起胆固醇移动,导致胆汁中胆固醇过高,胆汁变得黏稠,析出结晶并沉淀下来形成胆结石。'),       
        ('体重消瘦','当人体过分消瘦时,身体内腹壁松弛、腹肌薄弱,导致悬吊、固定胃位置的肌肉和韧带松弛无力,腹压下降,于是整个胃的生理位置就降低、胃蠕动减弱,从而引发胃下垂。'),
        ('体重肥胖','肥胖者会增加糖尿病患病发生率，有研究显示，在2型糖尿病中80%都是肥胖者，而且发生肥胖时间越长，患有糖尿病几率就越大。肥胖者特别是腹型肥胖者由于进食脂肪多、体内脂肪储存多、高胰岛素血症可增高血脂、血脂的清除等原因，所以，比普通人更容易表现为血脂紊乱。'),
        ('体重肥胖','肥胖者容易患高血压，有的肥胖人群会出现血压波动;20~30岁的肥胖者，高血压的发生率要比同年龄而正常体重者高1倍;40~50岁的肥胖者，高血压的发生几率要比非肥胖者高50%,一个中度肥胖(BMI>30)的人，发生高血压的几率是体重正常者的5倍多。'),
        ('体重肥胖','肥胖人群容易发生大动脉粥样硬化，易在高血压的作用下发生破裂，引起脑出血，甚至危及生命。其次，肥胖者血液中组织纤溶激活抑制因子较高，使血栓难以溶解,易发生脑梗死。而过多的脂质沉积在冠状动脉壁内，致使管腔狭窄、硬化，易发生冠心病、心绞痛，同时增加心脏泵血负担导致心功能衰竭。'),
        ('体重肥胖','肥胖造成胸壁与腹腔脂肪增厚，使肺容量下降、肺活量减少而影响肺部正常换气的功能。且因为换气不足，可能引起红血球增多症，造成血管栓塞。严重者可能发生肺性高血压、心脏扩大及梗塞性心衰竭。因为脂肪的堆积，亦可能影响气管内纤毛的活动，使其无法发挥正常功能。'),
        ('体重肥胖','肥胖者与正常人相比，胆汁酸中的胆固醇含量增多，超过了胆汁中的溶解度，因此肥胖者容易并发高比例的胆结石，据统计，30%的肥胖者手术发现有胆结石，而非肥胖者只占5%。肥胖者往往同时患有脂肪肝,据统计，肥胖者中脂肪肝患病率高达50%，远远高于非肥胖者发病率。'),
        ('低血压','低血压是指血压低于正常的水平。一般认为成年人上肢动脉血压低于90/60mmHg即为低血压。原发性低血压，比如生理性低血压，发病原因不清，与形体瘦弱、遗传因素有一定关联。继发性低血压是指某些疾病导致的低血压状态，一类为短期内迅速发生低血压，如大出血、脱水、感染、过敏等原因所致的血压急剧降低；另一类为缓慢发生逐渐加重，可能导致低血压的心脏病和内分泌疾病，包括甲状腺疾病、肾上腺功能不全、先天性心脏病、慢性心力衰竭等，还存在体位低血压、孕期低血压和餐后低血压等。'),
        ('高血压','高血压病是生活中常见慢性疾病,严重危害身体健康和生生活质量。高血压本身会引起头痛、眩晕、注意力不集中、情绪不稳定等症状。高血压对心脏血管的损害主要是冠状动脉血管，而心脏其他的细小动脉则很少度受累。有人研究认为，由于血压增高，冠状动脉血管伸张，刺激血管内层下平滑肌细胞增生，使动回脉壁弹力蛋白、胶原蛋白及粘多糖增多，血管内膜层和内皮细胞损伤，胆固醇和低密度脂蛋白易浸入动脉壁，以及纤维增生；另外，由于答平滑肌细胞内溶酶体增多，减少了对动脉壁上胆固醇等物质的消除。'),
        ('高血压','如果是长期的血压升高，有可能会导致尿蛋白升高，慢性肾功能不全，眼底视网膜动脉硬化，进一步有可能诱发眼底出血等疾病，从而造成眼底、大脑、心脏、肾脏等靶器官的损害,严重时会导致心肌梗死、脑出血、脑卒中、急性肾衰这类急性并发症，直接危害生命。'),
        ('高血压','有家族史的子女患高血压的危险是无家族史的2倍;有家族史患者较无家族史患者发病年龄偏低，血压水平较高。高血压随着年龄的增加而发病率上升，老年人高血压患病率普遍较高。大量吸烟、喝浓茶或浓咖啡等也可引起血压升高，这是因为尼古丁、茶碱、咖啡因这些物质能够兴奋交感神经系统，使心率加快、血压升高。饮酒对血压也有不小影响。'),
        ('心动过速','成人安静时心率超过100次/分钟（一般不超过160次/分钟），称为窦性心动过速，心动过速分生理性、病理性两种。跑步、饮酒、重体力劳动及情绪激动时心律加快为生理性心动过速，常见于兴奋、激动、吸烟、饮酒、喝浓茶或咖啡后；若高热、贫血、甲亢、出血、疼痛、缺氧、心衰和心肌病等疾病引起心动过速，称病理性心动过速，见于感染、发热、休克、贫血、缺氧、甲亢、心力衰竭等病理状态下，或见于应用阿托品、肾上腺素、麻黄素等药物后。'),
        ('心动过缓','成人安静时心率低于60次/分钟（一般在45次/分钟以上），称为窦性心动过缓，可见于长期从事重体力劳动的健康人和运动员；或见于甲状腺机能低下、颅内压增高、阻塞性黄疸以及洋地黄、奎尼丁或心得安类药物过量。如果心率低于40次/分钟，应考虑有病态窦房结综合征、房室传导阻滞等情况。如果脉搏强弱不等、不齐且脉率少于心率，应考虑心房纤颤。心率超过160次/分钟，或低于40次/分钟，大多见于心脏病患者，如常伴有心悸、胸闷等不适感，应及早进行详细检查，以便针对病因进行治疗。'),
        ('心动过缓','很多人都会有窦性心动过缓伴不齐，对于多数人来说是正常的，不必过于担心。窦性心动过缓是指心率低于60次/分钟的人，是否会出现此症状，与其心跳过缓的频率和引起心跳过缓的原因有关。在安静状态下，成年人的心率若在50～60次/分钟之间一般不会出现明显症状。尤其是一些训练有素的运动员以及长期从事体力劳动的人，在安静状态下即使其心率在40次/分钟左右也不会出现明显症状。'),
        ('心动过缓','生理性在正常睡眠时，由于迷走神经张力增高可出现窦性心动过缓，心率可在50次/分钟左右，个别可在40次/分钟左右。运动员白昼可在50次/分钟左右，夜间个别可低至38次/分钟左右。体力劳动者也常出现窦性心动过缓。可见于年轻人及老年人。代谢降低(如低温、重度营养不良恶病质、脑垂体功能低下、甲状腺功能减低症等)、电解质紊乱(如高钾血症、尿毒症或血液酸碱度改变者)也常出现窦性心动过缓。'),
        ('心动过缓','消化性溃疡合并窦性心动过缓，消化性溃疡在发病机制中，胃酸的分泌物主要受迷走神经张力控制，当其兴奋性增高时可引起窦性心动过缓。窦房结功能受损（如炎症、缺血、中毒或退行性变的损害等）而引起的窦性心动过缓。此外，可见于心肌受损，如心肌炎、心包炎、心内膜炎、心肌病、心肌梗死、心肌硬化等。也可能为一过性的窦房结炎症、缺血及中毒性损害所致。在急性心肌梗死发病早期发生率最高,窦性心动过缓的发生率为20%～40%。'),
        ('低脂血','血脂中的主要成分是甘油三酯和胆固醇，它们是生命细胞的基础代谢必需物质。其中甘油三酯参与人体内能量代谢，而胆固醇则主要用于合成细胞浆膜、类固醇激素和胆汁酸。低脂血症是指血液中脂类含量较低，包括总胆固醇含量，高密度脂蛋白，低密度脂蛋白以及甘油三酯的含量。常见于营养不良、吸收不良综合征、肝脏疾病、甲状腺功能亢进症、慢性感染与其他炎症、血液系统或其他恶性肿瘤、罕见的家族性缺陷等疾病，饮食不合理、营养摄入不均衡、过度节食导致等不正确的生活方式，也会会导致血脂异常。'),
        ('高脂血','血脂中的主要成分是甘油三酯和胆固醇，它们是生命细胞的基础代谢必需物质。其中甘油三酯参与人体内能量代谢，而胆固醇则主要用于合成细胞浆膜、类固醇激素和胆汁酸。为可靠地反映血脂水平的真实情况。高脂血症是由各种原因导致的血浆中的胆固醇、甘油三酯以及低密度脂蛋白水平升高和高密度脂蛋白过低的一种的全身质代谢异常疾病，胆固醇和甘油三酯水平的升高与动脉粥样硬化的发生有关。'),
        ('高脂血','原发性高脂血症是原来无任何其他疾病而发生高脂血症，一般是因为遗传因素。而继发性高脂血症是由于其它原因引起的高脂血症，比如：糖尿病、甲状腺功能减退、肾病综合征、肾移植、胆道阻塞等。暴饮暴食、嗜酒、偏食、饮食不规律等不良饮食习惯和长期精神紧张、导致内分泌代谢紊乱，也会导致的高脂血症；'),
    )

    for line in lines:
        hmtype=Indicator.objects.filter(name=line[0]).first()

        if hmtype:
            print(type(hmtype),line[0],line[1])
            RiskAnalyse.objects.get_or_create(hmtype = hmtype,risk =line[1])
    
    intervents = (
        ('吸烟','吸烟对人体的危害较大，戒烟是降低吸烟危害的唯一方法，戒烟越早越好，任何年龄戒烟均可获益，因此建议采用逐渐减少吸烟次数的方法，循序渐进的进行戒烟，如实在无法戒除建议减少吸烟量，或通过使用烟草替代品。'),
        ('吸烟','吸烟者建议补充维生素。烟气中的某些化合物，可使维生素a、b、c、e等的活性大为降低，并使体内的这些维生素得到大量消耗。因此，吸烟者宜经常多吃富含维生素的食物，如牛奶、胡萝卜、花生、玉米面、豆芽、白菜、植物油等。这样既可补充由于吸烟所引起的维生素缺乏，又可增强人体的自身免疫功能。'),
        ('吸烟','吸烟者建议经常多喝茶。因烟气中含有的化合物可导致动脉内膜增厚，胃酸分泌量显著减少及血糖增高等症，而茶叶中所特有的儿茶素等可有效防止胆固醇在血管壁沉积，增加胃肠蠕动及降低血、尿糖等。吸烟者宜经常多喝茶，以降低吸烟所带来的这些病症的发作。同时，茶能利尿、解毒，还可使烟中的一些有毒物随尿液排出，减少在体内停留时间。'),
        ('吸烟','经常吸烟易导致人体血液中硒元素含量偏低，而硒又是防癌抗癌所不可缺少的一种微量元素。因此，吸烟者应经常多吃一些含硒丰富的食物，如动物肝脏、海藻及虾类等。可适当补充含铁的食物，如动物肝脏、肉、海带、豆类。坚果和粗粮等含维生素e的食物可使吸烟者得肺癌的发病率降低约20%。'),
        ('吸烟','因吸烟使血管中的胆固醇及脂肪沉积量加大，大脑供血量减少，易致脑萎缩，加速大脑老化等。因此，应吃含饱和脂肪酸的肥肉等，增加降低或抑制胆固醇合成的食物，如牛奶、鱼类、豆制品及高纤维食物，富含β-胡萝卜素的碱性食物能有效抑制烟瘾，对减少吸烟量和戒烟都有一定作用。如胡萝卜、菠菜、豌豆苗、苜蓿、辣椒等。'),
        ('饮酒','饮酒时一定要先吃一部分食物后再喝酒，同时做到少量及慢慢喝，避免醉酒，每次喝酒时，一定要多饮水，避免体内细胞脱水，酒醒后再补充部分水，饮酒者日常应饮食均衡，适当补充复合维生素B1、B3等，如燕麦、全麦面包、动物内脏、瘦肉、花生、蔬菜、麦麸、牛奶等，常吃蜂蜜，果汁，不要吃油炸及脂肪食物。长期大量饮酒或酗酒对人体的危害较大，因此建议戒酒或控制饮酒量，加强体育锻炼。'),
        ('体重消瘦','排除如甲状腺、糖尿病、肾上腺、消化系统疾病等疾病的潜在影响，在此基础上做到科学增重，保持正常和规律的饮食，保证碳水化合物的摄入量，补充充足的蛋白质，以谷物为主,蛋、奶为辅,多吃水果。加强体育锻炼，保持充足而良好的睡眠。'),            
        ('体重肥胖','改变进食行为，增加咀嚼次数，减慢进食速度，饭前先喝一碗汤，既帮助消化液的分泌，又增加饱腹感，减少饮食量。限制总热能摄入量，以减少谷类主食摄入量为主。摄入量应低于消耗量，以使体重逐渐下降。采用高蛋白、低脂肪、低糖、高维生素、低盐饮食。如：多食用鸡蛋、牛奶、牛肉、鱼、虾、鸡、大豆、花生等高蛋白食物，限制高脂肪食物，如肥肉、动物内脏、油炸食品等，少食高热量的食物，如甜食、糖果、巧克力等，多食蔬菜、杂粮，食用适量水果，即每天摄入的钠盐少于5克。'),
        ('体重肥胖','坚持体力劳动或体育锻炼，选择适宜的运动项目和适宜的运动量，最佳运动时间为每天的15：00—17：00。如在饭前锻炼后间隔30min吃饭；饭后1.5h锻炼。可根据自身情况掌握运动强度。运动强度以每分钟脉搏次数为尺度，30-40岁不超过130次，40-50岁不超过120次，60岁以上不超过110次，并要根据个人情况循序渐进，以生理耐受量为限。开始运动的头两个月，体重下降不明显，但如坚持2个月以上疗效渐明显。'),
        ('体重肥胖','合理营养的关键在于“适度”，主要在通过平衡膳食来实现。平衡膳食是指膳食中所含营养素，种类齐全、数量充足、比例适当。食物多样、谷物为主,平衡膳食必须由多种食物组成，提倡广泛食用多种食物。多种食物包括五大类：谷类及薯类；动物性食物；豆类及其制品；蔬菜及水果类；纯热能食物。'),
        ('体重肥胖','控制食物量，不能多吃蔬菜、水果和薯类，含丰富蔬菜、水果和薯类的膳食吃多了，同样发胖。常吃豆类及其制品，含有丰富的蛋白质和维生素，含钙量较高，利用率高。经常吃适量的鱼、禽、蛋、瘦肉，少吃肥肉和荤油'),
        ('体重肥胖','I度肥胖者：体重以每周减轻0.5-1公斤为宜，应控制食量，进食低脂、低胆固醇、低盐食物；II度和III度肥胖者：除与I度肥胖者一样严格控制饮食外，在医生指导下使用减肥药物或饥饿疗法。'),
        ('体重肥胖','肥胖症由于怕热多汗，抵抗力低，皮肤紫纹及皱折处易磨损，易感染，引起皮炎、皮癣等，应勤洗澡，勤更衣，保持皮肤干燥清洁。'),
        ('体重肥胖', '肥胖患者在治疗前应到医院做一系列检查以排除有无其它内分泌代谢疾病，治疗期间应每天测体重1-2次。应慎重应用减肥药物，最好在医生指导下用药。'),
        ('糖尿病','目前尚无根治糖尿病的方法，但可以通过科学合理的治疗方法，使大多数糖尿病患者具有与非糖尿病者同等的生活质量和寿命。糖尿病综合管理的5个要点(又称五驾马车)包括：糖尿病教育、医学营养治疗、运动治疗、药物治疗、血糖监测。'),
        ('糖尿病','糖尿病教育：患者及家属应尽可能多的学习、了解糖尿病及其并发症相关知识，积极向专业人士寻求帮助，谨遵医嘱进行治疗，提高自我管理的意识及能力。'),
        ('糖尿病','医学营养治疗：医学营养治疗是糖尿病的基础管理措施，旨在帮助患者制定营养计划，形成良好的饮食习惯，确定合理的总能量摄入，合理均衡分配各种营养物质，恢复并维持理想体重。一般可根据身高（cm）-105估计理想体重。成人正常体重者完全卧床时每日每千克理想体重需要给予能量15~20kal，休息状态下25~30kcal ，根据体力劳动情况酌情增加能量摄入。'),
        ('糖尿病','膳食营养分配要均衡，碳水化合物供给量占总热量50~60%，成年患者每日主食摄入量为250~400g，限制单糖和双糖摄入。蛋白摄入量占总热量15~20%，成年患者每日每千克理想体重给予0.8~1.2g，至少半数蛋白应来自动物蛋白质。每日脂肪摄入量占总热量25~30%，其中饱和脂肪酸摄入量低于总能量的10%，胆固醇摄入量低于300mg/d。推荐富含膳食纤维的食品。每日摄入能量应合理分配于各餐次，可按照每日三餐1/5、2/5、2/5或1/3、1/3、1/3分配。'),
        ('糖尿病','运动治疗：运动治疗对于伴肥胖的2型糖尿病患者尤为重要，应在医师指导下进行，建议每周150min的中等强度运动。'),
        ('糖尿病','血糖监测：以血糖监测为主的病情监测亦非常重要。血糖监测指标主要是空腹和餐后血糖及糖化血红蛋白。糖化白蛋白可用于评价血糖控制方案调整后短期的疗效。患者可以使用便携式血糖仪在家中进行自我血糖监测。此外，病情监测还应包括心血管危险因素和并发症的监测，患者每年至少要进行一次血脂检查以及全面的心、肾、神经、眼底等相关检查。'),
        ('糖尿病','药物治疗：目前糖尿病治疗药物包括口服药和注射制剂两大类。口服降糖药主要有促胰岛素分泌剂、非促胰岛素分泌剂、二肽基肽酶-4抑制剂和钠-葡萄糖共转运蛋白2抑制剂。注射制剂有胰岛素及胰岛素类似物、胰高血糖素样多肽-1受体激动剂。'),
        ('低血压','很多低血压像高血压一样无法彻底根治，但通过对患者生活方式的调整，如饮食习惯、运动方式、用药等，可以有效地预防和控制其发生。日常应避免腰部弯曲、避免直接起身，如果出现低血压症状，挤压大腿、腹部和臀部肌肉能缓解相关症状。注意环境变化，需尽量减少气候和环境改变对血压的影响，例如秋冬季及时增加衣物、避免室温过低等。避免洗澡水过热或洗澡时间过长，使血管扩张而降低血压。对于脊髓损伤或自主神经功能衰竭所致的严重体位性低血压，站立之前使用腹带或弹力绷带对腹部或下肢短时加压。'),
        ('低血压','养成健康饮食的习惯，保证营养均衡，确保健康所需的所有营养。根据医嘱食用适量的盐，可缓解低血压症状。减少碳水化合物的摄入，为了防止餐后血压急剧下降，建议每天少食多餐，并限制高碳水化合物的食物，如土豆、大米、面条和面包等。加强营养，多食易消化富含蛋白质的食物，如鸡蛋、鱼、奶酪、牛奶等，多喝汤多饮水，适当增加盐分的摄入，同时注意补充铁剂和维生素，防止贫血。'),
        ('低血压','适当加强锻炼，保持良好的精神状态，以便改善血管的调节功能，加速血液循环，避免血压偏低。少喝酒，酒精会使人脱水，即使适度饮酒，也能降低血压；多喝水，水可以可增加血容量，从而升高血压。晚上睡觉时将头部垫高，可减轻低血压的症状。睡醒后几分钟再坐起，在床边坐1~3分钟，逐渐过渡到站立位，有助于促进静脉血向心脏回流，减少体位性低血压的发生，尽可能减少长时间卧床。'),
        ('高血压','培养正确的饮食习惯，日常生活中应该减少钠盐的摄入，以清淡饮食为主。减少高钠食品如酱油、腌制品、碳酸饮料等含钠量高的食物，中国膳食指南建议，成人每天食盐量不应超过6克。此外，多食富含钾的食物可以增加钠的排出，改善血管环境，增强血管弹性。适当增加黄豆、番茄、芹菜、食用菌等蔬菜以及橘子、苹果、香蕉、猕猴桃、菠萝、核桃、等新鲜水果的摄入量，以补充身体内的钾离子。'),
        ('高血压','保持平静心情，避免情绪激动及过度紧张焦虑。避免长期过度紧张工作和劳累，保证充足睡眠，劳逸结合，选择合适的运动锻炼和放松疗法如步行、太极拳等。运动量不宜太大，常用运动强度指标为运动时最大心率达到170减去年龄，且休息15—30分钟后恢复正常为宜。避免使用过热的水洗澡或长时间蒸汽浴。坚持长期用药，不擅自停药，不随意增减剂量，了解药物作用与副作用，坐位起立或平卧坐起时，动作尽量缓慢，以免引起昏厥，有异常及时报告医生，调节用药。'),
        ('心动过缓','通过参加各种强度适宜的运动，使心功能得到锻炼，从而使静息心率逐渐恢复正常。一般适宜的运动心率是“170-年龄”，如一个50岁人，运动心率控制在120次/分钟为宜，过快说明运动量过大，达不到也起不到效果。运动前要自觉舒适、无疲劳感，一般运动不要超过1小时，而且每次最佳时间为30分钟～60分钟，每周至少坚持3次运动。'),
        ('心动过缓','改正不良的生活方式，熬夜、吸烟、饮酒，少喝浓茶，特别是不要在睡前喝，否则容易导致失眠。保持适当体重，体重过瘦、营养不良无法为心脏提供所需能量，因此体重过瘦、营养不良者要通过健身运动，调节饮食来保持适宜的体重。'),
        ('心动过缓','在心动过缓急性发作时，除针对原发病因进行治疗、停用可减慢心率的药物外，可以使用阿托品、异丙肾上腺素提高心率。对于心率在每分钟40次或者更慢者，药物提高心率效果不明显，尤其是伴有反复晕厥或晕厥前兆的患者，应置入心脏起搏器。'),
        ('心动过速','心率增快危害健康、缩短寿命，增加心血管病的发病率和死亡率。常参加各种强度适宜的运动，就会使静息心率变慢。虽然运动时心率加快，但运动能使心功能得到锻炼，从而使静息心率减慢。一般适宜的运动心率是“170-年龄”，如一个50岁人，运动心率控制在120次/分钟为宜，过快说明运动量过大，达不到也起不到效果。运动前要自觉舒适、无疲劳感，一般运动不要超过1小时，而且每次最佳时间为30分钟～60分钟，每周至少坚持3次运动。'),
        ('心动过速','改正不良的生活方式，熬夜、吸烟、饮酒均可使静息心率加快。少喝浓茶，特别是不要在睡前喝，否则容易导致失眠。还应定时大便，保持排便顺畅。保持适当体重，肥胖会使心脏负担加重，心率加快，因此肥胖者要通过健身运动，调节饮食来保持适宜的体重。保持心态要平和，避免着急、生气，出现心率过快时，可通过听音乐、静心冥想等方式逐渐恢复平静。'),
        ('心动过速','某些疾病如高血压及冠心病引起的心率加快，可根据医嘱服用药物，心律平、异搏定等可终止某些心动过速的发作，但不能根治，推注药物有一定危险性，不主张长期服药防止心动过速的再发。射频消融术可根治心动过速，术后不再需要使用抗心律失常药物；患者无痛苦，操作方法简便。特点是创伤小、恢复快，治愈率高。'),
        ('低脂血','在排除原发型疾病的基础上，建议改善饮食习惯，合理膳食，荤素搭配，适当多吃些禽蛋、海鲜、动物肝脏等高胆固醇类食物，适量增加锻炼，定期复查血脂变化，如果无变化建议全面身体检查。'),
        ('高脂血','高血脂患者在排除原发型疾病的基础上，需注意日常饮食、运动锻炼，以减少心脑血管疾病及其他相关疾病的发生风险。建议控制饮食，减少饱和脂肪酸（植物油、鱼油）和胆固醇摄入，每日摄入量<300mg；减少每日摄入脂肪量(<30g食用油)，增加膳食纤维，补充植物固醇和可溶性纤维，限制盐摄入量，戒烟，限制饮酒，禁饮烈性酒。'),
        ('高脂血','加强体育锻炼，进行每周5~7天每次30分钟中等强度体育运动。有心脑血管疾病、心血管疾病危险因素者、高血压、糖尿病、吸烟、过量饮酒、肥胖者、早发性心血管疾病家族史者、有家族性高脂血症者和皮肤或肌腱有黄色瘤人群建议定期监测血脂水平,非药物治疗一般情况下，每3~6个月复查1次血脂；如血脂达标，可延长至每6~12个月复查1次。调脂药物治疗6周内复查血脂、肝功能、肌酸激酶水平；如血脂达标，可延长至6~12个月复查1次；如血脂未达标，3个月后再次复查，仍未达标，调整治疗方案。'),
    )

    for intervent in intervents:
        hmtype=Indicator.objects.filter(name=intervent[0]).first()
        HealthIntervent.objects.get_or_create(hmtype = hmtype,intervent =intervent[1])

#创建用户组
def creatgroup():
    print('删除所有组......')
    Group.objects.all().delete()
    print('建立用户组：健康管理、个人用户 ......')
    #Group.objects.get(name='个人用户')
    usergroup=Group.objects.create(name='个人用户')
    healthgroup=Group.objects.create(name='健康管理')

    print('用户组分配权限 ......')

    usertable=['userinfo', 'bodyinfo', 'bloodpressure','bcholesterin','smokediabetesinfo','contenttype']
    scaletable=['agescale', 'weightscale', 'bloodpressurescale', 'smokescale', 'diabetesscale', 'riskevaluatscale',
                'commonriskscale','tcscale','bmiscale','healthintervent','riskanalyse','singleassess','indicator','user']
    premissions = ['add', 'delete', 'change', 'view']
    for tb in usertable:
        for pm in premissions:
            pmtb = pm + '_' + tb
            perm = Permission.objects.get(codename=pmtb)
            usergroup.permissions.add(perm)
            healthgroup.permissions.add(perm)
    for tb in scaletable:
        for pm in premissions:
            pmtb = pm + '_' + tb
            perm = Permission.objects.get(codename=pmtb)
            healthgroup.permissions.add(perm)
    
def creatsystemset():
    lines = [['site_title', '健康管理分析系统', True],
            ['site_header', '健康管理分析', True],
            ['welcome_sign', '欢迎使用健康管理分析系统！', True],
            ['avatar_field', 'request.user.head_avatar', False],
            ['show_avatar', 'on', True],
            ['USE_CUSTOM_MENU', '1', True],
            ['site_logo', 'medias/health-logo.png', True],
            ]
    for line in lines:
        newdata = Options.objects.get_or_create(option_name=line[0])
        if newdata:
            print(type(newdata))
            newdata[0].valid = line[2]
            newdata[0].option_value = line[1]          
            newdata[0].save()


    lines = [['000I',1,5,'健康信息','left',3,'/healthinfo/dashboard/',None,300,1,None],
            ['0006',1,13,'健康标准','left',3,None,None,400,1,None],
            ['000I000S',2,0,'基本信息','left',0,'/admin/healthinfo/userinfo/',None,350,1,7],
            ['000I000W',2,0,'吸烟糖尿病史','left',0,'/admin/healthinfo/smokediabetesinfo/',None,340,1,7],
            ['000I000V',2,0,'身高体重信息','left',0,'/admin/healthinfo/bodyinfo/',None,330,1,7],
            ['000I000U',2,0,'血压信息','left',0,'/admin/healthinfo/bloodpressure/',None,320,1,7],
            ['000I000T',2,0,'血脂信息','left',0,'/admin/healthinfo/bcholesterin/',None,310,1,7],
            ['00060027',2,0,'ICVD吸烟评估标准','left',0,'/admin/healthinfo/smokescale/',None,180,1,6],
            ['0007',1,2,'认证授权','left',3,None,None,120,1,None],
            ['0008',1,3,'系统设置','left',3,None,None,110,1,None],
            ['0007000A',2,0,'用户管理','left',0,'/admin/auth/user/',None,110,1,4],
            ['0008000B',2,0,'基本设置','left',0,'/admin/django_admin_settings/options/general_option/',None,120,1,4],
            ['00080009',2,0,'菜单设置','left',0,'/admin/django_admin_settings/menu/',None,100,1,4],
            ['0008000A',2,0,'选项设置','left',0,'/admin/django_admin_settings/options/',None,110,1,4],
            ['000J',1,5,'健康评估','left',3,'/healthinfo/dashboard/',None,400,1,7],
            ['00060021',2,0,'ICVD年龄评估标准','left',0,'/admin/healthinfo/agescale/',None,200,1,6],
            ['00060026',2,0,'ICVD糖尿病评估标准','left',0,'/admin/healthinfo/diabetesscale/',None,170,1,6],
            ['00060020',2,0,'ICVD血压评估标准','left',0,'/admin/healthinfo/bloodpressurescale/',None,160,1,6],
            ['00060025',2,0,'ICVD体重评估标准','left',0,'/admin/healthinfo/weightscale/',None,190,1,6],
            ['0006001N',2,0,'ICVD十年发病风险常规标准','left',0,'/admin/healthinfo/commonriskscale/',None,130,1,6],
            ['0006001O',2,0,'ICVD十年发病风险评估标准','left',0,'/admin/healthinfo/riskevaluatscale/',None,140,1,6],
            ['00070008',2,0,'组管理','left',0,'/admin/auth/group/',None,100,1,4],
            ['00060022',2,0,'ICVD血脂评估标准','left',0,'/admin/healthinfo/tcscale/',None,150,1,6],
            ['000J0011',2,0,'BMI体重健康评估','left',0,'/healthinfo/weightassess/',None,440,1,7],
            ['000J000Y',2,0,'血压健康评估','left',0,'/healthinfo/bpassess/',None,430,1,7],
            ['000J0010',2,0,'血脂健康评估','left',0,'/healthinfo/bsassess/',None,420,1,7],
            ['000J000N',2,0,'缺血性心血管病发病风险评估','left',0,'/healthinfo/icvdrisk/',None,410,1,7],
            ['00060023',2,0,'BMI体重健康评估标准','left',0,'/admin/healthinfo/bmiscale/',None,220,1,6],
            ['0006001W',2,0,'健康指标分类','left',0,'/admin/healthinfo/indicator/',None,120,1,6],
            ['0006001X',2,0,'健康风险分析','left',0,'/admin/healthinfo/riskanalyse/',None,110,1,6],
            ['00060024',2,0,'健康风险干预','left',0,'/admin/healthinfo/healthintervent/',None,100,1,6],
            ['000J000W',2,0,'日常习惯评估','left',0,'/healthinfo/habitassess/',None,450,1,7],
            ['0006002D',2,0,'单项评估标准','left',0,'/admin/healthinfo/singleassess/',None,210,1,6],
            ['0005',1,7,'健康分析','left',3,None,None,500,1,None],
            ['00050002',2,0,'分地区不良习惯及慢性病分析','left',0,'/healthinfo/analye/',None,500,1,6],
            ['00050004',2,0,'吸烟人群分布分析','left',0,'/healthinfo/smokeanalye/',None,560,1,6],
            ['00050005',2,0,'饮酒人群分布分析','left',0,'/healthinfo/drinkanalye/',None,550,1,6],
            ['0005000E',2,0,'糖尿病人群分布分析','left',0,'/healthinfo/diabetesanalye/',None,530,1,6],
            ['0005000H',2,0,'肥胖人群分布分析','left',0,'/healthinfo/fatanalye/',None,540,1,6],
            ['0005000G',2,0,'高血压人群分布分析','left',0,'/healthinfo/hypertensionanalye/',None,520,1,6],
            ['0005000I',2,0,'高脂血人群分布分析','left',0,'/healthinfo/hyperlipemanalye/',None,510,1,6],]
    for line in lines:
        if line[10] == 7:
            id=ContentType.objects.filter(app_label='contenttypes', model='contenttype').first()
        elif line[10] == 6:
            id = ContentType.objects.filter(app_label='auth', model='user').first()
        elif line[10] == 4:
            id = ContentType.objects.filter(app_label='auth', model='permission').first()
        else:
            id = None    
        newdata = Menu(path=line[0], depth=line[1], numchild=line[2],\
            name=line[3], position=line[4], link_type=line[5], link=line[6], icon=line[7], \
            priority_level=line[8], valid=line[9], content_type=id)
        newdata.save()


#创建超级用户
def create_superuser():
    print('建立超级用户：admin：123456')
    username='admin'
    password='123456'
    if not User.objects.filter(username=username).first():
        user=User.objects.create_superuser(username=username,password=password)
        group = Group.objects.get(name='个人用户') 
        group.user_set.add(user)
        group = Group.objects.get(name='健康管理') 
        group.user_set.add(user)
    else:
        print('admin已存在！')

def main():
    print('System Init Start ......')
    print('创建用户组')
    creatgroup()
    print('删除所有用户......')
    User.objects.all().delete()
    print('创建超级用户')
    create_superuser()
    print('初始化系统设置')
    creatsystemset()

    print('生成健康评价标准数据')
    createscale()

    print('System Init End ......')


if __name__ == "__main__":  
    main()