import lodash from "lodash";

const setWith = (object, target, value) => {
  if (target.includes(".")) {
    const keys = target.split(".");
    let currentKey;
    keys.forEach((key, index) => {
      if (!currentKey) {
        if (typeof lodash.get(object, key) === "undefined")
          lodash.set(object, key, {});
        currentKey = key;
      } else {
        currentKey += `.${key}`;
        if (typeof lodash.get(object, currentKey) === "undefined") {
          lodash.set(
            lodash.get(object, currentKey.split(".").slice(0, -1).join(".")),
            key,
            {}
          );
        }
      }
    });
    lodash.set(
      lodash.get(object, currentKey.split(".").slice(0, -1).join(".")),
      currentKey.split(".").slice(-1)[0],
      value
    ); // ao final atribui valor passado
  } else lodash.set(object, target, value);
};

export default setWith;
