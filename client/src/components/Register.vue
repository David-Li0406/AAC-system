<template>
<div class="registerForm">
  <div class="background"></div>
  <div class="register_box">
    <div class="avator_box">
        <img src="../assets/写作.png" alt />
    </div>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="register_form">
    <!-- prop对应下面的rules -->
    <el-form-item label="邮箱" prop="Email">
        <el-input type="text" v-model="ruleForm.Email" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item :inline-message="true" label="验证码" prop="verificationCode">
      <el-col :span="14">
        <el-input type="text" v-model="ruleForm.verificationCode" autocomplete="off"></el-input>
      </el-col>
      <el-col :span="8" :offset="2">
        <el-form-item>
          <el-button type="primary" :loading="loading1" @click="send()" size='large'>
            <span v-if="!loading1">发送</span>
            <span v-else>Loading</span>
          </el-button>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item label="用户名" prop="User">
        <el-input type="text" v-model="ruleForm.User" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="昵称" prop="User">
        <el-input type="text" v-model="ruleForm.Nickname" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="Pass">
        <el-input type="password" v-model="ruleForm.Pass" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="确认密码" prop="doubleCheck">
        <el-input type="password" v-model="ruleForm.doubleCheck" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item style="text-align: center;">
        <el-button type="primary" :loading="loading" @click="submitForm('ruleForm')" size='large'>
          <span v-if="!loading">注册</span>
          <span v-else>Loading</span>
        </el-button>
    </el-form-item>
    </el-form>
    </div>

    <!-- 用来提示邮箱已经被注册的消息框 -->
    <el-dialog
    title="发送验证码失败"
    :visible.sync="dialogVisible0"
    width=30%>
      <span>邮箱已被注册！</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible0 = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示填写不符合规范的消息框 -->
    <el-dialog
    title="提交失败"
    :visible.sync="dialogVisible1"
    width=30%>
      <span>填写不符合规范！</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible1 = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示验证码错误的消息框 -->
    <el-dialog
    title="注册失败"
    :visible.sync="dialogVisible2"
    width=30%>
      <span>{{errorMessage}}</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible2 = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示注册成功的消息框 -->
    <el-dialog
    title="注册成功"
    :visible.sync="dialogVisible3"
    width=30%>
      <span>注册成功！点击确认跳转到登录页面</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="goToLogin()">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示邮箱不能为空的消息框 -->
    <el-dialog
    title="发送验证码失败"
    :visible.sync="dialogVisible4"
    width=30%>
      <span>邮箱不能为空！</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible4 = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示邮箱格式不正确的消息框 -->
    <el-dialog
    title="发送验证码失败"
    :visible.sync="dialogVisible5"
    width=30%>
      <span>邮箱格式不正确！</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible5 = false">确认</el-button>
      </span>
    </el-dialog>
        
    <!-- 用来提示发送成功的消息框 -->
    <el-dialog
    title="发送验证码成功"
    :visible.sync="dialogVisible6"
    width=30%>
      <span>验证码发送成功！请查看邮箱</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible6 = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示发送失败的消息框 -->
    <el-dialog
    title="发送验证码失败"
    :visible.sync="dialogVisible7"
    width=30%>
      <span>发送验证码失败！请稍后再试</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible7 = false">确认</el-button>
      </span>
    </el-dialog>

</div>
</template>


