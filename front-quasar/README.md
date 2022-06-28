
## Wedding Show - Front End
For the front-end I have decided to user Quasar Framework instead of pure HTML+CSS or other combinations such as Bootstrap+jQuery, because I consider it more elegant and I have more than 6 years of experience using it. Still, I consider that it maintains the need for knowledge in VueJS, being a shortcut only for the visual part.
#### References
- [Quasar Framework](https://quasar.dev)
#### Preparation
##### 1. Install Quasar CLI (to run dev mode or build)
- Requirements: Node 12+, Yarn v1 (strongly recommended) or NPM.
```bash
yarn global add @quasar/cli
# or
npm i -g @quasar/cli
```
##### 2. Assuming you have already cloned the repository go inside front-quasar folder
```
cd /path-to-project/front-quasar
```
##### 3. After clone install dependencies
```bash
yarn
# or
npm install
```
#### Usage
##### DEV: If you want to develop by using hot-code reloading, error reporting, etc. use the dev mode
```
quasar dev
```
##### PRO: To build the SPA project for production use the build command
```
quasar -m SPA build
```

