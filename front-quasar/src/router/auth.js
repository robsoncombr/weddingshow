const base_url = '/auth'

const routes = [
  {
    path: `${base_url}/signup`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/auth/SignUp.vue') }
    ]
  },
  {
    path: `${base_url}/signin`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/auth/SignIn.vue') }
    ]
  },
  {
    path: `${base_url}/weddings`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/auth/Weddings.vue') }
    ]
  },

]

export default routes
