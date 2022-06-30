// all requests to the api will use this parameter as the id for the wedding
const base_url_all = '/weddings'
const base_url_one = `${base_url_all}/:wedding`

const routes = [
  {
    path: base_url_all,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/wedding/All.vue') }
    ]
  },
  {
    path: base_url_one,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/wedding/One.vue') }
    ]
  },
]

export default routes
