import { boot } from 'quasar/wrappers'
import jwtParse from 'src/lib/jwtParse'
import setWith from 'src/lib/setWith'

const lib = {
  jwtParse,
  setWith,
}

export default boot(({ app }) => {
  app.config.globalProperties.$lib = lib
})

export { lib }
