import { createRouter, createWebHistory } from 'vue-router';

// 导入组件
import Home from '../components/UserList.vue';
import Test from '../components/AddUser.vue';


// 创建路由实例
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home,
            props: {
                name: 'Hello from router', // 这里可以设置默认值或者根据需要动态设置
            },
        },
        {
            path: '/test',
            name: 'Test',
            component: Test
        },
    ],
});

export default router;