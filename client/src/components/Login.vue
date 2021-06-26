<template>
<div class="loginForm">

  <div class="background"></div>

  <div class="login_box">
    <div class="avator_box">
        <img src="../assets/写作.png" alt />
    </div>

    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="login_form">
    <!-- prop对应下面的rules -->
    <el-form-item label="用户名/邮箱" prop="User">
        <el-input type="text" v-model="ruleForm.User" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="Pass">
        <el-input type="password" v-model="ruleForm.Pass" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item :inline-message="true">
    <el-checkbox v-model="remember" >记住我</el-checkbox>
    </el-form-item>
    <el-form-item style="text-align:center">
        <el-button type="primary" :loading="loading" @click="submitForm('ruleForm')" size='large'>
          <span v-if="!loading">登录</span>
          <span v-else>Loading</span>
        </el-button>
        <el-button @click="goToReg()">注册</el-button>
    </el-form-item>
    </el-form>
  </div>

    <!-- 用来提示用户名或密码错误的消息框 -->
    <el-dialog
    title="登录失败"
    :visible.sync="dialogVisible"
    width=30%>
      <span>用户名或密码错误</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">确认</el-button>
      </span>
    </el-dialog>

    <!-- 用来提示不符合填写规范的消息框 -->
    <el-dialog
    title="提交失败"
    :visible.sync="dialogVisible1"
    width=30%>
      <span>请填写用户名和密码</span>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible1 = false">确认</el-button>
      </span>
    </el-dialog>
</div>
</template>


<script>
  import https from '../api/https.js'
  import CryptoJS from 'crypto-js'

  // 十六位十六进制数作为密钥
  const key = CryptoJS.enc.Utf8.parse('13579BDFFDB97531');
  // 十六位十六进制数作为偏移量
  const iv = CryptoJS.enc.Utf8.parse('02468ACEECA86420');

  export default {
    data() {
      var validateUser = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else {
          if (this.ruleForm.Pass !== '') {
            this.$refs.ruleForm.validateField('Pass');
          }
          callback();
        }
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        }  else {
          callback();
        }
      };
      return {
        dialogVisible: false,
        dialogVisible1: false,
        remember: false,
        loading: false,
        ruleForm: {
          User: '',
          Pass: '',
        },
        rules: {
          User: [
            { validator: validateUser, trigger: 'blur' }
          ],
          Pass: [
            { validator: validatePass, trigger: 'blur' }
          ]
        }
      };
    },
    mounted(){
    //绑定事件
     window.addEventListener('keydown',this.keyDown);
    },
    created () {
      // 载入cookie
      let User = this.getCookie('userid');
      let Pass = this.decrypt(this.getCookie('password'));
      // 如果存在cookie则填入信息并勾选记住我
      if (User) {
        this.ruleForm.User = User;
        this.ruleForm.Pass = Pass;
        this.remember = true;
      }

    },
    methods: {
      goToReg(){
        this.$router.push('register');
      },
      keyDown(e){
        //如果是回车则执行登录方法
        if(e.keyCode == 13 && this.$route.path === '/login'){
          this.submitForm('ruleForm');
        }
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          var userid = this.ruleForm['User'];
          var pwd = this.ruleForm['Pass'];
          var loginInfo = {'userid': userid, 'password': pwd};
          if (valid) {
            this.loading = true;
            https.fetchPost('login', loginInfo).then((res) => {
              if (res.data['code'] === 200) {
                this.$store.commit('set_token', res.data['token']);
                this.$store.commit('set_user_type', res.data.user_type);
                // 存储用户信息
                this.setUserInfo();
                this.$router.push('/main/userMain');
                return true;
              } else {
                this.loading = false;
                this.dialogVisible = true;
                return false;
              }
            });
          } else {
            this.loading = false;
            this.dialogVisible1 = true;
            return false;
          }
        });
      },
      // 保存cookie方法
      setCookie (cName, value, expiredays) {
        var exdate = new Date();
        // 有效时间为当前时间加天数
        exdate.setDate(exdate.getTime() + expiredays);
        document.cookie = cName + '=' + value + ((expiredays == null) ? '' : ';expires=' + exdate.toGMTString());
      },
      // 读取cookie方法
      getCookie (key) {
        if (document.cookie.length > 0) {
          var start = document.cookie.indexOf(key + '=');
          if (start !== -1) {
            start = start + key.length + 1;
            var end = document.cookie.indexOf(';', start);
            if (end === -1) {
              end = document.cookie.length;
            }
            return unescape(document.cookie.substring(start, end));
          }
        }
        return '';
      },
      // 存储用户信息到cookie
      setUserInfo () {
        // 通过是否勾选记住我判断存储cookie还是清空cookie
        if (this.remember) {
            this.setCookie('userid', this.ruleForm.User, 7);
            // 使用Crypto加密密码
            let pwd = this.encrypt(this.ruleForm.Pass);
            this.setCookie('password', pwd, 7);
        } else {
            this.setCookie('userid', '', null);
            this.setCookie('password', '', null);
        }
      },
      // Crypto解密方法
      decrypt (word) {
        let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
        let srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
        let decrypt = CryptoJS.AES.decrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
        let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
        return decryptedStr.toString();
      },
      // Crypto加密方法
      encrypt (word) {
        let srcs = CryptoJS.enc.Utf8.parse(word);
        let encrypted = CryptoJS.AES.encrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
        return encrypted.ciphertext.toString().toUpperCase();
      },
    },
    destroyed(){
        window.removeEventListener('keydown',this.keyDown,false);
    }
  }
</script>

<style scoped>

  .loginForm {
      height: 100%;
  }
  .login_box {
        width: 430px;
        height: 350px;
        background-color: #fff;
        border-radius: 3px;
        position: absolute;
        left: 50%;
        top: 40%;
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
    .login_form{
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
