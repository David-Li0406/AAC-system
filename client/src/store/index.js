// 存储token相关信息

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        // 存储token
        token: '',
        user_type: '',
    },
    mutations: {
        // 设置token，并将token存入sessionStorage
        set_token (state, token) {
            state.token = token;
            sessionStorage.token = token;
        },
        // 删除token
        del_token (state) {
            state.token = '';
            sessionStorage.removeItem('token');
        },
        set_user_type (state, user_type) {
            state.user_type = user_type;
            sessionStorage.user_type = user_type;
        },
        del_user_type (state) {
            state.user_type = '';
            sessionStorage.removeItem('user_type');
        },
    }
});

export default store;

