import { boot } from 'quasar/wrappers'
import parseJwt from 'src/lib/parseJwt'
import setWith from 'src/lib/setWith'

const lib = {
  parseJwt,
  setWith,
}

export default boot(({ app }) => {
  app.config.globalProperties.$lib = lib
})

export { lib }
