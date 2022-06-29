const base_url = '/auth'

const routes = [
  {
    path: `${base_url}/signup`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/auth/Signup.vue') }
    ]
  },
  {
    path: `${base_url}/signin`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/auth/Signin.vue') }
    ]
  },
]

export default routes
