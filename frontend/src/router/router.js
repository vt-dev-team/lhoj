import { createRouter, createWebHistory } from "vue-router"
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
        path: "/problem/:id",
        name: "ProblemShow",
        component: () =>
            import ("../pages/problems/show.vue")
    }
]

const router = createRouter({
    linkActiveClass: 'active',
    history: createWebHistory(),
    routes
})

export default router;