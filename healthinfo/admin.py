from django.contrib import admin
from django.contrib.auth.models import User
from healthinfo.models import UserInfo,BodyInfo,SmokeDiabetesInfo,BloodPressure,Bcholesterin
from healthinfo.models import AgeScale,WeightScale,BloodPressureScale,SmokeScale,DiabetesScale
from healthinfo.models import RiskEvaluatScale,CommonRiskScale,TCScale,BMIScale
from healthinfo.models import HealthIntervent,RiskAnalyse,SingleAssess,Indicator
from django.contrib import messages

# Register your models here.
admin.site.site_header = '健康信息管理'

#数据表的增删改
@admin.register(UserInfo) 
class UserInfoAdmin(admin.ModelAdmin):
    #显示外键user的姓名
    def get_name(self,obj):
        return obj.user.last_name+obj.user.first_name
    get_name.short_description = u'姓名'
    # 在去掉显示列表list_display中主键id和外键user字段(user.id),增加姓名显示
    exclude =('id','user',)
    ex = lambda x:[f.name for f in UserInfo._meta.fields if f.name not in x]
    list_display = ex(exclude) 
    list_display.insert(0, 'get_name')

    #设置点击进入编辑界面的字段
    list_display_links = ('get_name','ssn')
    #设置只读的字段
    #readonly_fields = ('get_name', )
    #设置可编辑字段
    #list_editable = list_display[2:]
    list_editable =('province','city','sex',)
    #增加选择过滤器和搜索字段
    list_filter = ('user__last_name', 'province', 'city', 'sex')
    #增加搜索字段
    search_fields =('user__username','ssn','phone','user__email','user__first_name','job')
    #给测量时间增加时间分层筛选器
    date_hierarchy = 'birthday'  
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    #重载save_model方法，解决隐藏外键后无法保存抛出IntegrityError外键约束异常问题
    def save_model(self, request, obj, form, change):
        #判断修改还是新增
        if change:
            super().save_model(request, obj, form, change)
        else:
            obj.user = request.user
            cur = UserInfo.objects.filter(user=obj.user).first()
            #新增时判断是否已有数据(一对一关系)
            if not cur:
                super().save_model(request, obj, form, change)
            else:
                #通过django消息机制显示错误信息
                messages.error(request, "一对一外键错误，数据已存在无法新增，可使用修改数据功能！")
                #关闭非错误信息，针对显示两条信息，一条错误信息，一条保存成功信息
                messages.set_level(request, messages.ERROR)

@admin.register(BodyInfo) 
class BodyInfoAdmin(admin.ModelAdmin):
    def get_name(self,obj):
        return obj.user.last_name+obj.user.first_name
    get_name.short_description = u'姓名'
    exclude =('id','user',)
    ex = lambda x:[f.name for f in BodyInfo._meta.fields if f.name not in x]
    list_display = ex(exclude) 
    list_display.insert(0, 'get_name')
    list_display_links = ('get_name','measuretime')
    list_editable = list_display[2:]
    list_per_page = 10
    #给测量时间增加时间分层筛选器
    date_hierarchy = 'measuretime'    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(SmokeDiabetesInfo) 
