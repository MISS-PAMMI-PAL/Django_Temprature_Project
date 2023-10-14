from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import UserProfile, ContactTo, UserDesc, Traffic
from myconst.models import MyState

from django.db import transaction
from django.contrib import auth
from django.db.models import Q, F, Value, IntegerField
from django.db.models.functions import Cast, Coalesce

from django.http import Http404
# -----------------------------------------------
from cryptography.fernet import Fernet
import random

from rest_framework.response import Response
from django.http import JsonResponse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils import timezone
today = timezone.now().date()
# -----------------------------------------------

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def welcome_dashboard(request):
    context = { 
        #'login_modal_popup': 'False',
        'banner_modal_popup': 'False'
    }
    try: 
        # ============================== Traffic User +  Banner Control =============================
        if request.session.get('visitor', 'None') != 'True':  # When Anonymous user is first time
            # print(timezone.now()) print('new visitor')
            if Traffic.objects.filter(Q(traffic_date=today)).exists():
                traffic, created = Traffic.objects.update_or_create(traffic_date=today,
                                                                    defaults={"visit": F("visit") + 1})
            else:
                Traffic.objects.create(traffic_date=today, visit=1, login=0, login_failed=0, reset_pwd=0)
            request.session['visitor'] = 'True' 
            context['banner_modal_popup'] = 'True'
        # ===========================================================================================
        if request.session.get('super_id', 'None') != 'None':
            is_status = request.session.get('u_status')
            if is_status == "G":
                return redirect('guest_dashboard_conn')  # authenticated user which have name and mob no
            elif is_status == "O":
                return redirect('operator_dashboard_conn')
            elif is_status == "A":
                return redirect('admin_dashboard_conn')
            elif is_status == "S":
                return redirect('staff_dashboard_conn')  # w=worker, staff
            elif is_status == "M":
                return redirect('master_dashboard_conn') #admin
            else:
                try:
                    logout(request)
                except:
                    pass
                return render(request, 'welcome/index.html', context)
        else:
            return render(request, 'welcome/index.html', context)
            # return render(request, 'welcome/login.html', context)
    except:
        pass   
    return render(request, 'welcome/index.html', context)


def registration(request):
    # sms_balance()
    # sms_bulk()
    # print(otp_sms(8448604268, "1212"))
    # print(sms_balance())
    if request.method == 'POST':
        var_name = request.POST.get('name', 'None').strip()
        var_phone = request.POST.get('phone', 'None').strip()
        var_email = request.POST.get('email', 'None').strip()
        var_pass = request.POST.get('password1', 'None').strip()
        try:
            var_phone = int(var_phone)
        except:
            var_phone = 1
        var_phone = str(var_phone)
        if int(var_phone[0]) > 5:
            if (len(var_phone) == 10) and (var_pass != 'None') and (var_name != 'None'):
                if var_pass == request.POST.get('password2', 'None').strip():
                    try:
                        User.objects.get(username=var_phone)
                        messages.error(request, f'This {var_phone} mobile number already exist')
                        return render(request, 'welcome/registration.html')
                    except User.DoesNotExist:
                        '''user = User.objects.create_user(username=var_phone,         #phone
                                                        password=var_pass1,
                                                        email=var_name, #.lower(), # name
                                                        #first_name = request.POST[''],   # company Id
                                                        last_name="G")                     #  Is_admin'''
                        # auth.login(request, user)

                        if request.session.get('registration_sms_count', 'None') == 'None':  # one time send
                            number = str(random.randint(1000, 9999))
                            print("-----registration otp--------", number)

                            x = True
                            if x:  # otp_sms(var_username, number):
                                f_obj = Fernet(settings.FERNET_KEY)
                                encrypted_otp = f_obj.encrypt(number.encode('utf-8'))

                                request.session['reg_name'] = var_name
                                request.session['reg_phone'] = var_phone
                                request.session['reg_email'] = var_email
                                request.session['reg_gen_id'] = var_pass
                                request.session['reg_gen_key'] = str(encrypted_otp)  # encrypted_otp

                                request.session['registration_sms_count'] = 3
                                Traffic.objects.filter(Q(traffic_date=today)).update(msg=F('msg') + 1)
                                return redirect('reg_otp_decision_conn')
                            else:
                                messages.error(request, "Please try after some time, Server Down")
                                return render(request, 'welcome/registration.html')
                        else:
                            messages.error(request, f"OTP already send {var_phone}, or try again registration after 2 hours")
                            return redirect('reg_otp_decision_conn')

            messages.error(request, "Registration password wrong")
            return render(request, 'welcome/registration.html')
        else:
            messages.error(request, "Please enter correct mobile no")
            return render(request, 'welcome/registration.html')
    else:
        return render(request, 'welcome/registration.html')

