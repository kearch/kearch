const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const NODE_PROD = process.env.NODE_ENV === 'production';

module.exports = {
  entry: './js/index.js',

  mode: 'development',

  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.js',
    publicPath: '/'
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: () => [
                autoprefixer({
                  browsers: ['last 2 versions'],
                }),
              ],
            },
          },
          {
            loader: 'sass-loader',
          },
        ],
      }
    ]
  },

  plugins: [
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: "[name].css",
      chunkFilename: "[id].css"
    })
  ],

  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000,
    ignored: /node_modules/,
  },
};
