const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
      })
    ],
    module: {
      rules: [
        {
          test: /\.pdf$/,
          type: 'asset/resource',
          generator: {
            filename: 'assets/pdf/[name][ext]',
          },
        },
      ],
    },
  },
});