@transaction.atomic
def reg_otp_decision(request):
    if request.method == 'POST':
        reg_name = request.session.get('reg_name', 'None')
        reg_phone = request.session.get('reg_phone', 'None')
        reg_email = request.session.get('reg_email', 'None')
        reg_gen_id = request.session.get('reg_gen_id', 'None')  # pwd
        reg_gen_key = request.session.get('reg_gen_key', 'None')  # encrypted_otp

        reg_otp_user = request.POST.get('enter_otp', 'None').strip()  # enter otp

        f_obj = Fernet(settings.FERNET_KEY)
        # reg_sys_otp = reg_gen_key (both are same)
        reg_otp_sys = f_obj.decrypt(bytes(reg_gen_key[2:(len(reg_gen_key) - 1)].encode('utf-8')))
        
        # =============================================
        try:
            reg_otp_user = int(reg_otp_user)
        except:
            messages.error(request, f'Wrong, Please enter correct-OTP')
            return render(request, 'welcome/reg_otp_decision.html')
        # =============================================
        sms_countdown = int(request.session.get('registration_sms_count'))
        if (sms_countdown > 0) and (reg_phone != 'None'):
            
            if int(reg_otp_sys) == reg_otp_user:
                try:
                    User.objects.get(username=reg_phone)
                    messages.error(request, f'This {reg_phone} mobile number All ready exist')
                    return render(request, 'welcome/registration.html')
                except User.DoesNotExist:
                    user_ins = User.objects.create_user(username=reg_phone,  # phone
                                                    password=reg_gen_id, #pwd
                                                    email=reg_email,     # email
                                                    first_name=reg_name,  # name in lower()
                                                    last_name="G")       # Is_admin
                    # Created User Decription ==============
                    UserDesc.objects.create(user_ins=user_ins, device_ip="0.0.0.0",
                                            device_loc="India", sms_life=5)
                    # Created User Profile ==============
                    state_ins = get_object_or_404(MyState, id=1)
                    UserProfile.objects.create(user_ins=user_ins,
                                                #profile_img="None",
                                                email=reg_email,
                                                gender=0,
                                                so_name="None",
                                                house="None",
                                                building="None",
                                                colony="None",
                                                city="None",
                                                post="None",
                                                pincode="None",
                                                police_station="None",
                                                dist="None",
                                                state=state_ins)
                    # after managed ==============
                    Traffic.objects.filter(Q(traffic_date=today)).update(guest=F('guest') + 1)
                    try:
                        del request.session['reg_name']
                        del request.session['reg_phone']
                        del request.session['reg_email']
                        del request.session['reg_gen_id']
                        del request.session['reg_gen_key']
                        del request.session['registration_sms_count']
                    except:
                        pass
                    messages.success(request, f'Registration successful {reg_name} {reg_phone} , Pass-{reg_gen_id} <--- Please Remember PASSWORD !!!, Now click to Login')
                    return redirect(to='welcome_dashboard_conn')
            else:
                request.session['registration_sms_count'] = sms_countdown - 1
                messages.error(request, f'Left {sms_countdown}-times, Please enter correct OTP')
                return render(request, 'welcome/reg_otp_decision.html')
        else:
            try:
                del request.session['reg_name']
                del request.session['reg_phone']
                del request.session['reg_email']
                del request.session['reg_gen_id']
                del request.session['reg_gen_key']
                del request.session['registration_sms_count']
            except:
                pass
            messages.error(request, f'you enter many times wrong otp')
            return redirect(to='welcome_dashboard_conn')
    else:
        if request.session.get('reg_phone', 'None') != 'None':
            return render(request, 'welcome/reg_otp_decision.html')
        else:
            return redirect(to='welcome_dashboard_conn')


