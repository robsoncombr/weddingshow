import { boot } from 'quasar/wrappers'
import lodash from 'lodash'
import jwtParse from 'src/lib/jwtParse'
import setWith from 'src/lib/setWith'

const lib = {
  jwtParse,
  setWith,
  lodash,
  $get: (object, path, defaultValue = null) => lodash.get(object, path, defaultValue),
  // TODO: $set usando lodash.setWith ???
  $debug: (...data) => dev ? console.debug(data) : () => {},
}

export default boot(({ app }) => {
  app.config.globalProperties.$lib = lib
})

export { lib }
