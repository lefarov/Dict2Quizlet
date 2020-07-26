module.exports = {
  devServer: {
    proxy: {
      '^/autocomplete/': {
        target: 'https://dict.leo.org/dictQuery/m-query/conf/ende/query.conf/strlist.json',
        pathRewrite: { '^/autocomplete/': '' },
        changeOrigin: true,
        logLevel: 'debug',
      },
    },
  },
  configureWebpack: {
    devtool: 'source-map',
  },
};