def forgot_pwd(request):   
    if request.method == "POST":
        phone_no = request.POST.get('no_mob', 'None').strip()
        print("phone_no", phone_no)
        if (len(phone_no) == 10) and (phone_no != 'None') and (int(phone_no[0]) > 5):
            user_ins = User.objects.select_related('userdesc_user').filter(id__gt=2, username__exact=phone_no)  #allow 10 user ke badh password change kr skte h
            if user_ins.exists():  # 20
                user_ins = user_ins.first()
                
                if int(user_ins.userdesc_user.sms_life) > 0:
                    UserDesc.objects.filter(id=user_ins.userdesc_user.id).update(sms_life=F('sms_life') - 1)  # update desc

                    if request.session.get('forgot_sms_count', 'None') == 'None':
                        Traffic.objects.filter(Q(traffic_date=today)).update(reset_pwd=F('reset_pwd') + 1)  # update traffic
                        number = str(random.randint(1000, 9999))
                        x = True
                        if x:  # otp_sms(phone_no, number)
                            print("----- forgot otp --------", number)
                            f_obj = Fernet(settings.FERNET_KEY)
                            encrypted_otp = f_obj.encrypt(number.encode('utf-8'))

                            request.session['forgot_phone_no'] = phone_no
                            request.session['forgot_gen_key'] = str(encrypted_otp)
                            request.session['forgot_sms_count'] = 4
                            Traffic.objects.filter(Q(traffic_date=today)).update(msg=F('msg') + 1)
                            return redirect(to='forgot_pwd_otp_decision_conn')
                        else:
                            messages.error(request, "Please try after some time, Server Down")
                            return redirect(to='forgot_pwd_conn')
                    else:
                        del request.session['forgot_phone_no']
                        del request.session['forgot_gen_key']
                        del request.session['forgot_sms_count']
                        messages.error(request, f"OTP already send on {phone_no}, or try again forgot")
                        return redirect('forgot_pwd_conn')
                else:
                    messages.error(request, "You changes password more than 5 times, so please contact to company")
                    return render(request, 'welcome/forgot_pwd.html')

        messages.error(request, f'Mobile no {phone_no} not registered !')
        return render(request, 'welcome/forgot_pwd.html')

    return render(request, 'welcome/forgot_pwd.html')


def forgot_pwd_otp_decision(request):  # forgot decision
    if request.method == "POST": 
        forgot_phone_no = request.session.get('forgot_phone_no', 'None').strip()
        forgot_gen_key = request.session.get('forgot_gen_key', 'None').strip()

        forgot_otp_user = request.POST.get('forgot_otp', 'Enter your otp').strip()
        new_pass = request.POST.get('new_pass', 'None').strip()
        conf_pass = request.POST.get('conf_pass', 'Nones').strip()  # <----- none_s

        if (len(forgot_phone_no) == 10) and (forgot_gen_key != 'None') and (new_pass != 'None') and (conf_pass != 'Nones'):
            sms_countdown = int(request.session.get('forgot_sms_count'))
            print("f sms_countdown=",sms_countdown)
            if (sms_countdown) > 0:
                #request.session['forget_count'] = counter + 1
                f_obj = Fernet(settings.FERNET_KEY)
                forgot_otp_sys = f_obj.decrypt(bytes(forgot_gen_key[2:(len(forgot_gen_key) - 1)].encode('utf-8')))
                
                if int(forgot_otp_sys) == int(forgot_otp_user):
                    if new_pass == conf_pass:
                        ins_user = User.objects.filter(username=forgot_phone_no)
                        if ins_user.exists():
                            # save login pass
                            current_user = ins_user.last()
                            current_user.set_password(new_pass)
                            current_user.save()
                            # save wallet pass

                            # if current_user.last_name != "G":
                                #print("current_user.last_name != G:")
                                # Activated.objects.filter(user_ins_id=current_user.id).update(transaction=new_pass)
                            # update_session_auth_hash(request)
                            # logout(request)
                            try:
                                del request.session['forgot_phone_no']
                                del request.session['forgot_gen_key']
                                del request.session['forgot_sms_count']
                            except:
                                pass
                            messages.info(request, f"Login Password {new_pass} Changed successfully ")
                            return redirect(to='welcome_dashboard_conn')

                    messages.error(request, f'Password does not matched')
                    return render(request, 'welcome/forgot_pwd_otp_decision.html')
                else:
                    request.session['forgot_sms_count'] = sms_countdown - 1
                    messages.error(request, f'Left {(sms_countdown)}-times, please enter correct otp')
                    return render(request, 'welcome/forgot_pwd_otp_decision.html')
            else:
                try:
                    del request.session['forgot_phone_no']
                    del request.session['forgot_gen_key']
                    del request.session['forgot_sms_count']
                except:
                    pass
                messages.error(request, f'you enter many times wrong otp')
                return redirect(to='welcome_dashboard_conn')
        else:
            messages.error(request, f'Try again or Contact to company')
            return render(request, 'welcome/index.html')
    else: 
        if request.session.get('forgot_phone_no', 'None') != 'None':
            return render(request, 'welcome/forgot_pwd_otp_decision.html')
        else:
            return redirect(to='welcome_dashboard_conn')


