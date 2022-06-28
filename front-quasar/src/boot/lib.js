import { boot } from 'quasar/wrappers'
import setWith from 'src/lib/setWith'

const lib = {
  setWith,
}

export default boot(({ app }) => {
  app.config.globalProperties.$lib = lib
})

export { lib }
