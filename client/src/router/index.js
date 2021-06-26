import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Login from '@/components/Login'
import Register from '@/components/Register'
import newPage from '@/components/Main/newPage'
import articleSquare from '@/components/Main/articleSquare'
import personalCenter from '@/components/Main/personalCenter'
import userMain from '@/components/Main/userMain'
import result from '@/components/Main/result'
import post from '@/components/Main/post'
import permissionManagement from '@/components/main/permissionManagement'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/main',
      name: 'Main',
      component: Main,
      redirect: '/main/userMain',
      meta: {
        title: '主页面',
        required: true,
      },
      children: [
        {
          path: 'newPage',
          name: 'newPage',
          component: newPage,
          meta: {
            title: '新建页面',
            required: true,
          },
        },
        {
          path: 'result',
          name: 'result',
          component: result,
          meta: {
            title: '结果页面',
            required: true,
          },
        },
        {
          path: 'permissionManagement',
          name: 'permissionManagement',
          component: permissionManagement,
          meta: {
            title: '权限管理页面',
            admin_required: true,
          },
        },
        {
          path: 'articleSquare',
          name: 'articleSquare',
          component: articleSquare,
          meta: {
            title: '作文广场',
            required: true,
          },
        },
        {
          path: 'post',
          name: 'post',
          component: post,
          meta: {
            title: '用户发布',
            required: true,
          },
        },
        {
          path: 'personalCenter',
          name: 'personalCenter',
          component: personalCenter,
          meta: {
            title: '个人页面',
            required: true,
          },
        },
        {
          path: 'userMain',
          name: 'userMain',
          component: userMain,
          meta: {
            title: '主页面',
            required: true,
          },
        },
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        title: '登录页面',
        required: false,
      },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        title: '注册页面',
        required: false,
      },
    },
    {
      path: '*',
      name: 'any',
      redirect: '/main/userMain',
      meta: {
        title: '主页面',
        required: true,
      },
    }
  ]
})

// 全局前置守卫，判断用户是否登陆，未登陆跳转至登陆页面
router.beforeEach((to, from, next) => {
  // 自动添加title
  if (to.meta.title) {
      console.log(1);
      document.title = to.meta.title;
  }
  // 路由中定义的是否需要登陆权限
  // 如果前往的页面需要登录
  if (to.meta.required) {
      // 如果用户已经登录，此时token存在store里
      if (store.state.token) {
          next();
      } else {
          // 如果用户刷新页面，store里的token消失，此时token在sessionStorage里也存了
          if (sessionStorage.getItem('token')) {
              store.state.token = sessionStorage.getItem('token');
              if(sessionStorage.getItem('user_type')){
                store.state.user_type = sessionStorage.getItem('user_type');
              }
              next();
          } else {
              // 跳转到登陆页面
              next({
                  path: '/login',
                  query: { redirect: to.fullpath }
              })
          }
      }
      // 如果不需要登录，直接跳转
  } else {
    if (to.meta.admin_required) {
      if(store.state.token && store.state.user_type == 'administrator'){
        next();
      }else{
        if(sessionStorage.getItem('token') && sessionStorage.getItem('user_type')){
          store.state.token = sessionStorage.getItem('token')
          store.state.user_type = sessionStorage.getItem('user_type')
          if(store.state.user_type == 'administrator'){
            next();
          }else{
            next({
              path: '/login',
              query: { redirect: to.fullpath }
            })
          }
        }else{
          next({
            path: '/login',
            query: { redirect: to.fullpath }
          })
        }
      }
    }else{
      next();
    }
  }
})

export default router;
