const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new webpack.DefinePlugin({
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      // other Vue feature flags...
    }),
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
};