class SmokeDiabetesInfoAdmin(admin.ModelAdmin):
    def get_name(self,obj):
        return obj.user.last_name+obj.user.first_name
    get_name.short_description = u'姓名'
    exclude =('id','user',)
    ex = lambda x:[f.name for f in SmokeDiabetesInfo._meta.fields if f.name not in x]
    list_display = ex(exclude) 
    list_display.insert(0, 'get_name')
    list_display_links = ('get_name',)
    list_editable = list_display[2:]
    list_per_page = 10
    #增加选择过滤器和搜索字段
    list_filter = ('user__last_name', 'smoke', 'drink', 'diabetes')
    #增加搜索字段
    search_fields =('user__username','user__last_name','user__email','user__first_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            obj.user = request.user
            cur = SmokeDiabetesInfo.objects.filter(user=obj.user).first()
            if not cur:
                super().save_model(request, obj, form, change)
            else:
                messages.error(request, "一对一外键错误，数据已存在无法新增，可使用修改数据功能！")
                messages.set_level(request, messages.ERROR)

@admin.register(BloodPressure) 
class BloodPressureAdmin(admin.ModelAdmin):
    def get_name(self,obj):
        return obj.user.last_name+obj.user.first_name
    get_name.short_description = u'姓名'
    exclude =('id','user',)
    ex = lambda x:[f.name for f in BloodPressure._meta.fields if f.name not in x]
    list_display = ex(exclude) 
    list_display.insert(0, 'get_name')
    list_editable = list_display[2:]
    list_display_links = ('get_name','measuretime')
    list_per_page = 10   
    date_hierarchy = 'measuretime'  
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Bcholesterin) 
class BcholesterinAdmin(admin.ModelAdmin):
    def get_name(self,obj):
        return obj.user.last_name+obj.user.first_name
    get_name.short_description = u'姓名'
    exclude =('id','user',)
    ex = lambda x:[f.name for f in Bcholesterin._meta.fields if f.name not in x]
    list_display = ex(exclude)
    list_display.insert(0, 'get_name')
    list_display_links = ('get_name','measuretime')
    list_editable = list_display[2:]
    list_per_page = 10   
    date_hierarchy = 'measuretime' 
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(AgeScale) 
class AgeScaleAdmin(admin.ModelAdmin):
    #取出所有字段的字段名称存入显示列表
    list_display = [f.name for f in AgeScale._meta.fields]
    #去掉ID加入可编辑列表
    list_editable = list_display[1:]
    list_per_page = 10

@admin.register(WeightScale) 
class WeightScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in WeightScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10


@admin.register(BloodPressureScale) 
class BloodPressureScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in BloodPressureScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10

@admin.register(SmokeScale) 
class SmokeScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in SmokeScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10   

@admin.register(DiabetesScale)
class DiabetesScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in DiabetesScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10   

@admin.register(TCScale)
class TCScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in TCScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10
    
@admin.register(RiskEvaluatScale) 
class RiskEvaluatScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in RiskEvaluatScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10
    
@admin.register(CommonRiskScale) 
class CommonRiskScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in CommonRiskScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10

  
@admin.register(BMIScale) 
class BMIScaleAdmin(admin.ModelAdmin):
    list_display=[f.name for f in  BMIScale._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10

@admin.register(RiskAnalyse) 
class RiskAnalyseAdmin(admin.ModelAdmin):
    list_display=[f.name for f in RiskAnalyse._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10


@admin.register(HealthIntervent) 
class HealthInterventAdmin(admin.ModelAdmin):
    list_display=[f.name for f in HealthIntervent._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10   
'''
#内联表不需要单独@admin.register(RiskAnalyse) 
class RiskAnalyseInline(admin.TabularInline):
    model = RiskAnalyse
    #以下在TabularInline不起作用，只在StackedInline可用
    max_num =2
    extra = 2

class HealthInterventInline(admin.TabularInline):
    model = HealthIntervent
    max_num =2
    extra = 2

@admin.register(HMType) 
class HMTypeAdmin(admin.ModelAdmin):
    list_display=[f.name for f in HMType._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10
    #inlines = [RiskAnalyseInline, HealthInterventInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(id=2)
        return qs
'''

@admin.register(Indicator) 
class IndicatorAdmin(admin.ModelAdmin):
    list_display=('id','name','parent')
    list_editable =('name','parent')

@admin.register(SingleAssess) 
class SingleAssessAdmin(admin.ModelAdmin):
    list_display=[f.name for f in SingleAssess._meta.fields]
    list_editable = list_display[1:]
    list_per_page = 10 



#admin.site.register(HMType, RiskAnalyse)

#admin.site.register(UserInfo)