<script>
  import https from '../api/https.js'
  export default {
    data() {
      var validateEmail = (rule, value, callback) => {
        var regEmail = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        if (value === '') {
          this.emailEmpty = true;
          callback(new Error('请输入邮箱'));
        } else {
          this.emailEmpty = false;
          if (!regEmail.test(value)) {
            this.emailFormateError = true;
            callback(new Error('邮箱格式错误'));
          }else{
            this.emailFormateError = false;
            var form = {'email': value}
            https.fetchPost('checkEmail', form).then((res) => {
              if (res.data['code'] === 200) {
                this.emailReg = false;
                callback();
              }else{
                this.emailReg = true;
                callback(new Error('邮箱已被注册'));
              }
            })
          }
        }
      };
      var validateUser = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else {
          var form = {
            'username': value,
          };
          https.fetchPost('checkUser', form).then((res) => {
            if (res.data['code'] === 200) {
              callback();
            }else{
              callback(new Error('用户名已被注册'));
            }
          })
        }
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请设置密码'));
        }  else {
          callback();
        }
      };
      var validateVC = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入验证码'));
        }  else {
          callback();
        }
      };
      var validateDoubleCheck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else {
          if(this.ruleForm.Pass!='' && value != this.ruleForm.Pass){
              callback(new Error('两次密码不一致'));
          }
          callback();
        }
      };
      return {
        errorMessage: '',
        loading: false,
        loading1: false,
        emailReg: false,
        emailEmpty: false,
        emailFormateError: false,
        dialogVisible0: false,
        dialogVisible1: false,
        dialogVisible2: false,
        dialogVisible3: false,
        dialogVisible4: false,
        dialogVisible5: false,
        dialogVisible6: false,
        dialogVisible7: false,
        ruleForm: {
          Email: '',
          verificationCode: '',
          User: '',
          Pass: '',
          doubleCheck: '',
        },
        rules: {
          Email: [
            { validator: validateEmail, trigger: 'blur' }
          ],
          verificationCode: [
            { validator: validateVC, trigger: 'blur' }
          ],
          User: [
            { validator: validateUser, trigger: 'blur' }
          ],
          Nickname: [
            { required: true, message: "请输入昵称", trigger: "blur" }
          ],
          Pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          doubleCheck: [
            { validator: validateDoubleCheck, trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        var email = this.ruleForm['Email'];
        var username = this.ruleForm['User'];
        var password = this.ruleForm['Pass'];
				var verificationCode = this.ruleForm['verificationCode'];
        var nickname = this.ruleForm['Nickname']
        var registerInfo = {
          'email': email,
          'username': username,
          'password': password,
					'verificationCode': verificationCode,
          'nickname': nickname,
        };
        console.log(registerInfo)

        this.$refs[formName].validate((valid) => {
          if (valid) {
            // 让注册按钮显示为loading
            this.loading = true;
            https.fetchPost('register', registerInfo).then((res) => {
              // 让注册按钮恢复
              this.loading = false;
              if (res.data['code'] === 200) {
                this.dialogVisible3 = true;
                return true;
              }else{
                this.errorMessage = res.data['message'];
                this.dialogVisible2 = true;
                return false;
              }
            })
          }else {
            this.dialogVisible1 = true;
            return false;
          }
        });
      },
      
      send(){
        if(this.emailEmpty){
          this.dialogVisible4 = true;
          return false;
        }else if(this.emailFormateError){
          this.dialogVisible5 = true;
          return false;
        }else if(this.emailReg){
          this.dialogVisible0 = true;
          return false;
        }else{
          console.log(1);
          https.fetchPost('confirm', {'email': this.ruleForm['Email']}).then((res) => {
            if (res.data['code'] === 200) {
              this.dialogVisible6 = true;
              return true;
            }else{
              this.dialogVisible7 = true;
              return false;
            }
          })
        }
      },

      goToLogin() {
        this.dialogVisible3 = false;
        this.$router.push("/login");
      }
    }
  }
</script>

<style scoped>

  .registerForm {
      height: 100%;
  }
  .register_box {
        width: 430px;
        height: 550px;
        background-color: #fff;
        border-radius: 3px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }
  .avator_box {
      height: 130px;
      width: 130px;
      border: 1px solid #eee;
      border-radius: 40%;
      padding: 10px;
      box-shadow: 0 0 10px #ddd;
      position: absolute;
      left: 50%;
      transform: translate(-50%, -50%);
    }
    img {
      height: 100%;
      width: 100%;
      border-radius: 50%;
      background-color: #eee;
        }
    .register_form{
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 0 20px;
        box-sizing: border-box;
    }
    .background{
        width:100%;
        height:100%;
        position: absolute;
        background-image: url(../assets/logo.jpg);
        background-size:100% 100%;
        opacity: .4;
        z-index:-1;
    }

</style>
