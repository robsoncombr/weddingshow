// all requests to the api will use this parameter as the id for the wedding
const base_url = '/:wedding'

const routes = [
  {
    path: `${base_url}`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/wedding/Gallery.vue') }
    ]
  },
  {
    path: `${base_url}/users`,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/wedding/Users.vue') }
    ]
  },
]

export default routes
