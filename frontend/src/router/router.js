import { createRouter, createWebHistory } from "vue-router"
import NProgress from 'nprogress'
const routes = [{
        path: "/",
        name: "HomePage",
        component: () =>
            import ("../pages/index.vue")
    },
    {
        path: "/news/:id",
        name: "NewsPage",
        component: () =>
            import ("../pages/announcements/show.vue")
    },
    {
        path: "/problems",
        name: "ProblemSet",
        component: () =>
            import ("../pages/problems/list.vue")
    },
    {
        path: "/problem/new",
        name: "ProblemNew",
        component: () =>
            import ("../pages/problems/new.vue")
    },
    {
        path: "/problem/:id",
        name: "ProblemShow",
        component: () =>
            import ("../pages/problems/show.vue")
    },
    {
        path: "/problem/:id/edit",
        name: "ProblemEdit",
        component: () =>
            import ("../pages/problems/edit.vue")
    },
    {
        path: "/problem/:id/data",
        name: "ProblemData",
        component: () =>
            import ("../pages/problems/dataset.vue")
    },
    {
        path: "/contests",
        name: "ContestSet",
        component: () =>
            import ("../pages/contests/list.vue")
    },
    {
        path: "/contest/new",
        name: "ContestNew",
        component: () =>
            import ("../pages/contests/new.vue")
    },
    {
        path: "/contest/:id",
        name: "ContestShow",
        component: () =>
            import ("../pages/contests/show.vue")
    },
    {
        path: "/contest/:id/edit",
        name: "ContestEdit",
        component: () =>
            import ("../pages/contests/edit.vue")
    },
    {
        path: "/contest/:id/rank",
        name: "ContestRank",
        component: () =>
            import ("../pages/contests/rank.vue")
    },
    {
        path: "/submissions",
        name: "SubmissionSet",
        component: () =>
            import ("../pages/submissions/list.vue")
    },
    {
        path: "/submission/:id",
        name: "SubmissionShow",
        component: () =>
            import ("../pages/submissions/show.vue")
    },
    {
        path: "/discuss",
        name: "DiscussList",
        component: () =>
            import ("../pages/discuss/list.vue")
    },
    {
        path: "/discuss/:id",
        name: "DiscussShow",
        component: () =>
            import ("../pages/discuss/show.vue")
    },
    {
        path: "/discuss/:id/edit",
        name: "DiscussEdit",
        component: () =>
            import ("../pages/discuss/edit.vue")
    },
    {
        path: "/discuss/new",
        name: "DiscussNew",
        component: () =>
            import ("../pages/discuss/new.vue")
    },
    {
        path: "/user/reg",
        name: "RegisterPage",
        component: () =>
            import ("../pages/users/register.vue")
    },
    {
        path: "/user/:id/modify",
        name: "UserModify",
        component: () =>
            import ("../pages/users/modify.vue")
    },
    {
        path: "/user/:id",
        name: "UserInfo",
        component: () =>
            import ("../pages/users/show.vue")
    },
    {
        path: "/user/mail",
        name: "UserMessage",
        component: () =>
            import ("../pages/users/message.vue")
    },
    {
        path: "/user/rank",
        name: "UserRank",
        component: () =>
            import ("../pages/users/list.vue")
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () =>
            import ("../pages/NotFound.vue")
    }
]

const router = createRouter({
    linkActiveClass: 'active',
    history: createWebHistory(),
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {
                selector: to.hash,
                behavior: 'smooth',
            }
        }
    },
    routes
})

router.beforeEach((to, from, next) => {
    NProgress.start()
    next()
})

router.afterEach(() => {
    NProgress.done()
})

export default router;