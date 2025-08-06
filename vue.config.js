const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // without DNS publicPath: process.env.NODE_ENV === 'production' ? '/airless/' : '/'
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/'
})