def login(request):
    context = {
        'hi':"hello", 
    }
    if request.method == 'POST':
        user_id_mob = request.POST.get('my_id').strip()
        pwd = request.POST.get('pass').strip()
        try:
            user_obj = User.objects.get(first_name=user_id_mob).username
        except User.DoesNotExist:
            user_obj = user_id_mob
        '''if User.objects.filter(Q(first_name__in=user_id_mob)).first():
            user_obj = User.objects.filter(first_name=user_id_mob).first()
        elif User.objects.filter(Q(username__in=user_id_mob)).first():
            user_obj = User.objects.filter(first_name=user_id_mob).first()'''
        user = auth.authenticate(username=user_obj, password=pwd)
        if user is not None:
            request.session['super_id'] = user.id
            request.session['u_phone'] = user.username # s means super
            request.session['u_name'] = user.first_name
            is_status = request.session['u_status'] = user.last_name
            auth.login(request, user)

            Traffic.objects.filter(Q(traffic_date=today)).update(login=F('login') + 1)
            if is_status == "Z":
                messages.error(request, f'Your User Id {user.username} blocked, Please contact at company')
                return redirect(to='welcome_dashboard_conn')
            elif is_status == "G": 
                messages.info(request, f'Login Guest User, Mob-{user.username} Successfully')
                return redirect(to='guest_dashboard_conn')  # authenticated user which have name and mob no
            elif is_status == "O":
                messages.info(request, f'Login Operator User {user.username} Successfully')
                return redirect(to='operator_dashboard_conn')
            elif is_status == "S":
                messages.info(request, f'Login Staff User {user.username} Successfully')
                return redirect(to='staff_dashboard_conn')
            elif is_status == "A":
                messages.info(request, f'Login Admin User {user.username} Successfully')
                return redirect(to='admin_dashboard_conn')
            elif is_status == "M":
                messages.info(request, f'Login Master User {user.username} Successfully')
                return redirect(to='master_dashboard_conn')
            else:
                messages.error(request, f'Your User Id {user.username} blocked, Please contact at company')
                return redirect(to='welcome_dashboard_conn')

        Traffic.objects.filter(Q(traffic_date=today)).update(login_failed=F('login_failed') + 1)
        messages.error(request, f'Mobile or password is incorrect')
        return render(request, 'welcome/login.html', context)
    return render(request, 'welcome/login.html', context)

def logout_user(request): 
    context = {
        # 'welcome_pro': WelcomeProduct.objects.filter(id__lte=12, is_available=True),  # limit [:12]
        # 'base_b_ins': ShowBanner.objects.filter(id__lte=5, is_active=True),
        # 'banner_ins': ShowBanner.objects.filter(id=6, is_active=True).first(),
        # 'banner_info': ShowBanner.objects.filter(id=15, is_active=True).first(),  # for advertisment
        # 'w_achievement': ShowBanner.objects.filter(id__gt=15, id__lte=30, is_active=True),  # 16-30
        # 'our_ty_ups': WelcomeProduct.objects.filter(id__gt=12, id__lte=20, is_available=True),  # [12:20],
        # 'c_footer_side': CompanyFooter.objects.filter(id__lte=8, active=True),  # [:8],
        # 'c_footer_center': CompanyFooter.objects.filter(id__gt=8, id__lte=16, active=True),  # [8:16],
        # 'welcome_side': CompanyFooter.objects.filter(id__gt=16, id__lte=25, active=True),
        # 'w_secure_h': WelcomeSecure.objects.filter(id=1, is_active=True).first(),
        # 'w_secure': WelcomeSecure.objects.filter(id__gt=1, id__lte=11, is_active=True),
        # # text_2-material text_3-color 2 #1-head 8 pices_body
        # 'docs': AdminDocument.objects.filter(is_active=True)[:10],
        # "login_modal_control": "False"
    }
    try:
        logout(request)
        # del request.session['super_id']
        # del request.session['s_phone']
        # del request.session['s_id']
        # del request.session['s_status']
        # del request.session['Secure_Key']
        request.session.flush()  # remove
        # return redirect('welcome', context)
        return render(request, 'welcome/index.html', context)
    except:
        return render(request, 'welcome/index.html', context)
   


def data_view(request): 
    return render(request, 'welcome/data_view.html')


def data_fatch_ajax(request):
    date_list = ["2019-08-09","2019-08-10","2019-08-11","2019-08-12","2019-08-13","2019-08-14"]
    value_list = [1000,2000,3000,2500,3000,5000]
    context = {
        'labels' : date_list,
        'values' : value_list
    } 
    return JsonResponse(data=context)
    

def freq_contact(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name', 'None').strip()
        f_mobile = request.POST.get('f_mobile', 'None').strip()
        f_email = request.POST.get('f_email', 'None').strip()
        f_message = request.POST.get('f_message', 'None').strip()
        print(f_name, f_mobile, f_email, f_message)
        if f_mobile.isnumeric() and (len(f_mobile) == 10) and (len(f_message) > 1):
            ContactTo.objects.create(name=f_name, mobile=f_mobile, email=f_email, query=f_message)
            messages.success(request, "Successfully sent message to company")
            return redirect('welcome_dashboard_conn')
    messages.error(request, "Please fill the correct values")
    return redirect('welcome_dashboard_conn')

def alpha_contact(request):
    return render(request, 'welcome/contact.html')


def alpha_rbalance(request):
    return render(request, 'welcome/rbalance.html')




 
